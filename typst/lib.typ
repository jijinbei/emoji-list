// 特定のtextに対応するemojiを検索し表示する関数
#let emoji-list(csv_path, ..row_texts) = {
  let csv = csv(csv_path).slice(1)
  for row_text in row_texts.pos() {
    for (emoji, txt) in csv {
      if [#txt] == row_text {
        block[
          #text(font: "Noto Color Emoji", emoji)#h(0.5em)#txt
        ]
      }
    }
  }
}