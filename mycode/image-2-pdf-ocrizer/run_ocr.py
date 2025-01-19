from typing import Dict
import os
import subprocess
import sys
import shutil
import argparse
from pathlib import Path

def _run_subprocess(command: list[str]) -> None:
    """コマンドを実行"""
    subprocess.run(command)

def run_ocr(pdfs_dir_path: str):
    """ocrスクリプトを実行する。"""
    command = [
        'python', 'image_ocrsizer/pdf_ocrizer.py',
        '--pdfs_dir_path', pdfs_dir_path
    ]
    _run_subprocess(command)

def args_parser():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--pdfs_dir_path", help="PDFファイルが格納されているフォルダを指定", type=str)
    
    args = parser.parse_args()
    
    return args

if __name__ == "__main__":
    args = args_parser()

    # Dockerコンテナでライブラリをインストールし、スクリプトを実行
    # テストフォルダパス：output/output_20250113155028
    # テストコマンド：python run_ocr.py --pdfs_dir_path output/output_20250113155028
    run_ocr(args.pdfs_dir_path)