#!/usr/bin/env bash

# This script is triggered by Claude Code Hooks to notify the user.
# It fuses rigorous TTY tracking with macOS native notification fallbacks.

MSG="${1:-Claude needs attention}"

# 1. Walk up process tree to find an ancestor with a real TTY
# (Because background hooks often lack a controlling terminal)
PID=$$
TTY=""
while [ "$PID" != "1" ] && [ -n "$PID" ]; do
  T=$(ps -o tty= -p "$PID" 2>/dev/null | tr -d ' ')
  if [ -n "$T" ] && [ "$T" != "??" ] && [ -e "/dev/$T" ]; then
    TTY="/dev/$T"
    break
  fi
  PID=$(ps -o ppid= -p "$PID" 2>/dev/null | tr -d ' ')
done

# 2. Send Terminal Sequences if a valid TTY is found
if [ -n "$TTY" ]; then
  # Send OSC 777 desktop notification to Ghostty
  if [ -n "$TMUX" ]; then
    # Use tmux DCS passthrough sequence (requires 'set -g allow-passthrough on' in tmux.conf)
    printf '\033Ptmux;\033\033\033]777;notify;Claude Code;%s\007\033\\' "$MSG" > "$TTY"
  else
    printf '\033]777;notify;Claude Code;%s\007' "$MSG" > "$TTY"
  fi
  # Send Terminal Bell (\a) to trigger tab bounce/highlight
  printf '\a' > "$TTY"
fi

# 3. macOS Native Fallback (Ultimate Guarantee)
# We ONLY use this if we COULD NOT find a valid TTY to send the Ghostty notification to.
# This prevents duplicate notifications (one from Ghostty OSC 777, one from osascript).
if [ -z "$TTY" ] && command -v osascript &> /dev/null; then
  osascript -e "display notification \"$MSG\" with title \"Claude Code\"" >/dev/null 2>&1
fi

exit 0
