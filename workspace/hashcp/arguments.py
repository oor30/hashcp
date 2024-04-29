import argparse
from pathlib import Path
import os

IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'svg']
DEFAULT_OUTPUT = 'output'

def get_args():
  """コマンドライン引数を取得する
  """
  parser = argparse.ArgumentParser(
    prog='hashcp',
    description='copy files in directory, and rename the files hash value.'
  )
  # TODO: ディレクトリパスにも対応
  parser.add_argument('src_dir', help='source directory', type=existing_path)
  # TODO: ディレクトリパスに対応
  # TODO: ファイルパスに対応
  # parser.add_argument('dst_dir', help='destination directory', type=existing_path)
  parser.add_argument('-o', '--output', help='Set output directory name and csv name (default: %(default)s)', type=str, default=DEFAULT_OUTPUT)
  parser.add_argument('-r', '--recursive', help='Recursively ', action='store_true')
  parser.add_argument('-t', '--keeptree', help='copy files with keeping tree structure', action='store_true')
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