import ast
from pprint import pp
import sys
assignment_list = []
load_list = []
unused_var_list = []

with open("main.py") as f:
    tree = ast.parse(f.read())

class Visitor(ast.NodeVisitor):
    def visit_Assign(self, node):
        for targets in node.targets:
            if isinstance(targets, ast.Tuple):
                for vars in targets.elts:
                    if vars.id not in assignment_list:
                        assignment_list.append((vars.id,vars.lineno))
                    continue
            if isinstance(targets, ast.Name):
                if targets.id not in assignment_list:
                    assignment_list.append((targets.id, targets.lineno))

        self.generic_visit(node)

    def visit_Load(self, node):
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                load_list.append(node.id)

def find_unused_variables():
    Visitor().visit(tree)
    for assignment in assignment_list:
        if assignment[0] not in load_list:
            unused_var_list.append(assignment)
    return unused_var_list

def main():
    unused_var_list = find_unused_variables()
    if unused_var_list:
        for var in unused_var_list:
            print(f"Variable {var[0]} declared at line {var[1]} is not used")
    else:
        print("No unused variables found")
        
if __name__ == "__main__":
    main()
















