from __future__ import annotations

import datetime
import json
import logging
import os
import pprint
import random
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

import rich
import structlog
from flask import Flask, redirect, request, g
from structlog.stdlib import LoggerFactory

pp = pprint.PrettyPrinter(indent=4)

# Configuration constants
PHOST = '0.0.0.0'
PPORT = 1211
LOG_TO_FILE = True
LOG_STORAGE = Path('./logs/requests')
METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'LINK', 'VIEW', 
           'COPY', 'OPTIONS', 'UNLINK', 'PURGE', 'LOCK', 'UNLOCK', 'PROPFIND']

# IP request counter
ip_request_counts = defaultdict(int)

def print_html(data: Any) -> str:
    """Convert data to HTML-safe formatted string."""
    return pp.pformat(data).replace("\n", "<br>").replace("'", '"')

def setup_structlog() -> structlog.stdlib.BoundLogger:
    """Set up structlog configuration with Flask integration."""
    # Ensure log directory exists
    LOG_STORAGE.mkdir(parents=True, exist_ok=True)
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
            structlog.dev.ConsoleRenderer(colors=True) if not LOG_TO_FILE else structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        logger_factory=LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    # Set up file handler if needed
    if LOG_TO_FILE:
        st = int(time.time())
        log_file = LOG_STORAGE / f"web_requests_{st}.log"
        
        # Configure standard logging for file output
        logging.basicConfig(
            filename=str(log_file),
            level=logging.INFO,
            format="%(message)s",
        )
    
    logger = structlog.get_logger("network_listener")
    logger.info("Structlog initialized", timestamp=time.time())
    return logger

def get_client_ip() -> str:
    """Extract client IP address, handling proxy headers."""
    # Check for proxy added headers
    if 'X-Forwarded-For' in request.headers:
        # X-Forwarded-For can contain multiple IPs, take the first one
        return request.headers['X-Forwarded-For'].split(',')[0].strip()
    elif 'X-Real-IP' in request.headers:
        return request.headers['X-Real-IP']
    else:
        return request.remote_addr or 'unknown'

def get_ip_stats() -> dict:
    """Get statistics about IP addresses."""
    total_requests = sum(ip_request_counts.values())
    return {
        'total_unique_ips': len(ip_request_counts),
        'total_requests': total_requests,
        'ip_counts': dict(ip_request_counts),
        'top_ips': sorted(ip_request_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    }

# Initialize logging and Flask app
logger = setup_structlog()
app = Flask('simple_listener')

# Flask request logging middleware
@app.before_request
def log_request_info():
    """Log request information and count requests per IP."""
    client_ip = get_client_ip()
    ip_request_counts[client_ip] += 1
    
    # Bind context for this request
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        client_ip=client_ip,
        method=request.method,
        url=request.url,
        user_agent=request.headers.get('User-Agent', ''),
        request_count=ip_request_counts[client_ip],
        timestamp=time.time(),
        datetime=datetime.datetime.now().isoformat()
    )
    
    logger.info(
        "Request received",
        client_ip=client_ip,
        method=request.method,
        path=request.path,
        url=request.url,
        user_agent=request.headers.get('User-Agent', ''),
        request_count_for_ip=ip_request_counts[client_ip],
        total_unique_ips=len(ip_request_counts),
        headers=dict(request.headers)
    )

@app.after_request
def log_response_info(response):
    """Log response information."""
    logger.info(
        "Response sent",
        status_code=response.status_code,
        content_length=response.content_length
    )
    return response

logger.info("Flask started", host=PHOST, port=PPORT)
logger.info("Request logging initialized with IP counting")


def final_destination(route_attempt: str | None) -> tuple[str, int] | Any:
    """Handle all incoming requests with comprehensive logging."""
    # Make noise! - makes the console ding
    sys.stdout.write('\a')
    
    client_ip = get_client_ip()
    ts = time.time()
    dt = datetime.datetime.now()
    req = request
    headers = dict(req.headers)
    
    # Get payload
    payload = ""
    if len(req.form) > 0:
        payload = print_html(dict(req.form))
    else:
        try:
            payload = req.data.decode("utf8") if req.data else ""
        except Exception:
            payload = str(req.data)
    
    # Log the request details with structlog
    logger.info(
        "Processing request",
        route_attempt=route_attempt,
        payload=payload,
        query_string=req.query_string.decode("utf8") if req.query_string else "",
        host=req.host,
        path=req.path,
        protocol=req.environ.get('SERVER_PROTOCOL', ''),
        full_url=req.url
    )
    
    # Create response
    resp = f"{dt} EST {ts}<br>{request.method}"
    resp += f" Request made from <b>{client_ip}</b> (Request #{ip_request_counts[client_ip]}) to {req.host}<b>{req.path}</b><br>"
    resp += f"{headers.get('User-Agent', 'Unknown User Agent')}"
    
    if payload:
        resp += f"<h2>Payload:</h2>{payload}"
        
    resp += f"<h2>IP Statistics:</h2>"
    ip_stats = get_ip_stats()
    resp += f"Total unique IPs: {ip_stats['total_unique_ips']}<br>"
    resp += f"Total requests: {ip_stats['total_requests']}<br>"
    resp += f"<h3>Top 10 IPs by request count:</h3>"
    for ip, count in ip_stats['top_ips']:
        resp += f"{ip}: {count} requests<br>"
    
    print(f"{client_ip} (#{ip_request_counts[client_ip]}) requesting {req.host}{req.path} at {ts} {dt}")
    resp += f"<h2>Headers:</h2> {print_html(headers)}"

    # Response strategies
    foass_endpoints = [
        '/your%20port%20scanner/yours%20truly',
        '/asshole/yours%20truly',
        '/shit/yours%20truly',
        '/cool/yours%20truly',
        '/everyone/yours%20truly',
        '/rtfm/yours%20truly'
    ]
    other_sites = ['https://retirementplans.vanguard.com/', 'https://www.theonion.com/']
    emojis = ["💩", "☢", "☣", "🙅‍♂️", "🤏", "🖐", "🍯", "🥒",  "🧯", 
              "🤯", "🤬", "😡", "🤓", "👾", "🐱‍👤", "🐱‍🏍", "🙈", "⛏", "🔎", 
              "¯\\_(ツ)_/¯", "(T_T)"]

    match route_attempt:
        case 'emoji':
            emoji_choice = random.choice(emojis)
            logger.info("Returning emoji", emoji=emoji_choice)
            return (emoji_choice, 200)
        case 'showclientinfo':
            logger.info("Showing client info")
            return resp
        case 'stats':
            logger.info("Showing IP statistics")
            return f"<h1>IP Statistics</h1><pre>{json.dumps(ip_stats, indent=2)}</pre>"
        case _:
            response_type = random.choice(['stats', 'emoji'])
            logger.info("Random response", response_type=response_type)
            match response_type:
                case 'stats':
                    logger.info("Showing IP statistics")
                    return f"<h1>IP Statistics</h1><pre>{json.dumps(ip_stats, indent=2)}</pre>"
                case 'emoji':
                    return (random.choice(emojis), 200)
                case 'redirect':
                    return redirect(random.choice(other_sites), 302)  
# Route handlers
@app.route('/<route_attempt>', methods=METHODS)
@app.route('/', methods=METHODS)
def index(route_attempt: str | None = None) -> tuple[str, int] | Any:
    """Handle all routes with the same logging and response logic."""
    return final_destination(route_attempt)


def main() -> None:
    """Main entry point for the application."""
    print("Flask is listening")
    app.run(
        host=PHOST,
        port=PPORT,
        debug=True,
        use_reloader=False
    )


if __name__ == "__main__": 
    main()