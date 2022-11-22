import json
import os

from gitignore import DEFAULT_KEY, DEFAULT_VALUES, FILENAME, EDITOR


class GitignoreFile:
    """Represents a .gitignore file"""

    def __init__(self, options):
        """Constructor"""
        self.list = options.list
        self.replace = options.replace
        self.edit = options.edit
        self.quiet = options.quiet

        # Load .gitignorerc if it exists, else create it
        self.typelist = self.load_defaults()

        if not options.type:
            self.type = DEFAULT_KEY
            if DEFAULT_KEY not in self.typelist:
                self.typelist[DEFAULT_KEY] = DEFAULT_VALUES
        else:
            if options.type not in self.typelist:
                types = [f"'{_}'" for _ in self.typelist]
                typelist = ", ".join(types)
                p = typelist.rfind(",")
                if p > -1:
                    typelist = typelist[0:p] + ", or " + typelist[p + 2:]
                raise ValueError(f"If specified, type must be one of {typelist}")
            self.type = options.type

    def create(self):
        """Creates the .gitignore file"""
        if not self.quiet:
            print(f"Creating new {FILENAME}")

        with open(FILENAME, "wt") as f:
            for line in self.typelist[self.type]:
                f.write(line + "\n")

    def run(self):

        #   List the file if requested
        if self.list:
            if os.path.exists(FILENAME):
                self.list_file()
                exit(0)
            else:
                raise RuntimeError(f"No {FILENAME} file exists")

        #   Create the file if it does not exist,
        #   or if exists and the replace option was specified
        if os.path.exists(FILENAME):
            if self.replace:
                self.create()
            else:
                if not self.quiet:
                    print(f"Not replacing existing {FILENAME}")
                    print("Use -r flag to replace")
                    print("Try -h for help")
        else:
            self.create()

        #   List the contents of the file
        if not self.quiet and not self.edit:
            self.list_file()

        #   Bring it up in an editor if the edit option was specified
        if self.edit:
            self.edit_file()

    @staticmethod
    def load_defaults(write_file=True):
        """Gets the default ignored files by file type"""
        filename = os.path.expanduser("~/.gitignorerc")
        if os.path.exists(filename):
            with open(filename, "rt") as fp:
                defaults = json.load(fp)
        else:
            defaults = {
                "py": ["*.swp",
                       "*.pyc",
                       "*.pyo",
                       "__pycache__",
                       ".idea/",
                       "venv/",
                       "build/",
                       "dist/",
                       "*.egg-info/",
            ],
                "ly": ["*.swp", "*.mid", "*.midi", "*.ogg"],
                "java": ["*.swp", "build/", "doc/", "*.class", ".classpath", ".project"],
            }
            if write_file:
                with open(filename, "wt") as fp:
                    json.dump(defaults, fp, indent=2, sort_keys=True)
        return defaults

    @staticmethod
    def list_file():
        """Lists the file"""
        with open(FILENAME) as f:
            for line in f:
                line = line.strip()
                print(line)

    @staticmethod
    def edit_file():
        """Invokes an editor on the file"""
        os.system('{} {}'.format(EDITOR, FILENAME))

