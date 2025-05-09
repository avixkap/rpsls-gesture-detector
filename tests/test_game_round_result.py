import unittest
from utils.game_round_result import game_round_result


class TestGameRoundResult(unittest.TestCase):
    # Test cases for the game_round_result function
    def test_draw(self):
        result, player_score, computer_score = game_round_result("Rock", "Rock", 0, 0)
        self.assertEqual(result, "Draw")
        self.assertEqual(player_score, 0)
        self.assertEqual(computer_score, 0)

    # Test cases for the game_round_result function with extended rules
    def test_player_wins(self):
        result, player_score, computer_score = game_round_result("Rock", "Scissors", 0, 0)
        self.assertEqual(result, "You Win")
        self.assertEqual(player_score, 1)
        self.assertEqual(computer_score, 0)

    # Test cases for the game_round_result function with extended rules
    def test_computer_wins(self):
        result, player_score, computer_score = game_round_result("Rock", "Paper", 0, 0)
        self.assertEqual(result, "You Lose")
        self.assertEqual(player_score, 0)
        self.assertEqual(computer_score, 1)

    # Test cases for the game_round_result function with extended rules
    def test_extended_rules_player_wins(self):
        result, player_score, computer_score = game_round_result("Lizard", "Spock", 0, 0)
        self.assertEqual(result, "You Win")
        self.assertEqual(player_score, 1)
        self.assertEqual(computer_score, 0)

    # Test cases for the game_round_result function with extended rules
    def test_extended_rules_computer_wins(self):
        result, player_score, computer_score = game_round_result("Spock", "Lizard", 0, 0)
        self.assertEqual(result, "You Lose")
        self.assertEqual(player_score, 0)
        self.assertEqual(computer_score, 1)