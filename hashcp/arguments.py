import argparse
from pathlib import Path
import os

# オプション引数 -e=image を指定した場合の、対象ファイル拡張子
IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'svg']
# デフォルトの出力先ディレクトリ名
DEFAULT_OUTPUT = 'output'

def get_args():
  """コマンドライン引数を取得する
  """
  parser = argparse.ArgumentParser(
    prog='hashcp',
    description='copy files in directory, and rename the files hash value.'
  )
  # ---必須引数---
  # ソースディレクトリ
  parser.add_argument('src_dir', help='source directory', type=existing_path)
  # ---オプション引数---
  # 出力先ディレクトリ名
  parser.add_argument('-o', '--output', help='Set output directory name and csv name (default: %(default)s)', type=str, default=DEFAULT_OUTPUT)
  # 再帰実行フラグ
  parser.add_argument('-r', '--recursive', help='Recursively ', action='store_true')
  # ディレクトリ構造保持フラグ
  parser.add_argument('-t', '--keeptree', help='copy files with keeping tree structure', action='store_true')
  # ハッシュ化アルゴリズム
  parser.add_argument('-a', '--algorithm', help='choose hash algorithm (default: %(default)s)',
                      choices=['md5', 'sha256', 'sha3_256', 'sha1', 'sha224', 'sha384', 'sha512', 'sha3_224', 'sha3_384', 'sha3_512'], default='md5')
  # 対象ファイル拡張子
  parser.add_argument('-e',
                      '--extensions',
                      help='Type target file extensions separated by space. if you type \'all\', all files will be target. if you type \'image\', image files will be target({}).'.format(' '.join(IMAGE_EXTENSIONS)),
                      nargs='*',
                      type=str,
                      default=['image'])
  args = parser.parse_args()
  return args

def existing_path(path_str: str) -> Path:
    """文字列が指すファイルが存在すれば、そのファイルを指すPathオブジェクトを返す
    存在しなければ、ArgumentTypeErrorを送出する
    """
    path = Path(path_str)
    if not os.path.isdir(path):
        message = f"{path_str}: No such file or directory"
        raise argparse.ArgumentTypeError(message)
    return path