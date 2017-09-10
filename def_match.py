#import 
import nltk
import nltk.corpus
import nltk.stem.snowball
import nltk.tokenize.punkt
import string
from nltk import word_tokenize
from nltk.corpus import stopwords
import csv
import codecs
import re
import string
import os.path

out_final = []
in_final=[]
index_dict1={}
lists=[]
list1=[]
list2=[]
available = {}
value={}

def fees(outputfile,feefile,table_file):
    print ("fees")
    class stop(object):
        def __init__(self,table):
                self.info = table
        def getId(self):
                with open (table_file,'r') as infile:
                    translator = str.maketrans('', '', string.punctuation)
                    reader = csv.DictReader(infile)
                    fieldnames=reader.fieldnames
                return (self.info[fieldnames[0]].lower().translate(translator), self.info[fieldnames[1]].lower().translate(translator))
        def __str__(self):
                with open (table_file,'r') as infile:
                        reader = csv.DictReader(infile)
                        fieldnames=reader.fieldnames
                say = (self.info[fieldnames[0]],self.info[fieldnames[1]],self.info[fieldnames[2]],
                                self.info[fieldnames[3]])
                return (", ".join(say))
    if os.path.exists(table_file):
        fh = open(table_file,"r")
        getstop = csv.DictReader(fh)
        for place in getstop:
            current = stop(place)
            ids,id = current.getId()
            value[ids] = current
            available[id] = current
        for courses in set(list1):
            if courses in value: 
                    print (value[courses])                        
            if courses in available:
                    print (available[courses])       
                    #if os.path.exists(table_file):
    elif outputfile[:17]==feefile[:17]:
        f=open(feefile,'r')
        print (f.read())
        f.close()
    else:
        print ("not present")
    

def find_index(in_final,out_final):
    stop = set(stopwords.words('english'))
    k=0
    while k < len(out_final):
        index_dict1.clear()
        for item in in_final:
            line = [i for i in item.split() if i not in stop]
            for items in line:
                if items not in index_dict1:
                    index_dict1[items]=[m.start() for m in re.finditer(items,out_final[k][0])]
        
        for key in in_final:
            if len(key.split())==1:
                if key in out_final[k][0]:
                    lists.append(key)
            if len(key.split())==2:
                line = [i for i in key.split() if i not in stop]
                word_1= index_dict1[line[0]]
                word_2=index_dict1[line[len(line)-1]]
                for word_a in word_1:
                    for word_b in word_2:                
                        difference = abs(word_b-word_a)
                        if len(line[0])<=difference<=(len(key)-len(line[0]+str(1))):
                            list1.append(key)
            if len(key.split()) >2:

                line = [i for i in key.split() if i not in stop]
                word_1= index_dict1[line[0]]
                word_2=index_dict1[line[len(line)-2]]
                word_3 = index_dict1[line[len(line)-1]]
                
                for word_a in word_1:
                    for word_b in word_2:
                        difference1 = abs(word_b-word_a)
                        for word_bb in word_2:
                            for word_c in word_3:
                                difference2 = abs(word_c- word_b)
                                if len(line[0])<=difference1<=(len(key)-len(line[0])-len(line[len(line)-1])) and len(line[0])<= difference2<=(len(key)-len(line[0])-len(line[len(line)-1])):
                                    list2.append(key)

                                   

        k=k+1
    print (set(lists))
    print (len(set(lists)))
    print ("***************")
    print(set(list1))
    print (len(set(list1)))
    
    print("**************")
    print(set(list2))
    print (len(set(list2)))

def files(inputfile,outputfile,feefile,table_file):
    stop = set(stopwords.words('english'))
    translator = str.maketrans('', '', string.punctuation)
    input_csv = open(inputfile)
    output_csv = open(outputfile,encoding='utf8')
    in_list = [line for line in input_csv]
    out_list = [line for line in output_csv]
    for line in out_list:
        line=line.strip()
        line=re.sub('[0-9]+','',line)
        line = [line.lower().translate(translator)]
        line = [i for i in line if i not in stop]
        out_final.append(line)
    for line in in_list:
        line=line.strip('\n')
        line = (line.lower().translate(translator))
        in_final.append(line)
    
    find_index(in_final,out_final)
    fees(outputfile,feefile,table_file)

#files('input/engineering.csv','output/bharathuniv.ac.in.csv','output/nitdgp.ac.in.txt','output/bharathuniv.ac.in-tables.csv')
#files('input/engineering.csv','output/nitdgp.ac.in.csv','output/nitdgp.ac.in.txt','output/nitdgp.ac.in-tables.csv')
files('input/engineering.csv','output/nith.ac.in.csv','output/nith.ac.in.txt','output/nith.ac.in-tables.csv')
#files('input/engineering.csv','output/nita.ac.in.csv','output/nita.ac.in.txt','output/nita.ac.in-tables.csv')
#files('input/engineering.csv','output/nitc.ac.in.csv','output/nitc.ac.in.txt','output/nitc.ac.in-tables.csv')
#files('input/engineering.csv','output/nitdelhi.ac.in.csv','output/nitdelhi.ac.in.txt','output/nitdelhi.ac.in-tables.csv')
#files('input/engineering.csv','output/nitgoa.ac.in.csv','output/nitgoa.ac.in.txt','output/nitgoa.ac.in-tables.csv')
#files('input/engineering.csv','output/nitk.ac.in.csv','output/nitk.ac.in.txt','output/nitk.ac.in-tables.csv')
#files('input/engineering.csv','output/nitnagaland.ac.in.csv','output/nitnagaland.ac.in.txt','output/nitnagaland.ac.in-tables.csv')
#files('input/engineering.csv','output/iitb.ac.in.csv','output/iitb.ac.in.txt','output/iitb.ac.in-tables.csv')
#files('input/engineering.csv','output/iitk.ac.in.csv','output/iitk.ac.in.txt','output/iitk.ac.in-tables.csv')
#files('input/engineering.csv','output/iitd.ac.in.csv','output/iitd.ac.in.txt','output/iitd.ac.in-tables.csv')