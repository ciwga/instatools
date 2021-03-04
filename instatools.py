import instaloader
import os
import re


'''
username :| userid -> to remember
user1 : x1xx6x8
user2: xx94xx5x
user3 : x9x7x2x4
'''


L = instaloader.Instaloader()


def login():
    try:
        L.login(username, password)  # "username", "password"
    except instaloader.exceptions.TwoFactorAuthRequiredException:
        while True:
            try:
                code = input("Enter 2FA verification code: ")
                L.two_factor_login(code)
                break
            except instaloader.exceptions.BadCredentialsException:
                pass


# Download with post comments or without
def askforComment():
    while True:
        ask = input("Do you wanna download the post comments? (y or n): ")
        if ask.lower() == "n":
            L.download_comments = False
            break
        elif ask.lower() == "y":
            L.download_comments = True
            break
        else:
            print("only write y or n")


# Download video thumbnails or doesn't
def vidthumbnails():
    while True:
        vid = input("Do you wanna download the video thumbnails? (y or n): ")
        if vid.lower() == "n":
            L.download_video_thumbnails = False
            break
        elif vid.lower() == "y":
            L.download_video_thumbnails = True
            break
        else:
            print("only write y or n")


# Download post geotags or doesn't
def postgeo():
    while True:
        pgeo = input("Do you wanna download the post geotags? (y or n): ")
        if pgeo.lower() == "n":
            L.download_geotags = False
            break
        elif pgeo.lower() == "y":
            L.download_geotags = True
            break
        else:
            print("only write y or n")


# Make a directory
def mkdir():
    dirname = str(input("Enter the directory name: "))
    try:
        os.mkdir(dirname)
        os.chdir(dirname)
    except FileExistsError:
        os.chdir(dirname)


# Change the filename and dirname for posts
def postdirDownloader(obj):
    L.filename_pattern = f"{obj.profile}_""{date_utc}_UTC"
    L.download_post(obj, target=obj.profile)


# Change the filename and dirname for stories
def storyDownloader(object):
    L.filename_pattern = f"{object.owner_username}_""{date_utc}_UTC"
    L.download_storyitem(object, f"{object.owner_username}")


# Find out someone who unfollowed you
def unfollowers(getname):
    profile = instaloader.Profile.from_username(L.context, getname)
    followers = set(profile.get_followers())
    following = set(profile.get_followees())
    noback = following - followers
    for unfollower in noback:
        print(unfollower.username)


# Download specific stories from an instagram id
def specificStoryDownloader(*instaid):
    mkdir()
    vidthumbnails()
    L.download_stories(userids=(instaid), filename_target=None)


# Find out an instagram id from an instagram username
def getinstaid(instaname):
    L.check_profile_id(instaname)


# Download all people's stories you followed
def ownstories():
    mkdir()
    vidthumbnails()
    for story in L.get_stories():
        for item in story.get_items():
            storyDownloader(item)


# Download all posts of an instagram profile
def postDownloader(username):
    askforComment()
    vidthumbnails()
    postgeo()
    posts = instaloader.Profile.from_username(L.context, username).get_posts()
    for post in posts:
        postdirDownloader(post)


# Download a post, reel or igtv from a link
def singlepostDownloader():
    askforComment()
    vidthumbnails()
    postgeo()
    url = str(input("Paste the link: "))
    regcode = re.compile("(p|l|v)/([0-9]|[a-z]|[A-Z])+.*./")
    spanLocation = [i for i in regcode.search(url).span()]
    spoint = spanLocation[0]+2
    epoint = spanLocation[1]-1
    shortcode = url[spoint:epoint]
    singlepost = instaloader.Post.from_shortcode(L.context, shortcode)
    postdirDownloader(singlepost)


# Download highlights from an instagram user id
def highlightsDownloader(igid):
    mkdir()
    vidthumbnails()
    for highlight in L.get_highlights(igid):
        for item in highlight.get_items():
            L.filename_pattern = f"{highlight.owner_username}_""{date_utc}_UTC"
            L.download_storyitem(item, f'{highlight.title}')


# Get suggested profiles from profile
def similarProfile(simname):
    profile = instaloader.Profile.from_username(L.context, simname)
    for profiles in profile.get_similar_accounts():
        print(profiles.username)


# Get profile photo url from someone's instagram profile
def propicUrl(picname):
    profile = instaloader.Profile.from_username(L.context, picname)
    src = profile.profile_pic_url
    print(src)


# Download your instagram saved media
def savedMedia(yourusername):
    mkdir()
    askforComment()
    vidthumbnails()
    postgeo()
    profile = instaloader.Profile.from_username(L.context, yourusername)
    for media in profile.get_saved_posts():
        postdirDownloader(media)


# unfollowers(getusername)
# specificStoryDownloader(xxx784, x85xxx47)
# getinstaid(username)
# ownstories()
# postDownloader(username)
# singlepostDownloader()
# highlightsDownloader(igid)
# similarProfile(simname)
# propicUrl(picname)
# savedMedia(yourusername)


def main():
    print(
          " 1. Unfollowers\n",
          "2. Download stories for a specific instagram profile\n",
          "3. Find Instagram id of a profile\n",
          "4. Download instagram stories you followed\n",
          "5. Download all posts of an instagram profile\n",
          "6. Download a post from a link\n",
          "7. Download highlights of an instagram profile\n",
          "8. Download profile picture of an instagram account\n",
          "9. Download your saved posts"
          )

    choose = int(input("What would you like, write a number: "))
    if choose == 1:
        login()
        unfusername = str(input("Write an username: "))
        unfollowers(unfusername)
    elif choose == 2:
        login()
        storyid = int(input("Paste an instagram id: "))
        specificStoryDownloader(storyid)
    elif choose == 3:
        userigid = str(input("Write an instagram username: "))
        getinstaid(userigid)
    elif choose == 4:
        login()
        ownstories()
    elif choose == 5:
        postusername = str(input("Write an instagram username: "))
        try:
            postDownloader(postusername)
        except instaloader.exceptions.LoginRequiredException:
            login()
            postDownloader(postusername)
    elif choose == 6:
        oddpost = str(input("Write an instagram username: "))
        try:
            singlepostDownloader(oddpost)
        except instaloader.exceptions.LoginRequiredException:
            login()
            singlepostDownloader(oddpost)
    elif choose == 7:
        login()
        highlightid = int(input("Paste an instagram id of profile: "))
        highlightsDownloader(highlightid)
    elif choose == 8:
        profilephoto = str(input("Write an intagram username: "))
        propicUrl(profilephoto)
    elif choose == 9:
        login()
        yoursaved = str(input("What is your instagram username: "))
        savedMedia(yoursaved)
    else:
        print("Enter a valid number")


main()
