import os


def get_command_path(command):
    paths = os.getenv("PATH").split(os.pathsep)

    for path in paths:
        if os.path.exists(f"{path}/{command}"):
            return f"{path}/{command}"

    return None


def main():
    builtins = {"exit", "echo", "type"}

    # Wait for user input
    command = input("$ ").strip()

    match command.split(" "):
        case ["exit", code]:
            return int(code)
        case ["echo", *text]:
            print(*text)
        case ["type", builtin]:
            command_path = get_command_path(builtin)

            if builtin in builtins:
                print(f"{builtin} is a shell builtin")
            elif command_path:
                print(f"{builtin} is {command_path}")
            else:
                print(f"{builtin}: not found")
        case _:
            if get_command_path(command.split(" ")[0]):
                os.system(command)
            else:
                print(f"{command}: command not found")

    main()


if __name__ == "__main__":
    main()
