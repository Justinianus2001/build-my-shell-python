def main():
    # Wait for user input
    command = input("$ ")
    if command == "exit 0":
        return 0
    print(f"{command}: command not found")
    main()


if __name__ == "__main__":
    main()
