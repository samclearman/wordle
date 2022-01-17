from collections import defaultdict
from itertools import product

# import modal

from wordlist import read_wordlist
from wordbag import wordbag

all_words = read_wordlist('wordlist')
common_words = all_words[:all_words.index('aahed')]

def get_frequencies(remainder, should_print=False):
    possible_words = remainder if remainder else common_words
    frequencies = defaultdict(int)
    positions = defaultdict(lambda: [0,0,0,0,0])
    for word in possible_words:
        for i in range(len(word)):
            l = word[i]
            frequencies[l] += 1
            positions[l][i] += 1

    lines = []
    for l in 'abcdefghijklmnopqrstuvwxyz':
        freq = int(frequencies[l] / 26)
        freqs = '{:>2}'.format(freq)
        pos = [int(10 * (x / (sum(positions[l]) + 1))) for x in positions[l]]
        poss = ' '.join([str(x) for x in pos])
        lines.append((frequencies[l], f'{l}: {freqs} | {poss}'))

    for f, l in reversed(sorted(lines)):
        print(l)

    all_scores = defaultdict(dict)

    pos_scored = []
    for word in all_words:
        score = 0
        for i in range(len(word)):
            score += positions[word[i]][i]
        all_scores[word]['positional'] = score
        pos_scored.append((score, word))

    abs_scored = []
    for word in all_words:
        score = 0
        letters = set(word)
        for l in letters:
            score += frequencies[l]
        all_scores[word]['absolute'] = score
        abs_scored.append((score, word))
        
    if not should_print:
        return pos_scored, abs_scored
    else:
        print('\n')
        print('Top ten words by positional score:')
        for score, word in list(reversed(sorted(pos_scored)))[:10]:
            # print(f'{word} ({score}, {all_scores[word]["absolute"]}, {all_scores[word]["cut"]})')
            print(f'{word} (positional: {all_scores[word]["positional"]}, absolute: {all_scores[word]["absolute"]})')

        print('\n')
        print('Top ten words by absolute score:')
        for score, word in list(reversed(sorted(abs_scored)))[:10]:
            # print(f'{word} ({score}, {all_scores[word]["positional"]}, {cut_score(word)}, {all_scores[word]["cut"]})')
            print(f'{word} (positional: {all_scores[word]["positional"]}, absolute: {all_scores[word]["absolute"]})')

get_frequencies(all_words, should_print=True)

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

# @modal.function
# def cut_score(guess):
#     scores = []
#     for mask in all_masks(guess):
#         prune, remainder = wordbag(common_words)
#         prune(guess, mask)
#         scores.append(len(remainder()))
#     return max(scores), guess

# this could take a while
# cut_scored = []
# with modal.run():
# scored = cut_score.map(all_words)
# for score, word in scored:
#     all_scores[word]['cut'] = score
#     cut_scored.append((score, word))
        
# for word in all_words:
#     score = cut_score(word)
#     all_scores[word]['cut'] = score
#     cut_scored.append((score, word))
#     print(word, score)

# print('\n')
# print('Top ten words by cut score:')
# for score, word in list(sorted(cut_scored))[:10]:
#     print(f'{word} ({score}, {all_scores[word]["absolute"]}, {all_scores[word]["positional"]})') 
def freq_by_position():
    all_words = read_wordlist('wordlist')
    common_words = all_words[:all_words.index('aahed')]

    frequencies = defaultdict(int)
    positions = defaultdict(lambda: [0,0,0,0,0])
    for word in common_words:
        for i in range(len(word)):
            l = word[i]
            frequencies[l] += 1
            positions[l][i] += 1

    lines = []
    for l in 'abcdefghijklmnopqrstuvwxyz':
        freq = int(frequencies[l] / 26)
        freqs = '{:>2}'.format(freq)
        pos = [int(10 * (x / sum(positions[l]))) for x in positions[l]]
        poss = ' '.join([str(x) for x in pos])
        lines.append((frequencies[l], f'{l}: {freqs} | {poss}'))

    for f, l in reversed(sorted(lines)):
        print(l)

    scored = []
    for word in all_words:
        score = 0
        for i in range(len(word)):
            score += positions[word[i]][i]
        scored.append((score, word))

    print('\n')
    print('Top ten words:')
    for score, word in list(reversed(sorted(scored)))[:10]:
        print(f'{word} ({score})')
