#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import speech_recognition as sr
from location import Location

def get_random_location(countries_dir_path):
    location = Location()
    path = countries_dir_path

    dir_content = os.listdir(path)
    countries = [i for i in dir_content if os.path.isdir(i)]
    location.country = random.choice(countries)
    path += '/' + location.country

    dir_content = os.listdir(path)
    cities = [i for i in dir_content if os.path.isdir(i)]
    location.city = random.choice(cities)
    path += '/' + location.city

    dir_content = os.listdir(path)
    locations = [i for i in dir_content if os.path.isfile(i)]
    path += '/' + random.choice(locations)
    location.path = path

    return location

def record_guess():
    mic = sr.Recognizer()
    with sr.Microphone() as source:
        mic.adjust_for_ambient_noise(source)
        audio = mic.listen(source)
        
    try:
        sentence = mic.recognize_google(audio,language='pt-BR')
    except sr.UnkownValueError:
        sentence = "unknown"
        
    return sentence

def verify_guess(guess, location):
    return guess == location.country