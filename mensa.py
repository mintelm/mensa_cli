#!/bin/python3

import requests
import json
import os
import datetime

API = 'https://app.mensaplan.de/api/11102/de.mensaplan.app.android.regensburg/reg7.json'
TERM_WIDTH = 80 if int(os.popen('stty size', 'r').read().split()[1]) > 80 else \
                    int(os.popen('stty size', 'r').read().split()[1])

request = requests.get(API)

menus = json.loads(request.content)['days']
dt_string = datetime.datetime.now().strftime('%d.%m.%Y')

# check if first menu has todays date
if (dt_string != menus[0]['date'][5:]):
    del menus[0]

print(TERM_WIDTH * '-')
for menu in menus:
    print(menu['date'] + ' |\n' + (len(menu['date']) + 2) * '-')
    for category in menu['categories']:
        if 'name' not in category:
            print('no meals today... maybe holiday?')
            continue
        print(5 * '*', category['name'], 5 * '*')
        for meal in category['meals']:
            meal_formated = meal['name'].replace('\xad', '')
            print(meal_formated, end='')
            # align price to the end of line (price is always 5 characters)
            for _ in range(TERM_WIDTH - len(meal_formated) - 5):
                print(' ', end='')
            print(format(meal['pricing']['for'][0] / 100, '.2f'), end='€\n')
        if category != menu['categories'][-1]:
            print()
    print(TERM_WIDTH * '-')
