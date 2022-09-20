from tkinter import *
import pandas
import random
from gtts import gTTS
import os
import playsound


BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    word_data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = word_data.to_dict(orient="records")


# CHANGE FLASH CARD--------------------------------
def next_card():
    language = "fr"
    global flip_timer, current_card
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_image, image=fg_image)
    canvas.itemconfig(language_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=current_card["French"], fill="black")

    window.after(100)
    audio_output = gTTS(text=current_card["French"], lang=language)
    audio_output.save("french_word.mp3")
    playsound.playsound("french_word.mp3", True)
    os.remove("french_word.mp3")

    flip_timer = window.after(3000, flip_card)


# FLIP THE CARD------------------------------------
def flip_card():
    language = "en"
    # word = canvas.itemcget(word_text, "text")
    canvas.itemconfig(language_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=current_card["English"], fill="white")
    canvas.itemconfig(card_image, image=bg_image)

    audio_output = gTTS(text=current_card["English"], lang=language)
    audio_output.save("english_word.mp3")
    playsound.playsound("english_word.mp3", True)
    os.remove("english_word.mp3")


# UPDATE THE LIST AND CREATE A FILE----------------
def check_known():
    # del english_list[index]
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)

    next_card()


# UI SETUP-----------------------------------------

window = Tk()
window.title = "Flash Card"
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

fg_image = PhotoImage(file="./images/card_front.png")
bg_image = PhotoImage(file="./images/card_back.png")

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_image = canvas.create_image(400, 263, image=fg_image)
language_text = canvas.create_text(400, 150, fill="black", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, fill="black", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

check_image = PhotoImage(file="./images/right.png")
cross_image = PhotoImage(file="./images/wrong.png")

known_btn = Button(image=check_image, command=check_known, highlightbackground=BACKGROUND_COLOR)
known_btn.grid(column=0, row=1)
unknown_btn = Button(image=cross_image, command=next_card, highlightbackground=BACKGROUND_COLOR)
unknown_btn.grid(column=1, row=1)

next_card()


window.mainloop()