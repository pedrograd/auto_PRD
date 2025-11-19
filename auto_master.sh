#!/bin/bash
# AUTO_MASTER.SH
# ==============
# Universal automated PRD enhancement system - Shell wrapper
#
# Usage: ./auto_master.sh init | start | enhance | status | reset | git_sync
#
# This is a simple wrapper that calls auto_master.py with Python 3.
# Make sure to run: chmod +x auto_master.sh before first use.

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Call Python script with all arguments forwarded
python3 "$SCRIPT_DIR/auto_master.py" "$@"

