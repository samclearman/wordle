from collections import defaultdict

import modal

from wordlist import read_wordlist
from wordbag import wordbag
from cut_score import cut_score

all_words = read_wordlist('wordlist')
common_words = all_words[:all_words.index('aahed')]

def get_frequencies(words):
    absolute = defaultdict(int)
    positional = defaultdict(lambda: [0,0,0,0,0])
    for word in words:
        for i in range(len(word)):
            l = word[i]
            absolute[l] += 1
            positional[l][i] += 1

    lines = []
    for l in 'abcdefghijklmnopqrstuvwxyz':
        freq = int(absolute[l] / 26)
        freqs = '{:>2}'.format(freq)
        pos = [int(10 * (x / (sum(positional[l]) + 1))) for x in positional[l]]
        poss = ' '.join([str(x) for x in pos])
        lines.append((absolute[l], f'{l}: {freqs} | {poss}'))

    return absolute, positional

absolute, positional = get_frequencies(common_words)

def absolute_score(word, frequencies=absolute):
    score = 0
    letters = set(word)
    for l in letters:
        score += frequencies[l]
    return score

def positional_score(word, frequencies=positional):
    score = 0
    for i in range(len(word)):
        score += frequencies[word[i]][i]
    return score

if __name__ == '__main__':
    all_scores = defaultdict(dict)
    abs_scores = [(absolute_score(w), w) for w in all_words]
    for s, w in abs_scores:
        all_scores[w]['absolute'] = s
    pos_scores = [(positional_score(w), w) for w in all_words]
    for s, w in pos_scores:
        all_scores[w]['positional'] = s


    # this could take a while
    cut_scored = []
    with modal.run():
        scored = cut_score.map(all_words)
        for score, word in scored:
            all_scores[word]['cut'] = score
            cut_scored.append((score, word))

    def pp(word):
        print(f'{word} (positional: {all_scores[word]["positional"]}, absolute: {all_scores[word]["absolute"]}, cut: {all_scores[word]["cut"]})')


    print('Top ten words by positional score:')
    for score, word in list(reversed(sorted(pos_scores)))[:10]:
        pp(word)
    print('\n')
    print('Top ten words by absolute score:')
    for score, word in list(reversed(sorted(abs_scores)))[:10]:
        pp(word)
    print('\n')
    print('Top ten words by cut score:')
    for score, word in list(sorted(cut_scored))[:10]:
        pp(word)


        


