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


countwords=defaultdict(dict)
def parsetext(text,title, id):
    global stemmap
    global countwords
    global wordcount
    info = " "
    info = info.join(re.findall(u'{{infobox[^}]*\n}}', text))
    info = re.sub(u'{{infobox',' ',info)
    info = re.sub(u'[^a-zA-Z0-9 ]+',' ',info)
    info = re.sub(u'[ ]+',' ',info)
    info = info.lower()
    info = re.split(" ", info)
    wordcount+=len(info)
    for i in info:
        if i not in stop_words and len(i)>1:

            if stemmap[i]=="":
                stemmap[i]=stemmer.stem(i)
            if not countwords[stemmap[i]].get("d"):
                countwords[stemmap[i]]['d']=0
            if not countwords[stemmap[i]].get("tot"):
                countwords[stemmap[i]]['tot']=0
            if not countwords[stemmap[i]].get(id):
                countwords[stemmap[i]]['d']+=1
                countwords[stemmap[i]][id]=dict()
            if not countwords[stemmap[i]][id].get("i"):
                countwords[stemmap[i]][id]["i"]=0
            countwords[stemmap[i]]['tot']+=1
            countwords[stemmap[i]][id]["i"]+=1
            
    ref=" "
    ref = ref.join(re.findall(u'==References==[^=]+\n=', text))
    ref = re.sub(u'==References==',' ',ref)
    ref = re.sub(u'{{Reflist}}',' ',ref)
    ref = re.sub(u'{{Refbegin}}',' ',ref)
    ref = re.sub(u'{{Refend}}',' ',ref) 
    ref = re.sub(u'[^a-zA-Z0-9 ]+',' ',ref)
    ref = ref.lower()
    ref = re.sub(u'http',' ',ref)
    ref = re.sub(u'www',' ',ref)
    ref = re.sub(u'[ ]+',' ',ref)
    ref = re.split(" ", ref)
    wordcount+=len(ref)
    for i in ref:
        if i not in stop_words and len(i)>1:
            if stemmap[i]=="":
                stemmap[i]=stemmer.stem(i)
            if not countwords[stemmap[i]].get("d"):
                countwords[stemmap[i]]['d']=0
            if not countwords[stemmap[i]].get("tot"):
                countwords[stemmap[i]]['tot']=0
            if not countwords[stemmap[i]].get(id):
                countwords[stemmap[i]]['d']+=1
                countwords[stemmap[i]][id]=dict()
            if not countwords[stemmap[i]][id].get("r"):
                countwords[stemmap[i]][id]["r"]=0
            countwords[stemmap[i]]['tot']+=1
            countwords[stemmap[i]][id]["r"]+=1

    links=" "
    links = links.join(re.findall(u'==External links==[^=]+\n=', text))
    links = re.sub(u'==External links==',' ',links)
    links = re.sub(u'[^a-zA-Z0-9 ]+',' ',links)
    links = links.lower()
    links = re.sub(u'http',' ',links)
    links = re.sub(u'www',' ',links)    
    links = re.sub(u'[ ]+',' ',links)
    links = re.split(" ", links)
    wordcount+=len(links)
    for i in links:
        if i not in stop_words and len(i)>1:
            if stemmap[i]=="":
                stemmap[i]=stemmer.stem(i)
            if not countwords[stemmap[i]].get("d"):
                countwords[stemmap[i]]['d']=0
            if not countwords[stemmap[i]].get("tot"):
                countwords[stemmap[i]]['tot']=0
            if not countwords[stemmap[i]].get(id):
                countwords[stemmap[i]]['d']+=1
                countwords[stemmap[i]][id]=dict()
            if not countwords[stemmap[i]][id].get("l"):
                countwords[stemmap[i]][id]["l"]=0
            countwords[stemmap[i]]['tot']+=1
            countwords[stemmap[i]][id]["l"]+=1


            
    cat =" "
    cat = cat.join(re.findall(u'\[\[Category:(.*?)\]\]', text))
    cat = re.sub(u'[^a-zA-Z0-9 ]+',' ',cat)
    cat = re.sub(u'\[\[Category',' ',cat)
    cat = cat.lower()
    cat = re.sub(u'[ ]+',' ',cat)
    cat = re.split(" ", cat)
    wordcount+=len(cat)
    for i in cat:
        if i not in stop_words and len(i)>1:
            if stemmap[i]=="":
                stemmap[i]=stemmer.stem(i)

            if not countwords[stemmap[i]].get("d"):
                countwords[stemmap[i]]['d']=0
            if not countwords[stemmap[i]].get("tot"):
                countwords[stemmap[i]]['tot']=0
            if not countwords[stemmap[i]].get(id):
                countwords[stemmap[i]]['d']+=1
                countwords[stemmap[i]][id]=dict()            
            if not countwords[stemmap[i]][id].get("c"):
                countwords[stemmap[i]][id]["c"]=0
            countwords[stemmap[i]]['tot']+=1
            countwords[stemmap[i]][id]["c"]+=1


    titletext = re.sub(u'[^a-zA-Z0-9 ]+',' ',title)
    titletext = titletext.lower()
    titletext = re.sub(u'[ ]+',' ',titletext)
    titletext = re.split(" ", titletext)
    wordcount+=len(titletext)
    for i in titletext:
        if i not in stop_words and len(i)>1:
            if stemmap[i]=="":
                stemmap[i]=stemmer.stem(i)
            if not countwords[stemmap[i]].get("d"):
                countwords[stemmap[i]]['d']=0
            if not countwords[stemmap[i]].get("tot"):
                countwords[stemmap[i]]['tot']=0
            if not countwords[stemmap[i]].get(id):
                countwords[stemmap[i]]['d']+=1
                countwords[stemmap[i]][id]=dict()
            if not countwords[stemmap[i]][id].get("t"):
                countwords[stemmap[i]][id]["t"]=0
            countwords[stemmap[i]]['tot']+=1
            countwords[stemmap[i]][id]["t"]+=1


    text = re.sub(u'{{infobox[^}]*\n}}'," ", text)
    text = re.sub(u'==References==[^=]+\n=',' ', text)
    text = re.sub(u'==External links==[^=]+\n=',' ', text)
    text = re.sub(u'\[\[Category:(.*?)\]\]',' ', text)
    text = text.lower()
    text = re.sub(u'{{sfn[^}]+}}',' ', text)
    text = re.sub(u'[^a-zA-Z0-9 ]+',' ',text)
    text = re.sub(u'[ ]+',' ',text)
    text = re.split(" ", text)
    wordcount+=len(text)
    for i in text:
        if i not in stop_words and i != "" and len(i)>1:
            #print(i)
            if stemmap[i]=="":
                stemmap[i]=stemmer.stem(i)
            if not countwords[stemmap[i]].get("d"):
                countwords[stemmap[i]]['d']=0
            if not countwords[stemmap[i]].get("tot"):
                countwords[stemmap[i]]['tot']=0
            if not countwords[stemmap[i]].get(id):
                countwords[stemmap[i]]['d']+=1
                countwords[stemmap[i]][id]=dict()
            if not countwords[stemmap[i]][id].get("b"):
                countwords[stemmap[i]][id]["b"]=0
            countwords[stemmap[i]]['tot']+=1            
            countwords[stemmap[i]][id]["b"]+=1
        #print(stemmap[i], end="")
        #if countwords[stemmap[i]]!={}:
            #print(countwords[stemmap[i]])

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
    f = open(sys.argv[2]+"/index.txt","w")
    for i in countwords.keys():
        f.write(str(i)+'|f'+str(countwords[i]["tot"])+'d'+str(countwords[i]["d"])+':')
        for j in countwords[i].keys():
                if j not in ["tot","d"]:
                    f.write(str(j))
                    for k in countwords[i][j].keys():
                            f.write(str(k)+str(countwords[i][j][k]))
                    f.write(";")
        f.write('\n')
    f.close()
    f = open(sys.argv[2]+"/titles.txt","wb")
    pickle.dump(titleslist,f, protocol=pickle.HIGHEST_PROTOCOL)
    f.close()
    f = open(sys.argv[3],"w")
    f.write(str(wordcount)+str('\n')+str(len(countwords)))
    f.close()
    print(sys.getsizeof(str(countwords)))
    stop = timeit.default_timer()
    print (stop - start)
