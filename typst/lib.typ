// 特定のtextに対応するemojiを検索し表示する関数
#let emoji-list(csv_path, ..row_texts) = {
  set text(font: "Noto Color Emoji")
  let csv = csv(csv_path).slice(1)
  for (emoji, text) in csv {
    for row_text in row_texts.pos() {
      if [#text] == row_text {
        block[
          #emoji#h(0.5em)#text
        ]
      }
    }
  }
}