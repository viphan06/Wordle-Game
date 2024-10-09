import unittest
from unittest.mock import patch
from src.agilec_randomizer_service import get_words_from_service, get_word_list, get_a_random_word

class AgilecRandomizerServiceTests(unittest.TestCase):
    
    def test_canary(self):
        self.assertTrue(True)


    def test_get_words_from_service_returns_expected_words(self):       
        expected_result = '\n'.join(['FAVOR', 'SMART', 'GUIDE', 'TESTS', 'GRADE', 'BRAIN', 'SPAIN', 'SPINE', 'GRAIN', 'BOARD']) + '\n'
        self.assertEqual(expected_result, get_words_from_service())


    def test_get_a_word_list_returns_expected_list_of_words(self):
        self.assertEqual(['FAVOR', 'SMART', 'GUIDE', 'TESTS', 'GRADE', 'BRAIN', 'SPAIN', 'SPINE', 'GRAIN', 'BOARD'],
                         get_word_list())
        

    def test_get_word_list_raise_error_for_no_words(self):
        with patch('src.agilec_randomizer_service.get_words_from_service', return_value=''):
            with self.assertRaisesRegex(ValueError, "No words found in response"):
                get_word_list()
                
        
    def test_get_a_random_word_returns_two_different_words_called_twice(self):
        words_list = get_word_list()        
        self.assertNotEqual(get_a_random_word(words_list), get_a_random_word(words_list))


    def test_no_words_return(self):
        words_list = get_word_list()
        result_1 = get_a_random_word(words_list)
        with self.assertRaisesRegex(ValueError, "All words have been chosen"):
            for i in words_list:
                get_a_random_word(words_list)


if __name__ == '__main__':
    unittest.main()
