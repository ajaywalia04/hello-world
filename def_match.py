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
from itertools import zip_longest
import numpy as np
import time

out_final = []
in_final=[]
index_dict1={}
lists=[]
list1=[]
list2=[]
firstcolumn= {}
secondcolumn={}
mergedlist=[]
fee=[]
college=[]
table_fees=[]
TOLERANCE=1.4


def fees(outputfile,feefile,table_file,mergedlist):
    print ("fees")
    class college_headers(object):
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
        file = csv.DictReader(fh)
        #print (getstop)
        for place in file:
            current = college_headers(place)
            ids,id = current.getId()
            firstcolumn[ids] = current
            secondcolumn[id] = current
        for courses in set(mergedlist):
            if courses in firstcolumn: 
                    print (firstcolumn[courses])
                    table_fees.append(firstcolumn[courses])
                                         
            if courses in secondcolumn:
                    print (secondcolumn[courses])
                    table_fees.append(secondcolumn[courses])
        with open('result_be.csv', 'a+') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow(["college", "course", "fees"])
            for row in zip_longest(college, set(mergedlist),table_fees ):
                writer.writerow(row)         
                    #if os.path.exists(table_file):
    elif outputfile[:-4]==feefile[:-4]:
        with open(feefile, 'r') as myfile:
            data=myfile.read().replace('\n', '')
            print (data)
            fee.append(data)
            with open('result_be.csv', 'a+') as outcsv:
                writer = csv.writer(outcsv)
                writer.writerow(["college", "course", "fees"])
                for row in zip_longest(college, set(mergedlist),fee ):
                    writer.writerow(row)
          
    else:
        print ("not present")
    

def find_index(in_final,out_final):
    stop = set(stopwords.words('english'))
    k=0
    while k < len(out_final):
        index_dict1.clear()        
        for items in in_final:
            line = [i for i in items.split() if i not in stop]
            for item in line:
                if item not in index_dict1:
                    index_dict1[item]=[m.start() for m in re.finditer(item,out_final[k][0])]
        for key in in_final:
            in_words = key.split()
            if len(in_words) == 1:
                if key in out_final[k][0]:
                    lists.append(key)
            if len(in_words) == 2:
                line = [i for i in in_words if i not in stop]
                word_1 = index_dict1[line[0]]
                word_2 = index_dict1[line[1]]
                for word_a in word_1:
                    for word_b in word_2:                
                        difference = abs(word_b - word_a)
                        if len(line[0])<=difference<=(len(key)-len(line[0])+1):
                            list1.append(key)
            if len(in_words) > 2: 
                line = [i for i in in_words if i not in stop]
                word = []
                i = 0
                last_word_index = -1
                last_word = ''
                for item in line:                    
                    if item not in index_dict1 or len(index_dict1[item]) == 0:
                        word = []
                        break
                    else:
                        # print(item)
                        word.append(index_dict1[item])
                        if np.amax(index_dict1[item]) > last_word_index:
                            last_word_index = np.amax(index_dict1[item])
                            last_word = item
                        i = i + 1
                if i == len(line):
                    diff_total = 0
                    #sort word on basis of length of inner arrays to increase optimisation
                    word.sort(key=len)
                    for x in range(1, len(word)):
                        diff = 99999999
                        # res_l and res_r are result indexes from ar1[] and ar2[]
                        res_l = 0
                        res_r = 0
                        l = 0
                        while l < len(word[0]):
                            r = 0
                            while r < len(word[x]):                                
                                # If this pair is minimum, then update res_l, res_r and diff
                                if (abs(word[x][r] - word[0][l]) < diff):
                                   res_l = l
                                   res_r = r
                                   diff = abs(word[x][r] - word[0][l])                                   
                                r = r + 1
                            l = l + 1
                        diff_total = diff_total + diff
                else:
                    continue
                if(diff_total + len(last_word) > 4 and diff_total + len(last_word) < len(key) * TOLERANCE):
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
    print ("**************")
    mergedlist = lists+list1+list2
    print (set(mergedlist))
    print (len(set(mergedlist)))
    print ("***************")
    return mergedlist


def files(collegename,inputfile,outputfile,feefile,table_file):
    college.clear()

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
    college.append(collegename)
    mergedlist = find_index(in_final,out_final)
    fees(outputfile,feefile,table_file,mergedlist)
    #fees(outputfile,feefile,table_file)
start = time.time()
files('bharat university','input/engineering.csv','output/bharathuniv.ac.in.csv','output/bharat.ac.in.txt','output/bharathuniv.ac.in-tables.csv')
#files('iit kharagpur','input/be.csv','output/iitkgp.ac.in.csv','output/iitkgp.ac.in.txt','output/iitkgp.ac.in-tables.csv')
# files('input/engineering.csv','output/iitb.ac.in.csv','output/iitb.ac.in.txt','output/iitb.ac.in-tables.csv')
# files('input/engineering.csv','output/iitd.ac.in.csv','output/iitd.ac.in.txt','output/iitd.ac.in-tables.csv')
# files('input/engineering.csv','output/manit.ac.in.csv','output/manit.ac.in.txt','output/manit.ac.in-tables.csv')
#files('input/engineering.csv','output/mnit.ac.in.csv','output/mnit.ac.in.txt','output/mnit.ac.in-tables.csv')
#files('input/engineering.csv','output/nita.ac.in.csv','output/nita.ac.in.txt','output/nita.ac.in-tables.csv')
#files('input/engineering.csv','output/nitandhra.ac.in.csv','output/nitandhra.ac.in.txt','output/nitandhra.ac.in-tables.csv')
#files('input/engineering.csv','output/nitap.in.csv','output/nitap.in.txt','output/nitap.ac.in-tables.csv')
#files('nit calicut','input/engineering.csv','output/nitc.ac.in.csv','output/nitc.ac.in.txt','output/nitc.ac.in-tables.csv')
#files('input/engineering.csv','output/nitdelhi.ac.in.csv','output/nitdelhi.ac.in.txt','output/nitdelhi.ac.in-tables.csv')
#files('input/engineering.csv','output/nitdgp.ac.in.csv','output/nitdgp.ac.in.txt','output/nitdgp.ac.in-tables.csv')
#files('input/engineering.csv','output/nitgoa.ac.in.csv','output/nitgoa.ac.in.txt','output/nitgoa.ac.in-tables.csv')
#files('input/engineering.csv','output/iitk.ac.in.csv','output/iitk.ac.in.txt','output/iitk.ac.in-tables.csv')
#files('input/be.csv','output/nith.ac.in.csv','output/nith.ac.in.txt','output/nith.ac.in-tables.csv')
#files('input/be.csv','output/nitj.ac.in.csv','output/nitj.ac.in.txt','output/nitj.ac.in-tables.csv')
# files('input/be.csv','output/nitjsr.ac.in.csv','output/nitjsr.ac.in.txt','output/nitjsr.ac.in-tables.csv')
# files('input/be.csv','output/nitk.ac.in.csv','output/nitk.ac.in.txt','output/nitk.ac.in-tables.csv')
# files('input/be.csv','output/nitkkr.ac.in.csv','output/nitkkr.ac.in.txt','output/nitkkr.ac.in-tables.csv')
# files('input/be.csv','output/nitmanipur.ac.in.csv','output/nitmanipur.ac.in.txt','output/nitmanipur.ac.in-tables.csv')
# files('input/be.csv','output/nitmeghalaya.in.csv','output/nitmeghalayengineeringa.in.txt','output/nitmeghalaya.ac.in-tables.csv')
# files('input/be.csv','output/nitmz.ac.in.csv','output/nitmz.ac.in.txt','output/nitmz.ac.in-tables.csv')
# files('input/be.csv','output/nitnagaland.ac.in.csv','output/nitnagaland.ac.in.txt','output/nitnagaland.ac.in-tables.csv')
# files('input/be.csv','output/nitp.ac.in.csv','output/nitp.ac.in.txt','output/nitp.ac.in-tables.csv')
# files('input/be.csv','output/nitpy.ac.in.csv','output/nitpy.ac.in.txt','output/nitpy.ac.in-tables.csv')
# files('input/be.csv','output/nitrkl.ac.in.csv','output/nitrkl.ac.in.txt','output/nitrkl.ac.in-tables.csv')
#files('nit raipur','input/engineering.csv','output/nitrr.ac.in.csv','output/nitrr.ac.in.txt','output/nitrr.ac.in-tables.csv')
#files('nit silchar','input/engineering.csv','output/nits.ac.in.csv','output/nits.ac.in.txt','output/nits.ac.in-tables.csv')
#files('input/engineering.csv','output/nitsikkim.ac.in.csv','output/nitsikkim.ac.in.txt','output/nitsikkim.ac.in-tables.csv')
#files('nit trichy','input/engineering.csv','output/nitt.edu.csv','output/nitt.edu.txt','output/nitt.ac.in-tables.csv')
#files('input/engineering.csv','output/nituk.ac.in.csv','output/nituk.ac.in.txt','output/nituk.ac.in-tables.csv')
#files('input/engineering.csv','output/nitw.ac.in.csv','output/nitw.ac.in.txt','output/nitw.ac.in-tables.csv')
#files('input/engineering.csv','output/svnit.ac.in.csv','output/svnit.ac.in.txt','output/svnit.ac.in-tables.csv')
#files('input/engineering.csv','output/vnit.ac.in.csv','output/vnit.ac.in.txt','output/vnit.ac.in-tables.csv')
#medical
# files('snmcagra','input/medical.csv','output/snmcagra.ac.in.csv','output/snmcagra.ac.in.txt','output/snmcagra.ac.in-table.csv')
# files('pimsmmm','input/medical.csv','output/pimsmmm.com.csv','output/pimsmmm.com.txt','output/pimsmmm.com-tables.csv')
# files('bgsaims','input/medical.csv','output/bgsaims.edu.in.csv','output/bgsaims.edu.in.txt','output/bgsaims.edu.in-tables.csv')
# files('cmccbe','input/medical.csv','output/cmccbe.ac.in.csv','output/cmccbe.ac.in.txt','output/cmccbe.ac.in-tables.csv')
# files('gmersmcjunagadh','input/medical.csv','output/gmersmcjunagadh.org.csv','output/gmersmcjunagadh.org.txt','output/gmersmcjunagadh.org-tables.csv')
# files('jjmmc','input/medical.csv','output/jjmmc.org.csv','output/jjmmc.org.txt','output/jjmmc.org-tables.csv')
# files('kims.rvsangha.org','input/medical.csv','output/kims.rvsangha.org.csv','output/kims.rvsangha.org.txt','output/kims.rvsangha.org-tables.csv')
end = time.time()
print ("*****************")
print (end - start)
print ("*****************")























