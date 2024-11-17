import unittest
from parameterized import parameterized
from src.wordle import Matches, Status, PlayResponse, tally, play

globals().update(Matches.__members__)

class WordleTests(unittest.TestCase):

    def test_canary(self):
        self.assertTrue(True)


    @parameterized.expand([
        ("FAVOR", "FAVOR", [EXACT_MATCH] * 5),
        ("FAVOR", "TESTS", [WRONG_MATCH] * 5),
        ("FAVOR", "RAPID", [PARTIAL_MATCH, EXACT_MATCH, WRONG_MATCH, WRONG_MATCH, WRONG_MATCH]),
        ("FAVOR", "MAYOR", [WRONG_MATCH, EXACT_MATCH, WRONG_MATCH, EXACT_MATCH, EXACT_MATCH]),
        ("FAVOR", "RIVER", [WRONG_MATCH, WRONG_MATCH, EXACT_MATCH, WRONG_MATCH, EXACT_MATCH]),
        ("FAVOR", "AMAST", [PARTIAL_MATCH, WRONG_MATCH, WRONG_MATCH, WRONG_MATCH, WRONG_MATCH]),
        ("SKILL", "SKILL", [EXACT_MATCH] * 5),
        ("SKILL", "SWIRL", [EXACT_MATCH, WRONG_MATCH, EXACT_MATCH, WRONG_MATCH, EXACT_MATCH]),
        ("SKILL", "CIVIL", [WRONG_MATCH, PARTIAL_MATCH, WRONG_MATCH, WRONG_MATCH, EXACT_MATCH]),
        ("SKILL", "SHIMS", [EXACT_MATCH, WRONG_MATCH, EXACT_MATCH, WRONG_MATCH, WRONG_MATCH]),
        ("SKILL", "SILLY", [EXACT_MATCH, PARTIAL_MATCH, PARTIAL_MATCH, EXACT_MATCH, WRONG_MATCH]),
        ("SKILL", "SLICE", [EXACT_MATCH, PARTIAL_MATCH, EXACT_MATCH, WRONG_MATCH, WRONG_MATCH]),
    ])
    def test_tally_for_target_guess(self, target, guess, expected_result):
        self.assertEqual(expected_result, tally(target, guess))
    

    @parameterized.expand([
        ("FAVOR", "FOR", ValueError, "The length of guess is not 5"),
        ("FAVOR", "FERVER", ValueError, "The length of guess is not 5"),
        ("FAVOR", "F1O7E", ValueError, "There are non alphabetical letters")
    ])
    def test_tally_for_exceptions(self, target, guess, expected_exception, expected_message):
        with self.assertRaisesRegex(expected_exception, expected_message):
            tally(target, guess)
            

    @parameterized.expand([
        ("FAVOR", "FAVOR", [EXACT_MATCH] * 5, Status.WIN, "Amazing!", 0, 1),
        ("FAVOR", "FAVOR", [EXACT_MATCH] * 5, Status.WIN, "Splendid!", 1, 2),
        ("FAVOR", "FAVOR", [EXACT_MATCH] * 5, Status.WIN, "Awesome!", 2, 3),
        ("FAVOR", "FAVOR", [EXACT_MATCH] * 5, Status.WIN, "Yay!", 3, 4),
        ("FAVOR", "FAVOR", [EXACT_MATCH] * 5, Status.WIN, "Yay!", 4, 5),
        ("FAVOR", "FAVOR", [EXACT_MATCH] * 5, Status.WIN, "Yay!", 4, 5),
        ("FAVOR", "FAVOR", [EXACT_MATCH] * 5, Status.WIN, "Yay!", 5, 6),
        ("FAVOR", "FAVOR", [EXACT_MATCH] * 5, Status.LOSS, "It was FAVOR, better luck next time!", 6, 7),
        ("FAVOR", "TESTS", [WRONG_MATCH] * 5, Status.IN_PROGRESS, "", 0, 1),
        ("FAVOR", "TESTS", [WRONG_MATCH] * 5, Status.IN_PROGRESS, "", 1, 2),
        ("FAVOR", "TESTS", [WRONG_MATCH] * 5, Status.IN_PROGRESS, "", 2, 3),
        ("FAVOR", "TESTS", [WRONG_MATCH] * 5, Status.IN_PROGRESS, "", 3, 4),
        ("FAVOR", "TESTS", [WRONG_MATCH] * 5, Status.IN_PROGRESS, "", 4, 5),
        ("FAVOR", "TESTS", [WRONG_MATCH] * 5, Status.LOSS, "It was FAVOR, better luck next time!", 5, 6),
        ("FAVOR", "TESTS", [WRONG_MATCH] * 5, Status.LOSS, "It was FAVOR, better luck next time!", 7, 8),
        
    ])
    def test_play_for_target_guess(self, target, guess, expected_result, expexted_status, expected_message, current_attempt, expected_attempt): 
        self.assertEqual({PlayResponse.ATTEMPTS : expected_attempt,  
                          PlayResponse.TALLY_RESPONSE : expected_result, 
                          PlayResponse.GAME_STATUS : expexted_status, 
                          PlayResponse.MESSAGE : expected_message}, 
                         play(target, guess, current_attempt))


    def test_play_invalid_guess_on_first_attempt(self):
        with self.assertRaisesRegex(ValueError, "The length of guess is not 5"):
            play("FAVOR", "FOR", 0)


    def test_play_invalid_spelling_on_first_attempt(self):
        self.assertRaisesRegex(ValueError, "Not a word", play, "FAVOR", "FEVER", 0, lambda spelling_check_fail: False)
    

    def test_play_valid_spelling_on_first_attempt(self):
        self.assertEqual({PlayResponse.ATTEMPTS : 1,  
                          PlayResponse.TALLY_RESPONSE : [EXACT_MATCH, WRONG_MATCH, EXACT_MATCH, WRONG_MATCH, EXACT_MATCH], 
                          PlayResponse.GAME_STATUS : Status.IN_PROGRESS, 
                          PlayResponse.MESSAGE : ""}, 
                          play("FAVOR", "FEVER", 0, lambda spelling_check_success: True))
            

    def test_play_check_spelling_throws_exception(self):
        def spell_check_that_fails(word):
            raise ConnectionError("Network Error")
        
        self.assertRaisesRegex(ConnectionError, "Network Error", play, "FAVOR", "FEVER", 0, spell_check_that_fails)


if __name__ == '__main__': 
     unittest.main()
