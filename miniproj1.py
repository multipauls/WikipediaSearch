#total 30302
import nltk

import timeit
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")
from collections import defaultdict
import xml.sax
import re
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
words= defaultdict(dict)
titles=defaultdict(str)
docCount=0
stemmap=defaultdict(lambda:"")
start = 0

def parsetext(text,id):
    global stemmap
    global words
    newtext =""
    newcat=""
    newlink=""
    newref=""
    newinfo=""
    info = " "
    info = info.join(re.findall(u'{{infobox[^}]*\n}}', text))
    info = re.sub(u'[^a-zA-Z0-9 ]+',' ',info)
    info = re.sub(u'[ ]+',' ',info)
    info = re.split(" ", info)
    for i in info:
        if i not in stop_words:
            #print(i)
            if stemmap[i]=="":
                stemmap[i]=stemmer.stem(i)
            #if words[i]=="":
            #    words[i]==
            newinfo+=(stemmap[i]+" ")
    print(newinfo)
    ref=" "
    ref = ref.join(re.findall(u'==References==[^=]+\n=', text))
    ref = re.sub(u'[^a-zA-Z0-9 ]+',' ',ref)
    ref = re.sub(u'[ ]+',' ',ref)
    ref = re.split(" ", ref)
    for i in ref:
        if i not in stop_words:
            if stemmap[i]=="":
                stemmap[i]=stemmer.stem(i)
            #if words[i]=="":
            #    words[i]==
            newref+=(stemmap[i]+" ")
    #print(newref)
    links=" "
    links = links.join(re.findall(u'==External links==[^=]+\n=', text))
    links = re.sub(u'[^a-zA-Z0-9 ]+',' ',links)
    links = re.sub(u'[ ]+',' ',links)
    links = re.split(" ", links)
    for i in links:
        if i not in stop_words:
            if stemmap[i]=="":
                stemmap[i]=stemmer.stem(i)
            #if words[i]=="":
            #    words[i]==
            newlink+=(stemmap[i]+" ")
            
    cat =" "
    cat = cat.join(re.findall(u'\[\[Category:(.*?)\]\]', text))
    cat = re.sub(u'[^a-zA-Z0-9 ]+',' ',cat)
    cat = re.sub(u'[ ]+',' ',cat)
    cat = re.split(" ", cat)
    for i in cat:
        if i not in stop_words:
            if stemmap[i]=="":
                stemmap[i]=stemmer.stem(i)
            #if words[i]=="":
            #    words[i]==
            newcat+=(stemmap[i]+" ")

    text = re.sub(u'{{infobox[^}]*\n}}'," ", text)
    text = re.sub(u'==References==[^=]+\n=',' ', text)
    text = re.sub(u'==External links==[^=]+\n=',' ', text)
    text = re.sub(u'\[\[Category:(.*?)\]\]',' ', text)
    text = re.sub(u'[^a-zA-Z0-9 ]+',' ',text)
    text = re.sub(u'[ ]+',' ',text)
    text = re.split(" ", text)
    for i in text:
        if i not in stop_words:
            if stemmap[i]=="":
                stemmap[i]=stemmer.stem(i)
            #if words[i]=="":
            #    words[i]==
            newtext+=(stemmap[i]+" ")

class WikiHandler( xml.sax.ContentHandler):
    
    def __init__(self):
        self.page=0
        self.id=0
        self.text=0
        self.title=0
        self.count=0
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
        if(tag=="title"):
            self.title=0
        if(tag=="id"):
            self.id=0
        if(tag=="text"):
            self.text=0
            parsetext(self.buftext, self.bufid)
            if int(self.bufid)%200 == 0:
                print(timeit.default_timer()-start)
                print(self.bufid)
                
if __name__ == "__main__":                                            
    start = timeit.default_timer()
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    Handler = WikiHandler()
    parser.setContentHandler( Handler )
   
    parser.parse("wiki_text.txt")
    stop = timeit.default_timer()
    print (stop - start)