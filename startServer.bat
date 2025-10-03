@echo off
cd /d "%~dp0"
gunicorn responder:app -w 1 --chdir "%cd%" -b 0.0.0.0:1211 --access-logfile "%cd%\logs\gunicorn\request_log_%date:~10,4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%.txt" -t 1440 --timeout 1440 --graceful-timeout 1440 --keep-alive 1440
