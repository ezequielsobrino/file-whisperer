from file_manager import FileManager


def main():
    file_manager = FileManager()
    print("Welcome to the File Whisperer!")
    print("Type your commands in natural language. Type 'exit' to quit.")
    print("Example: 'Create a folder called test and a file inside it named example.txt'")
    
    while True:
        user_input = input("\nEnter your command: ")
        if user_input.lower() == 'exit':
            print("Thank you for using File Whisperer. Goodbye!")
            break
        
        try:
            result = file_manager.run_conversation(user_input)
            print("\nResult:")
            print(result)
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()