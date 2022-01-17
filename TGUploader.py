from time import sleep
from mkinf import sha256, timestamp2date
import sqlite3
import requests
import os
import sys
import re


class Database():
    def __init__(self, name='tGlog.db', directory=os.getcwd()):
        self.directory = directory
        self.name = name
        path = os.path.join(self.directory, self.name)
        self.dtb = sqlite3.connect(path)
        self.cur = self.dtb.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS UPFile'''
                         '''(file_sha256 text, file_name text,\
                             uploaded_time text)''')
        self.dtb.commit()

    def db_insert(self, fhash, name, time):
        self.cur.execute('''INSERT INTO UPFile VALUES (?,?,?)''',
                         [fhash, name, time])
        self.dtb.commit()

    def db_check(self, data):
        self.cur.execute('''SELECT * FROM UPFile WHERE file_sha256 = ?''',
                         [data])
        result = self.cur.fetchall()
        return len(result)


class TelegramBasicUpload(Database):

    def __init__(self):
        super().__init__()
        self.token = "enter token here"
        self.api = "https://api.telegram.org/bot"+self.token
        self.url = self.api+"/getUpdates"

        self.r = requests.get(self.url)
        if self.r.status_code == 404:
            print("ERROR:\nToken invalid (Line 38) or",
                  "no internet connection!!")
            sys.exit()

    def FileUpload(self, directory):
        ph = "/sendPhoto"
        vd = "/sendVideo"
        cp = "&caption="
        chvalue = ""    # Enter telegram chat id

        if not chvalue:
            resp = self.r.json()
            result = resp['result']
            regx = re.compile('-[0-9]+')
            values = regx.search(str(result))
            title = result[0]['message']['chat']['title']
            try:
                chvalue = values.group(0)
                print(f"Uploading to {title}...")
            except IndexError:
                print("Enter Telegram Chat ID (line 51)")
                sys.exit()

        ch_id = "?chat_id="+str(chvalue)
        for root, dirs, filenames in os.walk(directory):
            for filename in filenames:
                dirname = os.path.dirname(root+"/"+filename)
                files = os.path.join(dirname, filename)
                t_name = os.path.splitext(files)[0]

                sub = filename
                if self.db_check(sha256(files)) == 0:
                    if os.path.isfile(t_name+".txt"):
                        with open(t_name+".txt", "r", encoding="utf-8") as c:
                            for line in c:
                                if not line:
                                    break
                                sub = line
                    if filename.endswith('jpg'):
                        with open(files, 'rb') as image:
                            link = f"{self.api}{ph}{ch_id}{cp}{sub}"
                            requests.post(link, files={'photo': image})
                            print(f"{filename} was uploaded to telegram")
                            self.db_insert(sha256(files), filename,
                                           timestamp2date())
                            sleep(1.89)
                    elif filename.endswith("mp4"):
                        with open(files, 'rb') as video:
                            link = f"{self.api}{vd}{ch_id}{cp}{sub}"
                            requests.post(link, files={'video': video})
                            print(f"{filename} was uploaded to telegram")
                            self.db_insert(sha256(files), filename,
                                           timestamp2date())
                            sleep(1.89)
                    else:
                        os.remove(files)
                else:
                    print(f"{filename} already uploaded to telegram, " +
                          "Deleted !!")
                    os.remove(files)
        self.dtb.close()


def main():
    cl = TelegramBasicUpload()
    cl.FileUpload('Instagram_Data')


if __name__ == '__main__':
    main()
