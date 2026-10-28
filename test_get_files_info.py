from functions.get_files_info import get_files_info


def main():
    test_cases = [
        ("calculator", "."),
        ("calculator", "pkg"),
        ("calculator", "/bin"),
        ("calculator", "../"),
    ]

    for working_directory, directory in test_cases:
        result = get_files_info(working_directory, directory)
        print(f"Result for '{directory}' directory:")
        for line in result.split("\n"):
            print(f"    {line}")

if __name__ == "__main__":
    main()
