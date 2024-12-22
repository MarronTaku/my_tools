import cv2
from PIL import Image, ImageEnhance

def upscale_and_enhance_image(input_path, output_path, scale_factor=2.0):
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
    


# 実行例
input_file = "/home/mycode/image-2-pdf-ocrizer/input/sample.png"
output_file = "/home/mycode/image-2-pdf-ocrizer/output/sample_output.png"

upscale_and_enhance_image(input_file, output_file)
