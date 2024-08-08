import unittest
import os
import shutil
from main import create_folder, create_file, read_file, write_file, modify_file, list_folder, run_conversation

class TestFileWhisperer(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = 'test_directory'
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        # Remove the temporary directory after tests
        shutil.rmtree(self.test_dir)

    def test_create_folder(self):
        result = create_folder(os.path.join(self.test_dir, 'new_folder'))
        self.assertTrue('Folder created' in result)
        self.assertTrue(os.path.isdir(os.path.join(self.test_dir, 'new_folder')))

    def test_create_file(self):
        file_path = os.path.join(self.test_dir, 'test_file.txt')
        result = create_file(file_path, 'Hello, World!')
        self.assertTrue('File created' in result)
        self.assertTrue(os.path.isfile(file_path))
        with open(file_path, 'r') as f:
            self.assertEqual(f.read(), 'Hello, World!')

    def test_read_file(self):
        file_path = os.path.join(self.test_dir, 'read_test.txt')
        with open(file_path, 'w') as f:
            f.write('Test content')
        result = read_file(file_path)
        self.assertTrue('Test content' in result)

    def test_write_file(self):
        file_path = os.path.join(self.test_dir, 'write_test.txt')
        result = write_file(file_path, 'New content')
        self.assertTrue('Content written' in result)
        with open(file_path, 'r') as f:
            self.assertEqual(f.read(), 'New content')

    def test_modify_file(self):
        file_path = os.path.join(self.test_dir, 'modify_test.txt')
        with open(file_path, 'w') as f:
            f.write('Initial content\n')
        result = modify_file(file_path, 'Additional content')
        self.assertTrue('Content appended' in result)
        with open(file_path, 'r') as f:
            self.assertEqual(f.read(), 'Initial content\nAdditional content')

    def test_list_folder(self):
        os.makedirs(os.path.join(self.test_dir, 'list_test'))
        create_file(os.path.join(self.test_dir, 'list_test', 'file1.txt'))
        create_file(os.path.join(self.test_dir, 'list_test', 'file2.txt'))
        result = list_folder(os.path.join(self.test_dir, 'list_test'))
        self.assertTrue('file1.txt' in result and 'file2.txt' in result)

    def test_run_conversation(self):
        # This test is more complex and might require mocking the Groq API
        # For now, we'll just test a simple command
        result = run_conversation("Create a folder called 'documents' in D:\\repos\\file-whisperer\\test_directory\\ directory")
        self.assertTrue(os.path.isdir(os.path.join(self.test_dir, 'documents')))

if __name__ == '__main__':
    unittest.main()