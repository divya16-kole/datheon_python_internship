import random

# ==========================================
# HANGMAN - WORD GUESSING GAME
# Datheon Python Internship | Task 1
# ==========================================

WORDS = [
    "python", "computer", "programming", "developer",
    "college", "student", "keyboard", "internet",
    "function", "variable", "database", "software",
    "algorithm", "project", "machine"
]

MAX_ATTEMPTS = 6

HANGMAN_STAGES = [
    r"""
       +---+
       |   |
           |
           |
           |
      =========
    """,
    r"""
       +---+
       |   |
       O   |
           |
           |
      =========
    """,
    r"""
       +---+
       |   |
       O   |
       |   |
           |
      =========
    """,
    r"""
       +---+
       |   |
       O   |
      /|   |
           |
      =========
    """,
    r"""
       +---+
       |   |
       O   |
      /|\  |
           |
      =========
    """,
    r"""
       +---+
       |   |
       O   |
      /|\  |
      /    |
      =========
    """,
    r"""
       +---+
       |   |
       O   |
      /|\  |
      / \  |
      =========
    """
]


def display_header():
    """Display the game title and instructions."""
    print("\n" + "=" * 42)
    print("       H A N G M A N   C H A L L E N G E")
    print("=" * 42)
    print(" Guess the hidden word one letter at a time!")
    print(f" You have {MAX_ATTEMPTS} incorrect guesses allowed.")
    print(" Type 'quit' anytime to leave the game.")
    print("=" * 42)


def display_word(secret_word, guessed_letters):
    """Show guessed letters and blanks for hidden letters."""
    return " ".join(
        letter.upper() if letter in guessed_letters else "_"
        for letter in secret_word
    )


def get_guess(guessed_letters):
    """Get and validate a single-letter guess."""
    while True:
        guess = input("\n  Enter a letter: ").strip().lower()

        if guess == "quit":
            return None

        if len(guess) != 1 or not guess.isalpha() or not guess.isascii():
            print("  Please enter one English letter (A-Z).")
            continue

        if guess in guessed_letters:
            print(f"  You already guessed '{guess.upper()}'. Try another!")
            continue

        return guess


def play_round():
    """Run one complete round of Hangman."""
    secret_word = random.choice(WORDS)
    guessed_letters = set()
    wrong_guesses = 0

    while wrong_guesses < MAX_ATTEMPTS:
        print("\n" + "-" * 42)
        print(HANGMAN_STAGES[wrong_guesses])
        print("  WORD:     ", display_word(secret_word, guessed_letters))
        print(
            f"  ATTEMPTS: {MAX_ATTEMPTS - wrong_guesses}"
            f" / {MAX_ATTEMPTS}"
        )

        guessed_display = (
            ", ".join(sorted(letter.upper() for letter in guessed_letters))
            if guessed_letters else "None yet"
        )
        print("  GUESSED:  ", guessed_display)

        if all(letter in guessed_letters for letter in secret_word):
            print("\n" + "=" * 42)
            print("       CONGRATULATIONS! YOU WON!")
            print(f"       The word was: {secret_word.upper()}")
            print("=" * 42)
            return True

        guess = get_guess(guessed_letters)

        if guess is None:
            print("\n  You left the round. See you next time!")
            return None

        guessed_letters.add(guess)

        if guess in secret_word:
            print(f"  Correct! '{guess.upper()}' is in the word.")
        else:
            wrong_guesses += 1
            print(f"  Oops! '{guess.upper()}' is not in the word.")

    print("\n" + "-" * 42)
    print(HANGMAN_STAGES[MAX_ATTEMPTS])
    print("       GAME OVER!")
    print(f"       The word was: {secret_word.upper()}")
    print("-" * 42)
    return False


def main():
    """Start the game and offer replay."""
    display_header()

    wins = 0
    rounds = 0

    while True:
        result = play_round()

        if result is None:
            break

        rounds += 1
        if result:
            wins += 1

        print(f"\n  YOUR SCORE: {wins} win(s) in {rounds} round(s)")

        while True:
            choice = input("\n  Play again? (yes/no): ").strip().lower()

            if choice in ("yes", "y"):
                break
            elif choice in ("no", "n", "quit"):
                print("\n  Thanks for playing Hangman!")
                print("  Keep learning. Keep coding. Goodbye!\n")
                return
            else:
                print("  Please enter yes or no.")


if __name__ == "__main__":
    main()