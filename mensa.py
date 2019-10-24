#!/bin/python3

import requests
import json
import os

API = 'https://app.mensaplan.de/api/11102/de.mensaplan.app.android.regensburg/reg7.json'
TERM_WIDTH = 80 if int(os.popen('stty size', 'r').read().split()[1]) > 80 else \
                    int(os.popen('stty size', 'r').read().split()[1])

def print_div():
    for _ in range(TERM_WIDTH):
        print('-', end='')
    print()

def print_date(date):
    print(date, '|')
    for _ in range(len(date) + 1):
        print('-', end='')
    print()

def print_category(category):
    print(category['name'])
    for meal in category['meals']:
        meal_formated = meal['name'].replace('\xad', '')
        print(meal_formated, end='')
        # align price to the end of line (price is always 5 characters)
        for _ in range(TERM_WIDTH - len(meal_formated) - 5):
            print(' ', end='')
        print(format(meal['pricing']['for'][0] / 100, '.2f'), end='€\n')
    if category != menu['categories'][-1]:
        print()

request = requests.get(API)

menu = json.loads(request.content)
week_menu = menu['days']
del week_menu[0]

print_div()
for menu in week_menu:
    print_date(menu['date'])
    for category in menu['categories']:
        print_category(category)
    print_div()
