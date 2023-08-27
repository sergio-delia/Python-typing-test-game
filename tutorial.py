import curses
from curses import wrapper
import time
import random

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Welcome to the Speed Typing Test!")
    stdscr.addstr("\nPress any key to begin!")
    stdscr.refresh()
    stdscr.getkey()




def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM: {wpm}")

    for i, char in enumerate(current): #La funzione enumerate non fa altro che incrementare la i per ogni elemento in current_text come un indice
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)
        stdscr.addstr(0, i, char, color)


def load_test():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip() #strip serve per rimuovere il carattere invisibile \n che manda a capo le frasi nel file text.txt


def wpm_test(stdscr):
    target_text = load_test()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True) #Questo serve per dire al codice di non bloccarsi quando c'è il key = stdscr.getkey(). Solo che ora per non creare l'errore è necessario usare il try except

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)
        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text: #current_text è una lista ['h','e','l','l','o']. Join trasforma la lista in stringa usando ciò che c'è tra virgolette come separatore (in questo caso niente)
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if(ord(key) == 27):
            break

        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif(len(current_text) < len(target_text)):
            current_text.append(key)







def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) #Si associa a 1 il testo color verde e il background nero
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    #stdscr.clear()
    #stdscr.addstr(1, 5, "Hello world!", curses.color_pair(1)) # Partirà da 1 riga sotto, 5 caratteri a destra e con la configurazione di colori 1
    #stdscr.addstr(0, 0, "Hello world!")
    #stdscr.refresh()
    #key = stdscr.getkey()
    #print(key)

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(2, 0, "You completed the text! Press any key to continue...")
        key = stdscr.getkey()
        if ord(key) == 27:
            break


wrapper(main)