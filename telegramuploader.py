import os
import requests
import time

token = ''
chatid = ''
api = 'https://api.telegram.org/bot'+token
doc = '/sendDocument'
photo = '/sendPhoto'
vid = '/sendVideo'
chid = '?chat_id='
cap = '&caption='


'''Story Uploader to Telegram''',


def sendFiles():
    askdir = str(input("Paste instagram stories path: "))
    os.chdir(askdir)
    count = 1
    for root, dirs, filenames in os.walk(os.getcwd()):
        for name in filenames:
            dirname = os.path.dirname(root+"/"+name)
            if (count % 10) == 0:
                time.sleep(4.47)

            with open("log.txt", "r+") as f:
                if name in f.read():
                    print(f"{name} already uploaded to telegram")
                else:

                    if name.endswith("jpg"):
                        with open(f"{dirname}/{name}", 'rb') as image:
                            url = f"{api}{photo}{chid}{chatid}{cap}{name}"
                            requests.post(url, files={'photo': image})
                        print(f"{name} was uploaded to telegram")
                        with open("log.txt", "a") as logimage:
                            logimage.write("\n"+name)
                        time.sleep(1.87)

                    elif name.endswith("mp4"):
                        with open(f"{dirname}/{name}", 'rb') as video:
                            url = f"{api}{vid}{chid}{chatid}{cap}{name}"
                            requests.post(url, files={'video': video})
                        print(f"{name} was uploaded to telegram")
                        with open("log.txt", "a") as logvideo:
                            logvideo.write("\n"+name)
                        time.sleep(1.87)

                    else:
                        if name == "log.txt":
                            pass
                        else:
                            with open(f"{dirname}/{name}", 'rb') as docm:
                                url = f"{api}{doc}{chid}{chatid}{cap}{name}"
                                requests.post(url, files={'document': docm})
                            print(f"{name} was uploaded to telegram")
                            with open("log.txt", "a") as logdoc:
                                logdoc.write("\n"+name)
                            time.sleep(1.87)
            count += 1


sendFiles()
