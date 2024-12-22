from PIL import Image
from pathlib import Path
from pdf2image import convert_from_path
import pyocr
import pyocr.builders
import subprocess
import re
import os


def initialize_ocr_tool() -> tuple:
    """OCRツールを初期化して利用可能な言語を表示する。"""
    tools = pyocr.get_available_tools()
    if not tools:
        raise RuntimeError("No OCR tool found.")
    tool = tools[0]
    langs = tool.get_available_languages()
    print(f"Available languages: {', '.join(langs)}")
    lang = langs[1] if len(langs) > 1 else langs[0]
    print(f"Will use lang '{lang}'")
    return tool, lang


def extract_text_from_pdf(pdf_path: Path, tool, lang: str) -> str:
    """PDFから画像としてページを抽出し、OCRでテキストを取得する。"""
    pages = convert_from_path(str(pdf_path), 300)
    text = ""
    for i, page in enumerate(pages):
        page_text = tool.image_to_string(
            page, lang=lang, builder=pyocr.builders.TextBuilder(tesseract_layout=6)
        )
        # 不要なスペースを削除
        page_text = re.sub(r"([あ-んア-ン一-龥ー])\s+((?=[あ-んア-ン一-龥ー]))", r"\1\2", page_text)
        text += page_text
    return text, pages


def save_text_to_file(text: str, output_path: Path):
    """OCR結果のテキストをファイルに保存する。"""
    with open(output_path, mode="w", encoding="utf-8") as f:
        f.write(text)
    print(f"Text saved to {output_path}")


def save_tiff_from_pages(pages, output_path: Path):
    """PDFのページ画像をマルチページTIFFとして保存する。"""
    pages[0].save(
        str(output_path),
        "TIFF",
        compression="tiff_deflate",
        save_all=True,
        append_images=pages[1:],
    )
    print(f"TIFF saved to {output_path}")


def run_command(cmd: str):
    """シェルコマンドを実行する。"""
    print(f"Running command: {cmd}")
    returncode = subprocess.run(cmd, shell=True)
    if returncode.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")


def overlay_text_pdf(
    tiff_path: Path, pdf_path: Path, output_path: Path, lang: str = "jpn+eng"
):
    """テキストオンリーPDFを生成し、オーバーレイして最小サイズのPDFを作成する。"""
    text_pdf_path = tiff_path.with_name(tiff_path.stem + "_TO.pdf")
    
    # print(tiff_path.with_suffix("_TO"))

    # Tesseractコマンド
    cmd_tesseract = (
        f'tesseract -c page_separator="[PAGE SEPRATOR]" -c textonly_pdf=1 '
        f'"{tiff_path}" "{tiff_path.with_name(tiff_path.stem + "_TO")}" -l {lang} pdf'
    )
    run_command(cmd_tesseract)

    # QPDFコマンド
    cmd_qpdf = (
        f'qpdf --overlay "{text_pdf_path}" -- "{pdf_path}" "{output_path}"'
    )
    run_command(cmd_qpdf)


def process_pdf(pdf_name: str):
    """PDFを処理してOCR結果をテキストファイルとPDFに保存する。"""
    # パスの設定
    base_path = Path(".")
    pdf_path = base_path / "pdf_file" / f"{pdf_name}.pdf"
    txt_path = base_path / "txt_file" / f"{pdf_name}.txt"
    out_path = base_path / "pdf_file" / "output" / f"{pdf_name}.pdf"
    image_dir = base_path / "image_file"
    image_dir.mkdir(exist_ok=True)

    # OCRツール初期化
    tool, lang = initialize_ocr_tool()

    # OCR処理とテキスト抽出
    text, pages = extract_text_from_pdf(pdf_path, tool, lang)

    # テキスト保存
    save_text_to_file(text, txt_path)

    # TIFF保存
    tiff_path = image_dir / f"{pdf_name}.tif"
    save_tiff_from_pages(pages, tiff_path)

    # テキストPDFオーバーレイ処理
    overlay_text_pdf(tiff_path, pdf_path, out_path)

    print(f"Process completed. Output saved at {out_path}")


# 実行例
if __name__ == "__main__":
    process_pdf("sample_output")
