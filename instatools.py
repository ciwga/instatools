from time import sleep
from TGUploader import upload
import instaloader
import os
import re

dirname = os.path.dirname(os.path.abspath(__file__))
os.chdir(dirname)
try:
    os.mkdir("Instagram_Data")
except FileExistsError:
    pass

os.chdir(os.path.join(dirname, "Instagram_Data"))
L = instaloader.Instaloader()
L.iphone_support = False  # faster download, lower quality
L.download_video_thumbnails = False
# L.download_geotags = True
# L.download_comments = True


def cleaner():
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")


def usr():
    user = input("What is the username: ")
    return user


# taken from instaloader source code
def login():
    try:
        L.login("", "")  # "username", "password"
    except instaloader.exceptions.TwoFactorAuthRequiredException:
        while True:
            try:
                code = input("Enter 2FA verification code: ")
                L.two_factor_login(code)
                break
            except instaloader.exceptions.BadCredentialsException:
                pass


# Download an Instagram Post from a Link
def post_downloader():
    url = str(input("Paste the link: "))
    regcode = re.compile("(p|l|v)/([0-9]|[a-z]|[A-Z])+.*./")
    spanLocation = [i for i in regcode.search(url).span()]
    spoint = spanLocation[0]+2
    epoint = spanLocation[1]-1
    shortcode = url[spoint:epoint]
    post = instaloader.Post.from_shortcode(L.context, shortcode)
    if post.video_url is None:
        print("Post doesn't exist")
    else:
        print(post.get_sidecar_nodes)
        L.filename_pattern = f"{post.profile}_""{date_utc}_UTC"
        L.download_post(post, target=post.profile)


# Find out an instagram id from an instagram username
def getinstaid():
    x = L.check_profile_id(usr())
    x_code = re.compile("[0-9]+")
    y = x_code.search(str(x))
    return int(y.group(0))


# Download Instagram Stories of an Account --login required
def story_dl4_1account():
    login()
    L.download_stories(userids=[(getinstaid())], filename_target=None)


# Download Instagram Highlights of an Account --login required
def dl_hlight():
    try:
        os.mkdir("Instagram_Highlights")
    except FileExistsError:
        pass
    os.chdir(os.path.join(os.getcwd(), "Instagram_Highlights"))
    login()
    L.download_highlights(getinstaid())


# Unfollow --login required
def unfollowers():
    login()
    profile = instaloader.Profile.from_username(L.context, usr())
    followers = set(profile.get_followers())
    following = set(profile.get_followees())
    unfollow = following - followers
    for unf in unfollow:
        print(unf.username)


# All Instagram stories you followed --login required
def stories():
    try:
        os.mkdir("Stories_u_Followed")
    except FileExistsError:
        pass
    os.chdir(os.path.join(os.getcwd(), "Stories_u_Followed"))
    login()
    for story in L.get_stories():
        for item in story.get_items():
            L.filename_pattern = f"{item.owner_username}_""{date_utc}_UTC"
            L.download_storyitem(item, f"{item.owner_username}")


# Saved Posts --login required
def saved_posts():
    mxc = int(input("How many posts do you want to download " +
                    "from your saved posts?: "))
    login()
    L.download_saved_posts(mxc)


# Get profile picture url of an account
def p_url():
    profile = instaloader.Profile.from_username(L.context, usr())
    p_src = profile.profile_pic_url
    print(p_src)


# Download profile
def download_profile():
    try:
        os.mkdir("Profile_Scraping")
    except FileExistsError:
        pass
    os.chdir(os.path.join(os.getcwd(), "Profile_Scraping"))
    login()
    profile = instaloader.Profile.from_username(L.context, usr())
    L.download_profiles([profile], igtv=True, tagged=False,
                        highlights=True, stories=True)


def main():
    print(
        " 1. Unfollowers\n",
        "2. Download Instagram Stories of an account\n",
        "3. Download All Instagram Stories you followed\n",
        "4. Download an Instagram Profile you followed or " +
        "from a Public Account (-igtv, -stories, -highlights, -posts, etc.)\n",
        "5. Download a post from the Instagram Link (igtv, reels, etc.)\n",
        "6. Download Highlights of an Instagram Profile\n",
        "7. Download your saved posts\n",
        "8. Get the profile picture url of an Instagram Account"
        )

    menu = input("Enter a number: ")

    if menu == "1":
        unfollowers()
    elif menu == "2":
        story_dl4_1account()
    elif menu == "3":
        stories()
        u2t = input("Upload to Telegram downloaded files (Y|N): ")
        if u2t.lower() == 'y':
            upload(os.getcwd())
        else:
            print("Cancelled !!")
            pass
    elif menu == "4":
        download_profile()
    elif menu == "5":
        post_downloader()
    elif menu == "6":
        dl_hlight()
    elif menu == "7":
        saved_posts()
    elif menu == "8":
        p_url()
    else:
        cleaner()
        print("Invalid number !!")
        sleep(0.62)
        main()


main()
