class FunctionStats:
    def __init__(self):
        self.file = None
        self.lineno = None
        self.name = None
        self.loc = None

    def with_name(self, name):
        self.name = name
        return self

    def with_lineno(self, lineno):
        self.lineno = lineno
        return self

    def with_file(self, file):
        self.file = file
        return self

    def with_loc(self, loc):
        self.loc = loc
        return self

class ProjectStats:
    def __init__(self, name):
        self.project_name = name
        self.function_stats = []

    def add_function_stats(self, function_stats):
        self.function_stats += function_stats

    def accept(self, visitor):
        return visitor.visit(self)
