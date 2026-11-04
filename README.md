# pa-permission-data-dictionary-generator

Generates a data dictionary from a JSON file of permission entries. Each entry in the output holds the resource path, its permissions, a plain description built from a fixed template over the permission keys, the permission system used, and the other resources that share at least one granted permission key. File input only: directory input is not supported and is refused with an exit code of 1. A file input that yields zero entries also exits 1 and saves nothing. An output path that resolves to the input file is refused at exit 1. Focused on tools for analyzing and assessing file system permissions.

## Install

```
git clone https://github.com/ShadowGuard-AI/pa-permission-data-dictionary-generator.git
cd pa-permission-data-dictionary-generator
pip install -r requirements.txt
```

## Usage

```
python3 main.py --input-path input.json --permission-system acl [options]
```

## Parameters

- `--input-path, -i`: Required. Path to a file containing permission data. Directory input is not supported.
- `--output-file, -o`: Path to the output JSON file, default `permission_data_dictionary.json`.
- `--permission-system, -s`: Required. The permission system to analyze, one of `acl`, `posix`, `s3`. The system used is recorded in each dictionary entry.
- `--include-patterns, -I`: Zero or more glob patterns to include specific files/directories. Uses .gitignore syntax.
- `--exclude-patterns, -E`: Zero or more glob patterns to exclude specific files/directories. Uses .gitignore syntax.

## Verified in this wave

`python3 main.py --help` could not run in this sandbox: it exits 1 at import with `ModuleNotFoundError: No module named 'pathspec'`, because `pathspec` is not installed and installs are not made in this wave. Parameters above are taken from the argument parser in `main.py`, and `main.py` passes `py_compile`. No live generation run is claimed.

## License

See LICENSE.
