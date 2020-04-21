# -*- coding: utf-8 -*-

from tkinter import *
import tkinter as tk
from convert import romgan
from convert import ganrom
import os

root = Tk()
root.geometry("400x400")

hiraganaVar = tk.IntVar()

isHiragana = 0


def set_hiragana():
    global isHiragana
    isHiragana = 1


def set_romaji():
    global isHiragana
    isHiragana = 0


romajiButton = Radiobutton(root, variable=hiraganaVar, value=0, text="Romaji -> Hiragana", command=set_romaji)
hiraganaButton = Radiobutton(root, variable=hiraganaVar, value=1, text="Hiragana -> Romaji", command=set_hiragana)
romajiButton.pack()
hiraganaButton.pack()

inputLabel = Label(root, text="Input Text")
inputLabel.pack()


inputEntry = Entry(root)
inputEntry.pack()


def convert_on_click():
    if isHiragana == 0:
        text_output = romgan(inputEntry.get())
        output_text = Text(root, height=1)
        output_text.insert(1.0, text_output)
        output_text.pack()
        output_text.configure(bg=root.cget('bg'), relief="flat")
        output_text.configure(state="disabled")
    else:
        text_output = ganrom(inputEntry.get())
        output_text = Text(root, height=1)
        output_text.insert(1.0, text_output)
        output_text.pack()
        output_text.configure(bg=root.cget('bg'), relief="flat")
        output_text.configure(state="disabled")


convertButton = Button(root, text="Convert", command=convert_on_click)
convertButton.pack()

outputLabel = Label(root, text="Output Text")
outputLabel.pack()

root.mainloop()
