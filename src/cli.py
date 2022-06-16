import os
import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).parent.resolve()))

from file_reader.file_reader import FileReader
from cloner.repo_cloner import GitRepoCloner
from analyzer.analyzer import Analyzer
from model.git_repo import Project, GitRepo
from exporter.csv_exporter import CSVExporter
from plots.violin import SeabornViolinPlot
import argparse
from datetime import datetime


class Utils:
    def build_project_list(projects_path, project_list_file):
        file_reader = FileReader({'project_name':0, 'project_url':1})
        # project_list = file_reader.read_repo_list('repos_dataset.csv')
        project_list = file_reader.read_repo_list(project_list_file)
        # project_list = [Project('dummy/dummy','/Users/dpomian/hardwork/research/ml_projects_clones')]
        return [Project(project.project_name, f'{projects_path}/{project.project_name}') for project in project_list]

    def export_stats(stats, stats_file):
        csv_exporter = CSVExporter(stats_file, 'Project Name,File,Function Name,Line Number,LoC')
        csv_exporter.export(stats)



class Cli:
    def __init__(self, args):
        self._args = args

    def __clone_repositories(self, repo_list, dest_path):
        git_repo_cloner = GitRepoCloner(os.path.abspath(dest_path))
        git_repo_cloner.clone_repos(repo_list)

    def _clone_repos(self, args):
        file_reader = FileReader({'project_name':0, 'project_url':1})
        repo_list = file_reader.read_repo_list(args.repos_file)
        self.__clone_repositories(repo_list, os.path.abspath(args.dest_path))

    def _clone_single_repo(self, args):
        self.__clone_repositories([GitRepo(args.name, args.repo)], os.path.abspath(args.dest_path))

    def _violin_plot(self, args):
        print(f'stats file: {args.stats_files}')
        stats_files = [os.path.abspath(stats_file) for stats_file in args.stats_files]
        png_path = None
        if args.png is not None:
            png_path = os.path.abspath(args.png)
        v_plot = SeabornViolinPlot(stats_files, args.min_loc, args.max_loc, png_path)
        v_plot.plot()

    def _build_stats_multiple(self, args):
        print('building stats...')

        stats_file = f"outfiles/stats_{datetime.now().strftime('%Y_%m_%d__%H_%M_%S')}.csv"
        if args.stats_file is not None:
            stats_file = os.path.abspath(args.stats_file)

        analyzer = Analyzer()
        stats = analyzer.analyze(Utils.build_project_list(os.path.abspath(args.clone_path), os.path.abspath(args.repos_file)))
        Utils.export_stats(stats, stats_file)

        print('done!')

    def _build_stats_single(self, args):
        print('building stats...')

        stats_file = f"outfiles/stats_{datetime.now().strftime('%Y_%m_%d__%H_%M_%S')}.csv"
        if args.stats_file is not None:
            stats_file = os.path.abspath(args.stats_file)

        project = Project(args.name, os.path.abspath(args.path))
        print(f'project: {project.project_url}')
        analyzer = Analyzer()
        stats = analyzer.analyze([project])
        Utils.export_stats(stats, stats_file)

        print('done!')


    def _parse_args(self, myargs):
        parser = argparse.ArgumentParser(description="Repos Stats", prog="pylocstats", allow_abbrev=True)

        subparsers = parser.add_subparsers(required=True, help='commands')

        clone_parser = subparsers.add_parser('clone', help='Clone multiple git repos')
        clone_parser.add_argument("--repos-file", help="repo list file", required=True)
        clone_parser.add_argument("--dest-path", help="destination path", required=True)
        clone_parser.set_defaults(func=self._clone_repos)

        clone_single_parser = subparsers.add_parser('clone-single', help='Clone a single git repo')
        clone_single_parser.add_argument('--name', help='project name', required=True)
        clone_single_parser.add_argument('--repo', help='git repository', required=True)
        clone_single_parser.add_argument('--dest-path', help='destination path', required=True)
        clone_single_parser.set_defaults(func=self._clone_single_repo)

        build_stats_parser = subparsers.add_parser('stats', help='Build Lines of Code stats')
        build_stats_parser.add_argument('--repos-file', help='repo list file', required=True)
        build_stats_parser.add_argument('--clone-path', help='repo clone path', required=True)
        build_stats_parser.add_argument('--stats-file', help='output stats file', required=False)
        build_stats_parser.set_defaults(func=self._build_stats_multiple)

        build_stats_single_parser = subparsers.add_parser('stats-single', help='Single project')
        build_stats_single_parser.add_argument('--name', help='project name', required=True)
        build_stats_single_parser.add_argument('--path', help='project path', required=True)
        build_stats_single_parser.add_argument('--stats-file', help='output stats file', required=True)
        build_stats_single_parser.set_defaults(func=self._build_stats_single)

        plot_parser = subparsers.add_parser('plot', help='Violin plots')
        plot_parser.add_argument("--stats-files", nargs='+', help="stats files", required=True)
        plot_parser.add_argument('--min-loc', help='Min lines of code. Default is 0', required=False)
        plot_parser.add_argument('--max-loc', help='Max lines of code.', required=False)
        plot_parser.add_argument('--png', help='PNG file', required=False)
        plot_parser.set_defaults(func=self._violin_plot)

        args = parser.parse_args(myargs)
        if hasattr(args, 'func'):
            args.func(args)

    def run(self):
        self._parse_args(self._args)


def main():
    cli = Cli(sys.argv[1:])
    cli.run()
    return None


if __name__ == '__main__':
    main()
