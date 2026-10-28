from functions.run_python_file import run_python_file


def main():
    test_cases = [
        ("calculator", "main.py"),
        ("calculator", "main.py", ["3 + 5"]),
        ("calculator", "tests.py"),
        ("calculator", "../main.py"),
        ("calculator", "nonexistent.py"),
        ("calculator", "lorem.txt"),
    ]

    for working_directory, file, *args in test_cases:
        arguments = args[0] if args else None
        result = run_python_file(working_directory, file, arguments)
        print(f"Result for '{file}' file:")
        print(result)

if __name__ == "__main__":
    main()
