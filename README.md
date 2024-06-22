# hashcp

## 概要

ファイルを複製 & ファイル名をハッシュ値に一括変更するプログラムです。
変換前後のファイル名の対応表（CSVファイル）も出力します。

大量の画像データ等を、重複しないファイル名に変更したい時などに有効です。

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
