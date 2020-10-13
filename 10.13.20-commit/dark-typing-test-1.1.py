#!/usr/bin/python3
import random
import decimal
import time
from time import sleep
import PySimpleGUI as sg
decimal.getcontext().rounding = decimal.ROUND_DOWN


dark_quotes = ["A man lives three lives. The first one ends with the loss of naivety, the second, with the loss of innocence and the third... with the loss of life itself. It's inevitable that we go through all three stages.", "We're not free in what we do, because we're not free in what we want. We can't overcome what's deep within us.",
"The distinction between past, present and future is only a stubbornly persistent illusion", "Only when we've freed ourselves of emotion can we be truly free. Only when you're willing to sacrifice what you hold dearest.", "There are moments when we must understand that the decisions we make influence more than just our own fates.",
"Man is a strange creature. All his actions are motivated by desire, his character forged by pain. As much as he may try to suppress that pain, to repress the desire, he cannot free himself from the eternal servitude to his feelings. For as long as the storm rages within him, he cannot find peace. Not in life, not in death. And so he will do what he must, day in, day out. The pain is his vessel, desire his compass. It is all that man is capable of.",
"No matter how much we fight it we are connected by our blood. We can feel estranged from our families and not understand what they do. And still, in the end we will do anything for them.", "Black holes are considered to be the hellmouths of the universe. Those who fall inside disappear. Forever. But where to? What lies behind a black hole? Along with things, do space and time also vanish there? Or would space and time be tied together and be part of an endless cycle? What if everything that came from the past were influenced by the future?", "Have you heard of Master Zhuang's paradox? 'I dreamt I was a butterfly. Now I've woken up and I no longer know if I'm a person who dreamed he's a butterfly or if I’m a butterfly who's dreaming it's a person.", "We trust that time is linear. That it proceeds eternally, uniformly. Into infinity. But the distinction between past, present and future is nothing but an illusion. Yesterday, today and tomorrow are not consecutive, they are connected in a never-ending circle. Everything is connected.", "The distinction between past, present and future is only a stubbornly persistent illusion - Albert Einstein.", "What we know is a drop, what we don't know is an ocean", "And so we all die alike. No matter into which house we are born. No matter which gown. Whether we grace the earth briefly or for a long time. I alone tie my bonds. Whether I have extended hands or slapped them. We all face the same end. Those above have long forgotten us. They do not judge us. In death, I am all alone. And my only judge is me.", "Our thinking is shaped by dualism. Entrance, exit. Black, white. Good, evil. Everything appears as opposite pairs. But that's wrong.", "Now I have another Grandma, and she's the principal of my school. Her husband, who's fucking my mom, is looking for his son, who's my father! A few days ago I kissed my Aunt! And the crazy thing is... there's nothing wrong with any of them. They're okay. I'm what's wrong! I just want everything to go back to normal."]


def the_gui():
    global total_raw 
    total_raw = 0
    global total_net 
    total_net = 0
    global finish_push_ct
    finish_push_ct = 0
    sg.theme('Dark Blue 2')

    layout = [
              [sg.Multiline(size=(80, 6), font=20, default_text='Your quote will appear when you click Start Test', key='quote_output')],
              [sg.Multiline(size=(80, 6), font=20, do_not_clear=True, enter_submits=True, key='text_input')],
              [sg.Text(key='raw', font=12, size=(80, 6))],
              [sg.Button('Start Test', size=(13, 3), font=30), sg.Text(' ' *  48), sg.Button('Finish Test', size=(15, 3), font=30, bind_return_key=True), sg.Text(' ' * 47), sg.Button('Exit', size=(13, 3), font=30)]
              ]

    window = sg.Window('Dark Netflix Typing Test', layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == 'Start Test':
            random_quote = random.choice(dark_quotes)
            window['quote_output'].update(random_quote)
            window['text_input'].update('')
            window['text_input'].SetFocus()
            global start 
            start = decimal.Decimal(time.time())
        elif event == 'Finish Test':
            finish_push_ct += 1
            global decimal_time 
            decimal_time = decimal.Decimal(time.time()) - start
            global rounded_time 
            rounded_time = round(decimal_time, 2)
            words_list = random_quote.split()
            input_string = str(values['text_input'])
            input_list = input_string.split()
            for i in range(len(words_list) - len(input_list)):
                input_list.append('')
            correct_ct, incorrect_ct, incorrect_l, raw_wp, net_wp = stats(words_list, input_list)
            if len(incorrect_l) > 5:
                incorrect_l = incorrect_l[0:3]
                incorrect_l.append(' + {} others.'.format(incorrect_ct-3))
                incorrect_string = ', '.join(incorrect_l)
            total_raw += raw_wp
            raw_average = average(total_raw)
            total_net += net_wp
            net_average = average(total_net)
            window['raw'].update('Length of sample: {}s\nNumber of correct words: {}\nNumber of incorrect words: {}\nIncorrect words: {}\nRaw WPM: {}     Average: {}\nNet WPM: {}     Average: {}'.format(rounded_time, correct_ct, incorrect_ct, incorrect_string, raw_wp, raw_average, net_wp, net_average))
    window.close()


def stats(words_list, input_list):
    #incorrect/correct word calculations
    i = 0
    correct_count = 0
    correct_list = []
    incorrect_count = 0
    incorrect_list = []
    for word in words_list:
        if word == input_list[i]:
            correct_list.append(word)
            correct_count += 1
            i += 1
        else:
            incorrect_list.append(word)
            incorrect_count += 1
            i += 1

    #wpm calculations
    time_in_mins = float(decimal_time) / 60
    raw_character_count = 0
    for i in input_list:
        raw_character_count += len(i)
    raw_wpm = round(((raw_character_count / 5) / time_in_mins), 2)
    error_rate = incorrect_count / time_in_mins
    net_wpm = round((raw_wpm - error_rate), 2)

    return correct_count, incorrect_count, incorrect_list, raw_wpm, net_wpm


def average(inp):
    ave = inp / finish_push_ct
    return ave


if __name__ == '__main__':
    the_gui()
    print('Exiting Program')
