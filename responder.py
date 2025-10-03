from __future__ import annotations

import datetime
import logging
import os
import pprint
import random
import sys
import time
from pathlib import Path
from typing import Any

from flask import Flask, redirect, request

pp = pprint.PrettyPrinter(indent=4)

# Configuration constants
PHOST = '0.0.0.0'
PPORT = 1211
LOG_TO_FILE = True
LOG_STORAGE = Path('./logs/requests')
METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'LINK', 'VIEW', 
           'COPY', 'OPTIONS', 'UNLINK', 'PURGE', 'LOCK', 'UNLOCK', 'PROPFIND']


def print_html(data: Any) -> str:
    """Convert data to HTML-safe formatted string."""
    return pp.pformat(data).replace("\n", "<br>").replace("'", '"')

def setup_logging() -> logging.Logger:
    """Set up logging configuration."""
    st = int(time.time())
    LOG_STORAGE.mkdir(parents=True, exist_ok=True)
    log_file = LOG_STORAGE / f"web_requests_{st}.log"
    
    log_name = 'requestsLogger'
    logger = logging.getLogger(log_name)
    
    if LOG_TO_FILE and not logger.hasHandlers():
        log_file_handler = logging.FileHandler(log_file)
        log_file_handler.setFormatter(logging.Formatter('%(message)s'))
        log_file_handler.setLevel(1)
        logger.addHandler(log_file_handler)
        logger.parent.setLevel(0)
    else:
        logging.basicConfig(level=logging.INFO)
    
    logger.info(f"{datetime.datetime.now()} - {time.time()} - Logging has started")
    return logger

# Initialize logging and Flask app
logger = setup_logging()
app = Flask('simple_listener')

logger.info(f"Flask started - {PHOST}:{PPORT}")
logger.info("clientIP|unixtime|datetime|method|originalURL|userAgent|postPayload|host|path|requestParams|protocol|fullHeaderJSON")


def final_destination(route_attempt: str | None) -> tuple[str, int] | Any:
    """Handle all incoming requests with comprehensive logging."""
    # Make noise! - makes the console ding
    sys.stdout.write('\a')
    
    ts = time.time()
    dt = datetime.datetime.now()
    req = request
    headers = req.headers.environ
    html_header = print_html(headers)
    payload = ""
    
    # Check for proxy added headers
    if 'HTTP_X_FORWARDED_FOR' in headers:
        client_ip = headers['HTTP_REMOTE_ADDR']
        client_port = headers['HTTP_CLIENT']
        client_addr = headers['HTTP_CLIENT']
    else: 
        client_ip = headers['REMOTE_ADDR']
        client_addr = f"{headers['REMOTE_ADDR']}:{headers['REMOTE_PORT']}"
        
    log_record = f"{client_ip}|{ts}|{dt}|{req.method}|{req.url}|{headers['HTTP_USER_AGENT']}|"
    resp = f"{dt} EST  {ts}<br>{request.method}"
    
    resp += f" Request made from <b>{client_addr}</b> to {req.host}<b>{req.environ['RAW_URI']}</b><br>{headers['HTTP_USER_AGENT']} "
    
    # Handle payload
    if len(req.form) > 0:
        payload = print_html(dict(req.form))
    else:
        try:
            payload = req.data.decode(req.charset)
        except Exception:
            payload = str(req.data)
    
    if payload:
        resp += f"<h2>Payload:</h2>{payload}"
        
    log_record += f"{payload}|{req.host}|{req.path}|{req.query_string.decode(req.charset)}|{headers['SERVER_PROTOCOL']}|"
    log_record += str(headers).replace("'", '"')
    logger.info(log_record)
    
    print(f"{client_addr} requesting {req.host}{headers['RAW_URI']} at {ts}\t{dt}\t")
    resp += f"<h2>Header:</h2> {html_header}"

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
    emojis = ["💩", "🍆", "☢", "☣", "🙅‍♂️", "🤏", "🖐", "🍯", "🥒", "🏳‍🌈", "🧯", 
              "🤯", "🤬", "😡", "🤓", "👾", "🐱‍👤", "🐱‍🏍", "🙈", "⛏", "🔎", 
              "¯\\_(ツ)_/¯", "(T_T)"]

    match route_attempt:
        case 'fuck':
            return redirect('https://www.foaas.com' + random.choice(foass_endpoints), 302)
        case 'emoji':
            return (random.choice(emojis), 200)
        case 'othersite':
            return redirect(random.choice(other_sites), 302)
        case 'showclientinfo':
            return resp
        case _:
            return random.choice([
                redirect('https://www.foaas.com' + random.choice(foass_endpoints), 302),
                (random.choice(emojis), 200),
                redirect(random.choice(other_sites), 302)
            ])  
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