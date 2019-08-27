# -*- coding: utf-8 -*-

from regreplacer.metadata import Metadata
import argparse
import os
import pathlib
import time


class RegReplacer(object):
    def __init__(self):
        self.meta = Metadata()

        # Parse arguments provided
        parser = argparse.ArgumentParser()
        parser.add_argument('-v', '--version', action='version', version=self.meta.get_version())
        parser.add_argument('-t', '--template', dest='template', help='Register(.reg) template to use as template',
                            type=self.check_input1, default=".", required=False)
        parser.add_argument('-r', '--replacement', dest='replacement', help='Json file with replacements',
                            type=self.check_input2, default=".")
        parser.add_argument('-o', '--output', dest='output', help='Output path',
                            type=self.check_output, default="./OUTPUT.reg")

        self.args = parser.parse_args()

    @staticmethod
    def exists_file_or_path(path, extension):
        if path.endswith(extension):
            RegReplacer.exists_file(path)
        else:
            RegReplacer.exists_path(path)
        return path

    @staticmethod
    def exists_path(path):
        if not os.path.isdir(path):
            raise argparse.ArgumentTypeError("%s is not valid path" % path)
        return path

    @staticmethod
    def exists_file(path):
        if not os.path.isfile(path):
            raise argparse.ArgumentTypeError("%s is not valid file" % path)
        return path

    @staticmethod
    def check_input1(path):
        extension = ".reg"
        return RegReplacer.exists_file_or_path(path, extension)

    @staticmethod
    def check_input2(path):
        extension = ".json"
        return RegReplacer.exists_file_or_path(path, extension)

    @staticmethod
    def check_output(path):
        extension = ".reg"
        if os.path.isdir(os.path.dirname(path)) and path.endswith(extension):
            pathlib.Path(path).touch()  # Create empty file if path exists but not the file
        return RegReplacer.exists_file_or_path(path, extension)

    def run(self):
        start_time = time.time()
        print("\nExecution complete!")
        # TO-DO
        print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    replacer = RegReplacer()
    print(replacer.args)
    replacer.run()
