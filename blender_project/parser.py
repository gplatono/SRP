relations = ['on', 'above', 'below', 'left', 'right', 'at', 'touching', 'near', 'in front of', 'behind', 'over', 'under', 'in', 'between']
colors = ['black', 'red' ,'brown', 'green', 'blue', 'yellow']
arguments = ['lamp', 'table', 'block', 'book', 'chair', 'bookshelf', 'ceiling light', 'ceiling fan', 'desk', 'sofa', 'tv', 'recycle bin', 'pencil', 'laptop', 'apple', 'bowl', 'plate', 'banana']
parts = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', 'east', 'north', 'west', 'ceiling', 'recycle', 'bin', 'wall', 'light', 'fan']
determiners = ['a', 'the', 'other', 'another', 'all']
pronouns = ['it', 'this', 'these', 'those']
conj = ['and']
numerals = ['one', 'two', 'three']

class Token:
    def __init__(self, token):
        self.token = token

    def signature(self):
        return "token"

    def __repr__(self):
        return self.signature() + ":" + self.token

class Conj(Token):
    def __init__(self, token):
        self.token = token

    def signature(self):
        return "conj"

class Part(Token):
    def __init__(self, token):
        self.token = token

    def signature(self):
        return "part"
    
class Idx(Token):
    def __init__(self, token):
        self.token = token

    def signature(self):
        return "idx"

class Num(Token):
    def __init__(self, token):
        self.token = token

    def signature(self):
        return "num"

class Pro(Token):
    def __init__(self, token):
        self.token = token

    def signature(self):
        return "pro"

class Det(Token):
    def __init__(self, token):
        self.token = token

    def signature(self):
        return "det"

class Mod(Token):
    def __init__(self, token):
        self.token = token

    def signature(self):
        return "mod"

class Argument(Token):
    def __init__(self, argument, det=None, mod=None):
        self.token = argument
        self.det = det
        self.mod = mod

    def signature(self):
        return "arg"

    def __str__(self):
        dt = self.det if self.det is not None else ""
        md = self.mod if self.mod is not None else ""
        return self.signature() + ":" + self.token + "\ndet: " + dt + "\nmod: " + md + "\n"

class Relation(Token):
    def __init__(self, relation, relatums=[], referents=[]):
        self.token = relation
        self.relatums = relatums
        self.referents = referents

    def signature(self):
        return "rel"

    def __repr__(self):
        ret_val = self.signature() + ":" + self.token + "\n"
        for arg in self.relatums:
            ret_val += arg.__str__() + "\n"
        for arg in self.referents:
            ret_val += arg.__str__() + "\n"
        return ret_val

def set_objects(scene_objects):
    global arguments
    arguments = scene_objects

def tokenize(word):
    if word in relations:
        return Relation(word)
    elif word in pronouns:
        return Pro(word)
    elif word in conj:
        return Conj(word)
    elif word in colors:
        return Mod(word)
    elif word in determiners:
        return Det(word)
    elif word in arguments:
        return Argument(word)
    elif word in parts:
        return Part(word)
    elif word in numerals:
        return Num(word)
    return word

grammar = {}
grammar["mod", "arg"] = lambda x, y: Argument(y.token, y.det, x.token)
grammar["det", "arg"] = lambda x, y: Argument(y.token, x.token, y.mod)
#grammar["arg", "idx"] = lambda x, y: Argument(x.token, x.det, x.mod, y.token)
grammar["arg", "rel"] = lambda x, y: Relation(y.token, y.relatums + [x], y.referents)
grammar["rel", "arg"] = lambda x, y: Relation(x.token, x.relatums, x.referents + [y])
grammar["rel", "part"] = lambda rel, part: \
                         Relation(rel.token, rel.relatums, rel.referents[:-1] + [Argument(rel.referents[-1].token + " " + part.token, rel.referents[-1].det, rel.referents[-1].mod)]) \
                         if len(rel.referents) > 0 else \
                            Relation(rel.token, rel.relatums, [Argument(part.token)])
    
grammar["part", "part"] = lambda part1, part2: Argument(part1.token + " " + part2.token)
grammar["arg", "part"] = lambda arg, part: Argument(arg.token + " " + part.token, arg.det, arg.mod) 

def parse(response):
    parse_stack = []
    response = response.lower().split()
    #print (response)
    response = [tokenize(item) for item in response if issubclass(type(tokenize(item)), Token)]
    print (response)
    if response == []:
        return None
    #for item in response:
    idx = 0    
    current = response[0]
    while idx < len(response):
        if parse_stack != [] and (parse_stack[-1].signature(), current.signature()) in grammar:
            current = grammar[(parse_stack[-1].signature(), current.signature())](parse_stack[-1], current)
            parse_stack.pop()
        else:
            parse_stack += [current]
            idx += 1
            if idx < len(response):
                current = response[idx]
    print (parse_stack)
    










































