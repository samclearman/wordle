import random
from collections import defaultdict

from rich import print

from wordlist import read_wordlist
from wordbag import wordbag

answer = 'query'

wordlist = read_wordlist('wordlist')

def check(word, answer):
    if not word in wordlist:
        return None

    result = [0,0,0,0,0]
    a = [l for l in answer] 
    for i in range(len(word)):
        if word[i] == a[i]:
            result[i] = 2
            a[i] = ''
    for i in range(len(word)):
        if result[i] == 2:
            continue
        try:
            j = a.index(word[i])
            result[i] = 1
            a[j] = ''
        except ValueError:
            pass

    return result

def make_game(answer):
    def checker(guess):
        return check(guess, answer)
    return checker

def pp(word, mask):
    s = ''
    for i in range(len(word)):
        if mask[i] == 2:
            s += '[black on green]' + word[i] + '[/black on green]'
        elif mask[i] == 1:
            s += '[black on yellow]' + word[i] + '[/black on yellow]'
        else:
            s += word[i]
    print(s)

def solve(checker):
    prune, remainder = wordbag(wordlist)
    guesses = 0
    while len(remainder()) > 0:
        guess = "orate" if guesses == 0 else random.choice(remainder())
        mask = checker(guess)
        prune(guess, mask)
        pp(guess, mask)
        guesses += 1
    return guesses

# guesses = 0
# successes = 0
# for _ in range(100):
#     answer = random.choice(wordlist)
#     checker = make_game(answer)
#     g = solve(checker)
#     if g <= 6:
#         guesses += g
#         successes += 1
#     print(f'Solved {answer} in {g} guesses\n')
# print(f'Solved {successes} / 100 words')
# print(f'Average score: {guesses/successes}')

# starting with random word
# Solved 2067 / 2315 words
# Average score: 4.597968069666183

# start w/ "orate"
# Solved 2074 / 2315 words
# Average score: 4.490356798457087

guesses = 0
successes = 0
all_words = read_wordlist('wordlist')
common_words = all_words[:all_words.index('aahed')]
for word in common_words:
    checker = make_game(word)
    g = solve(checker)
    if g <= 6:
        guesses += g
        successes += 1
    print(f'Solved {answer} in {g} guesses\n')
print(f'Solved {successes} / {len(common_words)} words')
print(f'Average score: {guesses/successes}')
