import glob
import re
import os
from natsort import natsorted
IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'svg']


def searchTargetFiles(root_dir: str, extensions: list[str], recursive: bool) -> list[str]:
  """指定ディレクトリの中から、指定拡張子のファイルの相対パスを再帰的に探して返す
  """
  files = glob.glob('*', recursive=recursive, root_dir=root_dir)
  print(files)
  if 'all' in extensions:
    extensions.clear()
  elif 'image' in extensions:
    extensions.remove('image')
    extensions += IMAGE_EXTENSIONS
  extensions = [e.upper() for e in extensions] + [e.lower() for e in extensions]
  files = natsorted([file for file in files if (re.match(r'.+({})$'.format('|'.join(['.' + e for e in extensions])), file) and os.path.isfile(os.path.join(root_dir, file)))])
  return files