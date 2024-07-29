import unittest
from unittest.mock import patch, MagicMock
from plaud_sync.transcription import transcribe_audio

class TestTranscription(unittest.TestCase):
    @patch('plaud_sync.transcription.requests.post')
    def test_transcribe_audio(self, mock_post):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'text': 'We are on our way.'}
        mock_post.return_value = mock_response

        # Test the transcription function
        result = transcribe_audio('dummy_path')
        self.assertEqual(result, 'We are on our way.')

        # Test error handling
        mock_response.status_code = 500
        result = transcribe_audio('dummy_path')
        self.assertTrue(result.startswith('Transcription failed'))

if __name__ == '__main__':
    unittest.main()