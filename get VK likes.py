import vk
import time

# Log in using VK... (read more in VK API documentation)
app_id = ''
user_login = ''
user_password = ''
# ... or using access token
access_token = ''

# Depending on your choice, use one of the following session authorizations (uncomment it)
# session = vk.AuthSession(app_id=app_id, user_login=user_login, user_password=user_password)
# session = vk.Session(access_token=access_token)
api = vk.API(session)


def get_latest_posts_from_groups(group_ids, number_of_posts, api_ver):
    all_posts = []
    req_counter = 0
    for group in group_ids:
        req_counter += 1
        if req_counter == 3:
            # VK API allows to make only 3 requests per second
            time.sleep(1)
            req_counter = 0
        latest_posts = api.wall.get(owner_id="-" + str(group), count=str(number_of_posts), filter="all", v=str(api_ver))
        latest_posts = latest_posts['items']
        latest_posts_ids = [[item['id'], item['owner_id'], item['date']] for item in latest_posts]
        all_posts.extend(latest_posts_ids)
    return all_posts


def get_latest_posts_from_friend(friend_ids, number_of_posts, api_ver):
    all_posts = []
    req_counter = 0
    for friend in friend_ids:
        req_counter += 1
        if req_counter == 3:
            # VK API allows to make only 3 requests per second
            time.sleep(1)
            req_counter = 0
        try:
            latest_posts = api.wall.get(owner_id=str(friend), count=str(number_of_posts), filter="all", v=str(api_ver))
        except Exception:
            # friend profile can be private/deleted
            continue
        latest_posts = latest_posts['items']
        latest_posts_ids = [[item['id'], item['owner_id'], item['date']] for item in latest_posts]
        all_posts.extend(latest_posts_ids)
    return all_posts


def filter_liked_group_posts(group_posts, user_id, days, api_ver):
    liked_group_posts = []
    req_counter = 0
    for post in group_posts:
        if (time.time() - post[2]) / (24 * 60 * 60) > days:
            continue
        req_counter += 1
        if req_counter == 3:
            time.sleep(1)
            req_counter = 0
        info = api.likes.isLiked(user_id=user_id, type="post", owner_id=str(post[1]), item_id=str(post[0]), v=str(api_ver))
        if info['liked'] == 1:
            liked_group_posts.append("https://vk.com/wall" + str(post[1]) + "_" + str(post[0]))
    return liked_group_posts


def filter_liked_friend_posts(friend_posts, user_id, days, api_ver):
    liked_friend_posts = []
    req_counter = 0
    for post in friend_posts:
        if (time.time() - post[2]) / (24 * 60 * 60) > days:
            continue
        req_counter += 1
        if req_counter == 3:
            time.sleep(1)
            req_counter = 0
        info = api.likes.isLiked(user_id=user_id, type="post", owner_id=str(post[1]), item_id=str(post[0]), v=str(api_ver))
        if info['liked'] == 1:
            liked_friend_posts.append("https://vk.com/wall" + str(post[1]) + "_" + str(post[0]))
    return liked_friend_posts


def user_liked_group_posts(user_id, number_of_posts, days, api_ver):
    subscriptions = api.users.getSubscriptions(user_id=str(user_id), v=str(api_ver))
    group_ids = subscriptions['groups']['items']
    all_posts = get_latest_posts_from_groups(group_ids, str(number_of_posts), str(api_ver))
    return filter_liked_group_posts(all_posts, str(user_id), days, str(api_ver))


def user_liked_friend_posts(user_id, number_of_posts, days, api_ver):
    friends = api.friends.get(user_id=str(user_id), v=str(api_ver))
    friend_ids = friends['items']
    all_posts = get_latest_posts_from_friend(friend_ids, str(number_of_posts), str(api_ver))
    return filter_liked_friend_posts(all_posts, str(user_id), days, str(api_ver))


def save_links_in_txt(links):
    output = open('links.txt', 'w')
    for link in links:
        print(link, file=output)
    output.close()


def main():
    user_id = input("Enter id of the user whose likes you want to get:")
    source_type = input("Enter the type of source ('groups' or 'friends'):")
    number_of_posts = input("Enter how many posts need to be checked in each source (1 to 100):")
    number_of_days = int(input("Enter how many previous days should be considered:"))
    api_ver = input("Enter VK API's version (e.g. 5.101):")
    print("Processing...")
    start_time = time.time()
    if source_type == 'groups':
        save_links_in_txt(user_liked_group_posts(user_id, number_of_posts, number_of_days, api_ver))
    elif source_type == 'friends':
        save_links_in_txt(user_liked_friend_posts(user_id, number_of_posts, number_of_days, api_ver))
    else:
        print("Wrong 'type of source' input")
    print("Success.\n Result saved in 'links.txt' file.\n Running time:", (time.time() - start_time) / 60, "minutes")


main()
