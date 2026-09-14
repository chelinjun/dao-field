#!/usr/bin/env bash
# TianDao Seed · one-click launch (Linux/macOS). Browser auto-opens via app.py.
cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
    echo "[错误] 没找到 python3。请先安装 Python 3.8+。"
    echo "[ERROR] python3 not found. Install Python 3.8+ first."
    read -n1 -r -p "按任意键退出 / Press any key to exit..."
    exit 1
fi

python3 app.py
