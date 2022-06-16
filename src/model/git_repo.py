class Project:
    def __init__(self, project_name, url = None):
        self.project_name = project_name
        self.project_url = url

    def add_files(self, files):
        self.files = files
        return self


class GitRepo(Project):
    def __init__(self, project_name, url):
        super().__init__(project_name, url)