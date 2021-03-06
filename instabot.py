# importing requests library to make http requests
import requests
import urllib3
import matplotlib.pyplot as plt
# importing textblob library to delete negative comments posted
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

# adding global variables which will remain constant throughout the program
APP_ACCESS_TOKEN = "387324467.c39e406.357156de69064cfb861647d1e171d7d7"
BASE_URL = 'https://api.instagram.com/v1/'
sandbox_users = ["eviledmpredator"]
count = [0, 0, 0]
name = ["", "", ""]
exp = (0.1, 0.1, 0.1)
# creating a variable menu
menu = "\nChoose from the following options:\n1.View your own details\n2.Get user_id of an instagram user\n" \
       "3.Retrieve Your latest post\n4.Retrieve a user's latest post\n5.Recent media liked by you\n" \
       "6.Like a user's post\n7.Get List of comments on a user's post\n8.Comment on a user's post" \
       "\n9.View a pie chart tags \n10.Delete -ve comments from post \n11.exit\n"


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
    show_menu()


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
            recent_img_url = recent_post["data"][0]["images"]["standard_resolution"]["url"]
            urllib3.disable_warnings()
            connection_pool = urllib3.PoolManager()
            resp = connection_pool.request('GET', recent_img_url)
            f = open("own_post.jpg", 'wb')
            f.write(resp.data)
            f.close()
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
                recent_img_url = recent_post["data"][0]["images"]["standard_resolution"]["url"]
                urllib3.disable_warnings()
                connection_pool = urllib3.PoolManager()
                resp = connection_pool.request('GET', recent_img_url)
                f = open("recent.jpg", 'wb')
                f.write(resp.data)
                f.close()
                resp.release_conn()
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
    show_menu()


# full fledged function to like a user's recent post
def like_a_users_post(insta_username):
    post_id = get_user_recent_posts(insta_username)
    request_url = BASE_URL + "media/{}/likes".format(post_id)
    print("Requesting:\n{}".format(request_url))
    like = requests.post(request_url, data={'access_token': APP_ACCESS_TOKEN}).json()
    print(like)
    if like['meta']['code'] == 200:
        print("Like was successful")
    else:
        print("Like not successful")
    show_menu()


# full fledged function to get a list of comments on a user's recent post
def get_list_of_comments_on_users_post(insta_username):
    post_id = get_user_recent_posts(insta_username)
    request_url = BASE_URL + "media/{}/comments?access_token={}".format(post_id, APP_ACCESS_TOKEN)
    print("Requesting:\n{}".format(request_url))
    comments_on_this_post = requests.get(request_url).json()
    if comments_on_this_post["meta"]["code"] == 200:
        for i in range(0, len(comments_on_this_post["data"])):
            print(comments_on_this_post["data"][i]["from"]["username"], end=" : ")
            print(comments_on_this_post["data"][i]["text"])
            print()
    else:
        print("Status code other than 200")
    show_menu()


# full fledged function to comment on a user's recent post
def comment_on_a_users_post(insta_username):
    post_id = get_user_recent_posts(insta_username)
    request_url = BASE_URL + "media/{}/comments".format(post_id)
    print("Requesting:\n{}".format(request_url))
    comment_to_post = input("Enter your comment: ")
    comment = requests.post(request_url, data={'access_token': APP_ACCESS_TOKEN, 'text': comment_to_post}).json()
    print(comment)
    if comment['meta']['code'] == 200:
        print("comment was successful")
    else:
        print("comment not successful")
    show_menu()


# Defining a function to delete negative comments from the recent post of a user
def delete_negative_comment(insta_username):
    media_id = get_user_recent_posts(insta_username)
    req_url = BASE_URL + 'media/' + media_id + '/comments/?access_token=' + APP_ACCESS_TOKEN
    print(req_url)
    comment_info = requests.get(req_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            for i in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][i]['id']
                comment_text = comment_info['data'][i]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if blob.sentiment.p_neg > blob.sentiment.p_pos:
                    print('Negative comment : ' + comment_text)
                    delete_url = BASE_URL + 'media/' + media_id + '/comments/' + comment_id + '?access_token=' + APP_ACCESS_TOKEN
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print('Comment successfully deleted!\n')
                    else:
                        print('Unable to delete comment!')
                else:
                    print('Positive comment : ' + comment_text + '\n')
        else:
            print('There are no existing comments on the post!')
    else:
        print('Status code other than 200 received!')
    show_menu()


username = input("Enter the username for which you want to perform these actions\n"
                 "You can only perform actions for sandbox users\nYour Sandbox users are:\n{}\n"
                 .format(sandbox_users))


# this function takes tags one by one as input and evaluates them
def tag_analysis():
    i = 0
    print('Maximum of 3 tags allowed...!!!...')
    while True:
        tag = input('Enter the tag to be evaluated : ')
        name[i] = tag
        req_url = BASE_URL + 'tags/' + tag + '?access_token=' + APP_ACCESS_TOKEN
        tag_info = requests.get(req_url).json()
        count[i] = tag_info['data']['media_count']
        print('Do you want to evaluate another tag')
        ans = input()
        i = i + 1
        if ans == 'n':
            break
        elif ans == 'y':
            continue
        else:
            exit()

    print(count)


# this function makes use of global variables modified by the tag_analysis fxn and plots a pie chart
def plot():
    labels = name
    sizes = count

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=exp, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()
    show_menu()


# creating High level design of function show_menu()
def show_menu():
    if len(username) > 0:
        choice = int(input(menu))
        if choice == 1:
            self_info()
        elif choice == 2:
            user_id = get_user_id(username)
            print(user_id)
            show_menu()
        elif choice == 3:
            own_post_id = get_recent_posts()
            print("Your Post Has Been Downloaded")
            print("Your post ID is\n", own_post_id)
            show_menu()
        elif choice == 4:
            user_post_id = get_user_recent_posts(username)
            print("User's recent Post has been downloaded")
            print("The user's post ID is\n", user_post_id)
            show_menu()
        elif choice == 5:
            recent_media_liked_by_self()
        elif choice == 6:
            like_a_users_post(username)
        elif choice == 7:
            get_list_of_comments_on_users_post(username)
        elif choice == 8:
            comment_on_a_users_post(username)
        elif choice == 9:
            tag_analysis()
            plot()
        elif choice == 10:
            delete_negative_comment(username)
        elif choice == 11:
            exit(code="Application Closed")
        else:
            exit(code="You did'nt entered one of the choices above")
    else:
        exit(code="You have to enter a username")


show_menu()
