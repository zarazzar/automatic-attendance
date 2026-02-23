#!/bin/bash

# Script untuk menjalankan absen otomatis
# Digunakan untuk cron job

cd "$(dirname "$0")"
/usr/bin/python3 main.py >> logs/attendance_$(date +\%Y\%m\%d).log 2>&1
