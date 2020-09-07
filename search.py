import sys
import os
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")
import re
import timeit
from functools import reduce
import linecache
from math import log
start=timeit.default_timer()
text = sys.argv[1]
text = text.lower()
if ':' in text:
    sub = text.split(':')
    query = [word for line in sub for word in line.split()]

else:
    query = text.split(" ")

tokdata=[]
flags=[]
flag=""
for l in range(len(query)):
    i=query[l]
    if i not in ['t','b','l','i','r','c']:

        flags.append(flag)
        stemmed = stemmer.stem(i)
        secind = open("index/merged/secind.txt", "r")
        wline =secind.readline()
        while wline!="":
            val=wline.split(" ")
            if stemmed<=val[0]:
                doc = val[1].split("\n")[0]
                break
            wline = secind.readline()

        docf = open("index/merged/mindex"+doc+".txt")

        wline=docf.readline()
        lno=0
        while wline!="":
            #print(lno)
            tok=wline.split("|")[0]
            if tok==stemmed:
                something=str(wline.split("|")[1])
                tokdata.append(something)
                lno+=1
                break
            wline=docf.readline()

        if wline=="":
            print("Error, no data found for token "+stemmed)
        for lno in range(len(tokdata)):
                tokdata[lno]=tokdata[lno].replace(':',";")
                tokdata[lno]=tokdata[lno].replace('\n',";")
    else:
        #print(flags)
        flag=i

#print(flags)        
dtok=[]
for i in range(len(tokdata)):
    tokdata[i]=tokdata[i].split(";")
    dtok.append(dict())
    for k in range(1,len(tokdata[i])):
        if flags[i]=="":
        
            temp=re.findall(r".*?\d+.*?",tokdata[i][k])
            if len(temp):
                dtok[i][int(temp[0])]=temp[1:]

        else:
            if flags[i] in tokdata[i][k]:
                temp=re.findall(r".*?\d+.*?",tokdata[i][k])
                if len(temp):
                    dtok[i][int(temp[0])]=temp[1:]
        if len(dtok[i]):
            dtok[i][-1]=tokdata[i][0]




endset = set(reduce(lambda x, y: x & y.keys() , dtok))
#print(type(endset))

if len(endset)==1:
    print("No matches found for all words, printing individual instead")
    endset = set(reduce(lambda x, y: x | y.keys() , dtok))
endset=sorted(endset-{-1})
titlefile=open("index/titles.txt")
tot=[]
out=[]
count=0
for j in endset:
    tfidf=[]
    x=(linecache.getline("index/titles.txt", j+1, module_globals=None))
    tfidf.append(x.split(" ")[1:-1])
    ans=[]
    ans.append(x.split(" ")[-1])
    ans[0]=int(ans[0].rstrip('\n')) #total words in doc
    ans.extend([0]*2)
    
    for i in range(len(dtok)):

        # 
        #
        #print(len(re.split('[A-Z]+',dtok[i][-1])))
        for k in dtok[i]:
            if k==j:
                v=re.split('[A-Z]+',dtok[i][-1])
                #print(type(v))
                ans[2]+=int(v[2]) #total no of docs
                
                for l in range(len(dtok[i][k])):
                    #print(re.split('[a-z]+',dtok[i][k][l]))
                    ans[1]+=int(re.split('[a-z]+',dtok[i][k][l])[1]) #frequency of words in the doc
    #print(ans)
    tfidf.append((ans[1]/ans[0])*(log(40000/ans[2])))
    tot.append(tfidf)
    #temp.append()

tot= sorted(tot, key=lambda x: x[1], reverse=True)
for i in tot:
    if count<30:
        for j in i[0]:
            print(j+" ", end="")
        print("")
        count+=1
print(timeit.default_timer()-start)
