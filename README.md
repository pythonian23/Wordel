# Wordel
## About
A Wordle clone that started out as an attempt to make nice, modular code, but ended up as a bunch of spaghetti code that somehow works.
## Run
```
python main.py [FLAGS]
```
## Files
### `main.py`
- Creates and runs the Wordel object according to the provided flags.
### `wordel.py`
- Holds the Wordel class and a function to easily get words from a source & cache the results.
- This should be what's being imported if anyone wants to use or extend this for some reason.
### `utils.py`
- Holds functions that are not directly related to the function of the project,
but are used internally.
## Usage
|              Flag | Shorthand   | Description                       |
|------------------:|:------------|:----------------------------------|
|          `--help` | `-h`        | Show this help message and exit   |
|          `--hard` | `-H`        | Enable hard mode                  |
|         `--debug` | `-d`        | Debug                             |
| `--answer STRING` | `-A STRING` | Set the answer to a specific word |
|     `--chars INT` | `-c INT`    | The number of characters per row  |
|  `--attempts INT` | `-a INT`    | The number of attempts to allow   |

