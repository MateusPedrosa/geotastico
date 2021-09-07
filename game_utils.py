#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import speech_recognition as sr
from location import Location
from dtw import *

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

# codebook: dictionary {'country': array}
def recognize_guess(query, codebook):
    threshold = 100
    min_d = None
    for key, value in codebook.items():
        distance = dtw(query, value)
        if min_d == None or distance < min_d:
            min_d = distance
            country = key

    if min_d > threshold:
        # guessed country is not on codebook
        return None

    return country