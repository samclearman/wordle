from collections import defaultdict

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
            if w[i] == g[i]:
                return False
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

def wordbag(words):
    _words = words

    def prune(guess, mask):
        nonlocal _words
        _words = [w for w in _words if possible(w, guess, mask)]

    def remainder():
        return _words

    return prune, remainder
