import glob
import os
import hashlib
import shutil
import csv
import re
import argparse
from natsort import natsorted
from pathlib import Path

DEFAULT_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'svg']
DEFAULT_OUTPUT = 'output'

def get_args():
  """コマンドライン引数を取得する
  """
  parser = argparse.ArgumentParser(
    prog='hashFilename',
    description='指定されたディレクトリ配下にあるファイルを複製し、ファイル名をファイルのハッシュ値に変更して保存します。'
  )
  parser.add_argument('src_dir', help='path to source root directory', type=existing_path)
  parser.add_argument('-o', '--output', help='set output directory name and csv name (default: %(default)s)', type=str, default=DEFAULT_OUTPUT)
  parser.add_argument('-r', '--recursive', help='execute recursive', action='store_true')
  parser.add_argument('-e', '--extensions', help='choose target file extensions. if you type \'all\', all files will be executed. (default: {})'.format(' '.join(DEFAULT_EXTENSIONS)), nargs='*', type=str, default=DEFAULT_EXTENSIONS)
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

def searchFile(root_dir: str, extensions: list[str], recursive: bool) -> list[str]:
  """指定ディレクトリの中から、指定拡張子のファイルの相対パスを再帰的に探して返す
  """
  tmp_files = glob.glob('**/*.*', recursive=recursive, root_dir=root_dir)
  files = natsorted([file for file in tmp_files if re.match(r'.+\.({})$'.format('|'.join(extensions)), file)])
  return files

def main():
  # コマンドライン引数
  args = get_args()
  src_dir = args.src_dir
  dst_dir = args.output
  recursive = args.recursive
  extensions = [t.upper() for t in args.extensions] + [t.lower() for t in args.extensions]
  files = searchFile(src_dir, extensions, recursive)

  # ファイルがなければ終了
  if not files:
    print('There is any files specified extensions({1}) in Directory \'{0}\'.'.format(src_dir, extensions))
    return
  
  # 保存場所
  if not os.path.isdir(dst_dir):
    os.mkdir(dst_dir)
  else:
    while True:
      choice = input("Directory \'{}\' is already exists. Delete files in the directory and execute?[y/N]: ".format(dst_dir)).lower()
      if choice in ['y', 'ye', 'yes']:
        shutil.rmtree(dst_dir)
        break
      elif choice in ['n', 'no']:
        print('cancel execute')
        return
      else:
        print('invalid input detected')
        continue
  FILE_NUM = len(files)
  print('{0} files found. Rename file in directory \'{1}\'...'.format(FILE_NUM, src_dir))

  # 実行
  with open('{}.csv'.format(DEFAULT_OUTPUT), 'w', newline='', encoding="utf-8") as c:
    writer = csv.writer(c)
    writer.writerow(['元ファイル場所', '元ファイル名', '変換後ファイル名'])
    cnt = 1
    for file in files:
      pro_bar = '{bar:{length}}'.format(bar='=' * int(cnt / FILE_NUM * 60), length=60)
      print('\r[{0}] {1:>{3}}/{2}'.format(pro_bar, cnt, FILE_NUM, len(str(FILE_NUM))), end='')
      orig_path = os.path.join(src_dir, file)
      with open(orig_path, 'rb') as f:
        _, extension = os.path.splitext(file)
        renamed_file_name = hashlib.md5(f.read()).hexdigest() + extension

        renamed_path = os.path.join(dst_dir, os.path.dirname(file), renamed_file_name)
        os.makedirs(os.path.dirname(renamed_path), exist_ok=True)
        shutil.copy(orig_path, renamed_path)

        writer.writerow([os.path.dirname(file), os.path.basename(file), renamed_file_name])
        cnt += 1
    print('')

  print('Renamed {} files.'.format(FILE_NUM))
  return

if __name__ == '__main__':
  main()