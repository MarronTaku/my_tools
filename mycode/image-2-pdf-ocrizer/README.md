# image-2-pdf-ocrizer
ブラウザ上でアクセスした電子書籍を自動でスクリーンショットし、電子書籍のPDFを生成します。生成したPDFにはOCRをかけることができます。

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
python3 main.py
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
python run_image_ocrizer.py
```