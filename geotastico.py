#!/usr/bin/env python
# coding: utf-8

# In[1]:


import speech_recognition as sr
import os
import random

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import unidecode
from tkinter import *
from PIL import ImageTk,Image


# In[2]:


class Location:
    def __init__(self):
        self.country = None 
        self.city = None
        self.path = None


# In[3]:


def get_random_location(page,countries_dir_path, windows=False):
    if windows:
        separator = '\\'
    else:
        separator = '/'
    
    global location
    location = Location()
    path = countries_dir_path

    dir_content = os.listdir(path)
    countries = [i for i in dir_content if os.path.isdir(path + separator + i)]
    location.country = random.choice(countries)
    path += separator + location.country

    dir_content = os.listdir(path)
    cities = [i for i in dir_content if os.path.isdir(path + separator + i)]
    location.city = random.choice(cities)
    path += separator + location.city

    dir_content = os.listdir(path)
    locations = [i for i in dir_content if os.path.isfile(path + separator + i)]
    path += separator + random.choice(locations)
    location.path = path
        
    
    page.my_img = ImageTk.PhotoImage(Image.open(location.path))
    
    if page.my_label != None:
        page.my_label.configure(image=page.my_img)
        page.my_label.image = page.my_img

    return location


# In[4]:


def verify_guess(guess, location):
    return unidecode.unidecode(guess).lower() == location.country


# In[5]:


def record_guess():
    global sentence
    mic = sr.Recognizer()
    with sr.Microphone() as source:
        mic.adjust_for_ambient_noise(source)
        audio = mic.listen(source)
        
    try:
        sentence = mic.recognize_google(audio,language='pt-BR')
    except sr.UnknownValueError:
        sentence = "unknown"
        
    return sentence


# In[6]:


def record_and_verify_guess(controller,windows=False):
    record_guess()
    if verify_guess(sentence,location):
        global score
        score += 1
        get_random_location(controller.frames["PageOne"],countries_path, windows)
        controller.show_frame("PageOne")
    else:
        controller.frames["PageTwo"].label2.configure(text="A localização correta era: " + location.city + ", " + location.country)
        controller.frames["PageTwo"].label3.configure(text="Total de acertos: " + str(score))
        controller.show_frame("PageTwo")


# In[7]:


def reset_score():
    global score
    score = 0


# In[8]:


try:
    import tkinter as tk                # python 3
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk     # python 2
    import tkFont as tkfont  # python 2
    
countries_path = "paises"
win = True
score = 0

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Small Fonts', size=40, weight="bold")
        self.button_font = tkfont.Font(family='Small Fonts', size=20, weight="bold")#, slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Geotástico", font=controller.title_font)
        label.pack(side="top", fill="x", padx=500, pady=300)

        button1 = tk.Button(self, text="Jogar", font=controller.button_font,
                            command=lambda:[get_random_location(controller.frames["PageOne"],countries_path, windows=win),controller.show_frame("PageOne")])
        button2 = tk.Button(self, text="Sair", font=controller.button_font,
                            command=lambda: controller.destroy())
        button1.pack()
        button2.pack()

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Que país é esse?", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Gravar", font=controller.button_font,
                           command=lambda:record_and_verify_guess(controller, windows=win))
        button.pack()
        
        button = tk.Button(self, text="Voltar para o início", font=controller.button_font,
                           command=lambda:[reset_score(),controller.show_frame("StartPage")])
        button.pack()
        
        self.my_img = None
        self.my_label = None
        
        get_random_location(self, countries_path, windows=win)
        
        self.my_img = ImageTk.PhotoImage(Image.open(location.path))
        self.my_label = Label(self,image=self.my_img)
        self.my_label.pack()

        
        #panel.configure(image=img2)
        #panel.image = img2

class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label1 = tk.Label(self, text="Você errou!", font=controller.title_font)
        self.label1.pack(side="top", fill="x", pady=10)
        self.label2 = tk.Label(self, text="A localização correta era: " + location.city + ", " + location.country, font=controller.title_font)
        self.label2.pack(side="top", fill="x", pady=6)
        self.label3 = tk.Label(self, text="Total de acertos: " + str(score), font=controller.title_font)
        self.label3.pack(side="top", fill="x", pady=2)
        button = tk.Button(self, text="Voltar para o início", font=controller.button_font,
                           command=lambda:[reset_score(),controller.show_frame("StartPage")])
        button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()


# In[ ]:




