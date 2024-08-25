# FileWhisperer

FileWhisperer is an intelligent file management assistant that uses natural language processing to perform various file and folder operations. Powered by the Groq API, it allows users to interact with their file system using plain English commands.

## Features

- Create folders and files
- Read file contents
- Write to files
- Modify existing files
- List folder contents
- All operations performed through natural language commands

## Video Demonstration

[![FileWhisperer Demo](https://img.youtube.com/vi/fgtj3Y_wMyM/0.jpg)](https://youtu.be/fgtj3Y_wMyM)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7+
- A Groq API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/ezequielsobrino/file-whisperer.git
   cd file-whisperer
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate` or `.\venv\Scripts\Activate.ps1` in powershell
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

To use FileWhisperer, run the main script and provide your command as a prompt:

```python
python main.py
```

Then, enter your file management command in natural language. For example:

```
Create a folder called 'documents', create a file inside it called 'notes.txt' with the content 'Hello, World!', and then list the contents of the folder.
```

FileWhisperer will interpret your command and perform the requested operations.

## Examples

Here are some example commands you can try:

- "Create a new folder named 'projects' and a file named 'todo.txt' inside it with the content 'Start coding'"
- "Read the contents of the file 'notes.txt' in the 'documents' folder"
- "Append the line 'New task: Learn Python' to the file 'todo.txt' in the 'projects' folder"
- "List all files in the 'documents' folder"

## Contributing

Contributions to FileWhisperer are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgements

- [Groq API](https://www.groq.com/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
