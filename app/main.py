import os


def main():
    builtins = {"exit", "echo", "type"}
    paths = os.getenv("PATH").split(":")

    # Wait for user input
    command = input("$ ")

    match command.split():
        case ["exit", code]:
            return int(code)
        case ["echo", *text]:
            print(*text)
        case ["type", builtin]:
            command_path = next((f"{path}/{builtin}" for path in paths if os.path.exists(f"{path}/{builtin}")), None)

            if builtin in builtins:
                print(f"{builtin} is a shell builtin")
            elif command_path:
                print(f"{builtin} is {command_path}")
            else:
                print(f"{builtin}: not found")
        case _:
            print(f"{command}: command not found")

    main()


if __name__ == "__main__":
    main()
