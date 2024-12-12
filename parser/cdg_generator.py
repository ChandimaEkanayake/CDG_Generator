from graphviz import Digraph


def generate_cdg(dependencies, output_path):
    """
    Generates a Component Dependency Graph (CDG) showing relationships 
    between files, classes, and functions, and their dependencies.
    """
    graph = Digraph(format="png")
    graph.attr(rankdir="LR")  # Left-to-right layout

    # Add file-level nodes
    for file_name in dependencies["files"]:
        graph.node(file_name, label=f"File: {file_name}", shape="box")

    # Add class-level nodes and dependencies
    for class_name, methods in dependencies["classes"].items():
        file_name = class_name.split(":")[0]  # Extract file from class_name
        graph.node(class_name, label=f"Class: {class_name}", shape="ellipse")

        # Connect class to the file it belongs to
        graph.edge(file_name, class_name)

        # Add methods and connect them to their class
        for method in methods:
            method_full_name = f"{class_name}.{method}"
            graph.node(method_full_name, label=f"Method: {method}", shape="diamond")
            graph.edge(class_name, method_full_name)

    # Add function-level nodes and dependencies
    for function_name, calls in dependencies["functions"].items():
        file_name = function_name.split(":")[0]  # Extract file from function_name
        graph.node(function_name, label=f"Function: {function_name}", shape="oval")

        # Connect function to the file it belongs to
        graph.edge(file_name, function_name)

        # Connect function to other functions/methods it calls
        for call in calls:
            if call in dependencies["functions"]:  # Call is a standalone function
                graph.edge(function_name, call)
            elif call in dependencies["classes"]:  # Call is a class
                graph.edge(function_name, call)
            elif any(call in methods for methods in dependencies["classes"].values()):
                # Call is a method (find the parent class)
                for class_name, methods in dependencies["classes"].items():
                    if call in methods:
                        method_full_name = f"{class_name}.{call}"
                        graph.edge(function_name, method_full_name)

    # Save the graph
    graph.render(output_path, cleanup=True)
