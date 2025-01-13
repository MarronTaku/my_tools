from typing import Dict
import os
import subprocess
import sys
import shutil

def _run_subprocess(command: list[str]) -> None:
    """コマンドを実行"""
    subprocess.run(command)

def run_ocr_in_docker(image: str, script: str):
    """指定したDockerコンテナ内でスクリプトを実行する。"""
    print(f"Dockerコンテナで {script} を {image} イメージを使用して実行しています...")
    
    command = [
        "docker", "run", "--rm",
        "-v", f"{os.getcwd()}:/app",  # 現在のディレクトリをコンテナの/appにマウント
        "-w", "/app",                 # コンテナ内で作業ディレクトリを/appに設定
        image,                        # 使用するDockerイメージ
        "/bin/bash", "-c",            # Bashを使って複数のコマンドを実行
        "python", script  # ライブラリをインストールしてスクリプトを実行
    ]
    subprocess.run(command)

if __name__ == "__main__":
    # 設定
    docker_image = "image_ocrizer:latest" # 使用するDockerイメージ
    python_script = "image_ocrsizer/pdf_ocrizer.py" # 実行するPythonスクリプト

    # Dockerコンテナでライブラリをインストールし、スクリプトを実行
    run_ocr_in_docker(docker_image, python_script)