# Network Request Listener/Honeypot

A Python Flask-based network monitoring tool designed to capture, log, and analyze incoming HTTP requests. This project serves as a honeypot to detect potential attackers, port scanners, and unusual network activity with structured logging and IP request counting.

## Features

- **Structured Logging with Structlog**: JSON-formatted logs with context-aware request tracking
- **IP Request Counting**: Tracks and displays request counts per IP address
- **Comprehensive Request Logging**: Captures client IP, timestamps, headers, payloads, and user agents
- **Multi-port Monitoring**: Listens on common ports (80, 443, 8080, etc.) via Nginx proxy
- **Security Response Strategies**: Responds with random redirects or emojis to confuse attackers
- **Flexible Deployment**: Can run standalone with Flask or with Gunicorn and Nginx
- **Real-time Statistics**: View IP statistics and request patterns

## Prerequisites

### Required Software
- **Python 3.12+**
- **pip** (Python package installer)
- **nginx** (for proxy functionality)

### macOS Installation
```bash
# Install Python (if not already installed)
brew install python

# Install nginx
brew install nginx

# Verify installations
python3 --version
nginx -v
```

### Linux Installation
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip nginx

# CentOS/RHEL
sudo yum install python3 python3-pip nginx

# Verify installations
python3 --version
nginx -v
```

## Setup Instructions

### 1. Clone and Setup Project
```bash
# Clone the repository
git clone <repository-url>
cd network-listener

# Install Python dependencies
pip3 install -r requirements.txt
```

### 2. Configure Paths
The project uses absolute paths in nginx configuration. You need to update the paths in `nginxProxy.conf`:

```bash
# Edit the nginx configuration
nano nginxProxy.conf

# Update these lines to match your project path:
# access_log /YOUR/FULL/PATH/TO/network-listener/logs/nginx/localhost.access.log;
# error_log  /YOUR/FULL/PATH/TO/network-listener/logs/nginx/localhost.error.log;
```

### 3. Make Scripts Executable
```bash
chmod +x startServer.sh
chmod +x nginxProxy.sh
```

## Project Structure

```
├── responder.py          # Main Flask application with structlog
├── nginx.conf           # Basic Nginx configuration
├── nginxProxy.conf      # Advanced Nginx proxy configuration
├── nginxProxy.sh        # Script to start Nginx proxy
├── startServer.sh       # Script to start Gunicorn server
├── requirements.txt     # Python dependencies
└── logs/                # Log directory (created automatically)
    ├── requests/        # Structured JSON request logs
    ├── nginx/          # Nginx access and error logs
    └── gunicorn/       # Gunicorn logs
```

## Configuration

### Server Settings
- **Host**: `0.0.0.0` (all network interfaces)
- **Flask/Gunicorn Port**: `1211` (default) 
- **Monitored Ports**: 21, 25, 80, 443, 465, 587, 3000, 3333, 5000, 5555, 8080, 8888, 8889

### Logging Configuration
- **Request Logs**: `logs/requests/web_requests_[timestamp].log`
- **Log Format**: Structured JSON with contextual information
- **IP Tracking**: Automatic counting and statistics per IP address

## Deployment Options

### Option 1: Direct Flask (Development)
```bash
python3 responder.py
```

### Option 2: With Gunicorn (Recommended)
```bash
./startServer.sh
```

### Option 3: With Nginx Proxy (Full Setup)
```bash
# Start Nginx proxy (creates log directories automatically)
./nginxProxy.sh

# In another terminal, start the Flask app with Gunicorn
./startServer.sh
```

## Special Routes

The application includes several special routes for testing and demonstration:

- `/showclientinfo` - Displays detailed client information and IP statistics
- `/stats` - Shows IP request statistics in JSON format
- `/fuck` - Redirects to FOAAS endpoints
- `/emoji` - Returns random emoji
- `/othersite` - Redirects to random sites
- Any other route - Random response (redirect or emoji)

## Security Features

- **Structured Request Auditing**: All requests logged with full context in JSON format
- **IP Request Tracking**: Monitors request patterns per IP address
- **Response Obfuscation**: Responds with random content to hide monitoring purpose
- **Audio Alerts**: Console bell sound for new requests
- **Client Fingerprinting**: Captures detailed client information including proxy headers
- **Real-time Statistics**: Live tracking of unique IPs and request counts

## Log Analysis

Request logs are now in structured JSON format for easy analysis:
```json
{
  "client_ip": "127.0.0.1",
  "method": "GET",
  "path": "/",
  "request_count_for_ip": 1,
  "total_unique_ips": 1,
  "timestamp": "2025-10-03 15:05:41",
  "event": "Request received",
  "level": "info"
}
```

Analyze for:
- Attack patterns and frequency by IP
- Request counting and rate analysis
- User agent patterns
- Payload inspection
- Port scanning detection

## Troubleshooting

### Permission Issues
```bash
# If nginx fails to start
sudo nginx -s stop  # Stop any running nginx
sudo nginx -c /full/path/to/nginxProxy.conf

# If log files can't be created
sudo chown -R $USER:$USER logs/
```

### Path Issues
- Ensure all paths in `nginxProxy.conf` are absolute paths
- Verify log directories are created with proper permissions
- Check that nginx has write access to log directories

## Requirements

- Python 3.12+
- Flask 3.0+
- Gunicorn 21.2+
- Structlog 23.1+
- Rich 13.5+
- Nginx (latest stable)

## Installation

1. Follow the setup instructions above
2. Install system dependencies (Python, nginx)
3. Install Python dependencies: `pip3 install -r requirements.txt`
4. Configure paths in `nginxProxy.conf`
5. Make scripts executable
6. Choose deployment method and run

## Notes

- Designed for security research and network monitoring
- Use responsibly and in compliance with local laws
- Not intended for production web serving
- Consider firewall rules when exposing to networks
- Logs contain sensitive information - secure appropriately