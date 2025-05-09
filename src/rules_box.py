from tkinter import messagebox

def show_rules():
    """
    Displays the rules of the 'Rock, Paper, Scissors, Lizard, Spock' game 
    in a Tkinter message box.

    This function opens an informational popup window that explains the 
    interactions between the different hand gestures in the extended 
    version of the classic game.

    Returns:
        None
    """
    rules_text = (
        "Rock crushes Scissors\n"
        "Scissors cuts Paper\n"
        "Paper covers Rock\n"
        "Rock crushes Lizard\n"
        "Lizard poisons Spock\n"
        "Spock smashes Scissors\n"
        "Scissors decapitates Lizard\n"
        "Lizard eats Paper\n"
        "Paper disproves Spock\n"
        "Spock vaporizes Rock"
    )
    messagebox.showinfo("Rules", rules_text)
