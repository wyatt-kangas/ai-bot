from functions.write_file import write_file


def main():
    test_cases = [
        ("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
        ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
        ("calculator", "/tmp/temp.txt", "this should not be allowed"),
    ]

    for working_directory, file, content in test_cases:
        result = write_file(working_directory, file, content)
        print(f"Result for '{file}' file:")
        print(result)

if __name__ == "__main__":
    main()
