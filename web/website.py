from flask import Flask, render_template, request
from datetime import datetime, timedelta
from time import sleep
import sqlite3, subprocess, evdev, json

app =  Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def show_data():
    if request.method == 'GET':
        start_date = datetime.now().strftime("%Y-%m-%d")
        end_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        start_date = request.form['start_date']
        end_date = request.form['end_date']
    title = "CardReader"
    table = read(start_date, end_date)
    service_status = check_cardreader_service()
    device_list = list_input_device()
    page = render_template("index.html", title=title, table=table,
                           start_date_value=start_date, end_date_value=end_date,
                           status=service_status, device_list=device_list)
    return page


@app.route('/start_service', methods=['POST'])
def start_cardreader_service():
    try:
        subprocess.check_output(['sudo','systemctl', 'start', 'cardReader.service'])
        sleep(1)
        return check_cardreader_service()
    except Exception as err:
        return str(err)


@app.route('/stop_service', methods=['POST'])
def stop_cardreader_service():
    try:
        subprocess.check_output(['sudo','systemctl', 'stop', 'cardReader.service'])
        return "Stopped"
    except Exception as err:
        return str(err)

@app.route('/set_device', methods=['POST'])
def set_device():
    device_path = request.form['device_path']
    filename = "/etc/cardReader.conf"
    try:
        conf = read_conf_file(filename)
    except:
        conf = {}
    conf["device"] = device_path
    write_conf_file(filename, conf)
    stop_cardreader_service()
    sleep(1)
    start_cardreader_service()
    return "OK"


def check_cardreader_service():
    try:
        output = subprocess.check_output(['sudo', 'systemctl', 'is-active', 'cardReader.service']).decode("utf-8")[:-1]
        if output == "active":
            return "Running"
        else:
            return "Stopped"
    except:
        return "Stopped"


def read_conf_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def write_conf_file(filename, content):
    with open(filename, 'w') as f:
        f.write(json.dumps(content))


def read_today():
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    return read(today, tomorrow)

        
def read(start_date, end_date):
    rows = []
    with sqlite3.connect("/home/pi/sqlite3/cardrecord.db") as conn:
        c = conn.cursor()
        for row in c.execute("select * from record where time between ? and ?", (start_date, end_date)):
            rows.append("<tr><td>"+'</td><td>'.join(row)+"</td></tr>")
        return ''.join(rows)


def list_input_device():
    output = ""
    print(evdev.list_devices())
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        output = output + "<option value=\"%s\">%s</options>" % (device.path, device.name)
    return output
        



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
