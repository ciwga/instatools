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
                    try:
                        i = r_list[index]['channel_post']['chat']['id']
                        title = r_list[index]['channel_post']['chat']['title']
                        z[title] = i
                    except KeyError:
                        pass
            if z is None:
                print("Send a message to channel/group and try again!!")
                sys.exit()
            print(z)
            channel_name = str(input("Enter the Channel/Group Name: "))
            chid_value = z.get(channel_name)
        else:
            if len(r_list) == 0:
                print(" TIP:\nSend a message to group involved the bot ",
                      "or disable privacy mode using bot father")
                sys.exit()
            else:
                try:
                    chid_value = r_list[0]['message']['chat']['id']
                except KeyError:
                    chid_value = r_list[0]['channel_post']['chat']['id']

    ph = "/sendPhoto"
    vd = "/sendVideo"
    cp = "&caption="
    ch_id = "?chat_id="+str(chid_value)

    for root, dirs, filenames in os.walk(dirn):
        for filename in filenames:
            dirname = os.path.dirname(root+"/"+filename)
            t_name = os.path.splitext(dirname+"/"+filename)[0]
            sub = filename
            if db_check(filename) == 0:
                if os.path.isfile(t_name+".txt"):
                    with open(t_name+".txt", "r", encoding="utf-8") as c:
                        for line in c:
                            if not line:
                                break
                            sub = line
                if filename.endswith('jpg'):
                    with open(f"{dirname}/{filename}", 'rb') as image:
                        link = f"{api}{ph}{ch_id}{cp}{sub}"
                        requests.post(link, files={'photo': image})
                        print(f"{filename} was uploaded to telegram")
                        db_insert(filename)
                        sleep(1.89)
                elif filename.endswith("mp4"):
                    with open(f"{dirname}/{filename}", 'rb') as video:
                        link = f"{api}{vd}{ch_id}{cp}{sub}"
                        requests.post(link, files={'video': video})
                        print(f"{filename} was uploaded to telegram")
                        db_insert(filename)
                        sleep(1.89)
                else:
                    os.remove(dirname+"/"+filename)
            else:
                print(f"{filename} already uploaded to telegram, " +
                      "Deleted !!")
                os.remove(dirname+"/"+filename)


if __name__ == "__main__":
    tgdb.close()
