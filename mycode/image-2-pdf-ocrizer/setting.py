from typing import Dict

def setting_params() -> Dict:
    # パラメータを設定
    params = {
        'pages': '1',                    # ページ数
        'output_head_dir_name': 'output',    # 出力ファイル名
        'span': '3'                       # 自動スクリーンショットの間隔[s]
    }
    
    return params