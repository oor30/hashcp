
https://github.com/oor30/hashcp/assets/66106684/f29232b8-c88f-4ad3-9a91-dd7ec18b1444
# hashcp

[README in English](https://github.com/oor30/hashcp/blob/master/README-en.md)

## 概要

ファイルを複製 & ファイル名をハッシュ値（MD5）に一括変更するプログラムです。<br>
変換前後のファイル名の対応表（CSVファイル）も出力します。

大量の画像データ等を、重複しないファイル名に変更したい時などに有効です。

![hashcp_demo](https://github.com/oor30/hashcp/assets/66106684/e4d76912-721d-45db-8ed0-a4f3d0f67ba9)

## 導入方法

### 必要環境

- Python
- pip

### インストール

```zsh
pip install git+https://github.com/oor30/hashcp.git
```

## 使い方

```zsh
hashcp [options] <directory>
```

### オプション

```zsh
-o --output <directory>
```

複製先のディレクトリ名とCSVファイル名を指定します（デフォルト： output）。

```zsh
-r --recursive
```

サブディレクトリ内のファイルも、再帰的に実行します。

```zsh
-e --extensions <extensions...>
```

対象となるファイルの拡張子を、スペース区切りで指定します。

```zsh
-t --keeptree
```

ディレクトリ構造を保持したまま複製します。
