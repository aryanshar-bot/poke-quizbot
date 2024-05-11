# Pokemon Quiz Bot for Telegram

## Overview

This is a simple Telegram bot created by [Aryan](https://github.com/aryanshar-bot) that quizzes users on their knowledge of the Pokemon series. The bot asks questions related to the Pokemon show and displays the user's score at the end of the quiz.

## Features

- Randomly selects questions from a JSON database.
- Displays the user's score at the end of the quiz.
- Supports multiple-choice questions.
- Easy to deploy and integrate with Telegram.

## Requirements

- Python 3.9+
- Python Telegram Bot library

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/aryanshar-bot/poke-quizbot.git
    ```

2. Install the required dependencies:

    ```bash
    pip install telebot
    ```

3. Obtain a Telegram bot token from the BotFather and replace `"YOUR_TOKEN"` in `main.py` with your token.

4. Run the bot:

    ```bash
    python main.py
    ```

## Usage

1. Start the bot by searching for its username on Telegram or clicking on the provided link.
2. Start the quiz by sending the command `/start`.
3. Send /quiz to start the quiz
3. Answer the questions by selecting the correct option.
4. Once all questions are answered, the bot will display your score.

## Contributing

Contributions are welcome! If you have any ideas for new features or improvements, feel free to open an issue or submit a pull request.
