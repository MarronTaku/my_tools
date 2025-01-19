from PIL import Image
from pathlib import Path
from pdf2image import convert_from_path
import pyocr
import pyocr.builders
import subprocess
import re
import os
import argparse
from PyPDF2 import PdfMerger

def initialize_ocr_tool() -> tuple:
    """
    OCRツールを初期化して利用可能な言語を表示する。
    """
    tools = pyocr.get_available_tools()
    if not tools:
        raise RuntimeError("No OCR tool found.")
    tool = tools[0]
    # langs = tool.get_available_languages()
    # print(f"Available languages: {', '.join(langs)}")
    # lang = langs[1] if len(langs) > 1 else langs[0]
    lang = "eng+jpn"
    print(f"Will use lang '{lang}'")
    return tool, lang

def extract_text_from_pdf(pdf_path: Path, tool, lang: str) -> str:
    """
    PDFから画像としてページを抽出し、OCRでテキストを取得する。
    """
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
    """
    OCR結果のテキストをファイルに保存する。
    """
    with open(output_path, mode="w", encoding="utf-8") as f:
        f.write(text)
    print(f"Text saved to {output_path}")


def save_tiff_from_pages(pages, output_path: Path):
    """
    PDFのページ画像をマルチページTIFFとして保存する。
    """
    pages[0].save(
        str(output_path),
        "TIFF",
        compression="tiff_deflate",
        save_all=True,
        append_images=pages[1:],
    )
    print(f"TIFF saved to {output_path}")


def run_command(cmd: str):
    """
    シェルコマンドを実行する。
    """
    print(f"Running command: {cmd}")
    returncode = subprocess.run(cmd, shell=True)
    if returncode.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")


def overlay_text_pdf(
    tiff_path: Path, pdf_path: Path, output_path: Path, lang: str = "jpn+eng"
):
    """
    テキストのみのPDFを生成し、オーバーレイして最小サイズのPDFを作成する。
    """
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

def create_character_embedding_pdf(tool, lang, pdf_file_path, pdfs_dir_path):
    """文字埋め込みPDFを作成する"""
    # ファイル名を抽出し、拡張子を除去
    pdf_name = os.path.splitext(os.path.basename(pdf_file_path))[0]

    # ファイルパスの設定
    base_path = Path.cwd() / extract_dir(pdf_file_path)
    pdf_path = base_path / f"{pdf_name}.pdf"
    txt_path = base_path / "txt_file" / f"{pdf_name}.txt"
    out_path = base_path / "output" / f"{pdf_name}.pdf"
    image_dir_path = base_path / "image_file"
    
    # OCR処理とテキスト抽出
    text, pages = extract_text_from_pdf(pdf_path, tool, lang)

    # テキスト保存
    save_text_to_file(text, txt_path)

    # TIFF保存
    tiff_path = image_dir_path / f"{pdf_name}.tif"
    save_tiff_from_pages(pages, tiff_path)

    # テキストPDFオーバーレイ処理
    overlay_text_pdf(tiff_path, pdf_path, out_path)

    print(f"Process completed. Output saved at {out_path}")

def get_pdf_file_path_specified_folder(pdfs_dir_path):
    """指定したフォルダのpdfファイルパスを取得する"""
    pdf_files = [os.path.join(pdfs_dir_path, f) for f in os.listdir(pdfs_dir_path) if f.endswith('.pdf')]
    
    # ファイルがない場合は処理を終了
    if not pdf_files:
        print("指定されたフォルダに.pdfファイルがありません。")
        return
    
    # 指定されたフォルダ内の.pngファイルを全て取得
    pdf_files_path_sorted = sorted(pdf_files)
    
    return pdf_files_path_sorted

def create_dir(output_base_dir: str, dir_name: str) -> None:
    """ディレクトリを作成する"""
    base_path = Path.cwd()
    dir_path = base_path / output_base_dir / dir_name
    dir_path.mkdir(exist_ok=True)

def extract_dir(file_path: str) -> str:
    """親ディレクトリのパスを取得する"""
    # Pathオブジェクトを作成
    path = Path(file_path)
    # 親ディレクトリのパスを取得
    directory = path.parent
    return str(directory)

def process_pdf(pdfs_dir_path: str):
    """PDFを処理してOCR結果をテキストファイルとPDFに保存する。"""
    # PDFファイルが格納されているフォルダから全てのPDFファイルパスを取得
    pdf_files_path = get_pdf_file_path_specified_folder(pdfs_dir_path)
    # print(pdf_files_path)
    
    # OCRツール初期化
    tool, lang = initialize_ocr_tool()
    # print(tool, lang)
    
    # ファイルの親ディレクトリを取得し、ディレクトリを作成
    output_base_dir = extract_dir(pdf_files_path[0])
    create_dir(output_base_dir, "txt_file")
    create_dir(output_base_dir, "output")
    create_dir(output_base_dir, "image_file")
    
    # 文字埋め込みPDFを生成
    for pdf_file_path in pdf_files_path:
        create_character_embedding_pdf(tool, lang, pdf_file_path, pdfs_dir_path)
        print()

def concatenate_pdf_file(pdfs_dir_path: Path):
    """複数のPDFファイルを一つに結合する"""
    # 文字埋め込みPDFが生成されているディレクトリから、PDFファイルパスを取得
    ocr_done_dir_path = os.path.join(pdfs_dir_path, "output")
    ocr_done_files_path = get_pdf_file_path_specified_folder(ocr_done_dir_path)
    
    # 各PDFファイルを追加
    merger = PdfMerger()
    for pdf in ocr_done_files_path:
        merger.append(pdf)
    
    # 結合したPDFファイルを保存
    merged_output = os.path.join(ocr_done_dir_path, "merged_output.pdf")
    merger.write(merged_output)
    merger.close()
    print(f"Merged output saved at {merged_output}")

def args_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("--pdfs_dir_path", help="pdfファイルが格納されているフォルダを指定", type=str)
    
    args = parser.parse_args()
    
    return args

# 実行例、複数ページ対応
if __name__ == "__main__":
    args = args_parser()
    pdfs_dir_path: Path = args.pdfs_dir_path
    
    # 文字埋め込みpdfの生成
    process_pdf(pdfs_dir_path)
    
    # PDFファイルを結合する
    concatenate_pdf_file(pdfs_dir_path)