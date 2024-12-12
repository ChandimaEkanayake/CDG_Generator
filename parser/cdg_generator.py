from graphviz import Digraph

def generate_cdg(dependencies, output_path):
    """
    Generates a Component Dependency Graph (CDG) based on extracted dependencies.
    Shows relationships between files, classes, and functions.
    """
    graph = Digraph(format="png")
    graph.attr(rankdir="LR")

    # Add nodes and edges for files
    for file_name in dependencies["files"]:
        graph.node(file_name, label=f"File: {file_name}", shape="box")

    # Add nodes and edges for classes
    for class_name, methods in dependencies["classes"].items():
        graph.node(class_name, label=f"Class: {class_name}", shape="ellipse")
        for method in methods:
            method_full_name = f"{class_name}.{method}"
            graph.node(method_full_name, label=f"Method: {method}", shape="diamond")
            graph.edge(class_name, method_full_name)

    # Add nodes and edges for functions
    for function_name, calls in dependencies["functions"].items():
        graph.node(function_name, label=f"Function: {function_name}", shape="oval")
        for call in calls:
            if call in dependencies["functions"]:
                graph.edge(function_name, call)

    # Save the graph
    graph.render(output_path, cleanup=True)
