relations = ['on', 'above', 'below', 'left', 'right', 'at', 'touching', 'near', 'front', 'behind', 'over', 'under', 'in', 'between']
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
    def __init__(self, token, conjoints=[]):
        self.token = token
        self.args = conjoints

    def conjoin(self, arg):
        if type(arg) is Mod and self.args != [] and type(self.args[-1]) is Argument:
            return Conj(self.token, self.args + [Argument(self.args[-1].token, arg)])
        elif type(arg) is Argument and self.args != [] and type(self.args[-1]) is Mod:
            print ("==========", [Argument(arg.token, ar) for ar in self.args if type(ar) is Mod] + [arg])
            return Conj(self.token, [Argument(arg.token, ar) for ar in self.args if type(ar) is Mod] + [arg])
        else:
            return Conj(self.token, self.args + [arg])

        print ("TESTTESTSETSETSET:", self.__repr__())
        return Conj(self.token, self.args) 

    def signature(self):
        return "conj"

    def __repr__(self):
        ret_val = super().__repr__() + "\n"
        for arg in self.args:
            ret_val += arg.__repr__() + "\n"
        return ret_val

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
    def __init__(self, det="", adj=""):
        self.det = det
        self.adj = adj

    def signature(self):
        return "mod"

    def __repr__(self):
        return self.signature() + ":" + self.det + " " + self.adj 

class Argument(Token):
    def __init__(self, argument, mod=None):
        self.token = argument
        self.mod = mod

    def signature(self):
        return "arg"

    def __str__(self):
        md = self.mod.__repr__() if self.mod is not None else ""
        return self.signature() + ":" + self.token + " " + md

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
        return Mod(adj=word)
    elif word in determiners:
        return Mod(det=word)
    elif word in arguments:
        return Argument(word)
    elif word in parts:
        return Part(word)
    elif word in numerals:
        return Num(word)
    return word

grammar = {}
grammar["mod", "mod"] = lambda mod1, mod2: Mod(mod1.det, mod2.adj)
#grammar["det", "mod"] = lambda det, mod: Argument("", det.token, mod.token)
grammar["mod", "arg"] = lambda mod, arg: Argument(arg.token, mod)
#grammar["det", "arg"] = lambda x, y: Argument(y.token, x.token, y.mod)
#grammar["arg", "idx"] = lambda x, y: Argument(x.token, x.det, x.mod, y.token)
grammar["arg", "rel"] = lambda x, y: Relation(y.token, y.relatums + [x], y.referents)
grammar["rel", "arg"] = lambda x, y: Relation(x.token, x.relatums, x.referents + [y])
grammar["rel", "part"] = lambda rel, part: \
                         Relation(rel.token, rel.relatums, rel.referents[:-1] + [Argument(rel.referents[-1].token + " " + part.token, rel.referents[-1].mod)]) \
                         if len(rel.referents) > 0 else \
                            Relation(rel.token, rel.relatums, [Argument(part.token)])
grammar["mod", "conj"] = lambda mod, conj: conj.conjoin(mod)
grammar["conj", "arg"] = lambda conj, arg: conj.conjoin(arg)    
grammar["part", "part"] = lambda part1, part2: Argument(part1.token + " " + part2.token)
grammar["arg", "part"] = lambda arg, part: Argument(arg.token + " " + part.token, arg.mod)
grammar["rel", "conj"] = lambda rel, conj: Relation(rel.token, rel.relatums, conj.args)

def parse(response):
    parse_stack = []
    response = response.lower().split()
        
    print (response)
    
    response = [tokenize(item) for item in response if issubclass(type(tokenize(item)), Token)]
    print (response)
    if response == []:
        return None
    #for item in response:
    idx = 0    
    current = response[0]
    while idx < len(response):
        if parse_stack != [] and (parse_stack[-1].signature(), current.signature()) in grammar:
            print (parse_stack[-1], current)
            current = grammar[(parse_stack[-1].signature(), current.signature())](parse_stack[-1], current)
            parse_stack.pop()
        else:
            parse_stack += [current]
            idx += 1
            if idx < len(response):
                current = response[idx]
    print (parse_stack)
    #for item in parse_stack:
    #    if type(item) is Relation and item.token == "between":
    #        print (item.referents)










































