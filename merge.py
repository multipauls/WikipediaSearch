import os
import timeit
import re

start = timeit.default_timer()
mcount = 0
lcount=0
tfiles = len(next(os.walk("index/"))[2])-1
f=[]
for i in range(tfiles):
    wpath = "index/index"+str(i)+".txt" 
    f.append(open(wpath,'r'))

token=[]
line=[]
val=[]

curtoken = ""
curfile = -1
curvaluef = 0
curvalued =0
curline = ""
filepath="index/merged/mindex"+str(mcount)+".txt"
filem=open(filepath,'w')
secind=open("index/merged/secind.txt",'w')
flag=0
doneset=set()
#while True:
for j in range(0, tfiles):
        line.append(f[j].readline())
        token.append(re.findall(u'[^|]*', line[j])[0])
        val.append([int(re.findall(u'F(.*?)D', line[j])[0]),int(re.findall(u'D(.*?):', line[j])[0])])
        #print(token,curtoken)
        #print(token[j],curtoken)
ctr=0
while flag==0:
    for j in range(0, tfiles):
        if j not in doneset:      
            if token[j]==curtoken:
                curvaluef+=val[j][0]
                curvalued+=val[j][1]
                #print(re.findall(u'[^:]*', line[j]))
                curfile=j
                curline+=re.sub(u'[^a-zA-Z1-9;]','',re.findall(u'[^:]*', line[j])[2])
                line[j]=f[j].readline()
                if line[j]=="":
                    doneset.add(j)
                    token[j]="~"
                    #print("here")
                else:
                    token[j]=re.findall(u'[^|]*', line[j])[0]
                    #print(j)
                    val[j]=[int(re.findall(u'F(.*?)D', line[j])[0]),int(re.findall(u'D(.*?):', line[j])[0])]
            
            #print(val[j],curtoken)
            else:
                ctr+=1
                if ctr==tfiles:
                    for j in range(0, tfiles):
                        if j not in doneset:
                            line[j]=f[j].readline()
                            if line[j]=="":
                                doneset.add(j)
                                token[j]="~"
                                #print("here")
                            else:
                                token[j]=re.findall(u'[^|]*', line[j])[0]
                                #print(line[j])
                                val[j]=[int(re.findall(u'F(.*?)D', line[j])[0]),int(re.findall(u'D(.*?):', line[j])[0])]
                    filem.write(curtoken+'|F'+str(curvaluef)+'D'+str(curvalued)+':'+curline+'\n')
                    curtoken=min(token)
                    curfile=token.index(curtoken)
                    curvaluef=val[curfile][0]
                    curvalued=val[curfile][1]
                    curline=re.sub(u'[^a-zA-Z1-9;]','',re.findall(u'[^:]*', line[curfile])[2])
                    ctr=0
                    lcount+=1


                    
        if lcount==20000:
            filem.close()
            
            secind.write(str(curtoken)+" "+str(mcount)+"\n")
            mcount+=1
            filepath="index/merged/mindex"+str(mcount)+".txt"
            filem=open(filepath,'w')
            lcount=0

        #if lcount%2000==0:
        #    print(str(mcount)+" "+str(lcount)+" "+str(timeit.default_timer()-start))
        if len(doneset)==tfiles:
            flag=1
secind.write(str(curtoken)+" "+str(mcount)+"\n")
for i in range(tfiles):    
    f[i].close()
    os.remove("index/index"+str(i)+".txt") 
secind.close()
print(timeit.default_timer()-start)