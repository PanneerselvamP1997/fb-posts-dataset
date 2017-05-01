f=open("preprocess_combined.txt","r")
la=[]
for line in f:
	l=line.strip('\n')
	l=l.split("__label__")
	la.append(l[1])
f.close()
f=open("label_twitter.txt","w")
for l in la:

 	f.write(l+"\n")
f.close()

