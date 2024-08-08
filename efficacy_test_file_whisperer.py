import os
import shutil
import json
from main import run_conversation

def verify_action(command, expected_outcome, verification_function):
    result = run_conversation(command)
    success = verification_function(result)
    return {
        "command": command,
        "expected_outcome": expected_outcome,
        "result": result,
        "success": success
    }

def run_efficacy_tests():
    test_dir = 'efficacy_test_directory'
    os.makedirs(test_dir, exist_ok=True)

    tests = [
        {
            "command": f"Create a folder called 'documents' in {test_dir}",
            "expected_outcome": "Folder 'documents' is created",
            "verification": lambda _: os.path.isdir(os.path.join(test_dir, 'documents'))
        },
        {
            "command": f"Create a file named 'notes.txt' in the 'documents' folder in {test_dir} with the content 'This is a test note.'",
            "expected_outcome": "File 'notes.txt' is created with correct content",
            "verification": lambda _: os.path.isfile(os.path.join(test_dir, 'documents', 'notes.txt')) and 
                                      open(os.path.join(test_dir, 'documents', 'notes.txt')).read().strip() == 'This is a test note.'
        },
        {
            "command": f"Read the contents of the file 'notes.txt' in the 'documents' folder in {test_dir}",
            "expected_outcome": "Contents of 'notes.txt' are correctly returned",
            "verification": lambda result: 'This is a test note.' in result
        },
        {
            "command": f"Append the line 'This is an additional note.' to the file 'notes.txt' in the 'documents' folder in {test_dir}",
            "expected_outcome": "New line is appended to 'notes.txt'",
            "verification": lambda _: 'This is an additional note.' in open(os.path.join(test_dir, 'documents', 'notes.txt')).read()
        },
        {
            "command": f"List all files in the 'documents' folder in {test_dir}",
            "expected_outcome": "List of files in 'documents' folder is returned",
            "verification": lambda result: 'notes.txt' in result
        },
        {
            "command": f"Create 3 files named 'file1.txt', 'file2.txt', and 'file3.txt' in the 'documents' folder in {test_dir}, each containing the text 'This is file number X' where X is the file number",
            "expected_outcome": "3 new files are created with correct content",
            "verification": lambda _: all(os.path.isfile(os.path.join(test_dir, 'documents', f'file{i}.txt')) and 
                                          open(os.path.join(test_dir, 'documents', f'file{i}.txt')).read().strip() == f'This is file number {i}'
                                          for i in range(1, 4))
        }
    ]

    results = []
    for test in tests:
        result = verify_action(test["command"], test["expected_outcome"], test["verification"])
        results.append(result)

    # Clean up
    shutil.rmtree(test_dir)

    return results

def print_results(results):
    print("Efficacy Test Results:")
    print("----------------------")
    for result in results:
        print(f"Command: {result['command']}")
        print(f"Expected outcome: {result['expected_outcome']}")
        print(f"Result: {'Success' if result['success'] else 'Failure'}")
        if not result['success']:
            print(f"Actual result: {result['result']}")
        print("----------------------")

    success_rate = (sum(1 for result in results if result['success']) / len(results)) * 100
    print(f"Overall success rate: {success_rate:.2f}%")

if __name__ == "__main__":
    results = run_efficacy_tests()
    print_results(results)