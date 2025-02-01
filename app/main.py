def main():
    builtins = {"exit", "echo", "type"}

    # Wait for user input
    command = input("$ ")

    match command.split():
        case ["exit", code]:
            return int(code)
        case ["echo", *text]:
            print(*text)
        case ["type", builtin]:
            if builtin in builtins:
                print(f"{builtin} is a shell builtin")
            else:
                print(f"{builtin}: not found")
        case _:
            print(f"{command}: command not found")

    main()


if __name__ == "__main__":
    main()
