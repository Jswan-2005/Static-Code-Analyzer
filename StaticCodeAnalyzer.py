''' This is a basic linter, created using the Python AST module
    Current capabilties include, unused variable, import, function calls & parameters checking.
    Additonally, the linter checks if any line length exceeds the line_suggestion_limit as issues a warning.
    Additonally, the linter checks (extremely basic functionality) if variables are snake_case and suggest a warning if they are not.
'''
import ast
import pprint as pp
import sys
line_suggestion_limit = 80

filename = sys.argv[1] if len(sys.argv) > 1 else None
if filename is None:
    print("No filename provided")
    sys.exit(1)
try:
    with open("main.py") as f:
        tree = ast.parse(f.read())
except FileNotFoundError:
    print("File Error")
    sys.exit(1)

class Visitor(ast.NodeVisitor):
    '''Covers unused variables, unused imports & uncalled functions'''
    def __init__(self):
        self.assignment_list = []
        self.load_list = []
        self.import_list = []
        self.snake_case = True
        self.func_assignments = []
        self.func_calls = []
        self.func_params = []
        self.used_params = []

    #Visits all assignments
    def visit_Assign(self, node):
        for targets in node.targets:
            if isinstance(targets, ast.Name):
                if targets.id not in self.assignment_list:
                    if (targets.id != targets.id.lower()):
                        self.snake_case = False
                    self.assignment_list.append((targets.id, targets.lineno))
        self.generic_visit(node)

    #Visits all ast.Name nodes
    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.load_list.append(node.id)
        self.generic_visit(node)

    #Visits all imports (does not currently support 'from module import syntax')
    def visit_Import(self, node):
        for alias in node.names:
            if ((str(alias.name)) not in self.import_list):
                self.import_list.append(str(alias.name))
        self.generic_visit(node)

    #Visits all function definitions
    def visit_FunctionDef(self, node):
        self.func_assignments.append((node.name, node.lineno))
        self.func_params = []
        for arg in node.args.args:
            self.func_params.append((arg.arg, arg.lineno))
        self.used_params = []
        for node in node.body:
            add = True
            text = ast.dump(node)
            for arg in self.func_params:
                comparision_string = "id=" + f"'{arg[0]}'"
                if comparision_string in text and arg[0] not in self.used_params:
                    self.used_params.append(arg[0])
        self.generic_visit(node)

    #Visits all functions calls
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.func_calls.append(node.func.id)
        self.generic_visit(node)

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
                pp.pprint(f"Variable {var[0]} declared at line {var[1]} is not used")
        else:
            pp.pprint("No unused variables found")

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
            pp.pprint("No unused imports found")
        else:
            for import_ in self.import_list:
                if import_ not in used_import_list:
                    pp.pprint(f"Unused import {import_}")

    def unused_function_params_summary(self):
        for func_param in self.func_params:
            if func_param[0] not in self.used_params:
                pp.pprint(f"Unused function parameter {func_param[0]} declared at line {func_param[1]}")

    def uncalled_function_summary(self):
        for func in self.func_assignments:
            if func[0] not in self.func_calls:
                pp.pprint(f"Uncalled function {func[0]} at line {func[1]}")

    def snake_case_checker(self):
        if not self.snake_case:
            pp.pprint("Suggestion | PEP 8 Suggests using snake_case as the standard naming convention for most identifiers")

def line_len_checker():
    line_no = 0
    with open("main.py") as f:
        for line in f:
            if len(line.strip()) >= line_suggestion_limit:
                pp.pprint(f"Line of length >= {line_suggestion_limit} on line {line_no}")
            line_no += 1

def main():
    visit = Visitor()
    visit.visit(tree)
    #Unused Variables Check
    visit.unused_variables_summary()
    #Unused Import Check
    visit.unused_import_summary()
    #snake_case checker
    visit.snake_case_checker()
    #line length checker
    line_len_checker()
    #Uncalled functions check
    visit.uncalled_function_summary()
    #Unused function paramters check
    visit.unused_function_params_summary()

if __name__ == "__main__":
    main()