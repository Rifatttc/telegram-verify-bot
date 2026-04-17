#!/bin/bash
pkg update && pkg upgrade -y
pkg install python -y
pip install telethon
python termux_tool.py
