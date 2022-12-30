import json


class FileOpener():


    def open_file(file_name):
        with open(file_name, 'r') as read_file:
            f = read_file.read()

        return f

    def open_json_file(file_name):
        f = open(file_name)
        data = json.load(f)

        return data