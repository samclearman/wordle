import random
from collections import defaultdict
from rich import print

answer = 'query'

def read_wordlist(path):
    with open(path) as f:
        return [line.rstrip() for line in f.readlines()]

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

def possible(word, guess, mask):
    if word == guess:
        return False
    w = [l for l in word]
    g = [l for l in guess]
    w_counts = defaultdict(int)
    g_bounds_lower = defaultdict(int)
    g_bounds_upper = {}
    for i in range(len(w)):
        if mask[i] == 2:
            if w[i] != g[i]:
                return False
            g_bounds_lower[g[i]] += 1
    for i in range(len(w)):
        if mask[i] == 1:
            g_bounds_lower[g[i]] += 1
        elif mask[i] == 0:
            g_bounds_upper[g[i]] = g_bounds_lower[g[i]]
    for i in range(len(w)):
        w_counts[w[i]] += 1
    for l, b in g_bounds_lower.items():
        if w_counts[l] < b:
            return False
    for l, b in g_bounds_upper.items():
        if w_counts[l] > b:
            return False
    return True

def solve(answer):
    goodlist = wordlist
    guesses = 0
    while len(goodlist) > 0:
        guess = random.choice(goodlist)
        mask = check(guess, answer)
        goodlist = [word for word in goodlist if possible(word, guess, mask)]
        pp(guess, mask)
        guesses += 1
    return guesses

guesses = 0
successes = 0
for _ in range(100):
    answer = random.choice(wordlist)
    g = solve(answer)
    if g <= 6:
        guesses += g
        successes += 1
    print(f'Solved {answer} in {g} guesses\n')
print(f'Solved {successes} / 100 words')
print(f'Average score: {guesses/successes}')
