from pynput import mouse

left_up_x, left_up_y, right_down_x, right_down_y = [0,0,0,0]
num_press = 0

def get_mouse_click_point():
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
    # 範囲の確認
    # print(f"left_up_x: {left_up_x}")
    # print(f"left_up_y: {left_up_y}")
    # print(f"right_down_x: {right_down_x}")
    # print(f"right_down_y: {right_down_y}")

    top_left = [int(left_up_x), int(left_up_y)]
    under_right = [int(right_down_x), int(right_down_y)]

    return top_left, under_right
    
def on_click(x, y, button, pressed):
    global left_up_x, left_up_y, right_down_x, right_down_y, num_press
    if pressed:
        # 1回目のクリックはウィンドウの切り替え用で何もしない
        if num_press == 0:
            num_press = 1
        # 2回目のクリックはスクリーンショットを撮る範囲の左上を指定
        elif num_press == 1:
            num_press = 2
            left_up_x, left_up_y = x, y
        # 3回目のクリックはスクリーンショットを撮る範囲の右下を指定して終了
        else:
            right_down_x, right_down_y = x, y
            return False