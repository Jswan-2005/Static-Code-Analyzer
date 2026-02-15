import ast
import sys

line_suggestion_limit = 80

with open("main.py") as f:
    tree = ast.parse(f.read())


class Visitor(ast.NodeVisitor):
    '''Covers unused variables & unused imports'''
    def __init__(self):
        self.assignment_list = []
        self.load_list = []
        self.import_list = []
        self.snake_case = [True]


    def visit_Assign(self, node):
        for targets in node.targets:
            if isinstance(targets, ast.Name):
                if targets.id not in self.assignment_list:
                    if (targets.id != targets.id.lower()):
                        snake_case[0] = False
                    self.assignment_list.append((targets.id, targets.lineno))
        self.generic_visit(node)

    def visit_Load(self, node):
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                self.load_list.append(node.id)


    def visit_Import(self, node):
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if ((str(alias.name)) not in self.import_list):
                        self.import_list.append(str(alias.name))

    def find_unused_variables(self):
        unused_var_list = []
        for assignment in self.assignment_list:
            if assignment[0] not in self.load_list:
                unused_var_list.append(assignment)
        return unused_var_list

    def unused_variables_summary(self):
        unused_var_list = self.find_unused_variables()
        if unused_var_list:
            for var in unused_var_list:
                print(f"Variable {var[0]} declared at line {var[1]} is not used")
        else:
            print("No unused variables found")

    def find_used_import_list(self):
        used_import_list = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                if node.id in self.import_list and node.id not in used_import_list:
                    used_import_list.append(node.id)
        return used_import_list

    def unused_import_summary(self):
        used_import_list = self.find_used_import_list()
        if len(self.import_list) == len(used_import_list):
            print("No unused imports found")
        else:
            for _import in self.import_list:
                if _import not in used_import_list:
                    print(f"Unused import {_import}")

def snake_case_checker(snake_case):
    if not snake_case[0]:
        print("Suggestion | PEP 8 Suggests using snake_case as the standard naming convention for most identifiers")

def line_len_checker():
    line_no = 0
    with open("main.py") as f:
        for line in f:
            if len(line.strip()) >= line_suggestion_limit:
                print(f"Line of length >= {line_suggestion_limit} on line {line_no}")
            line_no += 1

def main():
    visit = Visitor()
    visit.visit(tree)
    #Unused Variables Check
    visit.unused_variables_summary()
    #Unused Import Check
    visit.unused_import_summary()
    #snake_case checker
    snake_case_checker(visit.snake_case)
    #line length checker
    line_len_checker()

    VisitorMemory().visit(tree)


if __name__ == "__main__":
    main()