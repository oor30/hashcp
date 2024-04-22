import glob
import os
import hashlib
import shutil
import csv
import re
import argparse
from natsort import natsorted
from pathlib import Path

IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'svg']
DEFAULT_OUTPUT = 'output'

def get_args():
  """コマンドライン引数を取得する
  """
  parser = argparse.ArgumentParser(
    prog='hashFilename',
    description='copy files in directory, and rename the files hash value.'
  )
  parser.add_argument('src_dir', help='source directory', type=existing_path)
  # parser.add_argument('dst_dir', help='destination directory', type=existing_path)
  parser.add_argument('-o', '--output', help='Set output directory name and csv name (default: %(default)s)', type=str, default=DEFAULT_OUTPUT)
  parser.add_argument('-r', '--recursive', help='Recursively ', action='store_true')
  parser.add_argument('-t', '--keeptree', help='copy files with keeping tree structure', action='store_true')
  parser.add_argument('-e',
                      '--extensions',
                      help='Type target file extensions separated by space. if you type \'all\', all files will be target. if you type \'image\', image files will be target({}).'.format(' '.join(IMAGE_EXTENSIONS)),
                      nargs='*',
                      type=str,
                      default='image')
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

def searchTargetFiles(root_dir: str, extensions: list[str], recursive: bool) -> list[str]:
  """指定ディレクトリの中から、指定拡張子のファイルの相対パスを再帰的に探して返す
  """
  files = glob.glob('**/*', recursive=recursive, root_dir=root_dir)
  if 'all' in extensions:
    extensions.clear()
  elif 'image' in extensions:
    extensions.remove('image')
    extensions += IMAGE_EXTENSIONS
  extensions = [e.upper() for e in extensions] + [e.lower() for e in extensions]
  files = natsorted([file for file in files if (re.match(r'.+({})$'.format('|'.join(['.' + e for e in extensions])), file) and os.path.isfile(os.path.join(root_dir, file)))])
  return files

def main():
  # コマンドライン引数
  args = get_args()
  SRC_DIR = args.src_dir
  DST_DIR = args.output
  IS_RECURSIVE = args.recursive
  KEEP_TREE = args.keeptree
  extensions = args.extensions
  files = searchTargetFiles(SRC_DIR, extensions, IS_RECURSIVE)

  # ファイルがなければ終了
  if not files:
    print('There is any files specified extensions({1}) in Directory \'{0}\'.'.format(SRC_DIR, ','.join(extensions)))
    return
  
  # 対象ファイル数確認
  FILE_NUM = len(files)
  while True:
    choice = input('{0} files found. Run these files?[y/N]'.format(FILE_NUM)).lower()
    if choice in ['y', 'ye', 'yes']:
      break
    elif choice in ['n', 'no']:
      print('canceled')
      return
    else:
      print('invalid input detected')
      continue
  
  # 保存場所
  if not os.path.isdir(DST_DIR):
    os.mkdir(DST_DIR)
  else:
    while True:
      choice = input("Directory \'{}\' is already exists. Will you delete these files in the directory and run?[y/N]: ".format(DST_DIR)).lower()
      if choice in ['y', 'ye', 'yes']:
        shutil.rmtree(DST_DIR)
        break
      elif choice in ['n', 'no']:
        print('canceled')
        return
      else:
        print('invalid input detected')
        continue

  # 実行
  print('Copying and renaming files with extensions({0}) in directory \'{1}\'...'.format(','.join(extensions), SRC_DIR))
  with open('{}.csv'.format(DEFAULT_OUTPUT), 'w', newline='', encoding="utf-8") as c:
    writer = csv.writer(c)
    writer.writerow(['元ファイル場所', '元ファイル名', '変換後ファイル名'])
    cnt = 1
    PROG_BAE_WIDTH = shutil.get_terminal_size().columns - 4 - len(str(FILE_NUM))*2
    for file in files:
      prog_bar = '{bar:{length}}'.format(bar='=' * int(cnt / FILE_NUM * PROG_BAE_WIDTH), length=PROG_BAE_WIDTH)
      print('\r[{0}] {1:>{3}}/{2}'.format(prog_bar, cnt, FILE_NUM, len(str(FILE_NUM))), end='')
      orig_path = os.path.join(SRC_DIR, file)
      with open(orig_path, 'rb') as f:
        _, extension = os.path.splitext(file)
        renamed_file_name = hashlib.md5(f.read()).hexdigest() + extension

        renamed_path = os.path.join(DST_DIR, os.path.dirname(file), renamed_file_name) if KEEP_TREE else os.path.join(DST_DIR, renamed_file_name)
        os.makedirs(os.path.dirname(renamed_path), exist_ok=True)
        shutil.copy(orig_path, renamed_path)

        writer.writerow([os.path.dirname(file), os.path.basename(file), renamed_file_name])
        cnt += 1
    print('')

  print('Finished running. Copied and renamed {} files.'.format(FILE_NUM))
  return

if __name__ == '__main__':
  main()