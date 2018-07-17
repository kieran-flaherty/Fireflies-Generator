import urllib.request
import json
from random import randint
from os import path

def get_ryhmes(word):
    '''Returns a list of rhymes pulled from the datamuse API'''
    api_url = 'https://api.datamuse.com/words?rel_rhy={0}&md=s'
    with urllib.request.urlopen(api_url.format(word)) as data:
        data = json.loads(data.read())
    words = []
    for d in data:
        words.append(d['word'])
    return words

def get_last(phrase):
    '''Return last word of a phrase'''

    words = phrase.split(' ')
    return words[-1]

def generate():
    '''generates a lyric of the form
     "you would not believe your {x} if 10,000 {y}" '''
    
    
    with open(path.join(path.dirname(__file__),'list.txt')) as f: #get words from filr
        body_parts = f.readlines()
    
    for i,b in enumerate(body_parts):
        body_parts[i] = b.strip('\n') #Strip trailing whitespace
    
    x = body_parts[randint(0,len(body_parts)-1)]
    ryhmes = get_ryhmes(get_last(x))

    if ryhmes == []: #Calls function again within itself if no rhymes are found
        return generate()

    y = ryhmes[randint(0,len(ryhmes)-1)]

    return 'You would not beleive your {0} if 10,000 {1}'.format(x,y)

def write_examples(x):
    '''Writes x examples to the text file'''
    for i in range(1,x+1):
        with open(path.join(path.dirname(__file__),'examples.txt'),'a+') as f:
            f.write(generate()+'\n')



# Originally wrote this function to pull rhymes from rhymezone,
# but it was buggy and only worked with certain words depending on the format of
# the pages HTML, then I found the datamuse API

# def get_ryhmes(word):
#     '''Returns the 3 syllable rhymes of a word'''

#     url = 'https://www.rhymezone.com/r/rhyme.cgi?typeofrhyme=perfect&loc=thesql&Word='+word
#     html = urllib.request.urlopen(url).read() 
#     html = str(html) #Converts hmtl to string from bytes

#     three_syl = html[html.find('3 syllables'):html.find('4 syllables')] #Only interested in words with 3 syllables
#     three_syl = three_syl.split('\\n') #Splits string into a list
    
#     for i,l in enumerate(three_syl):
#         if any(char in l for char in ['(',')',' ','<','>']):
#             three_syl.pop(i) 
        
            
#     three_syl.pop(0) #remove first object from list as it isnt a word
#     words = []
#     for i in three_syl:
#         r = i[i.find('\">')+2:i.find('</a')] #r is a line in the HTML that might contain a rhyme (manually inspected it for this)
#         if '&' in r or ';' in r or r == 'b' or r == 'br' or 'd\\' in r: #Filters our items that are not words
#             pass
#         else:
#             words.append(r) #add r to words

#     return words
