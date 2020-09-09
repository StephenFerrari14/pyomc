import click
import glob
from shutil import copyfile, rmtree
from os import path, makedirs
import re
import xmltodict
from collections import OrderedDict
from typing import List
import subprocess

pyPathRegex = re.compile(r'(.*)\/.*.py')
propertyRegex = re.compile(r'.*\${(.*)}.*')


# Add aliases
@click.command()
@click.option('--directory', default='./', help='Directory to compile Python files from')
@click.option('--target', default='./py-target', help='Directory to save compiled Python files to')
@click.option('--config', default='./pom.xml', help='Location of config file to compile with')
@click.option('--compile-only', is_flag=True, help='Only compile files and don\'t run')
@click.argument('file')
def pyom(directory, target, config, compile_only, file):
    files = getPyFiles(directory, target)
    # Delete target
    removeTarget(target)
    # Copy files to target folder
    copyFiles(files, target)
    # Parse pom for properties
    properties = parseXML(config)
    # Replace properties in target python files
    injectProperties(properties, target)
    # Run py file
    if not compile_only:
        run(file)


def getPyFiles(directory, target) -> List:
    files = getFiles(directory)
    # Make a filter function for files and accept an exclusion option
    # remove pyom filter at end
    files = [f for f in files if 'venv' not in f and target not in f and 'pyom' not in f]
    return files


def getFiles(directory) -> List:
    files = glob.glob(directory + '/**/*.py', recursive=True)
    return files


def removeTarget(target) -> None:
    if path.exists(target):
        rmtree(target)


def copyFiles(files, target) -> None:
    for f in files:
        compileFile = target + f[1:]
        filePath = pyPathRegex.search(compileFile).group(1)
        if not path.exists(filePath):
            makedirs(filePath, exist_ok=True)
        copyfile(f, target + f[1:])


def parseXML(xmlfile) -> OrderedDict:
    with open(xmlfile) as fd:
        pom = xmltodict.parse(fd.read())
    return pom['project']['properties']


def injectProperties(properties, directory):
    files = getFiles(directory)
    for f in files:
        print(f)
        # Think this would be better parsing each line and swapping files but this is easier for right now
        fin = open(f, "rt")
        data = fin.read()
        # Get all properties from data
        # Doesn't work on all lines
        regexMatch = propertyRegex.search(data)
        if regexMatch:
            for group in regexMatch.groups():
                print(group)
        # data = data.replace('pyton', 'python')
        fin.close()
        fin = open(f, "wt")
        fin.write(data)
        fin.close()

        # file1 = open(f, 'r')
        # Lines = file1.readlines()

        count = 0
        newFile = ''
        # Strips the newline character
        # for line in Lines:
            # print("Line{}: {}".format(count, line.strip()))


def run(file):
    subprocess.call('python ' + file, shell=True)


if __name__ == "__main__":
    pyom()
