def main():
    # Wait for user input
    command = input("$ ")

    command_split = command.split()

    match command_split[0]:
        case "exit":
            return 0
        case "echo":
            print(" ".join(command_split[1:]))
        case _:
            print(f"{command}: command not found")

    main()


if __name__ == "__main__":
    main()
