import sys
import pickle
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")
#text = sys.argv[1]
indexfile = sys.argv[1]
f = open(indexfile+"/index.txt","rb")
indextext=pickle.load(f)
f.close()
f = open(indexfile+"/titles.txt","rb")
titletext=pickle.load(f)
f.close()
query = text.split(" ")
#for i in query:
#	if i[:2] == "t:":
for i in query:
	print()