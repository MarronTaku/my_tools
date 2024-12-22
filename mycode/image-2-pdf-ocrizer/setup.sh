#!/bin/bash

# 更新と必要なパッケージのインストール
echo "Updating system and installing required packages..."
apt update
apt install -y tesseract-ocr tesseract-ocr-eng tesseract-ocr-jpn x11-utils poppler-utils

# # Python仮想環境を作成
echo "Creating a Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# 必要なPythonパッケージをインストール
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete! Remember to activate the virtual environment with 'source venv/bin/activate'."
