import random


greetings = [
    "Hello",
    "Bonjour",
    "Guten Tag",
    "Hola",
    "Ciao",
    "Olá",
    "Dzień dobry",
    "Привіт",
    "Geia sou",
    "Hej",
    "Nǐ hǎo",
    "Konnichiwa",
    "안녕하세요",
    "नमस्ते",
    "Merhaba",
    "Aloha",
    "Salem",
    "Góðan dag",
    "Прывітанне",
    "Привет"
]


def say_hello():
    return random.choice(greetings)
