from evdev import InputDevice, categorize, ecodes, KeyEvent
import datetime, time, json
import sqlite3





letter_list = []
            
def start_record():
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY and event.value==KeyEvent.key_down:
            key = ecodes.KEY[event.code][4:]
            if key != 'ENTER':
                letter_list.append(key)
            else:
                card = ''.join(letter_list)
                save(card)
                letter_list.clear()


def save(card):
    with sqlite3.connect("/home/pi/sqlite3/cardrecord.db") as conn:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c = conn.cursor()
        c.execute("insert into record values ( ?, ?)", (card, time))
        conn.commit()


with open("/etc/cardReader.conf", 'r', encoding='utf8') as f:
    conf = json.load(f)
dev = InputDevice(conf["device"])
start_record()
