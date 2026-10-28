from functions.get_file_content import get_file_content


def main():
    test_cases = [
        ("calculator", "lorem.txt"),
        ("calculator", "main.py"),
        ("calculator", "pkg/calculator.py"),
        ("calculator", "/bin/cat"),
        ("calculator", "pkg/does_not_exist.py"),
    ]

    for working_directory, file in test_cases:
        result = get_file_content(working_directory, file)
        print(f"Result for '{file}' file:")
        print(result)
        print(f"{file} length: {len(result)}")
        print(f"{file} truncated: {'truncated' in result}")
if __name__ == "__main__":
    main()
