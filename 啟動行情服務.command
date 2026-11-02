#!/bin/bash
cd "$(dirname "$0")"
echo "資產日常行情服務已啟動。請保持此視窗開啟，然後重新整理 App。"
/Users/katherine/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 quote_server.py
