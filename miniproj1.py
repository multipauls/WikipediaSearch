import nltk
import timeit
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")
from collections import defaultdict
import timeit
import xml.sax
import re
words= defaultdict(dict)
titles=defaultdict(str)
docCount=0
stemmap=defaultdict(lambda:"")
def stemming(word):
    if stemmap[word]=="":
        stemmap[word]=stemmer.stem(word)
    return stemmer.stem(word)
def parsetext(text):
    newtext =""
    text = re.sub(u'=References==[^=]*=','=',text)
    text = re.sub(u'=External links==[^=]*=','=',text)
    text = re.sub(u'[^a-zA-Z0-9 ]+',' ',text)
    text = re.sub(u'[ ]+',' ',text)
    text = re.split(" ", text)
    for i in text:
        newtext+=(stemming(i)+" ")
    print(newtext)

class WikiHandler( xml.sax.ContentHandler):
    
    def __init__(self):
        self.page=0
        self.id=0
        self.text=0
        self.title=0
        self.count=0
        self.count_title=0
        self.bufid=""
        self.title_words=defaultdict(int)
        self.body_words=defaultdict(int)

    
    def startElement(self,tag,attr):
        global docCount
        if(tag=="id" and self.page==0):
            self.page=1
            self.id=1
            self.bufid=""
            docCount+=1
        elif(tag=="title"):
            self.title=1
            self.buftitle=""
        elif(tag=="text"):
            self.text=1
            self.buftext=""
            
    def characters(self,data):
        if (self.id==1 and self.page==1):
            self.bufid += data
            titles[int(self.bufid)]=self.buftitle
        elif(self.title==1 ):
            self.buftitle += data
        elif(self.text==1):
            self.buftext += data
       
                     
    def endElement(self,tag):
        #global fp_titlefile
        if(tag=="page"):
            self.page=0
            self.count+=1
            self.count_title+=1
        if(tag=="title"):
            self.title=0
        if(tag=="id"):
            self.id=0
        if(tag=="text"):
            self.text=0
            parsetext(self.buftext)
                
if __name__ == "__main__":                                            #main
    start = timeit.default_timer()
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    Handler = WikiHandler()
    parser.setContentHandler( Handler )
   
    parser.parse("wiki_text.txt")
    stop = timeit.default_timer()
    print (stop - start)