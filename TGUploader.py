from time import sleep
import sqlite3
import requests
import os
import sys


tgdb = sqlite3.connect("tg_log.db")
cursor = tgdb.cursor()
z = {}


def db_create():
    cursor.execute('''CREATE TABLE IF NOT EXISTS Uploaded_Files'''
                   '''(file_name text)''')
    tgdb.commit()


db_create()


def db_insert(value):
    cursor.execute('''INSERT INTO Uploaded_Files VALUES (?)''', [value])
    tgdb.commit()


def db_check(data):
    cursor.execute('''SELECT * FROM Uploaded_Files WHERE file_name = ?''',
                   [data])
    result = cursor.fetchall()
    return len(result)


def upload(dirn):
    token = ""  # "telegram_bot_token"
    api = "https://api.telegram.org/bot"+token
    url = api+"/getUpdates"

    r = requests.get(url)
    if r.status_code == 404:
        print("ERROR:\nToken invalid or no internet connection!!")
        sys.exit()
    else:
        jr = r.json()
        r_list = jr['result']
        if len(r_list) > 1:
            for index in range(0, len(r_list)):
                try:
                    i = r_list[index]['message']['chat']['id']
                    title = r_list[index]['message']['chat']['title']
                    z[title] = i
                except KeyError:
                    pass
            print(z)
            channel_name = str(input("Enter the Channel Name: "))
            chid_value = z.get(channel_name)
        else:
            if len(r_list) == 0:
                print(" TIP:\nSend a message to group involved the bot ",
                      "or disable privacy mode using bot father")
                sys.exit()
            else:
                chid_value = r_list[0]['message']['chat']['id']

    ph = "/sendPhoto"
    vd = "/sendVideo"
    cp = "&caption="
    ch_id = "?chat_id="+str(chid_value)

    for root, dirs, filenames in os.walk(dirn):
        for filename in filenames:
            dirname = os.path.dirname(root+"/"+filename)
            if db_check(filename) == 0:
                if filename.endswith('jpg'):
                    with open(f"{dirname}/{filename}", 'rb') as image:
                        link = f"{api}{ph}{ch_id}{cp}{filename}"
                        requests.post(link, files={'photo': image})
                        print(f"{filename} was uploaded to telegram")
                        db_insert(filename)
                        sleep(1.87)
                elif filename.endswith("mp4"):
                    with open(f"{dirname}/{filename}", 'rb') as video:
                        link = f"{api}{vd}{ch_id}{cp}{filename}"
                        requests.post(link, files={'video': video})
                        print(f"{filename} was uploaded to telegram")
                        db_insert(filename)
                        sleep(1.87)
                else:
                    os.remove(dirname+"/"+filename)
            else:
                print(f"{filename} already uploaded to telegram, " +
                      "Deleted !!")
                os.remove(dirname+"/"+filename)


if __name__ == "__main__":
    tgdb.close()
