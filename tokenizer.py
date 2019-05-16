# -*- coding: utf-8 -*-
"""
Created on Fri May 10 19:54:20 2019

@author: Binish125
"""

import codecs
import math
import os
import re
from copy import deepcopy


#files containing stop words
Stop_word_file='nepali'
stop_words=[]
decoded_stop_words=codecs.open(Stop_word_file,encoding='utf-8')
for line in decoded_stop_words:
    stop_words.append(line.strip("\n").strip("\ufeff"))

    
class Tokenizer:
    
    global tokens;
    
    def makeTokens(self,sentence=""):
        tokens=sentence.split(" ");
        self.tokens=tokens
        
    def remove_stop_words(self):
        temp=self.tokens
        new_tokens=[]
        for token in temp:
            token = re.sub('\\r\\ufeff|\\r\\n\\ufeff\\n|-|’\\n|।\\n|\\n|\,|\"|\'| \)|\(|\)| \{| \}| \[| \]|!|‘|’|“|”| \:-|\?|।|/|\—', '', 
	token)
            token = re.sub(r'[0-9०-९]','',token)
            #stemming - removing मा|को|ले in words
            if re.findall(r'^.*(मा|को|ले|लाई|हरू|बाट|समेत|बीच)$', token):
                token = re.findall(r'^(.*)(?:मा|को|ले|लाई|हरू|बाट|समेत|बीच)$', token)
                token=token[0]
            if(token == ''):
                continue;
            elif(token not in stop_words):
                new_tokens.append(token)
        self.tokens=new_tokens
                
    def get_tokens(self):
        return self.tokens
    
    def show_tokens(self):
        print(self.tokens)


class tfidfVectorizer:

    #article path
    training_data_set='.\\16NepaliNews\\16719\\testRun'
    tokenizer=Tokenizer()
    
    #TF of the entire corpus
    corpus_tf=[]
    
    #idf of the entire corpus
    corpus_idf={}
    
    #tf-idf of the entire corpus
    corpus_tfidf=[]
    
    #contains the word set for the entire corpous
    
    wordSet={}
    
    #contains the word dictionary (token : count) for the entire article set
    wordDict={}
    
    #contains the word counts of article wise
    wordDictList=[]
    
    #contains tokens sets of all articles
    tokens_set=[]
    
    def calculate(self,):
        for files in os.walk(self.training_data_set):
            for index,file in enumerate(files[2]):
                print("File number " + str(index+1) + " : ")
                try:
                    decoded_file=codecs.open(files[0]+"\\"+file,encoding='utf-8')
                    data=decoded_file.read()
                    self.tokenizer.makeTokens(data)
                    self.tokenizer.remove_stop_words()
                    self.tokens_set.append(self.tokenizer.get_tokens())
                    print("Length of token : " + str(len(self.tokenizer.get_tokens())))
                    self.wordSet=set(self.tokenizer.get_tokens()).union(self.wordSet)
                except:
                    continue;
                    
        #print(self.tokens_set)        
        print("Total elements in the set : " + str(len(self.wordSet)))
        
        
        #This is a very problematic line of code
        #self.wordDict=dict.fromkeys(self.wordSet,0)
        self.wordDict={ key : 0 for key in self.wordSet }
        #print(self.wordDict)
        
        #count number of words and add to dict
        for index,token_set in enumerate(self.tokens_set):
            self.wordDictList.append(deepcopy(self.wordDict))
        
        self.word_count()
    
    def word_count(self):
        for index,token_set in enumerate(self.tokens_set):
            for token in token_set:
                self.wordDictList[index][token]+=1

        
    def show_wordSet(self):
        print(self.wordSet)
        
        
    #computing TF (Number of word appear in article / total number words in documents)  
    def computeTF(self,wordDict,token_set):
        tfDict={}
        tokenCount=len(token_set)
        for word,count in wordDict.items():
            tfDict[word]=count/float(tokenCount)
        return tfDict
        
    
    #compute TF of entire corpus
    def corpusTF(self):
        tf_set=[]
        for index in range(self.numberOfarticle()):
            tf_set.append(self.computeTF(self.wordDictList[index],self.tokens_set[index]))
        self.corpus_tf=tf_set
    
    #get TF of the given article
    def articleTF(self,article_number):
        return(self.computeTF(self.wordDictList[article_number-1],self.tokens_set[article_number-1]))
        
    
    #computing IDF (log(Number of documents/Number of documents that contains word w))
    def computeIDF(self,articleList):
        idfDict={}
        NumberOfArticles=len(self.tokens_set)
        idfDict=dict.fromkeys(articleList[0].keys(),0)
        for article in articleList:
            for word,val in  article.items():
                if val>0:
                    idfDict[word] +=1
        for word,val in idfDict.items():
            idfDict[word]= math.log(NumberOfArticles/float(val))
        self.corpus_idf=idfDict
    
    
    #get IDF of the corpus
    def corpusIDF(self):
        self.computeIDF(self.wordDictList)
    
    #get tfidf of the entire corpus
    def corpusTFIDF(self):
        for tf in self.corpus_tf:
            tfidf={}
            for word,val in tf.items():
                tfidf[word]=val*self.corpus_idf[word]
            self.corpus_tfidf.append(tfidf)
    
    #show article tf-idf
    def getTFIDF(self,article_number):
        return( self.corpus_tfidf[article_number-1]  )  
    
    #get the total number of articles
    def numberOfarticle(self):
        return len(self.tokens_set)
   
    #tf-idf of an specific article
    def computeTFIDF(self,tf,idf):
        tfidf={}
        for word,val in tf.items():
            tfidf[word]=val * idf[word]
        return tfidf;
    
    def show_DictList(self,article_num):
        print(self.wordDictList[article_num-1])
                
                
vectorizer=tfidfVectorizer()
vectorizer.calculate()
vectorizer.corpusTF()
vectorizer.corpusIDF()
vectorizer.corpusTFIDF()
tfidf=vectorizer.getTFIDF(11) #get the tfidf of an specific article

# the final output of the code -> vectorizer.corpus_tfidf 
# dictionary containing the tf-idf values of the entire corpus

highest_score=0.0
mvw=[];
important_words=[]
for token,val in tfidf.items():
    if(val>0):
        important_words.append(token)
        if(val==highest_score):
            mvw.append(token)
        elif(val>highest_score):
            highest_score=val
            mvw=[token];
        
print("Most Important Word : " + str(mvw) + " -> "+  str(highest_score))
print("Other Words : " + str(important_words))
print("length : " + str(len(important_words)))


