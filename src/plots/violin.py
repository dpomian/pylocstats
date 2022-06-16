import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).parent.parent.resolve()))

import matplotlib.pyplot as plt
from file_reader.file_reader import CSVFileReader
import numpy as np
import seaborn as sns
import pandas as pds


class SeabornViolinPlot:
    def __init__(self, stats_files, min_loc, max_loc, png_path):
        self._stats_files = stats_files
        self._min_loc = min_loc
        self._max_loc = max_loc
        self._plot = self._plot_violin
        self._png_path = png_path

    def _build_arr(self, data, proj_name):
        arr = np.array([[np.log(loc), proj_name] for loc in data if loc > 0])
        return arr

    def _build_dataframe_arrays(self, locs_list, prj_names):
        arr = self._build_arr(locs_list[0], prj_names[0])
        for i in range(len(locs_list[1:])):
            arr = np.concatenate((arr, self._build_arr(locs_list[i+1], prj_names[i+1])))

        df = pds.DataFrame(arr, columns=['loc', 'project'])
        df = df.explode('loc')
        df['loc'] = df['loc'].astype('float')

        return df

    def _compute_ticks(self, prj_names, df):
        groupby_project = df.groupby('project')
        mins = []
        medians = []
        q25s = []
        q75s = []
        maxs = []
        for project_name in prj_names:
            mins.append(groupby_project.loc.min()[project_name])
            medians.append(groupby_project.loc.median()[project_name])
            # q25s.append(groupby_project.loc.quantile(0.25)[project_name])
            # q75s.append(groupby_project.loc.quantile(0.75)[project_name])
            maxs.append(groupby_project.loc.max()[project_name])

        ticks = mins + q25s + medians + q75s + maxs
        ticks.sort()
        tick_labels = [int(np.exp(x)) for x in ticks]

        return ticks, tick_labels

    def _plot_violin(self):
        sns.set_theme(style="ticks")

        # Initialize the figure with a logarithmic x axis
        f, ax = plt.subplots(figsize=(7, 6))

        # filenames = ['/Users/dpomian/hardwork/pywork/rstats/outfiles/django_stats_newloccount.csv',
        #              '/Users/dpomian/hardwork/pywork/rstats/outfiles/tensorflow_stats.csv',
        #              '/Users/dpomian/hardwork/pywork/rstats/outfiles/DTLK_DTLK_stats.csv']
        filenames = self._stats_files

        raw_data = [self.__get_data_to_plot(filename, self._min_loc, self._max_loc) for filename in filenames]
        locs_list = [data['locs'] for data in raw_data]
        prj_names = [data['project_name'] for data in raw_data]

        df = self._build_dataframe_arrays(locs_list, prj_names)

        # violin = sns.violinplot(x='loc', y='project', data=df, whis=[0, 100], width=.5, palette="vlag", inner='quartiles')
        # violin = sns.violinplot(x='loc', y='project', data=df, whis=[0, 100], width=.5, palette="vlag", inner='box')
        violin = sns.violinplot(x='loc', y='project', data=df, palette="vlag")
        # violin.set(title='Lines of code per function comparison')
        ticks, tick_labels = self._compute_ticks(prj_names, df)
        violin.set_xticks(ticks)
        violin.set_xticklabels(tick_labels)

        ax.xaxis.grid(True)
        ax.yaxis.grid(True)
        ax.set(ylabel="Projects")
        ax.set(xlabel="Lines of code per function")
        ax.set_title('Lines of code comparison\n', fontdict={'fontsize': 20, 'fontweight':'bold'})
        # sns.despine(trim=True, left=True)
        if self._png_path is None:
            plt.show()
        else:
            print(f'exporting file: {self._png_path}')
            plt.savefig(self._png_path, bbox_inches='tight')

    def plot(self):
        self._plot()


    def __get_data_to_plot(self, stats_file, min_loc, max_loc):
        fr = CSVFileReader({'project_name': 0, 'filename': 1, 'function_name': 2, 'line_no': 3, 'loc': 4})
        data = fr.read_file(stats_file)

        locs = []
        for e in data:
            try:
                loc = int(e['loc'])
                if (min_loc is None or loc >= int(min_loc)) and (max_loc is None or loc <= int(max_loc)):
                    locs.append(int(e['loc']))
            except ValueError as ve:
                print(f'Error: e: {e}')
        # locs = sorted(locs)[10000:]
        # data_to_plot = [locs]
        # data_to_plot = locs

        return {'project_name': data[0]['project_name'], 'locs':locs}

