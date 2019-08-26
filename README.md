# liked-posts-vk

This program allows you to get links to posts which user liked in his/her VK feed.

Here is short description of how it works:
Firstly, we get the list of groups/friends that user follows. Then for each group/friend we collect last few posts that have been published. In the end, for each post we check whether user liked it or not.

# How to use it
* Authorize in VK by entering your login details in the first part of the program.
* Run the program and set search parameters:
```
*Input example*
Enter id of the user whose likes you want to get:123456
Enter the type of source ('groups' or 'friends'):groups
Enter how many posts need to be checked in each source (1 to 100):5
Enter how many previous days should be considered:30
Enter VK API's version (e.g. 5.101):5.101

```

# Limitations
Note that VK API has the limit of 5000 requests per day. Each run of this program makes X requests if user following X groups. Though you may consider caching group identifiers to avoid this limit.

Also note that VK API allows to make only 3 requests per second and this affects performance of the program. If you enter too big searching parameters it may take few days to complete the search. 

For the first run, normal running time is 10 minutes for an average social network user. For the following run you may want not to check all previously checked posts. In this case tweak 4th parameter.

# Authorization
https://vk.com/dev/access_token

# Useful links
https://vk.com/dev/manuals
