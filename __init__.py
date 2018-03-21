#!/usr/bin/env python2
import argparse
import os.path
import os
import inspect
import shutil
import sys
import datetime

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

parser = argparse.ArgumentParser(description="Make a single page " +
                                 "documentation of a single Python file")
parser.add_argument('pyfile', type=str, help='The filename of the python file')
parser.add_argument('--example',
                    help='add example usage jupyter notebook')

args = parser.parse_args()
# make directory with same base name as python file
basename = os.path.splitext(os.path.basename(args.pyfile))[0]
from pathlib import Path
print Path(inspect.getfile(inspect.currentframe()))
qdpath = os.path.dirname(os.path.abspath(os.path.realpath(inspect.getfile(inspect.currentframe()))))
print qdpath
try:
    os.mkdir(basename)
    #os.mkdir(os.path.join(basename, '_static'))
    shutil.copytree(os.path.join(qdpath, '_static'), os.path.join(basename, '_static'))
    #os.mkdir(os.path.join(basename, '_templates'))
    shutil.copytree(os.path.join(qdpath, '_templates'), os.path.join(basename, '_templates'))
except OSError:
    if query_yes_no('Directory "{0}/" exists, replace?'.format(basename),
                    default="no"):
        shutil.rmtree(basename + '/')
        os.mkdir(basename)
        #os.mkdir(os.path.join(basename, '_static'))
        shutil.copytree(os.path.join(qdpath, '_static'), os.path.join(basename, '_static'))
        #os.mkdir(os.path.join(basename, '_templates'))
        shutil.copytree(os.path.join(qdpath, '_templates'), os.path.join(basename, '_templates'))
    else:
        sys.exit(1)

now = datetime.datetime.now()
year = now.strftime("%Y")
dt = now.ctime()
date = now.strftime("%m/%d/%y")
# copy all sphinx quickstart files there
path = '{basename}/'.format(basename=basename)
with open(os.path.join(qdpath,'<tmplt>.rst'), 'r') as rst:
    rst_str = rst.read().format(basename=basename, datetime=dt, date=date)
with open(os.path.join(path, '{0}.rst'.format(basename)), 'w') as rst:
    rst.write(rst_str)
with open(os.path.join(qdpath,'conf.py.txt'), 'r') as conf:
    conf_str = conf.read().format(basename=basename, year=year, date=date,
                                  datetime=dt, ver='')
with open(os.path.join(path, 'conf.py'), 'w') as conf:
    conf.write(conf_str)
# run and convert the example, if given
if args.example is not None:
    print "do the example"
# do the spinx-build command
os.system('sphinx-build -b singlehtml {basename}/ ./ {basename}.py'.format(basename=basename))
# remove the directory
shutil.rmtree(basename + '/')
