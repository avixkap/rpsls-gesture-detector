from tkinter import messagebox


def show_rules():
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
