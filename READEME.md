# Network Request Listener/Honeypot

A Python Flask-based network monitoring tool designed to capture, log, and analyze incoming HTTP requests. This project serves as a honeypot to detect potential attackers, port scanners, and unusual network activity.

## Features

- **Comprehensive Request Logging**: Captures client IP, timestamps, headers, payloads, and user agents
- **Multi-port Monitoring**: Listens on common ports (80, 443, 8080, etc.) via Nginx proxy
- **Security Response Strategies**: Responds with random redirects or emojis to confuse attackers
- **Flexible Deployment**: Can run standalone with Flask or with Gunicorn and Nginx
- **Structured Logging**: Separate log files for requests, Nginx access/errors, and Gunicorn

## Project Structure

```
├── responder.py          # Main Flask application
├── nginx.conf           # Basic Nginx configuration
├── nginxProxy.conf      # Advanced Nginx proxy configuration
├── nginxProxy.bat       # Windows script to start Nginx
├── nginxProxy.sh        # Linux script to start Nginx
├── startServer.bat      # Windows script to start Gunicorn
├── startServer.sh       # Linux script to start Gunicorn
└── logs/                # Log directory
    ├── requests/        # Request logs
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
- **Log Format**: `clientIP|unixtime|datetime|method|originalURL|userAgent|postPayload|host|path|requestParams|protocol|fullHeaderJSON`

## Deployment Options

### Option 1: Direct Flask (Development)
```bash
python responder.py
```

### Option 2: With Gunicorn (Production)
```bash
# Windows
startServer.bat

# Linux/WSL
./startServer.sh
```

### Option 3: With Nginx Proxy
```bash
# Start Nginx proxy
# Windows
nginxProxy.bat

# Linux/WSL  
./nginxProxy.sh

# Then start the Flask app with Gunicorn
./startServer.sh
```

## Special Routes

The application includes several special routes for testing and demonstration:

- `/showclientinfo` - Displays detailed client information
- `/fuck` - Redirects to FOAAS endpoints
- `/emoji` - Returns random emoji
- `/othersite` - Redirects to random sites
- Any other route - Random response (redirect or emoji)

## Security Features

- **Request Auditing**: All requests are logged with full details
- **Response Obfuscation**: Responds with random content to hide the monitoring purpose
- **Audio Alerts**: Console bell sound for new requests
- **Client Fingerprinting**: Captures detailed client information including proxy headers

## Log Analysis

Request logs contain pipe-separated values that can be analyzed for:
- Attack patterns and frequency
- Geolocation of requests (via IP)
- User agent analysis
- Payload inspection
- Port scanning detection

## Requirements

- Python 3.12+
- Flask
- Gunicorn (optional, for production)
- Nginx (optional, for proxy setup)

## Installation

1. Clone or download the project
2. Install Python dependencies:
   ```bash
   pip install flask gunicorn
   ```
3. Ensure log directories exist (created automatically)
4. Choose deployment method and run

## Notes

- Designed for security research and network monitoring
- Use responsibly and in compliance with local laws
- Not intended for production web serving
- Consider firewall rules when exposing to networks