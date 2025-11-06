#!/bin/zsh
# log file

SCRIPT_DIR="${0:A:h}"
LOGFILE="${SCRIPT_DIR}/session_log.txt"

# header
{
  print ""
  print "=== $(env -i TZ=UTC date -u) ==="
  print "\$ $1"
} >> "$LOGFILE"

# run the command; mirror to terminal AND append to log
zsh -lc -- "$1" 2>&1 | tee -a "$LOGFILE"

print "[done]" | tee -a "$LOGFILE"