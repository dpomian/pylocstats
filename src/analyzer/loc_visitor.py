import ast
from _ast import FunctionDef
from typing import Any
from model.project_stats import FunctionStats

class LocVisitor(ast.NodeVisitor):
    def __init__(self, file):
        self.file = file
        self.function_stats_list = []

    def visit_FunctionDef(self, node: FunctionDef) -> Any:
        fun_stats = FunctionStats().with_file(self.file).with_name(node.name).with_lineno(node.lineno)
        fun_stats = fun_stats.with_loc(self._compute_loc(self.file, node.lineno, node.end_lineno))
        self.function_stats_list.append(fun_stats)
        ast.NodeVisitor.generic_visit(self, node)

    def _compute_loc(self, filename, start_lineno, end_lineno):
        lines = []
        count = 0
        with open(filename) as ifile:
            lines = ifile.readlines()[start_lineno:end_lineno+1]
        in_docstring = False
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                continue
            if line[0] == "#":
                continue

            if (line.startswith('"""') or line.startswith("'''")) and (line.endswith('"""') or line.endswith('"""')):
                if line != '"""' and line != "'''":
                    continue

            if line.startswith('"""') or line.startswith("'''"):
                if not in_docstring:
                    in_docstring = True
                else:
                    in_docstring = False
                continue

            if in_docstring:
                continue
            count += 1
        return count
