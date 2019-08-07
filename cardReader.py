from evdev import InputDevice, categorize, ecodes, KeyEvent
import datetime, threading, time
import smtplib, ssl
import sqlite3

dev = InputDevice('/dev/input/by-id/usb-Interflex_Datensysteme_GmbH_COKG_IF72_USB-RS232_Reader_01490489-event-kbd')

letter_list = []

class keyboard(threading.Thread):
    def __init__(self, thread_id, name):
        threading.Thread.__init__(self)
        self.thread_id=thread_id
        self.name=name

    def run(self):
        start_record()
            
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
                #print(card_list)

def save(card):
    with sqlite3.connect("/home/pi/sqlite3/cardrecord.db") as conn:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c = conn.cursor()
        c.execute("insert into record values ( ?, ?)", (card, time))
        conn.commit()

def mail():
    toaddrs = "kirk.lu@wacker.com"
    server = smtplib.SMTP("smtp.office365.com", 587)
    user = "pisender11121@outlook.com"
    password = "!QAZ2wsx3edc"

    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(user, password)
    
def mail(recipient_list, subject, body):
    server = smtplib.SMTP("smtp.office365.com", 587)
    user = "pisender11121@outlook.com"
    password = "!QAZ2wsx3edc"
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(user, password)
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = ", ".join(recipient_list)
    server.sendmail(user, recipient_list, msg.as_string())
    print("done")
    server.close()

        
if __name__ == "__main__":
    thread1 = keyboard(1,"keyboard1")
    thread1.start()
    print("ok")
    while 1:
        cmd=input("input:")
        if cmd == "showcard":
            print(card_list)
        if cmd == "showletter":
            print(letter_list)
        if cmd == "mail":
            print("mail send")
