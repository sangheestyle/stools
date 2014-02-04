import os
import json

def read_json(path):
    with open(path) as fp:
        return json.load(fp)

def read_json_folder(folder_path=None, ends_with='.json'):
    json_list = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(ends_with):
                json_content = read_json(os.path.join(root, file))
                json_list.append(json_content)
    return json_list