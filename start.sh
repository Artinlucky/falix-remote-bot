#!/bin/bash
Xvfb :99 -screen 0 1024x768x24 &

echo "Starting bot..."
python bot.py
