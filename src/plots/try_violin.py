class TryViolin:
    def __init__(self):
        self.plot = self._malinda

    def _malinda(self):
        plt.figure(figsize=(5, 4))
        data3 = get_data_to_plot(self._stats_file, self._min_loc, self._max_loc)
        violin_parts2 = plt.violinplot(data3, vert=False, showmeans=False, showmedians=False,
                                       showextrema=False)
        for pc2 in violin_parts2['bodies']:
            pc2.set_facecolor('silver')
            pc2.set_edgecolor('black')
            pc2.set_linewidth(1)
            pc2.set_alpha(0.5)
        # plt.title("Class LOC distribution in ML and Non ML Projects")
        # plt.xlabel('Number of Code Lines')
        green_diamond = dict(marker='x')
        bp3 = plt.boxplot(data3, vert=False, widths=0.2, showfliers=False, whis=1.5, flierprops=green_diamond)
        for element in ['boxes', 'whiskers', 'fliers', 'means', 'medians', 'caps']:
            plt.setp(bp3[element], color='black')
        # plt.yticks(range(1, len(labels) + 1), labels)

        plt.tick_params(axis="x", direction="in", pad=1)
        plt.xticks(np.linspace(min(data3), max(data3), 3).astype(int))
        plt.yticks([])
        for line in bp3['medians']:
            # get position data for median line
            x, y = line.get_xydata()[1]  # top of median line
            # overlay median value
            plt.text(x, y, '%d' % x,
                     horizontalalignment='center')  # draw above, centered
        # for line in bp3['boxes']:
        #     x, y = line.get_xydata()[0]  # bottom of left line
        #     plt.text(x, y, '%.1f' % x,
        #          horizontalalignment='center',  # centered
        #          verticalalignment='top')  # below
        #     x, y = line.get_xydata()[3]  # bottom of right line
        #     plt.text(x, y, '%.1f' % x,
        #          horizontalalignment='center',  # centered
        #          verticalalignment='top')  # below
        for line in bp3['medians']:
            # get position data for median line
            x, y = line.get_xydata()[1]  # top of median line
            # overlay median value
        plt.text(x, 0.4, '%d' % x, horizontalalignment='center', fontsize=10)
        # plt.text(43, 0.4, '%d' % 43,horizontalalignment='center',fontsize=10)
        #    plt.vlines(2, 0.75, 1, colors='gray')
        #    plt.text( 2.5,0.6, '%d' % 2, horizontalalignment='center', fontsize=12)
        # #   plt.vlines(1, 0, 1, colors='silver')
        #    plt.text( 1.3,0.6, '%d' % 1, horizontalalignment='center', fontsize=12)
        #    # plt.vlines(1,0.5,1.5 ,linestyles='dotted',colors='silver' )
        #    plt.vlines(14, 0.75, 1, colors='gray')
        #    plt.text( 14, 0.6,'%d' % 22, horizontalalignment='center', fontsize=12)
        #    plt.box(True)
        # plt.savefig(fileName, bbox_inches='tight')
        plt.show()

    def plot(self):
        self._plot()

    def _plot1(self):
        d = {'loc': get_data_to_plot(self._stats_file, self._min_loc, self._max_loc), 'project':'django'}
        df = pds.DataFrame(data=d)
        print(f'df: {df}')

    def _plot2(self):
        # libraries & dataset
        data = get_data_to_plot(self._stats_file, self._min_loc, self._max_loc)
        log_data = [np.log(n) for n in data if n > 0]
        data = log_data
        d = {'loc': data, 'project':'django'}
        df = pds.DataFrame(data=d)
        # print(f'type(df): {type(df)}')
        # print(f'df: {df}')

        ax = sns.violinplot(x="project", y="loc", data=df)

        # Calculate number of obs per group & median to position labels
        print(f'df["loc"]: {df["loc"]}')
        medians = df.groupby(['project'])['loc'].median().values
        print(f'medians: {medians}')
        print(f'val counts: {df["loc"].value_counts().keys}')
        nobs = df['loc'].value_counts().values
        nobs = [str(x) for x in nobs.tolist()]
        nobs = ["n: " + i for i in nobs]

        # Add it to the plot
        pos = range(len(nobs))
        for tick, label in zip(pos, ax.get_xticklabels()):
            print(f'tick: {tick}')
            ax.text(pos[tick],
                    medians[tick] + 0.03,
                    nobs[tick],
                    horizontalalignment='center',
                    size='x-small',
                    color='w',
                    weight='semibold')

        plt.show()

class ViolinPlot:
    def __init__(self, stats_file, min_loc, max_loc):
        self._stats_file = stats_file
        self._min_loc = min_loc
        self._max_loc = max_loc
        self._plot = self._plotHorBoxForPaper

    def plot(self):
        # self._plot()
        seaborn_violin = SeabornViolin(self._stats_file, self._min_loc, self._max_loc)
        seaborn_violin.plot()

    def _plot1(self):
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(9, 4), sharey=True)
        ax.set_title('Default violin plot')
        ax.set_ylabel('Observed values')
        data = self._get_data_to_plot()
        parts = ax.violinplot(data, showmeans=False, showmedians=True, showextrema=False)
        self._set_plot_color(parts, '#ff6100')
        self._set_quartiles(ax, data)
        plt.subplots_adjust(bottom=0.15, wspace=0.05)
        plt.show()

    def _plotHorBoxForPaper(self):
        data3 = self._get_data_to_plot()
        data3 = [np.log(d) for d in data3 if d>0]
        plt.figure(figsize=(5, 4))
        violin_parts2 = plt.violinplot(data3, vert=False, showmeans=False, showmedians=True, showextrema=True)
        for pc2 in violin_parts2['bodies']:
            pc2.set_facecolor('silver')
            pc2.set_edgecolor('black')
            pc2.set_linewidth(1)
            pc2.set_alpha(0.5)
        plt.title("Function LOC distribution")
        plt.xlabel('Number of Code Lines')
        green_diamond = dict(marker='x')
        # bp3 = plt.boxplot(data3, vert=False, widths=0.2, showfliers=False, whis=1.5, flierprops=green_diamond)
        # for element in ['boxes', 'whiskers', 'fliers', 'means', 'medians', 'caps']:
        #     plt.setp(bp3[element], color='blue')
        # plt.yticks(range(1, len(labels) + 1), labels)

        # self._show_value_for('medians', bp3)
        # self._show_value_for('boxes', bp3)
        # self._show_value_for('whiskers', bp3)
        # plt.tick_params(axis="x", direction="in", pad=1)
        # plt.xticks(np.linspace(min(data3), max(data3), 20).astype(int))
        plt.show()

    def _show_value_for(self, component, boxplot):
        if component not in boxplot:
            return
        for line in boxplot[component]:
            # get position data for median line
            x, y = line.get_xydata()[1]  # top of median line
            # overlay median value
            plt.text(x, y, '%d' % x, horizontalalignment='center')  # draw above, centered

    def _set_plot_color(self, parts, color):
        for pc in parts['bodies']:
            pc.set_facecolor(color)
            pc.set_edgecolor('black')
            pc.set_alpha(1)

    def _set_quartiles(self, ax, data):
        ax.xaxis.set_tick_params(direction='out')
        ax.xaxis.set_ticks_position('bottom')
        quartile1, medians, quartile3 = np.percentile(data, [25, 50, 75], axis=1)
        whiskers = np.array([
            self._adjacent_values(sorted_array, q1, q3)
            for sorted_array, q1, q3 in zip(data, quartile1, quartile3)])
        whiskers_min, whiskers_max = whiskers[:, 0], whiskers[:, 1]

        inds = np.arange(1, len(medians) + 1)
        ax.scatter(inds, medians, marker='o', color='white', s=30, zorder=3)
        ax.vlines(inds, quartile1, quartile3, color='k', linestyle='-', lw=5)
        ax.vlines(inds, whiskers_min, whiskers_max, color='k', linestyle='-', lw=1)

    def _adjacent_values(self, vals, q1, q3):
        upper_adjacent_value = q3 + (q3 - q1) * 1.5
        upper_adjacent_value = np.clip(upper_adjacent_value, q3, vals[-1])

        lower_adjacent_value = q1 - (q3 - q1) * 1.5
        lower_adjacent_value = np.clip(lower_adjacent_value, vals[0], q1)
        return lower_adjacent_value, upper_adjacent_value
