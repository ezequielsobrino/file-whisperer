import os
import json
from groq import Groq
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Obtener la clave API de Groq
groq_api_key = os.getenv('GROQ_API_KEY')

# Inicializar el cliente de Groq con la clave API
client = Groq(api_key=groq_api_key)
MODEL = 'llama3-groq-70b-8192-tool-use-preview'

def create_folder(path):
    """Create a new folder"""
    try:
        os.makedirs(path, exist_ok=True)
        return json.dumps({"result": f"Folder created at {path}"})
    except Exception as e:
        return json.dumps({"error": str(e)})

def create_file(path, content=""):
    """Create a new file with optional content"""
    try:
        with open(path, 'w') as f:
            f.write(content)
        return json.dumps({"result": f"File created at {path}"})
    except Exception as e:
        return json.dumps({"error": str(e)})

def read_file(path):
    """Read the contents of a file"""
    try:
        with open(path, 'r') as f:
            content = f.read()
        return json.dumps({"result": content})
    except Exception as e:
        return json.dumps({"error": str(e)})

def write_file(path, content):
    """Write content to a file (overwrite)"""
    try:
        with open(path, 'w') as f:
            f.write(content)
        return json.dumps({"result": f"Content written to {path}"})
    except Exception as e:
        return json.dumps({"error": str(e)})

def modify_file(path, content):
    """Append content to an existing file"""
    try:
        with open(path, 'a') as f:
            f.write(content)
        return json.dumps({"result": f"Content appended to {path}"})
    except Exception as e:
        return json.dumps({"error": str(e)})

def list_folder(path):
    """List the contents of a folder"""
    try:
        contents = os.listdir(path)
        return json.dumps({"result": contents})
    except Exception as e:
        return json.dumps({"error": str(e)})

def run_conversation(user_prompt):
    messages = [
        {
            "role": "system",
            "content": "You are a file management assistant. Use the provided functions to manage files and folders based on user requests."
        },
        {
            "role": "user",
            "content": user_prompt,
        }
    ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "create_folder",
                "description": "Create a new folder",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path where to create the folder",
                        }
                    },
                    "required": ["path"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "create_file",
                "description": "Create a new file with optional content",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path where to create the file",
                        },
                        "content": {
                            "type": "string",
                            "description": "The content to write in the file (optional)",
                        }
                    },
                    "required": ["path"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "Read the contents of a file",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path of the file to read",
                        }
                    },
                    "required": ["path"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "write_file",
                "description": "Write content to a file (overwrite)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path of the file to write",
                        },
                        "content": {
                            "type": "string",
                            "description": "The content to write in the file",
                        }
                    },
                    "required": ["path", "content"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "modify_file",
                "description": "Append content to an existing file",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path of the file to modify",
                        },
                        "content": {
                            "type": "string",
                            "description": "The content to append to the file",
                        }
                    },
                    "required": ["path", "content"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "list_folder",
                "description": "List the contents of a folder",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path of the folder to list",
                        }
                    },
                    "required": ["path"],
                },
            },
        },
    ]
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        max_tokens=4096
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    if tool_calls:
        available_functions = {
            "create_folder": create_folder,
            "create_file": create_file,
            "read_file": read_file,
            "write_file": write_file,
            "modify_file": modify_file,
            "list_folder": list_folder,
        }
        messages.append(response_message)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(**function_args)
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )
        second_response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )
        return second_response.choices[0].message.content
    else:
        return response_message.content

def main():
    print("Welcome to the File Whisperer!")
    print("Type your commands in natural language. Type 'exit' to quit.")
    print("Example: 'Create a folder called test and a file inside it named example.txt'")
    
    while True:
        user_input = input("\nEnter your command: ")
        if user_input.lower() == 'exit':
            print("Thank you for using File Whisperer. Goodbye!")
            break
        
        try:
            result = run_conversation(user_input)
            print("\nResult:")
            print(result)
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()