def game_round_result(player, computer, player_score, computer_score):
    """
    Determines the outcome of a Rock-Paper-Scissors-Lizard-Spock game round.

    Parameters:
    player (str): The player's choice. One of "Rock", "Paper", "Scissors", "Lizard", or "Spock".
    computer (str): The computer's choice. One of "Rock", "Paper", "Scissors", "Lizard", or "Spock".
    player_score (int): The current score of the player.
    computer_score (int): The current score of the computer.

    Returns:
    str: "Draw" if both choices are the same,
        "You Win" if the player's choice beats the computer's,
        "You Lose" otherwise.
    int: Updated player score.
    int: Updated computer score.

    Note:
    The game follows the extended rules:
    - Rock crushes Scissors and crushes Lizard
    - Paper covers Rock and disproves Spock
    - Scissors cuts Paper and decapitates Lizard
    - Lizard eats Paper and poisons Spock
    - Spock smashes Scissors and vaporizes Rock
    """
    winning_combinations = {
        "Rock": ["Scissors", "Lizard"],
        "Paper": ["Rock", "Spock"],
        "Scissors": ["Paper", "Lizard"],
        "Lizard": ["Spock", "Paper"],
        "Spock": ["Rock", "Scissors"],
    }

    if player == computer:
        return "Draw", player_score, computer_score
    elif computer in winning_combinations[player]:
        player_score += 1
        return "You Win", player_score, computer_score
    else:
        computer_score += 1
        return "You Lose", player_score, computer_score
