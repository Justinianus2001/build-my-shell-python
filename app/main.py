import functools
import os
import shlex
import subprocess
import sys


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
    out = sys.stdout
    err = sys.stderr

    if "2>" in command:
        command, output_file = command.split("2>")
        err = open(output_file.strip(), "w")
    elif ">" in command:
        command, output_file = command.replace("1>", ">").split(">")
        out = open(output_file.strip(), "w")

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

    main()


if __name__ == "__main__":
    main()
