from random import sample
import json


def unique(list1):
    # initialize a null list
    unique_list = []

    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    # return list
    return unique_list

word_list = 'common' # 'scrabble' or 'common'

with open('TWL06.txt') as f:
    words = f.readlines()
scrabble_words = [word[:-1] for word in words]

with open('common_words.txt') as f:
    words = f.readlines()
words = [word.split(' ')[0].upper() for word in words]

for length in range(8, 11):

    all_words = [word for word in words if len(word) == length and word in scrabble_words]
    alpha_words = [''.join(sorted(word)) for word in all_words]
    unique_letters = unique(alpha_words)

    word_dict = {}

    for letters in unique_letters:
        word_dict[letters] = [word for (word, alpha_word) in zip(all_words, alpha_words) if alpha_word == letters]


    f = open(f"{word_list}_{length}.json", "w")
    json.dump(word_dict, f)
    f.close()
