logfile=${PWD}/logs/gunicorn/request_log_$(date +%y%m%d_%H%M).txt
echo "Logging to $logfile"
mkdir -p $(dirname "$logfile")
gunicorn responder:app -w 1 --chdir . -b 0.0.0.0:1211 --access-logfile "$logfile" -t 1440 --timeout 1440 --graceful-timeout 1440 --keep-alive 1440
