from spatial import *
#from main import *

#List of  possible color modifiers
color_mods = ['black', 'red', 'blue', 'brown', 'green', 'yellow']

#Searches and returns the entity that has the given name
#associated with it
#Inputs: name - human-readable name as a string
#Return value: entity (if exists) or None
def get_entity_by_name(name, entities):
    for entity in entities:
        #print("NAME:",name, entity.name)
        if entity.name.lower() == name.lower():
            return entity
    for col in color_mods:
        if col in name:
            name = name.replace(col + " ", "")
            #print ("MOD NAME:", name)
    for entity in entities:
        #print(name, entity.name)
        if entity.name.lower() == name.lower():
            return entity
    return None


#Given the relations argument specification, returns the entities that
#satisfy that specification
#Inputs: arg - argument object
#Return value: the list of entities
def get_argument_entities(arg, entities):
    ret_val = [get_entity_by_name(arg.token, entities)]
    if ret_val == [None]:
        ret_val = []
        for entity in entities:            
            #print ("TYPE_STR: {} {}".format(entity.name, entity.type_structure))
            if (entity.type_structure is None):
                print ("NONE STRUCTURE", entity.name)                
            if (arg.token in entity.type_structure or arg.token in entity.name.lower() or arg.token == "block" and "cube" in entity.type_structure) \
               and (arg.mod is None or arg.mod.adj is None or arg.mod.adj == "" or entity.color_mod == arg.mod.adj or arg.mod.adj in entity.type_structure[-1].lower()):
                ret_val += [entity]    
    return ret_val



#Filters the entities list according to the set of constraints, i.e.,
#returns the list of entities satisfying certain criteria
#Inputs: entities - list of entities; constaints - list of constraints in the
#form (type, value), e.g., (color_mod, 'black')
#Return value: list of entities
def filter(entities, constraints):
    result = []
    for entity in entities:
        isPass = True
        for cons in constraints:
            #print("TYPE_STR:", entity.name, entity.get_type_structure())
            if cons[0] == 'type' and entity.get_type_structure()[-2] != cons[1]:
                isPass = False
            elif cons[0] == 'color_mod' and entity.color_mod != cons[1]:
                isPass = False
        if isPass:
            result.append(entity)
    return result


#For a description task, finds the best candiadate entity
#Inputs: relation - relation name (string), rel_constraints - the list of constraints
#imposed on the relatum, referents - the list of referent entities
#Return value: the best candidate entity
def eval_find(relation, rel_constraints, referents):
    candidates = filter(entities, rel_constraints)
    print ("CANDIDATES: {}".format(candidates))
    scores = []
    if len(referents[0]) == 1 or relation == "between":
        scores = [(cand, cand.name, max([globals()[rf_mapping[relation]](cand, *ref) for ref in referents if cand not in ref])) for cand in candidates]
    else:
        scores = [(cand, cand.name, max([np.mean([globals()[rf_mapping[relation]](cand, ref) for ref in refset]) for refset in referents if cand not in refset])) for cand in candidates]
    print ("SCORES: {}".format(scores))
    max_score = 0
    best_candidate = None
    for ev in scores:
        if ev[2] > max_score:
            max_score = ev[2]
            best_candidate = ev[0]
    return best_candidate

#Processes a truth-judgement annotation
#Inputs: relation, relatum, referent1, referent2 - strings, representing
#the relation and its arguments; response - user's response for the test
#Return value: the value of the corresponding relation function
def process_truthjudg(relation, relatum, referent1, referent2, response, entities):
    relatum = get_entity_by_name(relatum, entities)
    referent1 = get_entity_by_name(referent1, entities)
    referent2 = get_entity_by_name(referent2, entities)
    print (relatum, referent1, referent2)
    if relation != "between":
        return globals()[rf_mapping[relation]](relatum, referent1)
    else: return globals()[rf_mapping[relation]](relatum, referent1, referent2)

#Extracts the constraints (type and color) for the relatum argument
#from the parsing result.
#Inputs: relatum - string, representing the relation argument;
#rel_constraints - the type and color properties of the relatum
#Return value: The list of pairs ('constraint_name', 'constraint_value')
def get_relatum_constraints(relatum, rel_constraints):
    ret_val = [('type', relatum.get_type_structure()[-2]), ('color_mod', relatum.color_mod)]
    return ret_val

#Processes a description-tast annotation
#Inputs: relatum - string, representing the relation argument;
#response - user's response for the test
#Return value: the best-candidate entity fo the given description
def process_descr(relatum, response):
    rel_constraint = parse(response)
    if rel_constraint is None:
        return None
    relatum = get_entity_by_name(relatum)
    #print ("REF: {}".format(rel_constraint.referents))
    if rel_constraint is None:
        return "*RESULT: NO RELATIONS*"
    referents = list(itertools.product(*[get_argument_entities(ref) for ref in rel_constraint.referents]))
    print("REFS:", referents)
    relation = rel_constraint.token
    return eval_find(relation, get_relatum_constraints(relatum, rel_constraint), referents)