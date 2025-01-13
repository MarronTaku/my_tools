import cv2
import shutil
import os
from PIL import Image, ImageEnhance
from pathlib import Path


def move_file(src_path: str, dest_dir: str):
    """
    指定したファイルを新しいディレクトリに移動する関数。

    Args:
        src_path (str): 移動するファイルのパス。
        dest_dir (str): ファイルを移動する先のディレクトリのパス。
    """
    # パスオブジェクトを作成
    src = Path(src_path)
    dest = Path(dest_dir)

    # ディレクトリが存在しない場合は作成
    dest.mkdir(parents=True, exist_ok=True)

    # ファイルを移動
    shutil.move(str(src), str(dest / src.name))
    print(f"{src} を {dest} に移動しました。")

def _upscale_and_enhance_image(input_path: str, output_path: str, scale_factor: float = 1.0):
    """
    画像を指定したスケールで拡大し、鮮明化して出力する関数。

    Args:
        input_path (str): 入力画像のファイルパス。
        output_path (str): 拡大・鮮明化後の画像の保存先パス。
        scale_factor (float): 画像を拡大する倍率（例: 2.0で2倍）。
    """
    # カラー画像を読み込む
    image = cv2.imread(input_path)

    # 画像サイズを取得
    height, width = image.shape[:2]

    # 画像を拡大
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    upscaled_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)

    # シャープ化 (ガウシアンブラーを引き算する)
    gaussian_blur = cv2.GaussianBlur(upscaled_image, (0, 0), 3)
    sharpened_image = cv2.addWeighted(upscaled_image, 1.5, gaussian_blur, -0.5, 0)

    # 一時ファイルにシャープ化した画像を保存
    temp_path = "temp_upscaled_sharpened.png"
    cv2.imwrite(temp_path, sharpened_image)

    # PILでコントラストを調整
    pil_image = Image.open(temp_path)
    enhancer = ImageEnhance.Contrast(pil_image)
    contrast_image = enhancer.enhance(2.0)  # コントラストを2倍にする
    contrast_image.save(output_path)

    print(f"拡大・鮮明化した画像を保存しました: {output_path}")


def pngs_to_pdf(dir_path):
    """
    指定されたフォルダ内のすべての.pngファイルを一つのPDFに結合する。

    :param folder_path: .pngファイルが格納されたフォルダのパス
    """
    png_files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith('.png')]
    
    # ファイルがない場合は処理を終了
    if not png_files:
        print("指定されたフォルダに.pngファイルがありません。")
        return
    
    # 指定されたフォルダ内の.pngファイルを全て取得
    png_files_sorted = sorted(png_files)

    # 画像の見た目を向上させる
    for file in png_files:
        _upscale_and_enhance_image(file, file)

    # 画像の並び替え
    png_files_sorted = sorted(png_files)

    # 最初の画像を基にPDFを作成
    img_list = []
    first_image = Image.open(png_files_sorted[0])
    first_image.convert('RGB')
    
    # 2番目以降の画像をリストに追加
    for file in png_files_sorted[1:]:
        img = Image.open(file)
        img.convert('RGB')
        img_list.append(img)

    # PDFを保存
    output_path = os.path.join(dir_path, "output.pdf")
    first_image.save(output_path, "PDF", save_all=True, append_images=img_list)

    print(f"PDFが保存されました: {output_path}")