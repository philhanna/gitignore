import argparse

from gitignore import FILENAME, GitignoreFile

parser = argparse.ArgumentParser(
    description=f'Creates a basic {FILENAME} file in the current directory',
    prog="gitignore")
parser.add_argument('-l', '--list',
                    help=f'Lists the current {FILENAME}',
                    action='store_true')
parser.add_argument('-r', '--replace',
                    help=f'Replaces the current {FILENAME}, if it exists',
                    action='store_true')
parser.add_argument('-q', '--quiet',
                    help=f'Suppresses the printing of the {FILENAME} file',
                    action='store_true')
parser.add_argument('-e', '--edit',
                    action='store_true',
                    help='Edit the file when done')
typelist = GitignoreFile.load_defaults(write_file=False)
parser.add_argument('type', nargs='?',
                    help=f'Type of files ({[name for name in typelist]})'
                    )
options = parser.parse_args()
try:
    gfile = GitignoreFile(options)
    gfile.run()
except ValueError as ve:
    print(f"ERROR: {ve}")
