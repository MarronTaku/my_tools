import argparse
import pyautogui
import time
import os
import datetime

import mouse_point, make_pdf

def _make_output_dir(head_dir_name: str):
    """フォルダを作成する"""
    output_dir_path = "images2pdf/output/" + head_dir_name + "_" + str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    os.mkdir(output_dir_path)
    return output_dir_path

def _auto_screenshot_img(
    page_number: int, top_left: list, under_right: list, head_file_name: str, output_dir_path: str, span: int):
    """出力ファイル名(頭文字_連番.png)を定め、スクリーンショットを保存する"""
    # 出力ファイル名(頭文字_連番.png)
    output_file_name = head_file_name + "_" + str(page_number+1).zfill(4) + '.png'
    
    # スクリーンショット取得・保存処理
    # キャプチャ範囲： 左上のx座標, 左上のy座標, 幅, 高さ
    s = pyautogui.screenshot(region=(top_left[0], top_left[1], (under_right[0]-top_left[0]), under_right[1]-top_left[1]))
    
    # 出力パス： 出力フォルダ名 / 出力ファイル名
    s.save(output_dir_path + "/" + output_file_name)
    
    # 右矢印キー押下
    pyautogui.keyDown('right')
    
    # 次のスクリーンショットまで待機
    time.sleep(span)

def auto_screenshots(
    page: int, top_left: list, under_right: list, span: int, output_head_dir_name: str):
    """指定したページ数を自動でスクリーンショットを行う"""
    output_dir_path = _make_output_dir(output_head_dir_name)
    for page_number in range(page):
        _auto_screenshot_img(page_number, top_left, under_right, output_head_dir_name, output_dir_path, span)
        print(page_number)
    
    return output_dir_path

def args_parser():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--pages", help="スクリーンショットを行いたいページ数", type=int)
    parser.add_argument("--span", help="スクリーンショットを行う間隔[s]", type=int)
    parser.add_argument("--output_head_dir_name", help="出力するときの出力ファイル名", type=str)
    
    args = parser.parse_args()
    
    return args

def main():
    # パラメータを取得
    args = args_parser()
    
    # 左上と右下の座標を取得する
    top_left, under_right = mouse_point.get_mouse_click_point()
    
    # スクリーンショット画像を自動で取得する
    output_dir_path = auto_screenshots(
        page=args.pages, top_left=top_left, under_right=under_right,
        span=args.span, output_head_dir_name=args.output_head_dir_name)
    
    # 指定したフォルダーからpdfを作成する
    make_pdf.pngs_to_pdf(output_dir_path)

if __name__ == "__main__":
    main()