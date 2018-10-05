
class TreeNode(object):
    def __init__(self, content=None, children=None):
        self.content = content
        self.children = children

    def printable(self):
        return self.content + " [" + " ".join([child.printable() for child in self.children]) + "]" if self.children is not None else ""

relations = ['on', 'to the left of', 'to the right of', 'in front of', 'behind', 'above', 'below', 'over', 'under', 'near', 'touching', 'at', 'between']

grammar = {}

grammar[(<class 'ulf_parser.TName'>, <class 'ulf_parser.TNoun'>)] = lambda x: NArg(name = x.content)
grammar[(<class 'ulf_parser.TAdj'>, <class 'ulf_parser.NArg'>)] = lambda x, y: NArg(name = y.name, mod = y.mod + [x.content], det = y.det, plur = y.plur)
grammar[("TDet", "NArg")] = lambda x, y: NArg(name = y.name, mod = y.mod, det = x.content, plur = y.plur)
grammar[("TPlur", "TNoun")] = lambda x, y: NArg(name = None, mod = None, det = None, plur = True)
grammar[("TDet", "TNoun")] = lambda x, y: NArg(name = None, mod = None, det = x.content, plur = False)
grammar[("NArg", "TPrep", "NArg")] = lambda x, y, z: NRel(y.token, x, z)

class NRel(TreeNode):
    def __init__(self, token, arg1, arg2):
        self.relation = token
        self.arg1 = arg1
        self.arg2 = arg2
    
class Block(object):
    def __init__(self, token):
        self.block = token

class TDet(TreeNode):
    def __init__(self, content=None):
        super(TDet, self).__init__(content, None)

class TPrep(TreeNode):
    def __init__(self, content=None):
        super(TPrep, self).__init__(content, None)

class TNoun(TreeNode):
    def __init__(self, content=None):
        super(TNoun, self).__init__(content, None)

class TName(TreeNode):
    def __init__(self, content=None):
        super(TName, self).__init__(content, None)

class TPro(TreeNode):
    def __init__(self, content=None):
        super(TPro, self).__init__(content, None)

class TAdj(TreeNode):
    def __init__(self, content=None):
        super(TAdj, self).__init__(content, None)

class TPlur(TreeNode):
    def __init__(self):
        pass

class TPred(TreeNode):
    def __init__(self, content=None):
        super(TPred, self).__init__(content, None)

class TQ(TreeNode):
    def __init__(self):
        pass

class NColl(TreeNode):
    def __init__(self, children):
        super(NColl, self).__init__(None, children)

class NYesNo(TreeNode):
    def __init__(self, children):
        super(NYesNo, self).__init__(None, children)

class NArg(TreeNode):
    def __init__(self, name=None, mod=None, det=None, plur=False):
        self.name = Name
        self.mod = mod
        self.det = det
        self.plur = plur
       
class ULFQuery(object):
    def __init__(self, input):
        self.query = self.parse_tree(self.lispify(input))

    def terminal_node(self, token):
        if token in relations:
            return TPrep(token)
        elif '.d' in token or token == 'k':
            return TDet(token)
        elif '|' in token:
            return TName(token)
        elif '.pro' in token:
            return TPro(token)
        elif token == 'coll-of' or token == 'semval':
            return TPred(token)
        elif '.n' in token:
            return TNoun(token)
        elif token == '?':
            return TQ()
        elif token == 'plur':
            return TPlur()

    def parse_tree(self, tree):
        #print ("TREE:", tree)
        if type(tree) != list:
            return self.terminal_node(tree)
        else:
            old_tree = tree
            tree = list(map(self.parse_tree, tree))
            #print ("TREE:", old_tree, tree)
        if type(tree[0]) == TQ:
            return NYesNo(tree[1])
        elif len(tree) == 2:
            print (type(tree[0]))
            if (type(tree[0]), type(tree[1])) in grammar:
                print("result", grammar[(type(tree[0]), type(tree[1]))](tree[0], tree[1]))
                return grammar[(type(tree[0]), type(tree[1]))](tree[0], tree[1])
        elif len(tree) == 3:
            if (type(tree[0]), type(tree[1]), type(tree[2])) in grammar:
                return grammar[(type(tree[0]), type(tree[1]), type(tree[2]))](tree[0], tree[1], tree[2])      
        
    def lispify(self, input):
        stack = []
        current = []
        token = ""
        for char in input:
            if char == '(':
                stack.append(current)
                current = []
            elif char == ')':
                if token != "":
                    current += [token]
                    token = ""                
                if (len(stack) > 0):
                    stack[-1].append(current)
                    current = stack[-1]
                    stack.pop()                    
            elif char == ' ':
                if token != "":
                    current += [token]
                    token = ""
            else:
                token += char
        return current[0]               
             
    def parse(self, input):
        current = ""
        nodes = []        
        for char in input:
            if char == '(':
                pass
            elif char == ' ':
                if current != "":
                    nodes += [TreeNode(current)]
                    current = ""                    
            else:
                current += char                

        if input[0] == '(':
            nodes += [self.parse(input[1:])]
        elif input[0] == ')':
            return TreeNode(None, nodes)

'''
str = "(? ((the.d (|SRI|.n block.n)) on.p (the.d (|Target|.n block.n))))"
str = "(? ((some.d block.n) on.p (the.d (|Target|.n block.n))))"
str = "((what.d block.n) on.p (the.d (|SRI|.n block.n)))"
str = "((the.d (|SRI|.n block.n)) on.p what.pro)"
str = "((coll-of |B1| |B2| |B3|) (semval (what.d shape-pred.n)))"
query = ULFQuery(str)
print (query.query)
'''

#det = Det("test", ["children"])
#print(det.printable())
