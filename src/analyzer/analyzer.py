import os
import ast
from model.project_stats import ProjectStats, FunctionStats
from analyzer.loc_visitor import LocVisitor
from multiprocessing import Pool
from model.globals import GlobalQs

class AnalyzeError:
    def __init__(self, reason):
        self.reason = reason


class Analyzer:
    def __init__(self):
        self._pool_size = 10
        self._project_stats_list = []

    def _analyze_worker(self, project):
        project.add_files(self._get_files_for_project(project))
        project_stats = ProjectStats(project.project_name)
        print(f'processing project {project_stats.project_name}')

        for file in project.files:
            loc_visitor = LocVisitor(file)
            try:
                with open(file) as f:
                    try:
                        parsed = ast.parse(f.read())
                        loc_visitor.visit(parsed)
                        project_stats.add_function_stats(loc_visitor.function_stats_list)
                    except SyntaxError as e:
                        # print(f'syntax error in file: {file}')
                        GlobalQs.instance().get_error_q().put(f'syntax error in file: {file}')
                    except UnicodeDecodeError as e:
                        # print(f'unicode decode error in file: {file}')
                        GlobalQs.instance().get_error_q().put(f'unicode decode error in file: {file}')
            except FileNotFoundError as fnferr:
                print(fnferr)
        print(f'done processing project {project_stats.project_name}')
        return project_stats

    def _get_files_for_project(self, project):
        full_path = f'{project.project_url}'
        print(f'full_path: {full_path}')
        project_files = []
        for root, dirs, files in os.walk(full_path):
            project_files += [f'{root}/{file}' for file in files if file.endswith('.py')]
        return project_files

    def _enqueue_projects(self, project_list):
        for project in project_list:
            project.add_files(self._get_files_for_project(project))
            self.analyze_q.put(project)
            # print(project.files)

    def analyze(self, project_list):
        with Pool(processes=self._pool_size, initargs=(self._project_stats_list)) as p:
            results = p.map(self._analyze_worker, project_list)
        return results