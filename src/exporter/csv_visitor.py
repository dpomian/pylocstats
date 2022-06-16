class CSVVisitor:
    def visit(self, project_stats, delim=','):
        csv_lines = []
        for function_stats in project_stats.function_stats:
            csv_lines.append(f'{project_stats.project_name}{delim}{function_stats.file}{delim}{function_stats.name}{delim}{function_stats.lineno}{delim}{function_stats.loc}')

        return '\n'.join(csv_lines)