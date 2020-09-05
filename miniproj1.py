import sys
import timeit
import nltk
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")
from collections import defaultdict
import xml.sax
import re
import os
#import regex
stop_words = {"a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thick", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"}
titles=[""]
stemmap=defaultdict(lambda:"")
start = 0
wordcount=0
artcount = 0
stemcount =0
countwords=defaultdict(dict)
fcount = 0
def writetext(wpath):
    global countwords
    global stemcount
    global fcount
    global t
    global titles
    countwords = dict(countwords)
    countwords ={k: countwords[k] for k in sorted(countwords)}
    if not os.path.exists(wpath):
        os.mkdir(wpath)
    fname = "index"+str(fcount)+".txt"
    f = open(os.path.join(wpath,fname),"w")
    for i in countwords.keys():
        writestr=""
        writestr+=(str(i)+'|F'+str(countwords[i]["tot"])+'D'+str(countwords[i]["d"])+':')
        for j in countwords[i].keys():
                if j not in ["tot","d"]:
                    writestr+=(str(j))
                    for k in countwords[i][j].keys():
                            writestr+=(str(k)+str(countwords[i][j][k]))
                    writestr+=str(";")
        writestr+=('\n')
        f.write(writestr)
    f.close()
    t.write(titles[0])
    t.close()
    del(titles[0])
    titles.append("")
    t= open(os.path.join(wpath,"titles.txt"),"a")
    stemcount+=len(countwords)
    countwords.clear()
    countwords=defaultdict(dict,countwords)
    fcount+=1
    
def parsetext(text,title):
    global stemmap
    global countwords
    global wordcount
    global artcount
    global titles
    artcount+=1
    wcdoc=0
    idx = artcount
    info = " "
    info = info.join(re.findall(u'{{infobox[^}]*\n}}', text))
    info = re.sub(u'{{infobox',' ',info)
    info = re.sub(u'[^a-zA-Z0-9 ]+',' ',info)
    info = re.sub(u'[^a-zA-Z1-9]0[0]+[1-9]*[^a-zA-Z1-9]',' ',info)
    info = re.sub(u'[^a-zA-Z1-9][0-9]{5,}[A-Za-z0-9]*[^a-zA-Z1-9]',' ',info)
    info = re.sub(u'[^a-zA-Z1-9][0-9]{5,}[^a-zA-Z1-9]',' ',info)
    info = re.sub(u'[ ]+',' ',info)
    info = info.lower()
    info = re.split(" ", info)
    wordcount+=len(info)
    wcdoc+=len(info)
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
                countwords[stemmap[i]][idx]=dict()
            if not countwords[stemmap[i]][idx].get("i"):
                countwords[stemmap[i]][idx]["i"]=0
            countwords[stemmap[i]]['tot']+=1
            countwords[stemmap[i]][idx]["i"]+=1
            
    ref=" "
    ref = ref.join(re.findall(u'==References==[^=]+\n=', text))
    ref = re.sub(u'==References==',' ',ref)
    ref = re.sub(u'{{Reflist}}',' ',ref)
    ref = re.sub(u'{{Refbegin}}',' ',ref)
    ref = re.sub(u'{{Refend}}',' ',ref) 
    ref = re.sub(u'[^a-zA-Z0-9 ]+',' ',ref)
    ref = re.sub(u'[^a-zA-Z1-9]0[0]+[1-9]*[^a-zA-Z1-9]',' ',ref)
    ref = re.sub(u'[^a-zA-Z1-9][0-9]{5,}[A-Za-z0-9]*[^a-zA-Z1-9]',' ',ref)
    ref = re.sub(u'[^a-zA-Z1-9][0-9]{5,}[^a-zA-Z1-9]',' ',ref)
    ref = ref.lower()
    ref = re.sub(u'http',' ',ref)
    ref = re.sub(u'www',' ',ref)
    ref = re.sub(u'[ ]+',' ',ref)
    ref = re.split(" ", ref)
    wordcount+=len(ref)
    wcdoc+=len(ref)
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
                countwords[stemmap[i]][idx]=dict()
            if not countwords[stemmap[i]][idx].get("r"):
                countwords[stemmap[i]][idx]["r"]=0
            countwords[stemmap[i]]['tot']+=1
            countwords[stemmap[i]][idx]["r"]+=1

    links=" "
    links = links.join(re.findall(u'==External links==[^=]+\n=', text))
    links = re.sub(u'==External links==',' ',links)
    links = re.sub(u'[^a-zA-Z0-9 ]+',' ',links)
    links = re.sub(u'[^a-zA-Z1-9]0[0]+[1-9]*[^a-zA-Z1-9]',' ',links)
    links = re.sub(u'[^a-zA-Z1-9][0-9]{5,}[A-Za-z0-9]*[^a-zA-Z1-9]',' ',links)
    links = re.sub(u'[^a-zA-Z1-9][0-9]{5,}[^a-zA-Z1-9]',' ',links)
    links = links.lower()
    links = re.sub(u'http',' ',links)
    links = re.sub(u'www',' ',links)    
    links = re.sub(u'[ ]+',' ',links)
    links = re.split(" ", links)
    wordcount+=len(links)
    wcdoc+=len(links)
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
                countwords[stemmap[i]][idx]=dict()
            if not countwords[stemmap[i]][idx].get("l"):
                countwords[stemmap[i]][idx]["l"]=0
            countwords[stemmap[i]]['tot']+=1
            countwords[stemmap[i]][idx]["l"]+=1


            
    cat =" "
    cat = cat.join(re.findall(u'\[\[Category:(.*?)\]\]', text))
    cat = re.sub(u'[^a-zA-Z0-9 ]+',' ',cat)
    cat = re.sub(u'\[\[Category',' ',cat)
    cat = re.sub(u'[^a-zA-Z1-9]0[0]+[1-9]*[^a-zA-Z1-9]',' ',cat)
    cat = re.sub(u'[^a-zA-Z1-9][0-9]{5,}[A-Za-z0-9]*[^a-zA-Z1-9]',' ',cat)
    cat = re.sub(u'[^a-zA-Z1-9][0-9]{5,}[^a-zA-Z1-9]',' ',cat)
    cat = cat.lower()
    cat = re.sub(u'[ ]+',' ',cat)
    cat = re.split(" ", cat)
    wordcount+=len(cat)
    wcdoc+=len(cat)
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
                countwords[stemmap[i]][idx]=dict()            
            if not countwords[stemmap[i]][idx].get("c"):
                countwords[stemmap[i]][idx]["c"]=0
            countwords[stemmap[i]]['tot']+=1
            countwords[stemmap[i]][idx]["c"]+=1


    titletext = re.sub(u'[^a-zA-Z0-9 ]+',' ',title)
    titletext = titletext.lower()
    titletext = re.sub(u'[ ]+',' ',titletext)
    titletext = re.split(" ", titletext)
    wordcount+=len(titletext)
    wcdoc+=len(titletext)
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
                countwords[stemmap[i]][idx]=dict()
            if not countwords[stemmap[i]][idx].get("t"):
                countwords[stemmap[i]][idx]["t"]=0
            countwords[stemmap[i]]['tot']+=1
            countwords[stemmap[i]][idx]["t"]+=1


    text = re.sub(u'{{infobox[^}]*\n}}'," ", text)
    text = re.sub(u'==References==[^=]+\n=',' ', text)
    text = re.sub(u'==External links==[^=]+\n=',' ', text)
    text = re.sub(u'\[\[Category:(.*?)\]\]',' ', text)
    text = text.lower()
    text = re.sub(u'{{sfn[^}]+}}',' ', text)
    text = re.sub(u'[^a-zA-Z0-9 ]+',' ',text)
    text = re.sub(u'[^a-zA-Z1-9]0[0]+[1-9]*[^a-zA-Z1-9]',' ',text)
    text = re.sub(u'[^a-zA-Z1-9][0-9]{5,}[A-Za-z0-9]*[^a-zA-Z1-9]',' ',text)
    text = re.sub(u'[^a-zA-Z1-9][0-9]{5,}[^a-zA-Z1-9]',' ',text)
    text = re.sub(u'[ ]+',' ',text)
    text = re.split(" ", text)
    wordcount+=len(text)
    wcdoc+=len(text)
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
                countwords[stemmap[i]][idx]=dict()
            if not countwords[stemmap[i]][idx].get("b"):
                countwords[stemmap[i]][idx]["b"]=0
            countwords[stemmap[i]]['tot']+=1            
            countwords[stemmap[i]][idx]["b"]+=1
    titles[0]+=(" "+str(wcdoc)+"\n")

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
            pass
        elif(self.title==1 ):
            self.buftitle += data
        elif(self.text==1):
            self.buftext += data
       
                     
    def endElement(self,tag):
        global artcount
        global wpath
        global titles
        if(tag=="page"):
            self.page=0
        if(tag=="title"):
            self.title=0
        if(tag=="id"):
            self.id=0
        if(tag=="text"):
            self.text=0
            parsetext(self.buftext, self.buftitle)
            self.bufid=artcount
            titles[0]+=(str(self.bufid)+" "+str(self.buftitle))
            if (self.bufid%300==0):
                print(timeit.default_timer()-start)
                print(self.bufid)
            if (self.bufid%20000==0):
                writetext(wpath)


if __name__ == "__main__":                                            
    start = timeit.default_timer()
    wpath = sys.argv[2]
    if os.path.exists(os.path.join(wpath,"titles.txt")):
        os.remove(os.path.join(wpath,"titles.txt"))
    t = open(os.path.join(wpath,"titles.txt"),"w")
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    Handler = WikiHandler()
    parser.setContentHandler( Handler )
    
    parser.parse(sys.argv[1])
    writetext(wpath)

    t.close()
    f = open(sys.argv[3],"w")
    f.write(str(wordcount)+str('\n')+str(len(countwords)))
    f.close()
    stop = timeit.default_timer()
    print (stop - start)
