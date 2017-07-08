# importing requests library to make http requests
import requests

# adding global variables which will remain constant throughout the program
APP_ACCESS_TOKEN = "387324467.c39e406.357156de69064cfb861647d1e171d7d7"
BASE_URL = 'https://api.instagram.com/v1/'
# creating a variable menu
menu = "\nChoose from the following options:\n1.View your own details\n2.Get user_id of an instagram user\n" \
       "3.Retrieve Your latest post\n4.Retrieve a user's latest post\n5.Recent media liked by you\n" \
       "6.Like a user's post\n7.Get List of comments on a user's post\n8.Comment on a user's post\n9.exit\n"


# full fledged function to show user's own info
def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=' + APP_ACCESS_TOKEN)
    user_info = requests.get(request_url).json()
    if user_info["meta"]["code"] == 200:
        if len(user_info["data"]):
            print("Username: {}".format(user_info["data"]["username"]))
            print("No. of followers: {}".format(user_info["data"]["counts"]["followed_by"]))
            print("No. of people you are following: {}".format(user_info["data"]["counts"]["follows"]))
            print("No. of posts: {}".format(user_info["data"]["counts"]["media"]))
        else:
            print("User does not exist")
    else:
        print("status code other than 200")


# full fledged function to take username as input and return user id
def get_user_id(insta_username):
    request_url = BASE_URL + "users/search?q={}&access_token={}".format(insta_username, APP_ACCESS_TOKEN)
    print("Requesting URL \n{}".format(request_url))
    user_info = requests.get(request_url).json()
    if user_info["meta"]["code"] == 200:
        if len(user_info["data"]):
            return user_info['data'][0]['id']
        else:
            print("No user found")
    else:
        print("Status code other than 200 found")


# full fledged function to return one's own recent post's id
def get_recent_posts():
    request_url = BASE_URL + "users/self/media/recent/?access_token={}".format(APP_ACCESS_TOKEN)
    print("Requesting:\n{}".format(request_url))
    recent_post = requests.get(request_url).json()
    if recent_post["meta"]["code"] == 200:
        if len(recent_post["data"]) > 0:
            return recent_post["data"][0]["id"]
        else:
            print("No posts to show")
            return None
    else:
        print("Status code other than 200")
        return None


# full fledged function to take username as input and return user's recent post's id
def get_user_recent_posts(insta_username):
    user_id = get_user_id(insta_username)
    if user_id is not None:
        request_url = "https://api.instagram.com/v1/users/{}/media/recent/?access_token={}".format(user_id,
                                                                                                   APP_ACCESS_TOKEN)
        print("Requesting:\n{}".format(request_url))
        recent_post = requests.get(request_url).json()
        if recent_post["meta"]["code"] == 200:
            if len(recent_post["data"]) > 0:
                return recent_post["data"][0]["id"]
            else:
                print("No posts to show")
                return None
        else:
            print("Status code other than 200")
            return None


# full fledged function to print the id of media liked by self
def recent_media_liked_by_self():
    request_url = BASE_URL + "users/self/media/liked?access_token={}".format(APP_ACCESS_TOKEN)
    print("Requesting:\n{}".format(request_url))
    media_liked = requests.get(request_url).json()
    if media_liked["meta"]["code"] == 200:
        if len(media_liked["data"]) > 0:
            print(media_liked["data"][0]["id"])
        else:
            print("No media to show")
    else:
        print("Status code other than 200")


# full fledged function to like a user's recent post
def like_a_users_post(insta_username):
    post_id = get_user_recent_posts(insta_username)
    print("post_id = ", post_id)
    request_url = BASE_URL + "media/{}/likes".format(post_id)
    print("Requesting:\n{}".format(request_url))
    like = requests.post(request_url, data={'access_token': APP_ACCESS_TOKEN}).json()
    print(like)
    if like['meta']['code'] == 200:
        print("Like was successful")
    else:
        print("Like not successful")


# full fledged function to get a list of comments on a user's recent post
def get_list_of_comments_on_users_post(insta_username):
    post_id = get_user_recent_posts(insta_username)
    print("post_id = ", post_id)
    request_url = BASE_URL + "media/{}/comments?access_token={}".format(post_id, APP_ACCESS_TOKEN)
    print("Requesting:\n{}".format(request_url))
    comments_on_this_post = requests.get(request_url).json()
    if comments_on_this_post["meta"]["code"] == 200:
        for i in range(len(comments_on_this_post)):
            print(comments_on_this_post["data"][i]["from"]["username"], end=" : ")
            print(comments_on_this_post["data"][i]["text"])
            print()
    else:
        print("Status code other than 200")


# full fledged function to comment on a user's recent post
def comment_on_a_users_post(insta_username):
    post_id = get_user_recent_posts(insta_username)
    print("post_id = ", post_id)
    request_url = BASE_URL + "media/{}/comments".format(post_id)
    print("Requesting:\n{}".format(request_url))
    comment_to_post = input("Enter your comment: ")
    comment = requests.post(request_url, data={'access_token': APP_ACCESS_TOKEN, 'text': comment_to_post}).json()
    print(comment)
    if comment['meta']['code'] == 200:
        print("comment was successful")
    else:
        print("comment not successful")


# creating High level design of function show_menu()
def show_menu():
    insta_username = input("Enter the username for which you want to perform these actions")
    if len(insta_username) > 0:
        choice = int(input(menu))
        if choice == 1:
            pass
        elif choice == 2:
            pass
        elif choice == 3:
            pass
        elif choice == 4:
            pass
        elif choice == 5:
            pass
        elif choice == 6:
            pass
        elif choice == 7:
            pass
        elif choice == 8:
            pass
        elif choice == 9:
            exit(code="Application Closed")
        else:
            exit(code="You did'nt entered one of the choices above")
    else:
        exit(code="You have to enter a username")
