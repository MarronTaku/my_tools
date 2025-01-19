# ベースにするイメージ
FROM python:3.11.9

# シェルをbashに設定
SHELL ["/bin/bash", "-c"]

# タイムゾーンの設定
ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 入力待ちをオフ
ENV DEBIAN_FRONTEND=noninteractive

# 最小パッケージ
RUN apt update -y \
    && apt upgrade -y \
    && apt install -y --no-install-recommends \
    x11-apps \
    git \
    curl \
    zip \
    unzip \
    ca-certificates \
    wget \
    gnupg2 \
    lsb-release \
    cmake

# OCRに必要なパッケージのインストール
RUN apt install -y tesseract-ocr tesseract-ocr-eng tesseract-ocr-jpn x11-utils poppler-utils qpdf

# ocrに必要なライブラリのインストール
COPY image_ocrsizer/requirements.txt .
RUN pip install -r requirements.txt && rm requirements.txt

