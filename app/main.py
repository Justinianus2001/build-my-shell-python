import os
import shlex


def get_command_path(command):
    paths = os.getenv("PATH").split(os.pathsep)

    for path in paths:
        if os.path.exists(f"{path}/{command}"):
            return f"{path}/{command}"

    return None


def main():
    builtins = {"exit", "echo", "type", "pwd", "cd"}

    # Wait for user input
    command = input("$ ").strip()

    match shlex.split(command):
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
        case ["pwd"]:
            print(os.getcwd())
        case ["cd", path]:
            try:
                os.chdir(os.path.expanduser(path))
            except FileNotFoundError:
                print(f"cd: {path}: No such file or directory")
        case _:
            if get_command_path(shlex.split(command)[0]):
                os.system(command)
            else:
                print(f"{command}: command not found")

    main()


if __name__ == "__main__":
    main()
