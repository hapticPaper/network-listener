@echo off
cd /d "%~dp0"
nginx -c "%cd%\nginxProxy.conf"