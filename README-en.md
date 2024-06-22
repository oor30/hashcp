# hashcp

[日本語版 README](https://github.com/oor30/hashcp/blob/master/README.md)

## Summary

This program duplicates files and changes file names to hash values ​​in bulk.
It also outputs a table (CSV file) showing the correspondence between file names before and after conversion.

This is useful when you want to change the file names of large amounts of image data, etc. to unique file names.

## Getting start

### Requirement

- Python
- pip

### Install using pip

```zsh
pip install git+https://github.com/oor30/hashcp.git
```

## Usage

```zsh
hashcp [options] <directory>
```

### Optins

```zsh
-o --output <directory>
```

Specify the destination directory name and CSV file name (default: output).

```zsh
-r --recursive
```

It also recursively searches for files in subdirectories.

```zsh
-e --extensions <extensions...>
```

Specify the file extensions of the files to be included, separated by spaces.

```zsh
-t --keeptree
```

The directory structure will be preserved when you duplicate it.
