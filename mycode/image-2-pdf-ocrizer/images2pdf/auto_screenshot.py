import pyautogui
import time
import os
import datetime

def make_output_dir(head_foldername: str):
    folder_name = head_foldername + "_" + str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    os.mkdir(folder_name)
    return folder_name

def auto_screenshoot_img(page_number: int, top_left: list, under_right: list, head_filename: str, foldername: str, span: int):
    # 出力ファイル名(頭文字_連番.png)
    out_filename = head_filename + "_" + str(page_number+1).zfill(4) + '.png'
    # スクリーンショット取得・保存処理
    # キャプチャ範囲： 左上のx座標, 左上のy座標, 幅, 高さ
    s = pyautogui.screenshot(region=(top_left[0], top_left[1], (under_right[0]-top_left[0]), under_right[1]-top_left[1]))
    # 出力パス： 出力フォルダ名 / 出力ファイル名
    s.save(foldername + '/' + out_filename)
    # 右矢印キー押下
    pyautogui.keyDown('right')
    # 次のスクリーンショットまで待機
    time.sleep(span)

def auto_screenshoots(page: int, top_left: list, under_right: list, span: int,
                          head_foldername: str):
    foldername = make_output_dir(head_foldername)
    for page_number in range(page):
        auto_screenshoot_img(page_number, top_left, under_right, head_foldername, foldername, span=span)
        print(page_number)
    
    return foldername
