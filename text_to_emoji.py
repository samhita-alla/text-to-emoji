import json
import string
import re
import copy
import random

# To convert json data to dictionary
def load_emojis_json(emojis_file):
    with open(emojis_file) as f:
        emojis_dict = json.load(f)
    return emojis_dict

# To convert text to emoji
def text_to_emoji(emojis_dict, text):
    # Split the words by punctuations
    words_set = re.findall(r"[\w']+|[!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ ]", text)
    # A temp var
    temp_words_set = words_set

    # Convert user given text to lower case, for easier comparison
    words_set = [x.lower() for x in words_set]

    # To store the resultant text
    result_text = []

    # To store all the possible emojis
    possible_emojis = {}

    # Loop over all the words
    for index, each_word in enumerate(words_set):

        # If punctuation, directly add it to the result
        if each_word in string.punctuation:
            result_text.append(temp_words_set[index])

        # If each_word is the base key, check if the word is present in it
        elif each_word in emojis_dict['keys']:
            emoji_match = [each_key for each_key in emojis_dict['keys'] if each_word == each_key][0]

            # Store the matched emoji
            if each_word not in possible_emojis:
                possible_emojis[each_word] = emojis_dict[emoji_match]['char']

            # Store the emoji in the result
            result_text.append(possible_emojis[each_word])
 
        # If each_word is plural, remove the last character('s')      
        elif each_word[:-1] in emojis_dict:
            emoji_match = [each_key for each_key in emojis_dict if each_word[:-1] == each_key][0]

            if each_word not in possible_emojis:
                possible_emojis[each_word] = emojis_dict[emoji_match]['char']

            result_text.append(possible_emojis[each_word])

        # If each_word is not in the base keys, search for it the keywords (emojis.json) 
        else:
            # Create a copy of emojis_dict
            temp_emojis_dict = copy.deepcopy(emojis_dict)

            # Delete 'keys' from the dict, as the value of that dict isn't a dictionary
            del temp_emojis_dict['keys']

            # Create a new_emojis_dict to store the matched entries
            new_emojis_dict = {}

            # Flag to check for singular words
            flag_new_sing = 0

            # Flag to check for plural words
            flag_new_plur = 0

            # Loop over all the emojis
            for each_key, each_val in temp_emojis_dict.items():
                # If each_word is present in keywords
                if (each_word in each_val['keywords']):

                    # Store the entry in new_emojis_dict
                    new_emojis_dict[each_key] = each_val

                    # Assign flag_new_sing to 1
                    flag_new_sing = 1

            # Loop again to check for plural words
            for each_key, each_val in temp_emojis_dict.items():

                # Append 's' to all keywords
                mod_each_val = [each + 's' for each in each_val['keywords']]

                if (each_word in mod_each_val):
                    new_emojis_dict[each_key] = each_val
                    flag_new_plur = 1 

            # If neither singular nor plural, append the word to result
            if flag_new_sing == 0 and flag_new_plur == 0:
                result_text.append(temp_words_set[index])
                continue

            # Else, Store the possible emojis in possible_emojis dict and append a randomly chosen emoji to the result
            if flag_new_sing == 1 or flag_new_plur == 1:
                if each_word not in possible_emojis:
                    possible_emojis[each_word] = [each_val['char'] for each_val in list(new_emojis_dict.values())]
                result_text.append(random.choice(possible_emojis[each_word]))

    # Return the resultant statement, possible_emojis dict, and the actual words_set dict
    return result_text, possible_emojis, words_set
    