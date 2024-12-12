import ast
import os

def extract_class_and_function_dependencies(source_code, file_name):
    """
    Extracts class and function dependencies from a source code file.
    Tracks dependencies within classes and functions.
    """
    tree = ast.parse(source_code)
    dependencies = {"files": {}, "classes": {}, "functions": {}}

    # Store file-level dependencies
    file_dependencies = []

    # Walk through the AST
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):  # Function-level
            function_name = node.name
            dependencies["functions"][f"{file_name}:{function_name}"] = []
            for sub_node in ast.walk(node):
                if isinstance(sub_node, ast.Call):
                    # Handle function calls within this function
                    if isinstance(sub_node.func, ast.Name):
                        dependencies["functions"][f"{file_name}:{function_name}"].append(sub_node.func.id)
                    elif isinstance(sub_node.func, ast.Attribute):
                        dependencies["functions"][f"{file_name}:{function_name}"].append(sub_node.func.attr)

        elif isinstance(node, ast.ClassDef):  # Class-level
            class_name = node.name
            dependencies["classes"][f"{file_name}:{class_name}"] = []
            for class_node in ast.walk(node):
                if isinstance(class_node, ast.FunctionDef):  # Methods in class
                    method_name = class_node.name
                    dependencies["classes"][f"{file_name}:{class_name}"].append(method_name)

    # Return structured dependencies
    return dependencies

def extract_dependencies_from_repo(folder_path):
    """
    Recursively extracts dependencies from all Python files in a repo.
    """
    all_dependencies = {"files": {}, "classes": {}, "functions": {}}

    # Walk through the folder
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):  # Only process Python files
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    source_code = f.read()

                # Extract dependencies
                file_dependencies = extract_class_and_function_dependencies(source_code, file)
                # Merge results
                for key in all_dependencies:
                    all_dependencies[key].update(file_dependencies[key])

    return all_dependencies
