import sys
import nltk
import timeit
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")
from collections import defaultdict
import xml.sax
import re
from nltk.corpus import stopwords
import pickle
stop_words = set(stopwords.words('english'))
titles=defaultdict(str)
countwords=defaultdict(lambda:defaultdict(int))
stemmap=defaultdict(lambda:"")
start = 0
wordcount=0
def parsetext(text,title, id):
    global stemmap
    global countwords
    global wordcount
    newtext =defaultdict(lambda:0)
    newcat=defaultdict(lambda:0)
    newlink=defaultdict(lambda:0)
    newref=defaultdict(lambda:0)
    newinfo=defaultdict(lambda:0)
    newtitle=defaultdict(lambda:0)
    newdoc=defaultdict(lambda:0)
    info = " "
    info = info.join(re.findall(u'{{infobox[^}]*\n}}', text))
    info = re.sub(u'[^a-zA-Z0-9 ]+',' ',info)
    info = re.sub(u'[ ]+',' ',info)
    info = re.split(" ", info)
    wordcount+=len(info)
    for i in info:
        if i not in stop_words:

            if stemmap[i]=="":
                stemmap[i]=stemmer.stem(i)

            newinfo[stemmap[i]]+=1
            if countwords[stemmap[i]][id] == 0:
                countwords[stemmap[i]]['docs']+=1
            countwords[stemmap[i]][id]+=1
            countwords[stemmap[i]]['total']+=1


    ref=" "
    ref = ref.join(re.findall(u'==References==[^=]+\n=', text))
    ref = re.sub(u'[^a-zA-Z0-9 ]+',' ',ref)
    ref = re.sub(u'[ ]+',' ',ref)
    ref = re.split(" ", ref)
    wordcount+=len(ref)
    for i in ref:
        if i not in stop_words:
            if stemmap[i]=="":
                stemmap[i]=stemmer.stem(i)
            

            newref[stemmap[i]]+=1
            if countwords[stemmap[i]][id] == 0:
                countwords[stemmap[i]]['docs']+=1
            countwords[stemmap[i]][id]+=1
            countwords[stemmap[i]]['total']+=1

    links=" "
    links = links.join(re.findall(u'==External links==[^=]+\n=', text))
    links = re.sub(u'[^a-zA-Z0-9 ]+',' ',links)
    links = re.sub(u'[ ]+',' ',links)
    links = re.split(" ", links)
    wordcount+=len(links)
    for i in links:
        if i not in stop_words:
            if stemmap[i]=="":
                stemmap[i]=stemmer.stem(i)
            
            newlink[stemmap[i]]+=1
            if countwords[stemmap[i]][id] == 0:
                countwords[stemmap[i]]['docs']+=1
            countwords[stemmap[i]][id]+=1
            countwords[stemmap[i]]['total']+=1


            
    cat =" "
    cat = cat.join(re.findall(u'\[\[Category:(.*?)\]\]', text))
    cat = re.sub(u'[^a-zA-Z0-9 ]+',' ',cat)
    cat = re.sub(u'[ ]+',' ',cat)
    cat = re.split(" ", cat)
    wordcount+=len(cat)
    for i in cat:
        if i not in stop_words:
            if stemmap[i]=="":
                stemmap[i]=stemmer.stem(i)

            
            newcat[stemmap[i]]+=1
            if countwords[stemmap[i]][id] == 0:
                countwords[stemmap[i]]['docs']+=1
            countwords[stemmap[i]][id]+=1
            countwords[stemmap[i]]['total']+=1


    titletext = re.sub(u'[^a-zA-Z0-9 ]+',' ',title)
    titletext = re.sub(u'[ ]+',' ',titletext)
    titletext = re.split(" ", titletext)
    wordcount+=len(titletext)
    for i in titletext:
        if i not in stop_words:
            if stemmap[i]=="":
                stemmap[i]=stemmer.stem(i)

            newtitle[stemmap[i]]+=1
            if countwords[stemmap[i]][id] == 0:
                countwords[stemmap[i]]['docs']+=1
            countwords[stemmap[i]][id]+=1
            countwords[stemmap[i]]['total']+=1


    text = re.sub(u'{{infobox[^}]*\n}}'," ", text)
    text = re.sub(u'==References==[^=]+\n=',' ', text)
    text = re.sub(u'==External links==[^=]+\n=',' ', text)
    text = re.sub(u'\[\[Category:(.*?)\]\]',' ', text)
    text = re.sub(u'[^a-zA-Z0-9 ]+',' ',text)
    text = re.sub(u'[ ]+',' ',text)
    text = re.split(" ", text)
    wordcount+=len(text)
    for i in text:
        if i not in stop_words:
            if stemmap[i]=="":
                stemmap[i]=stemmer.stem(i)

            newtext[stemmap[i]]+=1
            if countwords[stemmap[i]][id] == 0:
                countwords[stemmap[i]]['docs']+=1
            countwords[stemmap[i]][id]+=1
            countwords[stemmap[i]]['total']+=1
    #print(countwords)


class WikiHandler( xml.sax.ContentHandler):
    
    def __init__(self):
        self.page=0
        self.id=0
        self.text=0
        self.title=0
        self.bufid=""

    
    def startElement(self,tag,attr):
        if(tag=="id" and self.page==0):
            self.page=1
            self.id=1
            self.bufid=""
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
        
        if(tag=="page"):
            self.page=0
        if(tag=="title"):
            self.title=0
        if(tag=="id"):
            self.id=0
        if(tag=="text"):
            self.text=0
            parsetext(self.buftext, self.buftitle, self.bufid)
                
if __name__ == "__main__":                                            
    start = timeit.default_timer()
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    Handler = WikiHandler()
    parser.setContentHandler( Handler )
    parser.parse(sys.argv[1])
    filetext=dict(countwords)
    f = open(sys.argv[2],"wb")
    pickle.dump(filetext,f)
    f.close()
    f = open(sys.argv[3],"w")
    f.write(str(wordcount)+str('\n')+str(len(countwords)))
    f.close()
    stop = timeit.default_timer()
    print (stop - start)
