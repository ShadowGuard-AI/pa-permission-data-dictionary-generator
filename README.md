# pa-permission-data-dictionary-generator
Generates a data dictionary from a JSON file of permission entries. Each entry in the output holds the resource path, its permissions, a plain description built from a fixed template over the permission keys, the permission system used, and the other resources that share at least one granted permission key. File input only: directory input is not supported and is refused with an exit code of 1. A file input that yields zero entries also exits 1 and saves nothing. An output path that resolves to the input file is refused at exit 1. - Focused on Tools for analyzing and assessing file system permissions

## Install
`git clone https://github.com/ShadowGuardAI/pa-permission-data-dictionary-generator`

## Usage
`python main.py --input-path input.json --output-file output.json --permission-system acl`

## Parameters
- `-h`: Show help message and exit
- `--input-path`, `-i`: Path to a file containing permission data. Directory input is not supported.
- `--output-file`, `-o`: Path to the output JSON file.
- `--permission-system`, `-s`: The permission system to analyze (e.g., acl, posix, s3). The system used is recorded in each dictionary entry.
- `--include-patterns`, `-I`: Glob patterns to include specific files/directories.  Uses .gitignore syntax.
- `--exclude-patterns`, `-E`: Glob patterns to exclude specific files/directories. Uses .gitignore syntax.

## License
Copyright (c) ShadowGuardAI
