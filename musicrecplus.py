'''
Names: Katie Ng, Katrina Taylor, Stephen Schau
Pledge: I pledge my honor that I have abided by the Stevens Honor Code.

CS115 - Music Recommendation System
'''

PREF_FILE = "musicrecplus.txt"

def main():
    ''' Main recommendation function '''
    user_map = load_users(PREF_FILE)
    username = input('Enter your name (put a $ symbol after your name if you wish your preferences to remain private): ').title()
    if username not in user_map:
        preferences = get_preferences(username, user_map)
        save_user_preferences(username, preferences, user_map, PREF_FILE)
    display_menu(username, user_map)


def load_users(file_name):
    ''' Loads in the users by splitting the input by the ':', such that the first part is the username and the second part is
        the user's preferred artists. Returns a dictionary containing a mapping of user names to a list of preferred artists. '''
    try:
        file = open(file_name, 'r')
    except:
        file = open(file_name, 'w')
        user_dic = {}
        file.close()
        return user_dic
    user_dic = {}
    for line in file:
        username, artists = line.strip().split(':')
        artist_list = artists.split(',')
        artist_list.sort()
        for i in range(len(artist_list)):
            artist_list[i] = artist_list[i].title()
        user_dic[username] = artist_list
    file.close()
    return user_dic


def get_preferences(username, user_map):
    ''' Returns list of the user's preferred artists. If system already knows user, it gets the preferences out of userMap dict. '''
    new_pref = ''
    if username in user_map:
        prefs = user_map[username]
        new_pref = input('Enter an artist that you like (Enter to finish): \n').title()
        prefs = []
    else:
        prefs = []
        new_pref = input('Enter an artist that you like (Enter to finish): \n').title()
    while new_pref != '':
        prefs.append(new_pref.strip())
        new_pref = input('Enter an artist that you like (Enter to finish): \n').title()
    prefs.sort()
    return prefs

def save_user_preferences(username, prefs, user_map, file_name):
    ''' Saves file after user quits '''
    user_map[username] = prefs
    sorted_user_map = dict(sorted(user_map.items(), key = lambda x: x[0]))
    file = open(file_name, 'w')
    for user in sorted_user_map:
        save = str(user) + ':' + ",".join(sorted_user_map[user]) + '\n'
        file.write(save)
    file.close()

def display_menu(username, user_map):
    ''' Displays the menu of the user's options (e, r, p, h, m, s, and q) '''
    while True:
        print('Enter a letter to choose an option: ')
        print('e - enter preferences')
        print('r - get recommendations')
        print('p - show most popular artists')
        print('h - how popular is the most popular artist')
        print('m - which user has the most likes')
        print('s - show preferences')
        print('q - save and quit')
        option = input()
        if option == 'e':
            prefs = get_preferences(username, user_map)
            save_user_preferences(username, prefs, user_map, PREF_FILE)

        elif option == 'r':
            if len(user_map.keys()) == 1:
                print('You are currently the only user registered. No recommendations found.')
            else:
                recs = get_recommendations(username, user_map[username], user_map)
                print_recs(recs, username)
        elif option == 'p':
            show_most_popular(user_map)
        elif option == 'h':
            how_popular(user_map)
        elif option == 'm':
            user_most_likes(user_map)
        elif option == 's':
            show_prefs(username, user_map)
        elif option == 'q':
            try:
                save_user_preferences(username, prefs, user_map, PREF_FILE)
                break
            except:
                break

###########################################################################
# GET RECOMMENDATIONS
###########################################################################

def num_matches(user_prefs, stored_prefs):
    ''' Returns the number of elements that match between two lists '''
    
    x = list(user_prefs)
    x.sort()            
    
    y = list(stored_prefs)
    y.sort()
    
    i, j, count = 0,0,0                 # i is index for userPrefs, j is index for storedPrefs
    while i < len(x) and j < len(y):
        if x[i] == y[j]:
            count += 1
            i += 1
            j += 1
        elif x[i] > y[j]:
            j += 1
        else:
            i += 1
    return count

def print_recs(recs, username):
    ''' Prints the recommendations based on the user's preferences '''
    if len(recs) == 0:
        print('No recommendations available at this time.')
    else:
        for artist in recs:
            print(artist)
            
def get_recommendations(curr_user, prefs, user_map):
    ''' Gets the recommendations for the current user based on the users in
        user_map and the user's preferences in prefs. Returns a list of recommended artists. '''

    best_user = find_best_user(curr_user, prefs, user_map)
    if best_user != None:
        complete_list = list(prefs)
        for user in best_user:
            complete_list += user_map[user]
        final_list = delete_duplicates(complete_list)
        recommendations = drop(prefs, final_list)
    else:
        recommendations = []
    return recommendations

def delete_duplicates(lst):
    ''' Deletes the duplicates of artists and returns the list of artist_dict '''
    artist_dict = {}
    for artist in lst:
        if artist in artist_dict:
            artist_dict[artist] += 1
        else:
            artist_dict[artist] = 1
    return list(artist_dict.keys())

def find_best_user(curr_user, prefs, user_map):
    ''' Finds the best user with the most common prefs to the current user '''
    users = user_map.keys()
    possible_users = []
    for user in users:
        if '$' not in user:
            possible_users.append(user)
    best_user = None
    best_score = 0
    for user in possible_users:
        score = num_matches(prefs, user_map[user])
        if score > best_score and curr_user != user and prefs != user_map[user]:
            best_score = score
            best_user = [user]
        elif score == best_score and curr_user != user and prefs != user_map[user] and best_user != None:
            best_score = score
            best_user.append(user)
    return best_user

def drop(list1, list2):
    ''' Returns a new list that contains only the elements in list2 that are not in list1 '''
    list1.sort()
    list2.sort()
    result = []
    i = j = 0
    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]:
            i += 1
            j += 1
        elif list1[i] < list2[j]:
            i += 1
        else:
            result.append(list2[j])
            j += 1
    while i < len(list1):
        result.append(list1[i])
        i += 1
    while j < len(list2):
        result.append(list2[j])
        j += 1
    return result

###########################################################################
# TOP (MOST POPULAR) ARTISTS
###########################################################################

def calculate_popularity(user_map):
    ''' Returns dictionary of the numerical "popularity" of each existing artist '''

    popularity_values = {}

    all_users = list(user_map.keys())
    public_users = list(filter(lambda name: name[-1] != 'S', all_users))

    for user in public_users:
        for artist in user_map[(user)]:
            if (artist) not in popularity_values:
                popularity_values[(artist)] = 1
            else:
                popularity_values[(artist)] += 1
    return popularity_values

def show_most_popular(user_map):
    ''' Returns a list of the 3 most popular artists (at most).
        Returns multiple artists if 2+ tie for most popular. Excludes private users. '''

    popularity = calculate_popularity(user_map)
    descending_pop = sorted(popularity.items(), key = lambda pair: pair[1], reverse = True)

    top_artists = []

    while len(top_artists) < 3:
        if descending_pop == []:
            return
        top_artists += [descending_pop[0][0]]
        descending_pop = descending_pop[1:]

    if top_artists == []:
        print('Sorry, no artists found.')
        return

    for artist in top_artists:
        print(artist)

def how_popular(user_map):
    ''' Returns numerical value of how popular the top (most popular) artist is '''
    popularity = calculate_popularity(user_map)
    descending_pop = sorted(popularity.items(), key = lambda pair: pair[1], reverse = True)

    if descending_pop == []:
        print('Sorry, no artists found.')
        return
    print(descending_pop[0][1])

###########################################################################
# USER WITH MOST LIKED ARTISTS
###########################################################################
        
def user_most_likes(user_map):
    ''' Returns the user with the most likes, excluding private users '''
    users = list(user_map)
    maximum = 0
    best_user = []
    for x in range(len(users)):
        if len(user_map[users[x]]) > maximum and users[x][-1] != '$':
            maximum = len(user_map[users[x]])
            best_user = [users[x]]
        if len(user_map[users[x]]) == maximum and users[x][-1] != '$':
            maximum = len(user_map[users[x]])
            best_user.append(users[x])
    if len(best_user) == 1:
        print(best_user[0])
    elif len(best_user) == 0:
        print('Sorry, no user found')
    elif len(best_user) > 1:
        for user in best_user[1:]:
            print(user)

###########################################################################
# SHOW PREFERENCES
###########################################################################

# Extra Credit: Show current user's preferences
def show_prefs(username, user_map):
    ''' Prints user's preferences '''
    prefs = user_map[username]
    if prefs == []:
        print('No artist preferences found')
        return
    else:
        for artist in prefs:
            print(artist)

###########################################################################
# MAIN
###########################################################################

if __name__ == "__main__": main()
