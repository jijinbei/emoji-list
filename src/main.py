import os
from dotenv import load_dotenv
from openai import OpenAI
from watchdog.observers import Observer
import time

from file_handler import TypstFileHandler


# 設定
TYPST_FILE = os.path.abspath(r"typst\example\test.typ")
OUTPUT_CSV = os.path.join(os.path.dirname(TYPST_FILE), "emoji_list.csv")

# ファイルの存在確認
if not os.path.exists(TYPST_FILE):
    raise FileNotFoundError(f"{TYPST_FILE}が見つかりません。")

# 環境変数の読み込み
load_dotenv()
if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError(".envファイルにAPIキーが設定されていません。")

# OpenAIクライアントの初期化
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# ファイル監視の開始
event_handler = TypstFileHandler(
    client=client, typst_file=TYPST_FILE, output_csv=OUTPUT_CSV
)
observer = Observer()
observer.schedule(event_handler, path=os.path.dirname(TYPST_FILE), recursive=False)
observer.start()
print(f"監視を開始しました: {TYPST_FILE}")

# メインループ
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
