import os
from os import environ
from flask import Flask, request
import telebot
import json
import random
import time
from telebot import types

BOT_TOKEN = environ.get("BOT_TOKEN","")
bot = telebot.TeleBot(BOT_TOKEN)

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return '', 200

with open('pokemon_questions.json', 'r') as file:
    questions = json.load(file)

user_scores = {}

@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    button = types.InlineKeyboardButton(text="Source Code", url="https://github.com/aryanshar-bot/poke-quizbot") 
    markup.add(button)
    bot.send_message(message.chat.id, "Welcome to the Pokémon Quiz Bot! 🎮\n Send /quiz to start the quiz.\n For Source Code click button below don't forget to give star ⭐", reply_markup=markup)

@bot.message_handler(commands=['quiz'])
def handle_quiz(message):
    if message.chat.id in user_scores:
        bot.send_message(message.chat.id, "You already have an active session. Finish it to start a new one.")
    else:
        random.shuffle(questions)
        user_scores[message.chat.id] = {"score": 0, "question_index": 0}
        send_question(message.chat.id)


def send_question(chat_id):
    user_data = user_scores[chat_id]
    question_index = user_data["question_index"]
    
    if question_index < 10:  
        question_data = questions[question_index]
        question_text = question_data["question"]
        options = question_data["options"]
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        for option in options:
            button = types.InlineKeyboardButton(text=option, callback_data=option)
            markup.add(button)
        
        bot.send_message(chat_id, question_text, reply_markup=markup)
    else:
        end_session(chat_id)


def end_session(chat_id):
    score = user_scores[chat_id]["score"]
    markup = types.InlineKeyboardMarkup(row_width=2)
    button = types.InlineKeyboardButton(text="Share Bot", url="tg://msg_url?text=%40poke_quiz_bot%0A%0AHello%20I%20used%20this%20bot.%20It%27s%20a%20good%20for%20a%20Pokemon%20fan.%0AIt%20has%20multiple%20and%20interesting%20quizzes%20based%20on%20Pokemon%20show.%0AYou%20should%20try%20this%20too.%0A%40poke_quiz_bot") 
    markup.add(button)
    
    bot.send_message(chat_id, f"End of Quiz! Your score: {score}\n Send /quiz to start again", reply_markup=markup)
    del user_scores[chat_id]  

@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    chat_id = call.message.chat.id
    user_answer = call.data
    user_data = user_scores.get(chat_id)

    if user_data:
        question_index = user_data["question_index"]
        question_data = questions[question_index]
        correct_answer = question_data["answer"]

        if user_answer == correct_answer:
            bot.send_message(chat_id, "Congratulations! Your answer is correct.")
            user_data["score"] += 1
            time.sleep(2)
            bot.delete_message(chat_id, call.message.message_id)
        else:
            bot.send_message(chat_id, f"Sorry, the correct answer is {correct_answer}.")
            bot.delete_message(chat_id, call.message.message_id)
        user_data["question_index"] += 1
        
        send_question(chat_id)

bot.polling()


# Your other bot handlers and functions here...

if __name__ == '__main__':
    app.run(port=int(os.environ.get('PORT', 8000)))
