# Text File Concatenator

A Python application that combines multiple plain-text files into a single file. Useful for composing prompts for LLMs. Features both GUI and command-line interfaces.

## Features

- **Two modes**: 
  - Concatenate all allowed plain-text files in a folder (with natural sorting)
  - Select specific files and arrange them in custom order
- **Clear output**: Each file's content is labeled with its filename
- **UTF-8 support** for international characters
- **Error handling**: Skips unreadable files and continues processing

## Installation

```bash
# Install required dependency
pip install natsort
```

## Usage

### GUI Mode

Launch without arguments:
```bash
python concatenator.py
```

**Folder Mode**: Select a folder to concatenate all allowed plain-text files in natural order (e.g., file1, file2, file10).

**File Selection Mode**: Pick specific files and arrange them in custom order. You can:
- Reorder files manually using the Move Up/Down buttons
- Sort all files naturally using the Sort button
- Remove selected files or clear all

Import file list: In File Selection Mode, click "Add From List..." to import file paths from a text file. The file should contain one path per line. Supported:
- Blank lines and comment lines starting with # or ;
- Paths can be wrapped in single or double quotes;
- Relative paths (resolved relative to the list file’s location);
- Environment variables and ~ expansion;
- Only allowed plain-text types are added; duplicates are skipped; missing or not-allowed entries are reported in a summary dialog.

Example list file (example_list.txt):
```
# One path per line (comments and blanks allowed)
"test file 1.txt"
test file 2.txt
; From subfolder (relative to this file)
Test folder\test file 4.txt
```

### Allowed file types

The app includes a static allow-list of common plain-text file types. A file is included if:
- Its extension is in the allow-list, or
- It matches a special filename (case-insensitive where applicable)

Extensions:
`.txt`, `.md`, `.markdown`, `.rst`, `.html`, `.htm`, `.xml`, `.csv`, `.tsv`,
`.ini`, `.cfg`, `.conf`, `.properties`, `.env`,
`.json`, `.yaml`, `.yml`, `.toml`,
`.py`, `.js`, `.jsx`, `.ts`, `.tsx`,
`.java`, `.c`, `.cpp`, `.h`, `.hpp`, `.cs`, `.go`, `.rb`, `.php`, `.swift`, `.kt`,
`.sh`, `.bash`, `.zsh`, `.fish`, `.ps1`, `.bat`,
`.sql`, `.pl`, `.lua`, `.r`, `.scala`, `.clj`, `.groovy`, `.dart`,
`.css`, `.scss`, `.less`

Special filenames:
`LICENSE`, `MAKEFILE`, `Makefile`, `Dockerfile`, `.editorconfig`, `.gitattributes`, `.gitignore`, `.dockerignore`

Note: `.ipynb` and any other types not listed above are excluded.

### CLI Mode

```bash
# Basic usage
python concatenator.py <folder_path> [output_path]

# Example
python concatenator.py /path/to/folder output.txt
```

## Output Format

```
--- File: document1.txt ---

[Content of document1.txt]


--- File: document2.txt ---

[Content of document2.txt]
```

## Requirements

- Python 3.6+
- tkinter (included with Python)
- natsort package

## Troubleshooting

**No GUI appears**: Ensure tkinter is installed (comes with most Python installations)

**Import error**: Install natsort with `pip install natsort`

**Unicode errors**: Ensure your text files are UTF-8 encoded

## License

Public domain - free to use and modify.
