from file_manager import FileManager

def configure_api_key(file_manager):
    print("\nGROQ API Key Configuration")
    print("To obtain your GROQ API Key, follow these steps:")
    print("1. Visit https://console.groq.com/keys")
    print("2. Log in or create an account if you don't have one")
    print("3. Generate a new API key in the dashboard")
    print("4. Copy the generated API key")
    print("\nNOTE: Save your API key in a secure place, as you won't be able to see it again after generating it.")
    print("The API key will be saved in a .env file in the current directory.")
    print("If you need to modify it later, you can edit this file directly.")
    
    api_key = input("\nPlease enter your GROQ API Key: ")
    file_manager.save_api_key(api_key)
    print("API Key saved successfully.")

def main():
    file_manager = FileManager()
    
    print("Welcome to the File Assistant!")
    
    if not file_manager.groq_api_key:
        print("The GROQ API Key has not been configured. Let's configure it now.")
        configure_api_key(file_manager)
    
    print("\nInstructions:")
    print("- Enter your file operation commands directly.")
    print("- To exit the program, type 'exit' or 'quit'.")
    print("\nYou can now start interacting with the File Assistant.")
    
    while True:
        user_input = input("\nEnter your command: ").strip().lower()
        
        if user_input in ['exit', 'quit']:
            print("Thank you for using the File Assistant. Goodbye!")
            break
        
        try:
            result = file_manager.run_conversation(user_input)
            print("\nResult:")
            print(result)
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()