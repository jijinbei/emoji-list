from watchdog.events import FileSystemEventHandler
import re
import os
from typing import List
from openai import OpenAI

from api import fetch_emojis
from data import EmojiDataList


class TypstFileHandler(FileSystemEventHandler):
    """
    ファイル変更イベントを監視するクラス
    """

    def __init__(self, client: OpenAI, typst_file: str, output_csv: str):
        self.client = client
        self.typst_file = typst_file
        self.output_csv = output_csv

    def on_modified(self, event):
        if os.path.abspath(event.src_path) == os.path.abspath(self.typst_file):
            print(f"{self.typst_file}が変更されました。進行中...")
            with open(self.typst_file, "r", encoding="utf-8") as f:
                content = f.read()
            items = emoji_list_parser(content)
            if items == None:
                return None

            emoji_data_list = EmojiDataList()
            # ChatGPT APIで絵文字を取得
            for item in items:
                # ToDo: 変わっていないものはAPIを呼ばないようにする
                emoji_data = fetch_emojis(client=self.client, text=item)
                if emoji_data != None:
                    emoji_data_list.append(emoji_data)

            # CSVファイルに書き込み
            emoji_data_list.to_csv(self.output_csv)


def emoji_list_parser(content: str) -> List[str]:
    """
    Typstファイルを解析して、#emoji-listセクションから項目を抽出する関数
    """
    # #emoji-list(...)の内容を抽出
    pattern = r"#emoji-list\(([\s\S]*?)\)"
    matches = re.findall(pattern, content)
    if not matches:
        print("#emoji-list()が見つかりませんでした。")
        return []

    # 全セクションから項目を抽出
    all_items = []
    for match in matches:
        items = re.findall(r"\[(.*?)\]", match)
        if not items:
            print("空の#emoji-list()セクションがあります。")
            continue
        all_items.extend(items)

    return all_items
