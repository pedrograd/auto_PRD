#!/bin/bash
# PRD Master - Shell Wrapper
# Simple wrapper for auto_master.py

python3 "$(dirname "$0")/auto_master.py" "$@"
