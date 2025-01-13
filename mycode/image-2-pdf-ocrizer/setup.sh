#!/bin/bash

# Python仮想環境を作成
echo "Creating a Python virtual environment..."
python3 -m venv .venv

# ライブラリのインストール
.venv/bin/pip3 install -r images2pdf/requirements.txt

# 仮想環境のアクティベート
source ./venv/bin/activate
