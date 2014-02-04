import os
import json

def json_filter(json_content, names):
    filtered = []
    for name in names:
        value = json_content
        for item in name:
            value = value.get(item)
        filtered.append(value)
    return filtered

def read_json(path=None, names=None):
    with open(path) as fp:
        json_content = json.load(fp)
    if names == None:
        return json_content
    else:
        return json_filter(json_content, names)

def read_json_folder(folder_path=None, ends_with='.json', names=None):
    json_list = []
    file_names = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(ends_with):
                json_content = read_json(os.path.join(root, file), names)
                json_list.append(json_content)
                file_names.append(file)
    return json_list, file_names