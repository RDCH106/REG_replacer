# -*- coding: utf-8 -*-

from regreplacer.metadata import Metadata
import argparse
import os
import pathlib
import time
import json


class RegReplacer(object):
    def __init__(self):
        self.meta = Metadata()

        # Parse arguments provided
        parser = argparse.ArgumentParser()
        parser.add_argument('-v', '--version', action='version', version=self.meta.get_version())
        parser.add_argument('-t', '--template', dest='template', help='Register(.reg) template to use as template',
                            type=self.check_input1, default=".", required=True)
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

    @staticmethod
    def load_json(path):
        with open(path) as json_file:
            data = json.load(json_file)["data"]
            # print(data)
            return data

    @staticmethod
    def load_reg(path):
        with open(path, 'r', encoding='utf-16-le') as reg_file:
            data = reg_file.read()
            # print(data)
            return data

    @staticmethod
    def find_replace(register_data, replacement_data):
        for replacement in replacement_data:
            if replacement[1] == "CURRENT_DIR":
                replacement[1] = os.path.dirname(os.path.realpath(__file__))
                replacement[1] += '\\'  # Add \ at the end of the path
            register_data = register_data.replace(replacement[0].replace('\\', '\\\\'), replacement[1].replace('\\', '\\\\'))
        print(register_data)

    def run(self):
        start_time = time.time()
        print("\nExecution complete!")
        # TO-DO
        ret_reg = RegReplacer.load_reg(self.args.template)
        ret_replacement = None
        if self.args.replacement != ".":
            ret_replacement = RegReplacer.load_json(self.args.replacement)
        RegReplacer.find_replace(ret_reg, ret_replacement)
        print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    replacer = RegReplacer()
    # print(replacer.args)
    replacer.run()
