# image-2-pdf-ocrizer
ブラウザ上でアクセスしたページを自動でスクリーンショットし、文字埋め込みPDFを生成します。

# 処理フロー
1. ブラウザーで電子書籍を表示し、自動スクリーンショットで画像を取得してPDFに変換する  
    1. 指定したページ数を自動でスクリーンショットする  
    2. スクリーンショットした画像が格納されているフォルダのpngファイルをPDFに変換する  
2. 変換したPDFをOCR処理を行い文字埋め込みPDFを生成する  
    1. 下記の処理を指定したページ数分繰り返す  
        1. PDFファイルが格納されているフォルダからPDFファイルを読み込む  
        2. OCRを行い、PDFファイルからテキスト抽出する  
        3. 抽出したテキストをPDFファイルに埋め込む  

## 動作環境の構築
1. venvでimages2pdfのPython環境を構築します。
```bash
bash setup.sh
```

2. dockerでimage_ocrizerのイメージファイルを構築します。
```bash
docker build -t image_ocrizer:latest .
``` 

## 実行方法
### PDF生成
1. pythonの実行します。
```bash
# venvを有効化
source ./venv/bin/activate

# 自動スクリーンショットを実行
python images2pdf.py
```
2. 合計3回クリックを行い、スクリーンショット範囲をクリックで指定します。
    1. ブラウザ選択
    2. スクリーンショット左上座標
    3. スクリーンショット右下座標  
3. 画面が自動で切り替わることを確認
4. 全てのスクリーンショットが完了したら「output_」フォルダにpngとpdfファイルが出力

### OCR化
1. PDF生成が完了したら、image_ocrizer/pdf_fileに生成したPDFファイルをコピーします。

2. pythonスクリーンショットを実行します。
```bash
# Dockerコンテナを起動
docker compose up -d

# コンテナ内部で実行
python run_image_ocrizer.py
```