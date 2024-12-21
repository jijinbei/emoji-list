# emoji-list

Typstで最適な絵文字を自動で入力してほしい！！ということで作ってみた

## 使い方

`.env`を作成し、

```
OPENAI_API_KEY="sk-proj-cXRxSZD......"
```

のように書きこむ

## 実行方法

実行方法は次のように書く

```
rye run emoji-list <typst-file>
```

例えば、

```
rye run emoji-list example\test.typ
```