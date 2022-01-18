from itertools import product
from wordbag import wordbag
from wordlist import read_wordlist

import modal

all_words = read_wordlist('wordlist')
common_words = all_words[:all_words.index('aahed')]

def legal(guess, mask):
    for l in set(guess):
        seen_zero = False
        for i in range(len(guess)):
            if guess[i] == l and mask[i] == 1 and seen_zero:
                return False
            if guess[i] == l and mask[i] == 0:
                seen_zero = True
    return True

def all_masks(guess):
    masks = []
    for m in product([0,1,2], repeat=5):
        if legal(guess, m):
            masks.append(m)
    return masks

@modal.function
def cut_score(guess):
    print(f'computing cut score for {guess}')
    scores = []
    for mask in all_masks(guess):
        prune, remainder = wordbag(common_words)
        prune(guess, mask)
        scores.append(len(remainder()))
    print(f'{guess}: {max(scores)}')
    return max(scores), guess
