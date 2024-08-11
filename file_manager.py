import os
import json
from groq import Groq
from dotenv import load_dotenv

class FileManager:
    """
    A class that provides a natural language interface for file and folder operations.

    This class uses the Groq API to interpret user commands and perform file system operations.
    The main public interface is the run_conversation method, which takes a user prompt
    and returns the result of the interpreted command.

    Attributes:
        groq_api_key (str): The API key for Groq.
        client (Groq): The Groq client instance.
        MODEL (str): The name of the Groq model to use.
    """

    def __init__(self):
        load_dotenv()
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        self.client = Groq(api_key=self.groq_api_key)
        self.MODEL = 'llama3-groq-70b-8192-tool-use-preview'

    def create_folder(self, path):
        try:
            os.makedirs(path, exist_ok=True)
            return json.dumps({"result": f"Folder created at {path}"})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def create_file(self, path, content=""):
        try:
            with open(path, 'w') as f:
                f.write(content)
            return json.dumps({"result": f"File created at {path}"})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def read_file(self, path):
        try:
            with open(path, 'r') as f:
                content = f.read()
            return json.dumps({"result": content})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def write_file(self, path, content):
        try:
            with open(path, 'w') as f:
                f.write(content)
            return json.dumps({"result": f"Content written to {path}"})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def modify_file(self, path, content):
        try:
            with open(path, 'a') as f:
                f.write(content)
            return json.dumps({"result": f"Content appended to {path}"})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def list_folder(self, path):
        try:
            contents = os.listdir(path)
            return json.dumps({"result": contents})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def run_conversation(self, user_prompt):
        """
        Process a user's natural language prompt and perform the requested file operation.

        This is the main public interface of the FileWhisperer class. It takes a user's
        natural language request, interprets it using the Groq API, and performs the
        corresponding file system operation.

        Args:
            user_prompt (str): The user's natural language request.

        Returns:
            str: The result of the operation or an error message.

        Raises:
            Exception: If there's an error in processing the request or performing the operation.
        """
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
        
        response = self.client.chat.completions.create(
            model=self.MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            max_tokens=4096
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        if tool_calls:
            available_functions = {
                "create_folder": self.create_folder,
                "create_file": self.create_file,
                "read_file": self.read_file,
                "write_file": self.write_file,
                "modify_file": self.modify_file,
                "list_folder": self.list_folder,
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
            second_response = self.client.chat.completions.create(
                model=self.MODEL,
                messages=messages
            )
            return second_response.choices[0].message.content
        else:
            return response_message.content