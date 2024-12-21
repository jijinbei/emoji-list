import csv


class EmojiData:
    def __init__(self, text: str, emoji: str):
        self.text = text
        self.emoji = emoji

    def is_emoji(self):
        print(f'Checking emoji: "{self.emoji}"')
        if self.emoji is None:
            return False
        # elif len(self.emoji) != 1: # ToDo: 一文字だけかを確認したいが、絵文字の長さがよく分からない
        #     print(len(self.emoji))
        #     return False
        else:
            return True


class EmojiDataList:
    def __init__(self):
        self.data = []
        return None

    def append(self, emoji_data):
        self.data.append(emoji_data)

    def to_csv(self, csv_file: str):
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["emoji", "text"])
            for item in self.data:
                writer.writerow([item.emoji, item.text])
