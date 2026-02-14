import ast
import sys

assignment_list = []
load_list = []
unused_var_list = []
import_list = []
used_import_list = []
line_suggestion_limit = 80
snake_case = [True]

with open("main.py") as f:
    tree = ast.parse(f.read())

class Visitor(ast.NodeVisitor):
    def visit_Assign(self, node):
        for targets in node.targets:
            if isinstance(targets, ast.Name):
                if targets.id not in assignment_list:
                    if (targets.id != targets.id.lower()):
                        snake_case[0] = False
                    assignment_list.append((targets.id, targets.lineno))
        self.generic_visit(node)

    def visit_Load(self, node):
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                load_list.append(node.id)


    def visit_Import(self, node):
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if ((str(alias.name)) not in import_list):
                        import_list.append(str(alias.name))

class VisitorMemory(ast.NodeVisitor):
    #Does not work with [X] * 10 syntax
    def visit(self, node):
            if isinstance(node, ast.List) and isinstance(node.ctx, ast.Load):
                if (len(node.elts)) > sys.maxsize:
                    print("Memory error, exceeding sys.maxsize")
            if isinstance(node, ast.Tuple) and isinstance(node.ctx, ast.Load):
                if (len(node.elts)) > sys.maxsize:
                    print("Memory error, exceeding sys.maxsize")
            self.generic_visit(node)


def find_unused_variables():
    for assignment in assignment_list:
        if assignment[0] not in load_list:
            unused_var_list.append(assignment)
    return unused_var_list

def find_used_import_list():
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            if node.id in import_list and node.id not in used_import_list:
                used_import_list.append(node.id)

def line_len_checker():
    line_no = 0
    with open("main.py") as f:
        for line in f:
            if len(line.strip()) >= line_suggestion_limit:
                print(f"Line of length >= {line_suggestion_limit} on line {line_no}")
            line_no += 1

def main():
    Visitor().visit(tree)
    VisitorMemory().visit(tree)
    #unused variable check
    unused_var_list = find_unused_variables()
    if unused_var_list:
        for var in unused_var_list:
            print(f"Variable {var[0]} declared at line {var[1]} is not used")
    else:
        print("No unused variables found")
    #unused import check
    find_used_import_list()
    if len(import_list) == len(used_import_list):
        print("No unused imports found")
    else:
        for _import in import_list:
            if _import not in used_import_list:
                print(f"Unused import {_import}")
    #line length check
    line_len_checker()
    #snake_case check
    if not snake_case[0]:
        print("Suggestion | PEP 8 Suggests using snake_case as the standard naming convention for most identifiers")


if __name__ == "__main__":
    main()

