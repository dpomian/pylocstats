import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__)))

from model.git_repo import GitRepo

class FileReader:
    def __init__(self, csv_fields : dict):
        """
        Args:
            csv_fields: Dictionary with key = field, and value = position
                Examples: {"project_name":0, "project_repo":1}
        Returns:
        """
        self._csv_fields = csv_fields

    def read_repo_list(self, filename):
        repo_list = []
        with open(filename) as ifile:
            lines = ifile.readlines()
            for line in lines[1:]:
                tokens = line.strip().split(',')
                repo_list.append(GitRepo(tokens[self._csv_fields['project_name']], tokens[self._csv_fields['project_url']]))

        return repo_list


class CSVFileReader:
    def __init__(self, csv_fields: dict):
        self._csv_fileds = csv_fields

    def read_file(self, filename, delim=','):
        data = []
        with open(filename) as ifile:
            lines = ifile.readlines()
            for line in lines[1:]:
                tokens = line.strip().split(delim)
                if tokens == ['']:
                    continue
                item = {}
                for csv_field in self._csv_fileds:
                    # print(f'tokens: {tokens}')
                    item[csv_field] = tokens[self._csv_fileds[csv_field]]
                data.append(item)
        return data
