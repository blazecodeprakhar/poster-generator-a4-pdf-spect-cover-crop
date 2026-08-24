@echo off
title Poster Studio Desktop
echo Starting Poster Studio Desktop App...
python PosterStudioApp.py
if %ERRORLEVEL% NEQ 0 (
    echo Error starting app. Press any key to exit...
    pause
)
