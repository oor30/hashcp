# HashFilename.py

## 概要

コマンドライン引数に指定したディレクトリ内に存在するファイルを複製し、ファイル名をファイルのハッシュ値に変換するプログラムです。
元のファイル名と変換後のファイル名の対応表をCSV形式で出力します。

## 使い方

```
python hashFilename.py [options] <directory>
```

### オプション

```
-o --output <directory>
```
複製先のディレクトリ名とCSVファイル名を指定します（デフォルト： output）。

```
-r --recursive
```
サブディレクトリ内のファイルも、再帰的に実行します。

```
-e --extensions <extensions...>
```
対象となるファイルの拡張子を、スペース区切りで指定します。
