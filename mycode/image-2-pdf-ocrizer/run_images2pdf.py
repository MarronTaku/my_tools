from typing import Dict
import os
import subprocess
import sys
import shutil

from setting import setting_params

def _run_subprocess(command: list[str]) -> None:
    subprocess.run(command)

def run_autoscreenshot(params: Dict) -> None:
    # 設定
    python_script = "images2pdf/auto_screenshot.py" # 実行するPythonスクリプト
    
    # 仮想環境を作成してライブラリをインストールし、スクリプトを実行して仮想環境を削除
    """仮想環境をアクティブにしてスクリプトを実行する。"""
    print(f"仮想環境で {python_script} を実行しています...")
    
    # コマンドの実行
    command = [
        'python', python_script,
        '--pages', params['pages'],
        '--span', params['span'],
        '--output_head_dir_name', params['output_head_dir_name']
    ]
    _run_subprocess(command)

if __name__ == "__main__":
    params = setting_params()
    
    # 設定
    docker_image = "image_ocrizer:latest" # 使用するDockerイメージ
    python_script = "images2pdf/auto_screenshot.py" # 実行するPythonスクリプト
    requirements_file = "images2pdf/requirements.txt"  # requirements.txtファイル
    
    run_autoscreenshot(params)
