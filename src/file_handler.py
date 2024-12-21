from watchdog.events import FileSystemEventHandler
import re
import csv
import os
from typing import List, Dict
from openai import OpenAI

from api import fetch_emojis
from data import EmojiDataList, EmojiData


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

            # すべてのemoji-list項目を解析
            items = emoji_list_parser(content)
            if items == []:
                return None

            # 既存データをCSVから読み込む
            existing_data = self.load_existing_data()

            # 新規データを取得
            new_data = EmojiDataList()
            for item in items:
                if not any(data.text == item for data in existing_data.data):
                    # 新しい項目のみAPIで取得
                    emoji_data = fetch_emojis(client=self.client, text=item)
                    if emoji_data:
                        new_data.unique_append(emoji_data)

            # 既存データと新規データを結合
            existing_data.concat(new_data)

            # 結果をCSVファイルに書き込み
            existing_data.to_csv(self.output_csv)

    def load_existing_data(self) -> EmojiDataList:
        """
        既存のCSVデータを読み込んでEmojiDataListとして返す
        """
        emoji_data_list = EmojiDataList()
        if not os.path.exists(self.output_csv):
            return emoji_data_list

        with open(self.output_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if "text" in row and "emoji" in row:
                    emoji_data_list.unique_append(
                        EmojiData(text=row["text"], emoji=row["emoji"])
                    )
        return emoji_data_list


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
