import unittest
from src.agilec_spellcheck_service import get_response, parse, is_spelling_correct

class AgilecSpellCheckServiceTests(unittest.TestCase):
    
    def test_canary(self):
        self.assertTrue(True)
    
    def test_get_response_returns_true(self):
        self.assertEqual('true', get_response("FAVOR"))


    def test_get_response_returns_false(self):
        self.assertEqual('false', get_response("FAVRO"))
    

    def test_parse_return_true_for_true(self):
        self.assertTrue(parse('true'))


    def test_parse_return_false_for_false(self):
        self.assertFalse(parse('false'))


    def test_parse_raise_error_not_true_or_false(self):
        with self.assertRaisesRegex(ValueError, "Did not receive true or false"): 
            parse('unexpected_result')


    def test_is_spelling_correct_returns_true(self):
        self.assertTrue(is_spelling_correct('FAVOR'))


    def test_is_spelling_correct_returns_false(self):
        self.assertFalse(is_spelling_correct('FAVRO'))
        

    def test_is_spelling_throws_network_error(self):
        def get_response_that_fails(word):
            raise ConnectionError("Network Error")
        
        self.assertRaisesRegex(ConnectionError, "Network Error", is_spelling_correct, "FAVOR", get_response_that_fails)
