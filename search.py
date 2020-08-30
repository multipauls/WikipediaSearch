import sys
import pickle
import os
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")
import re
#text = sys.argv[1]
indexfile = sys.argv[1]
f = open(os.path.join(indexfile,"index.txt"),"r")
indextext=f.read()
f.close()
f = open(os.path.join(indexfile,"titles.txt"),"rb")
titletext=pickle.load(f)
f.close()
idx = indextext.split("\n")
for i in range(len(idx)):
	idx[i]=idx[i].split("|")
text = sys.argv[2]
text = text.lower()
query = text.split(" ")
for i in query:
	if ':' in i:
		i=i.split(':')[1]
	stemmed = stemmer.stem(i)
	for j in range(len(idx)):
		if stemmed==idx[j][0]:
			output=re.sub(u'^.*?:', '', idx[j][1])
			output=output.split(";")
			for k in output:
				num=re.findall(u'^(\d+).*',k)
				if(num):
					print(titletext[int(num[0])])
