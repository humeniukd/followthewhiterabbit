from hashlib import md5
from itertools import permutations

ALPHABET_SIZE = 26
INPUT = 'poultry outwits ants'.replace(' ', '')

class Trie(object):
    global dic
    def __init__(self):
        self.children = [None] * ALPHABET_SIZE
        self.end = False

    def insert(self, key):
        tmp = dic
        l = len(key)
        for i in range(l):
            n = ord(key[i]) - 97
            if tmp.children[n] == None:
                tmp.children[n] = Trie()
            tmp = tmp.children[n]
        tmp.end = True

    def search(self, key):
        l = len(key)
        tmp = dic
        for i in range(l):
            n = ord(key[i]) - 97
            if tmp.children[n] == None:
                return None
            tmp = tmp.children[n]
        return tmp

dic = Trie()

words = []
query = [
    'e4820b45d2277f3844eac66c903e84be',
    '23170acc097c24edb98fc5488ab033fe',
    '665e5bcb0c20062fe8abaaf4628bb154'
]

map = {}
cache = {}

def subs(w):
    rest = INPUT
    for c in w:
        rest = rest.replace(c, '', 1)
    return rest

def normalize(str):
    tmp = list(str)
    tmp.sort()
    return ''.join(tmp)

f=open('wordlist', 'r')
if f.mode == 'r':
    for line in f.readlines():
        w = line[:-1]
        if all(c in INPUT for c in w):
            dic.insert(w)
            if len(w) > 7: words.append(w)

class Finder(object):
    global dic, cache
    def __init__(self, str, l=2):
        self.str = str
        self.l = l
        s = cache.get(str)
        if s:
            self.res = s
            return
        self.size = len(self.str)
        self.marked = [False] * self.size
        self.res = set()
        for i in range(self.size):
            self.dfs(i, '')
        cache[str] = self.res

    def dfs(self, i, str):
        str += self.str[i]
        n = dic.search(str)
        if n == None:
            return

        if n.end and len(str) >= self.l:
            self.res.add(str)

        self.marked[i] = True
        for item in range(self.size):
            if not self.marked[item]:
                self.dfs(item, str)
        self.marked[i] = False

def check(words):
    if words in map:
        return
    var = permutations(words)
    for v in var:
        map[v] = True
        phrase = ' '.join(v)
        hash =  md5(phrase).hexdigest()
        if hash in query:
            print(phrase)

for w1 in words:
    r1 = normalize(subs(w1))
    pairs1 = Finder(r1, 4).res
    for w2 in pairs1:
        r2 = normalize(subs(w1 + w2))
        pairs2 = Finder(r2).res
        for w3 in pairs2:
            if len(w1) + len(w2) + len(w3) == len(INPUT):
                check((w1, w2, w3))
            else:
                r3 = normalize(subs(w1 + w2 + w3))
                pairs3 = Finder(r3).res
                for w4 in pairs3:
                    check((w1, w2, w3, w4))



