from PIL import Image
import os

def pngs_to_pdf(folder_path):
    """
    指定されたフォルダ内のすべての.pngファイルを一つのPDFに結合する。

    :param folder_path: .pngファイルが格納されたフォルダのパス
    """
    # 指定されたフォルダ内の.pngファイルを全て取得
    png_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.png')]
    png_files_sorted = sorted(png_files)

    # ファイルがない場合は処理を終了
    if not png_files_sorted:
        print("指定されたフォルダに.pngファイルがありません。")
        return

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
    output_path = os.path.join(folder_path, "output.pdf")
    first_image.save(output_path, "PDF", save_all=True, append_images=img_list)

    print(f"PDFが保存されました: {output_path}")