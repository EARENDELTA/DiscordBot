@echo off
start "" docker start libretranslate
timeout /t 10
cd C:\DiscordBot
python bot.py