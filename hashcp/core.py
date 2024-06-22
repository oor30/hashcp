import os
import hashlib
import shutil
import csv

from hashcp.arguments import get_args
from hashcp.search import searchTargetFiles
from hashcp.confirm import confirm
from hashcp.progress_bar import ProgBar

IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'svg']
DEFAULT_OUTPUT = 'output'

def cli():
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
  if not confirm('{0} files found. Run these files?[y/N]'.format(len(files))):
    return
  
  # 保存場所
  # 存在する場合、上書きされることを確認
  if os.path.isdir(DST_DIR):
    if not confirm("Directory \'{}\' is already exists. Will you delete files in the directory and run?[y/N]: ".format(DST_DIR)):
      return
    else:
      shutil.rmtree(DST_DIR)
  # 存在しない場合、ディレクトリを作成
  else:
    os.mkdir(DST_DIR)
  print('Copying and renaming files with extensions({0}) in directory \'{1}\'...'.format(','.join(extensions), SRC_DIR))
  hashcp(files, SRC_DIR, DST_DIR, KEEP_TREE)
  print('Finished running. Copied and renamed {} files.'.format(len(files)))
  
def hashcp(files: list[str], src_dir: str, dst_dir: str, keep_tree: bool):
  # 実行
  with open('{}.csv'.format(DEFAULT_OUTPUT), 'w', newline='', encoding="utf-8") as c:
    writer = csv.writer(c)
    writer.writerow(['元ファイル場所', '元ファイル名', '変換後ファイル名'])
    prog_bar = ProgBar(len(files))
    for file in files:
      prog_bar.increment()
      # 元ファイルのパス
      orig_path = os.path.join(src_dir, file)
      with open(orig_path, 'rb') as f:
        _, extension = os.path.splitext(file)
        # ハッシュ化したファイル名
        renamed_file_name = hashlib.md5(f.read()).hexdigest() + extension

        # ハッシュ化したファイルのパス
        if keep_tree:
          renamed_path = os.path.join(dst_dir, os.path.dirname(file), renamed_file_name)
        else:
          renamed_path = os.path.join(dst_dir, renamed_file_name)
        os.makedirs(os.path.dirname(renamed_path), exist_ok=True)
        shutil.copy(orig_path, renamed_path)

        writer.writerow([os.path.dirname(file), os.path.basename(file), renamed_file_name])
    print('')
  return