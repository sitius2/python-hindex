#!/usr/bin/env python3

import os
import re
import argparse

VERSION = "1.6"

parser = argparse.ArgumentParser(description="Generate index.html from the files in the given directory,"
                                             " if no directory is specified,"" use the current one", )
parser.add_argument("-e", "--exclude", nargs=1, help="A file that contains names of files and directories "
                                                     "that shall be excluded in the index.html", default=None)
parser.add_argument("-t", "--title", nargs=1, help="Sets the title tag of the index.html", default="Server")
parser.add_argument("-h1", "--headline-files", nargs=1, help="Headline for the downloadable files section",
                    metavar="HEADLINE", default="Downloadable files")
parser.add_argument("-h2", "--headline-directories", nargs=1, help="Headline for the browseable"
                    "directories section", metavar="HEADLINE", default="Browseable directories")
parser.add_argument("-c", "--charset", nargs=1, help="Specify the charset that should be used in the meta tag",
                    default="utf-8")
parser.add_argument("-l", "--list-type", nargs=1, help="Specify the list type that should be use (default: 'ul'",
                    default="ul")
parser.add_argument("path", help="Path of which the index.html shall be created", default=os.getcwd())
parser.add_argument("-i", "--interactive", help="Enter interactive console mode", action="store_true")
parser.add_argument("-v", "--version", help="Print program version", action="version", version=VERSION)

args = parser.parse_args()


#   if len(sys.argv) > 1:
#    for arg in range(len(sys.argv)):
#        if sys.argv[arg][:1] != "-" and arg != len(sys.argv):
#            continue
#        elif arg == "-e":
#            exclude_file = sys.argv[arg+1]
#            if arg + 1 == len(sys.argv):
#                break
#        elif arg == "-t":
#            page_title = sys.argv[arg+1]
#            if arg + 1 == len(sys.argv):
#                break
#        elif arg == "-h1":
#            file_headline = sys.argv[arg+1]
#            if arg + 1 == len(sys.argv):
#                break
#        elif arg == "-h2":
#            dirs_headline = sys.argv[arg+1]
#           if arg + 1 == len(sys.argv):
#                break
#        elif arg == "-c":
#            html_charset = sys.argv[arg+1]
#            if arg + 1 == len(sys.argv):
#                break
#        elif arg == "-l":
#            html_list_type = sys.argv[arg+1]
#            if arg + 1 == len(sys.argv):
#                break
#        else:
#            if os.path.exists(sys.argv[arg]) and sys.argv[arg] != "":
#                work_path = sys.argv[arg]
#           else:
#                print("ERROR: Path does not exist...")
#                print(HELP_MSG)
#                sys.exit(1)
# else:
#    work_path = os.getcwd()


class HtmlFileCreator:
    def __init__(self, path=args.path, title=args.title, charset=args.charset, headline_files=args.headline_files,
                 headline_directories=args.headline_directories, list_type=args.list_type):
        self._path = "".join(path)
        self._title = "".join(title)
        self._charset = "".join(charset)
        self._headline_files = "".join(headline_files)
        self._headline_directories = "".join(headline_directories)
        self._list_type = "".join(list_type)

    _content = []
    _files = []
    _files_list = []
    _files_html = ""
    _dirs = []
    _dirs_list = []
    _dirs_html = ""
    _extension_pattern = r"\.[^.]+"

    _html_preset = ""

    def get_content(self):
        self._content = os.listdir(self._path)
        counter = len(exclude_files)
        iteration = 0
        while iteration <= counter:
            for x in self._content:
                for y in exclude_files:
                    if x == y:
                        self._content.remove(x)
            iteration += 1

    def sort_content(self):
        for item in self._content:
            if os.path.isdir(item):
                self._dirs.append(item)
            elif os.path.isfile(item):
                self._files.append(item)
            else:
                continue

    def create_html_page(self):
        self._html_preset = """<!DOCTYPE html />
<html>
<head>
    <title> """ + self._title + """</title>
    <meta charset=\"""" + self._charset + """\" />
</head>
<body>
    <h1>""" + self._headline_files + """</h1>
    <""" + self._list_type + """>
    """ + self._files_html.join(str(x) for x in self._files_list) + """
    </""" + self._list_type + """>
    <h1>""" + self._headline_directories + """</h1>
    <""" + self._list_type + """>
    """ + self._dirs_html.join(str(x) for x in self._dirs_list) + """
    </""" + self._list_type + """>
</body>
</html>"""

    def create_index_list(self):
        for item in self._dirs:
            self._dirs_list.append('<li><a href="{}">{}</a></li>\n'.format(item, item))
        for item in self._files:
            desc = re.search(self._extension_pattern, item)
            if desc is not None:
                self._files_list.append('<li><a href="{}" download>{}</a></li>\n'
                                        .format(item, item.replace(desc.group(), "")))
            else:
                self._files_list.append('<li><a href="{}" download>{}</a></li>\n'.format(item, item))

    def create_index_html(self):
        if os.path.exists("index.html"):
            try:
                with open("index.html", "w") as indexf:
                    indexf.seek(0)
                    indexf.truncate()
                    indexf.write(self._html_preset)
            except PermissionError:
                print("Can't create index.html, maybe try running as root?")
                import sys
                sys.exit(1)
        else:
            try:
                with open("index.html", "x") as indexf:
                    indexf.write(self._html_preset)
            except PermissionError:
                print("Can't create index.html, maybe try running as root?")
                import sys
                sys.exit(1)

exclude_files = []
if args.exclude is not None:
    exclude_list = "".join(str(x) for x in args.exclude)
    if os.path.exists(exclude_list):
        try:
            f = open(exclude_list, "r")
        except PermissionError:
            print("Can't open exclude file, maybe try running as root?")
            import sys
            sys.exit(1)
        lines = f.readlines()
        for line in lines:
            exclude_files.append(line.rstrip())
        f.close()
    else:
        print("Exclude file does not exist")


PageGen = HtmlFileCreator()
print("Getting files of directory...")
PageGen.get_content()
print("Sorting files and directories...")
PageGen.sort_content()
print("Creating index list...")
PageGen.create_index_list()
print("Creating page content...")
PageGen.create_html_page()
print("Creating index.html...")
PageGen.create_index_html()
print("Done!")
