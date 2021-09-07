#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import speech_recognition as sr

def get_random_location(countries_dir_path):
    location_path = countries_dir_path

    dir_content = os.listdir(location_path)
    countries = [i for i in dir_content if os.path.isdir(i)]
    country = random.choice(countries)
    location_path += '/' + country

    dir_content = os.listdir(location_path)
    cities = [i for i in dir_content if os.path.isdir(i)]
    city = random.choice(cities)
    location_path += '/' + city

    dir_content = os.listdir(location_path)
    locations = [i for i in dir_content if os.path.isfile(i)]
    location = random.choice(locations)
    location_path += '/' + location

    return [country, city, location_path]

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

def verify_guess(guess, country):
    return guess == country