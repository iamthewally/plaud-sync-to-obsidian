import unittest
import os
import tempfile
from plaud_sync.file_operations import move_files_to_backup, convert_wav_to_mp3

class TestFileOperations(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        os.rmdir(self.temp_dir)

    def test_move_files_to_backup(self):
        # Create a test file
        test_file = os.path.join(self.temp_dir, 'test.wav')
        with open(test_file, 'w') as f:
            f.write('test content')

        # Move the file
        moved_files = move_files_to_backup([self.temp_dir])

        # Check if the file was moved
        self.assertEqual(len(moved_files), 1)
        self.assertTrue(os.path.exists(moved_files[0]))

    def test_convert_wav_to_mp3(self):
        # This test requires a real WAV file to work properly
        # For now, we'll just check if the function runs without errors
        wav_path = "/Users/wa/Documents/GitHub/plaud-sync-to-obsidian/wav/R20240728-125536.WAV"
        mp3_path = os.path.join(self.temp_dir, 'test.mp3')
        
        convert_wav_to_mp3(wav_path, mp3_path)
        
        self.assertTrue(os.path.exists(mp3_path))

if __name__ == '__main__':
    unittest.main()