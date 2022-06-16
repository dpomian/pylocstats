import git
from multiprocessing import Pool
import os


class RepoCloner:
    def __init__(self, dest_folder):
        self._dest_folder = dest_folder

    def _clone_repo(self, repo):
        dest = f'{self._dest_folder}/{repo.project_name}'
        print(f'cloning {repo.project_url} into {dest}')
        if os.path.isdir(dest) and len(os.listdir(dest)) > 0:
            print(f'{dest} already exists and is not empty! skipping...')
            return
        try:
            git.Repo.clone_from(repo.project_url, dest)
        except git.GitCommandError as ex:
            print(f'error cloning {repo.project_url}')
            print(ex)


class GitRepoCloner(RepoCloner):
    def __init__(self, dest_folder):
        super().__init__(dest_folder)

    def clone_repos(self, repo_list):
        with Pool(10) as p:
            p.map(self._clone_repo, repo_list)
