import functools
import os
import readline
import shlex
import subprocess
import sys


builtins = {"exit", "echo", "type", "pwd", "cd"}
redirect_symbols = ["2>>", "1>>", ">>", "2>", "1>", ">"]


def completer(text, state):
    options = [command + " " for command in builtins if command.startswith(text)]
    return options[state] if state < len(options) else None


def handle_redirects(command, out, err, symbol):
    command, file = command.split(symbol)
    file = file.strip()

    match symbol:
        case "2>>":
            return command, out, open(file, "a")
        case "1>>" | ">>":
            return command, open(file, "a"), err
        case "2>":
            return command, out, open(file, "w")
        case "1>" | ">":
            return command, open(file, "w"), err


def get_command_path(command):
    paths = os.getenv("PATH").split(os.pathsep)

    for path in paths:
        if os.path.exists(f"{path}/{command}"):
            return f"{path}/{command}"

    return None


def main():
    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)

    while True:
        # Wait for user input
        command = input("$ ").strip()
        out = sys.stdout
        err = sys.stderr

        for symbol in redirect_symbols:
            if symbol in command:
                command, out, err = handle_redirects(command, out, err, symbol)
                break

        print = functools.partial(__builtins__.print, file=out)
        print_err = functools.partial(__builtins__.print, file=err)

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
                    print_err(f"cd: {path}: No such file or directory")
            case [file, *args]:
                if get_command_path(file):
                    subprocess.run([file, *args], stdout=out, stderr=err)
                else:
                    print_err(f"{command}: command not found")

        if out is not sys.stdout:
            out.close()

        if err is not sys.stderr:
            err.close()


if __name__ == "__main__":
    main()
