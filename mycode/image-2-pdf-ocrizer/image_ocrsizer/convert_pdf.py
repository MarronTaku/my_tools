from PIL import Image

def png_to_pdf(input_png_path, output_pdf_path):
    """
    PNG画像をPDFに変換する関数。

    Args:
        input_png_path (str): 入力PNG画像のパス。
        output_pdf_path (str): 出力PDFのパス。
    """
    # PNG画像を開く
    image = Image.open(input_png_path)

    # RGB形式に変換 (PDF保存のため)
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    # PDFとして保存
    image.save(output_pdf_path, "PDF")
    print(f"PNG画像をPDF形式で保存しました: {output_pdf_path}")

# 実行例
input_png = "/home/mycode/image-2-pdf-ocrizer/output/sample_output.png"  # 入力PNG画像のパス
output_pdf = "/home/mycode/image-2-pdf-ocrizer/output/sample_output.pdf"  # 出力PDFのパス

png_to_pdf(input_png, output_pdf)
