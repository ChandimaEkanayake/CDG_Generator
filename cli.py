import os
from parser.ast_parser import extract_dependencies_from_repo
from parser.cdg_generator import generate_cdg

def main():
    print("Welcome to the Component Dependency Graph Generator!")

    # Default repo folder
    repo_path = "repo"
    if not os.path.isdir(repo_path):
        print(f"Error: The folder '{repo_path}' does not exist.")
        return

    # Prompt for output file name
    cdg_name = input("Enter the output graph name (without extension, e.g., cdg_project): ").strip()

    try:
        # Extract dependencies
        print(f"Parsing Python files in the folder '{repo_path}'...")
        dependencies = extract_dependencies_from_repo(repo_path)
        print("Dependencies extracted successfully!")

        # Generate the CDG
        output_path = os.path.join("output", f"{cdg_name}.png")
        generate_cdg(dependencies, output_path)
        print(f"Component Dependency Graph saved to '{output_path}'")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
