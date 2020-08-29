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
stemmap=defaultdict(lambda:"")
start = 0
wordcount=0
def retdict():
    return defaultdict(int)

countwords=defaultdict(retdict)
def parsetext(text,title, id):
    global stemmap
    global countwords
    global wordcount
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

            if countwords[stemmap[i]][id] == 0:
                countwords[stemmap[i]]['docs']+=1
                countwords[stemmap[i]][id]=defaultdict(int)
            countwords[stemmap[i]]['total']+=1
            countwords[stemmap[i]][id]["info"]+=1

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
            

            if countwords[stemmap[i]][id] == 0:
                countwords[stemmap[i]]['docs']+=1
                countwords[stemmap[i]][id]=defaultdict(int)
            countwords[stemmap[i]]['total']+=1
            countwords[stemmap[i]][id]["ref"]+=1

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
            
            if countwords[stemmap[i]][id] == 0:
                countwords[stemmap[i]]['docs']+=1
                countwords[stemmap[i]][id]=defaultdict(int)
            countwords[stemmap[i]]['total']+=1
            countwords[stemmap[i]][id]["link"]+=1


            
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

            
            if countwords[stemmap[i]][id] == 0:
                countwords[stemmap[i]]['docs']+=1
                countwords[stemmap[i]][id]=defaultdict(int)
            countwords[stemmap[i]]['total']+=1
            countwords[stemmap[i]][id]["cat"]+=1


    titletext = re.sub(u'[^a-zA-Z0-9 ]+',' ',title)
    titletext = re.sub(u'[ ]+',' ',titletext)
    titletext = re.split(" ", titletext)
    wordcount+=len(titletext)
    for i in titletext:
        if i not in stop_words:
            if stemmap[i]=="":
                stemmap[i]=stemmer.stem(i)

            if countwords[stemmap[i]][id] == 0:
                countwords[stemmap[i]]['docs']+=1
                countwords[stemmap[i]][id]=defaultdict(int)
            countwords[stemmap[i]]['total']+=1
            countwords[stemmap[i]][id]["title"]+=1


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

            if countwords[stemmap[i]][id] == 0:
                countwords[stemmap[i]]['docs']+=1
                countwords[stemmap[i]][id]=defaultdict(int)
            countwords[stemmap[i]]['total']+=1            
            countwords[stemmap[i]][id]["title"]+=1


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
            if int(self.bufid)%300 ==0:
                print(timeit.default_timer()-start)
                print(self.bufid)
if __name__ == "__main__":                                            
    start = timeit.default_timer()
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    Handler = WikiHandler()
    parser.setContentHandler( Handler )
    parser.parse(sys.argv[1])
    filetext = dict(countwords)
    titleslist=dict(titles)
    f = open(sys.argv[2]+"/index.txt","wb")
    pickle.dump(filetext,f)

    #for word in countwords:
    #    f.write("||"+word+"|")
    #    for id in countwords[word]:
    #        f.write(str(id)+':'+str(countwords[word][id])+"|")

    #f.close()
    f = open(sys.argv[2]+"/titles.txt","wb")
    pickle.dump(titleslist,f)
    f.close()
    f = open(sys.argv[3],"w")
    f.write(str(wordcount)+str('\n')+str(len(countwords)))
    f.close()
    stop = timeit.default_timer()
    print (stop - start)
