import os
import unittest
from stools import io

class TestIO(unittest.TestCase):

    def setUp(self):
        self.json_folder_path = "data"
        self.ends_with = ".json"

    def test_json(self):
        json_names = [['category'],['extendedInfo','description']]
        json_list = io.read_json_folder(self.json_folder_path, self.ends_with, json_names)
        num_json_files = 0
        for root, folder, names in os.walk(self.json_folder_path):
            for name in names:
                if name.endswith('.json'):
                    num_json_files += 1
        print json_list
        self.assertEqual(type(json_list), type(list()))
        self.assertEqual(len(json_list), num_json_files)

if __name__=='__main__':
    unittest.main()