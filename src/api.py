from openai import OpenAI
from data import EmojiData


def fetch_emojis(client: OpenAI, text: str) -> EmojiData:
    """
    OpenAI APIを使って絵文字を生成する関数
    """
    # OpenAI Chat APIを呼び出し
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"次の文章に適した絵文字一つだけ提案してください: {text}",
            }
        ],
        model="gpt-4",  # 使用するモデル
    )

    # レスポンスから絵文字を抽出
    emoji = response.choices[0].message.content.strip()
    emoji_data = EmojiData(text, emoji)
    if emoji_data.is_emoji():
        return emoji_data
    else:
        return None
