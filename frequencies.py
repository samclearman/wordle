from collections import defaultdict

from wordlist import read_wordlist

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
