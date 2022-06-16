import unittest
import ast
from analyzer.loc_visitor import LocVisitor
from model.project_stats import ProjectStats


class LocVisitorTest(unittest.TestCase):
    def testFunStats(self):
        filename = 'test_files/TestProject/test.py'
        loc_visitor = LocVisitor(filename)
        project_stats = ProjectStats('TestProject')
        with open(filename) as ifile:
            try:
                parsed = ast.parse(ifile.read())
                loc_visitor.visit(parsed)
                project_stats.add_function_stats(loc_visitor.function_stats_list)
            except Exception as e:
                print(e)

        swap_fun_stats = project_stats.function_stats[0]
        self.assertEqual(1, swap_fun_stats.lineno)
        self.assertEqual(4, swap_fun_stats.loc)

        docstr_fun_stats = project_stats.function_stats[1]
        self.assertEqual(8, docstr_fun_stats.lineno)
        self.assertEqual(2, docstr_fun_stats.loc)

        comment_fun_stats = project_stats.function_stats[2]
        self.assertEqual(16, comment_fun_stats.lineno)
        self.assertEqual(6, comment_fun_stats.loc)

        one_line_docstr_fun = project_stats.function_stats[3]
        self.assertEqual(1, one_line_docstr_fun.loc)


if __name__ == '__main__':
    unittest.main()