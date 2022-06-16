import threading
from model.globals import GlobalQs
from exporter.csv_visitor import CSVVisitor


class CSVExporter:
    def __init__(self, filename, header):
        self._filename = filename
        self._threads_count = 10
        self._open_flag = "w"
        self._export(header)
        self._open_flag = "a"

    def _init_threads(self):
        for i in range(self._threads_count):
            threading.Thread(target=self._export_worker, daemon=True).start()

    def _export_worker(self):
        csv_visitor = CSVVisitor()
        while True:
            item = self._processed_q.get()
            print(f'exporting project: {item.project_name}')
            self._export(item.accept(csv_visitor))
            self._processed_q.task_done()

    def _export(self, csv_line):
        with open(self._filename, self._open_flag) as ofile:
            ofile.write(f'{csv_line}\n')
        # print(csv_line)

    def export(self, project_stats_list):
        csv_visitor = CSVVisitor()
        for ps in project_stats_list:
            print(f'exporting project: {ps.project_name}')
            self._export(ps.accept(csv_visitor))

    # def export(self, processed_q):
    #     self._processed_q = GlobalQs.instance().get_processed_q()
    #     self._init_threads()
    #     self._processed_q.join()
