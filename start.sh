#!/bin/bash

# Railway startup script for VouchBot
echo "Starting VouchBot..."

# Check if DISCORD_TOKEN is set
if [ -z "$DISCORD_TOKEN" ]; then
    echo "Error: DISCORD_TOKEN environment variable is not set!"
    echo "Please set DISCORD_TOKEN in Railway dashboard."
    exit 1
fi

# Start the bot
python vouch_bot1.py