import time
import mouse_point
import auto_screenshot
import make_pdf

def main():
    top_left, under_right = mouse_point.get_mouse_click_point()
    output_foldername = auto_screenshot.auto_screenshoots(page=367, top_left=top_left, under_right=under_right,
                                                          span=3, head_foldername="output")
    make_pdf.pngs_to_pdf(output_foldername)

if __name__ == "__main__":
    main()