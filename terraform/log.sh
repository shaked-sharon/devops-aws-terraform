#!/bin/bash
# Script for loging

LOGFILE="terraform/session_log.txt"

echo "" >> "$LOGFILE"
echo "=== $(date -u) ===" >> "$LOGFILE"
echo "$ $1" >> "$LOGFILE"

bash -lc "$1" >> "$LOGFILE" 2>&1

echo "[done]" >> "$LOGFILE"