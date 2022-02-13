from random import sample, shuffle
import json
from collections import Counter

def remove_letters(word, indices):
    sorted_indices = sorted(indices)
    new_word = ''
    for j, index in enumerate(sorted_indices):
        if j == 0:
            new_word = word[0:index]
        else:
            new_word += word[indices[j - 1] + 1: index]
    new_word += word[sorted_indices[-1]+1:]
    return new_word

def find_subchain(letters):
    length = len(letters)

    if letters not in word_dicts[length] or True in [word[-1] == 'S' for word in word_dicts[length][letters]]:
        return []

    if len(letters) == 3:
        if letters in word_dicts[3]:
            return [letters]
        else:
            return []

    is_to_remove = list(range(0, length))
    shuffle(is_to_remove)

    for i in is_to_remove:
        chain = find_subchain(remove_letters(letters, [i]))
        if chain != []:
            current_words = word_dicts[length][letters]
            next_words = word_dicts[length - 1][chain[0]]

            trivial_found = False
            for next_word in next_words:
                for current_word in current_words:
                    for i in range(0, length):
                        if next_word == remove_letters(current_word, [i]):
                            trivial_found = True
                            break
                    if trivial_found:
                        break
                if trivial_found:
                    break

            if not trivial_found:
                return [letters] + chain
    return []

word_list_generate = 'common'
word_list_check = 'scrabble'

with open('common_words.txt') as f:
    words = f.readlines()
words = [word.split(' ')[0].upper() for word in words]

with open('TWL06.txt') as f:
    scrabble_words = f.readlines()
scrabble_words = [word[:-1] for word in scrabble_words]

if word_list_check == 'scrabble':
    words_check = scrabble_words
else:
    words_check = words

word_dicts = {}
for length in range(3, 11):
    f = open(f"{word_list_generate}_{length}.json", "r")
    word_dicts[length] = json.load(f)

def generate_chain(length=9, start = None, verbose = False):

    if start:
        if verbose:
            print(f"Trying {start} with words {word_dicts[length][start]}")
        chain = find_subchain(start)
        if chain != []:
            detailed_dict = {}

            for letters in chain:
                detailed_dict[letters] = word_dicts[len(letters)][letters]

            return detailed_dict
        return []

    while True:
        start = sample(word_dicts[length].keys(), 1)[0]
        if verbose:
            print(f"Trying {start} with words {word_dicts[length][start]}")

        chain = find_subchain(start)
        if chain != []:
            detailed_dict = {}

            for letters in chain:
                detailed_dict[letters] = word_dicts[len(letters)][letters]

            return detailed_dict

def space_string(s, shuffle_string):
    if shuffle_string:
        l = list(s)
        shuffle(l)
        s = ''.join(l)
    new_s = ''
    for i in range(len(s)):
        new_s += s[i] + ' '
    return new_s

def find_added_letter(s1, s2):
    return list((Counter(s2) - Counter(s1)).keys())[0]

def play_game(length = 9, start_length = 3):
    chain_dict = generate_chain(starting_length = length, start=None, verbose=False)

    user_word = ''
    user_words = []
    hints = 0
    current_length = start_length
    while current_length <= length:
        current_stage = current_length - 2
        current_letters = list(chain_dict.keys())[-1 * (current_stage)]

        if current_stage == 1 or user_word == '*':
            print(f"{current_length} Letters \n")
            print(f"{space_string(current_letters, shuffle_string = True)}\n\n")
        else:
            previous_letters = list(chain_dict.keys())[-1 * (current_stage - 1)]
            added_letter = find_added_letter(previous_letters, current_letters)

            print(f"{current_length} Letters \n")
            print(f"{space_string(user_word + added_letter, shuffle_string=False)}\n\n")

        while True:
            print("Enter word (press Return to shuffle or '*' to give up and see answer):")
            user_word = input().upper()

            if user_word == '*':
                print(f"Answers: {', '.join(chain_dict[current_letters])}\n")
                user_words.append(chain_dict[current_letters])
                hints += 1
                break
            if user_word == '':
                print(f"{space_string(current_letters, shuffle_string=True)}\n\n")
            else:
                user_letters = ''.join(sorted(user_word))

                valid_word = user_word in words_check
                uses_letters = user_letters == current_letters
                if valid_word and uses_letters:
                    print(f"GOOD! {current_length} letters found!\n")
                    user_words.append(user_word)
                    break
                elif not valid_word and not uses_letters:
                    print(f"Invalid word and doesn't use the right letters. Please try again \n")
                elif not valid_word:
                    print(f"Invalid word. Please try again \n")
                elif not uses_letters:
                    print("Doesn't use the right letters. Please try again.\n")
                else:
                    raise(TypeError)
        current_length += 1

    print(f"Congratulations! You made it to {length} letters with {length - start_length - hints + 1} correct and {hints} hints")
    for i in range(start_length, length + 1):
        if type(user_words[i - start_length]) == str:
            print(f"{i} letters: {user_words[i - start_length]}")
        else:
            print(f"{i} letters: None (Answers: {', '.join(user_words[i - start_length])})")

    print(f"Press return to see all answers:")
    x = input()
    print("All answers")
    all_letters = list(chain_dict.keys())
    for i in range(len(all_letters)):
        print(f"{i + start_length} letters: {', '.join(chain_dict[all_letters[-1 - i]])}")
    return





