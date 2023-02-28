from time import sleep
from mkinf import sha256, timestamp2date
import sqlite3
import requests
import os
import sys
import inquirer


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
        self.token = "paste the token here"  # token
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
        chvalue = ''    # Paste a telegram chat id

        if chvalue:
            answer = f'id: {chvalue}'

        if not chvalue:
            # Send any message to the channel/group to detect a chat id !
            resp = self.r.json()
            chat = resp['result']

            dict_o = {}
            for i in range(len(chat)):
                try:
                    ids = chat[i]['my_chat_member']['chat']['id']
                    title = chat[i]['my_chat_member']['chat']['title']
                    dict_o.update({title: ids})
                except KeyError:
                    try:
                        ids = chat[i]['channel_post']['sender_chat']['id']
                        title = chat[i]['channel_post']['sender_chat']['title']
                        dict_o.update({title: ids})
                    except KeyError:
                        pass

            title_names = [name for name in dict_o.keys()]
            query = [
                inquirer.List(
                    'title',
                    message='Select the channel/group to upload the files',
                    choices=title_names
                ),
            ]
            answer = inquirer.prompt(query)['title']
            chvalue = str(dict_o[answer])

        abs_files = []
        ch_id = "?chat_id="+chvalue

        for root, dirs, filenames in os.walk(directory):
            for filename in filenames:
                dirname = os.path.dirname(root+"/"+filename)
                files = os.path.join(dirname, filename)
                abs_files.append(files)

        abs_files.sort(key=os.path.getmtime)
        for f in abs_files:
            t_name = os.path.splitext(f)[0]
            sub = f.split('\\')[-1]
            if self.db_check(sha256(f)) == 0:
                if os.path.isfile(t_name+".txt"):
                    with open(t_name+".txt", "r", encoding="utf-8") as c:
                        for line in c:
                            if not line:
                                break
                            sub = line
                if f.endswith('jpg'):
                    with open(f, 'rb') as image:
                        link = f"{self.api}{ph}{ch_id}{cp}{sub}"
                        print(f"{sub} is uploading to {answer}...")
                        requests.post(link, files={'photo': image})
                        print(f"{sub} was uploaded to telegram: {answer}")
                        self.db_insert(sha256(f), sub,
                                       timestamp2date())
                        sleep(1.89)
                elif f.endswith("mp4"):
                    with open(f, 'rb') as video:
                        link = f"{self.api}{vd}{ch_id}{cp}{sub}"
                        print(f"{sub} is uploading to {answer}...")
                        requests.post(link, files={'video': video})
                        print(f"{sub} was uploaded to telegram: {answer}")
                        self.db_insert(sha256(f), sub,
                                       timestamp2date())
                        sleep(1.89)
                else:
                    os.remove(f)
            else:
                print(f"{sub} already uploaded to telegram, " +
                      "Deleted !!")
                os.remove(f)
        self.dtb.close()


def main():
    cl = TelegramBasicUpload()
    cl.FileUpload('Instagram_Data')


if __name__ == '__main__':
    main()
