relations = ['on', 'above', 'below', 'left', 'right', 'at', 'touching', 'near', 'in front of', 'behind', 'over', 'under', 'in', 'between']
colors = ['black', 'red' ,'brown', 'green', 'blue', 'yellow']
objects = ['table', 'block', 'book', 'chair', 'bookshelf']

def parse_response(resp):
    
    return 0


count = 0
for subm in open('dump').read().split('###'):
    subm = subm.strip().split(':')
    if len(subm) >= 9 and int(subm[0]) >= 1000100:
        for resp in subm[8].split('\n'):
            response = [subm[4], resp]
            count += 1
            print (response)

print (count)
