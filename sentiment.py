# coding: utf-8
#B_N
#B_M_A

import snscrape.modules.twitter as sntwitter
import re
import simplemma  #lemmatizer en FR, pas si efficace.
from typing import Counter
import matplotlib.pyplot as plt


#scraper=sntwitter.TwitterSearchScraper("Nom since:2021-11-24 lang:fr")


lema=simplemma.load_data('fr')


#Il existe 4 fonctions principales
#traitement de texte sans négation
#traitement de texte avec négation
#traitement de tweets sans négation
#traitement de tweets avec négation





def clean(tweet):

    temp=tweet.lower()
    temp = re.sub("@[A-Za-z0-9_]+","", temp)        #éliminer les @word
    
    temp = re.sub("#[A-Za-z0-9_]+","", temp)        #éliminer les @#
    
    temp = re.sub("[0-9]+","", temp)                #éliminer les chiffres
    
    temp = re.sub(r"http\S+", "", temp)             #éliminer les liens http..
    
    temp = re.sub(r"www.\S+", "", temp)             #éliminer les liens www..
    
    temp = re.sub('[()!?]', ' ', temp)              #eliminer les caractères spéciaux
    
    temp = re.sub('\[.*?\]',' ', temp)              #eliminer les caractères spéciaux
    
    temp = re.sub("[^a-z0-9àéçèê]"," ", temp)       #^ veut dire exception, on présèrve ce qui caractérise le Français
    
    
    temp=temp.split()                               #on split la phrase en tokens
    return temp

def net():   #une fonction qu'on avait crée pour lemmatiser les listes d'émotions sur les quelles l'algo travaillera
    lema=simplemma.load_data('fr')
    lines=[]
    save=[]
    i=0
    with open('negative_words_fr.txt','r',encoding="UTF-8") as file:    
        for line in file:
            line=line.strip()
            lines.append(line)

            save.append(simplemma.lemmatize(line,lema))
            i=i+1
    print(i)

    with open('test.txt','w',encoding="UTF-8") as f:
        for item in save:
            f.write("{}\n".format(item))

#traitements de texte sans négation
def sentimentanalysistext2(test):
    temp=[]
    i=0
    t=[]
    #test=open('text.txt',encoding="UTF-8").read()
    t=clean(test)
    final_words=[]
    lines=[]
    negative=[]
    positive=[]
    with open('fichiers/stopwordsfr.txt','r',encoding="UTF-8") as file:
        for line in file:
            line=line.strip()

            lines.append(line)                       #remplir la var lines avec les stopwords
    for word in t:
        if word not in lines:                       #si le token n'est pas un stopword, on l'ajoute à final_words
            final_words.append(word)  
    linesp=[]
    linesn=[] 
    print(final_words)
    for token in final_words:                       #pour chaque token dans final words, on le lemmatize
        #print(token)
        temp.append(simplemma.lemmatize(token,lema))
        #print(test)  
        i=i+1        
    with open('fichiers/positive.txt','r',encoding="UTF-8") as file:       #remplir la var linesp avec les mots positifs       
        for line in file:
            line=line.strip()
            linesp.append(line)    
    with open('fichiers/negative.txt','r',encoding="UTF-8") as file:         #remplir la var linesn avec les mots négatifs
        for line in file:
            line=line.strip()
            linesn.append(line)               
    for word in temp:                           #tester chaque token si il est positif ou négatif
        if word in linesp:
            positive.append(word)          
        elif word in linesn:
            negative.append(word)
        else:
            pass   
             
    print(positive)
    print("\n\n\n")    
    print(negative)
    print("\n\n\n") 
    print(len(positive))
    print("\n\n\n") 
    print(len(negative))
    flist=[]
    positive1=positive.copy()    #faire une vraie copie de la liste contenant les mots positifs détéctés
    negative1=negative.copy()   #faire une vraie copie de la liste contenant les mots négatifs détéctés
    i=0        
    for te in positive:
        positive[i]="Positif"   #renommer tous les mots positifs en "Positif" pour le plot
        i=i+1
    i=0
    for te in negative:
        negative[i]="Negatif"   #renommer tous les mots négatifs en "Negatif" pour le plot
        i=i+1    
    w=Counter(positive)
    x=Counter(negative)    
    fig,ax1=plt.subplots()
    ax1.bar(w.keys(),w.values())
    ax1.bar(x.keys(),x.values())
    fig.autofmt_xdate()
    plt.savefig('static/graph.png')
    #plt.show()
    flist=[]
    flist.append(positive1) 
    flist.append(negative1) #le contenu de flist sera retourné à l'utilisateur dans une page html
    
    print("flist")
    print(flist)
    print("flist")
    return flist

#traitement de tweets sans négation
def sentimentanalysistwitter2(test):
    scraper=sntwitter.TwitterSearchScraper(test)
    j=0
    temp=[]
    i=0
    t=[]
    final_words=[]
    lines=[]
    negative=[]
    positive=[]
    line=[] 
    poswords=[]
    negwords=[]
    tweetscontent=[]
    with open('fichiers/negative.txt','r',encoding="UTF-8") as file:
        for line in file:
            line=line.strip()
            negwords.append(line)      
    with open('fichiers/positive.txt','r',encoding="UTF-8") as file:
        for line in file:
            line=line.strip()
            poswords.append(line)    
    with open('fichiers/stopwordsfr.txt','r',encoding="UTF-8") as file:     #remplir les stopwords/positifs/negatifs dans des variables
        for line in file:
            line=line.strip()

            lines.append(line)

    for i,tweet in enumerate(scraper.get_items()):              #pour chaque tweet qui résulte de notre scrapping
    #print(tweet.id,tweet.content,"{}\n\n".format(i))
        t=clean(tweet.content)                      #on le néttoie avec la fonction clean(éliminer ascii split ..)
        tweetscontent.append(tweet.content)         #on sauvegarde pour l'afficher à l'user plus tard
        for word in t:
            if word not in lines:
                final_words.append(word)                #éliminer les stopwords

        for token in final_words:
            #print(token)
            temp.append(simplemma.lemmatize(token,lema))        #lemmatiser chaque token
            #print(test)  
            i=i+1

        for word in temp:                               #tester chaque token si il est positif ou négatif
            if word in poswords:
                positive.append(word)  
            elif word in negwords:
                negative.append(word)
            else:
                pass                       
         
        
        temp=[]                             #reinstaliser les deux vars pour traiter le tweet suivant
        final_words=[]
    flist=[]
    positive1=positive.copy()
    negative1=negative.copy()                   #copie de listes à retourner à l'utilisateur
    flist.append(tweetscontent)
    flist.append(positive1)
    flist.append(negative1)
    i=0
    for te in positive:
        positive[i]="Positif"              #renommer tous les mots négatifs en "Negatif" et vice versa pour positifs, pour le plot
        i=i+1
    i=0
    for te in negative:
        negative[i]="Negatif"
        i=i+1    
    w=Counter(positive)
    x=Counter(negative)         
    fig,ax1=plt.subplots()
    ax1.bar(w.keys(),w.values())                    #création plot et sauvegarde de l'image
    ax1.bar(x.keys(),x.values())
    fig.autofmt_xdate()
    plt.savefig('static/graph.png')    
    print(positive)
    print("\n")    
    print(negative)
    print("\n") 
    print(len(positive))
    print("\n") 
    print(len(negative))    

    return flist                                # retourner une liste contenant, une liste de tweets, d'emotions positifs, et d'emotions négatifs



#pour traiter la négation on considère que pour un texte, chaque phrase est porteuse d'une emotion
#donc contrairement à l'autre traitement sans négation ou on tokenizait directement
#chaque phrase sera traitée à part



def sentimentanalysistextnegation(test):
    temp=[]
    i=0
    k=0
    t=[]
    #sentences=sent_tokenize(test)    #on pouvait utiliser sent_tokenize sauf qu'elle bug sur herokuapp
    sentences = re.compile('[.!?] ').split(test)   #on tokenize avec ce regex le texte en phrases
    #test=open('text.txt',encoding="UTF-8").read()
    #t=clean(test)
    final_words=[]
    lines=[]
    negative=[]
    positive=[]
    linesp=[]
    linesn=[]
    positiveneg=[]
    negativeneg=[]
    negat=False                 #var booléenne qui traite si il existe une négation ou non
    with open('fichiers/stopwordsfr.txt','r',encoding="UTF-8") as file:
        for line in file:
            line=line.strip()

            lines.append(line)                       #remplir la var lines avec les stopwords
    with open('fichiers/positive.txt','r',encoding="UTF-8") as file:       #remplir la var linesp avec les mots positifs       
        for line in file:
            line=line.strip()
            linesp.append(line)    
    with open('fichiers/negative.txt','r',encoding="UTF-8") as file:         #remplir la var linesn avec les mots négatifs
        for line in file:
            line=line.strip()
            linesn.append(line)      
          
    for sentence in sentences:   #comme pour les tweets ( pour chaque tweet dans tweets)
                                #maintenant c'est pour chaque PHRASE dans notre texte
        
        t=clean(sentence)       #on nettoie la phrase et on la tokenize en mots
        
        
        for word in t:
            if word not in lines:                       #si le token n'est pas un stopword, on l'ajoute à final_words
                final_words.append(word)  

        #print(final_words)
        for token in final_words:                       #pour chaque token dans final words, on le lemmatize ( le n' devient ne)
            
            temp.append(simplemma.lemmatize(token,lema))
            #print(test)  
            i=i+1        
            
         
        
        for word in temp:                           #chercher si il existe une négation, si oui on met la var negat à TRUE
            if word=="ne":
                negat=True         
                       
        for word in temp:                           #tester chaque token si il est positif ou négatif
            if (negat):             #si il existe un mot faisant reférence à la négation (ne)
                if word in linesp:
                    positiveneg.append(word)          #on remplit les mots positifs dans une liste dite "faux positifs=négatifs"
                elif word in linesn:
                    negativeneg.append(word)            ##on remplit les mots négatifs dans une liste dite "faux négatifs=positifs"
                else:
                    pass   
            else:                                       #si pas de négation, on met pos dans positifs..
                if word in linesp:
                    positive.append(word)
                elif word in linesn:
                    negative.append(word)
                else:
                    pass     
        if (negat):                         #si négation existe alors on met les faux positifs avec les négatifs, faux négatifs avec positifs..
            positive.extend(negativeneg)
            negative.extend(positiveneg)      
        positiveneg=[]
        negativeneg=[]        
        temp=[]
        final_words=[]     
        negat=False
        k=k+1                               #on remet les vars à vide et negat à false pour la prochaine phrase
        print(k)
                
    print("positif: ",positive)
    print("\n")    
    print("negatif: ",negative)
    print("\n") 
    print(len(positive))
    print("\n\n\n") 
    print(len(negative))
    i=0        
    flist=[]
    positive1=positive.copy()
    negative1=negative.copy()
    flist.append(positive1)             #flist contiendera les positifs et les négatifs
    flist.append(negative1)
    print(flist)

    for te in positive:
        positive[i]="Positif"
        i=i+1
    i=0
    for te in negative:
        negative[i]="Negatif"
        i=i+1    
    w=Counter(positive)
    x=Counter(negative)    
    fig,ax1=plt.subplots()                  #le plot affichera le nombre de positifs et négatifs
    ax1.bar(w.keys(),w.values())
    ax1.bar(x.keys(),x.values())
    fig.autofmt_xdate()
    plt.savefig('static/graph.png')
    #plt.show()
    

    
    
    
    
    return flist    


#même chose que pour la négation pour le texte(fonction précédente),chaque tweet est indépendant
def sentimentanalysistwitternegation(test):
    scraper=sntwitter.TwitterSearchScraper(test)
    j=0
    temp=[]
    i=0
    k=0
    t=[]
    final_words=[]
    lines=[]
    negative=[]
    positive=[]
    line=[] 
    poswords=[]
    negwords=[]
    tweetscontent=[]
    positiveneg=[]
    negativeneg=[]
    negat=False 
    with open('fichiers/negative.txt','r',encoding="UTF-8") as file:
        for line in file:
            line=line.strip()
            negwords.append(line)      
    with open('fichiers/positive.txt','r',encoding="UTF-8") as file:
        for line in file:
            line=line.strip()
            poswords.append(line)    
    with open('fichiers/stopwordsfr.txt','r',encoding="UTF-8") as file:
        for line in file:
            line=line.strip()

            lines.append(line)

    for i,tweet in enumerate(scraper.get_items()):
    #print(tweet.id,tweet.content,"{}\n\n".format(i))
        t=clean(tweet.content)
        tweetscontent.append(tweet.content)
        for word in t:
            if word not in lines:
                final_words.append(word) 

        for token in final_words:
            #print(token)
            temp.append(simplemma.lemmatize(token,lema))
            #print(test)  
            i=i+1
        for word in temp:                           #chercher si il existe une négation
            if word=="ne":
                negat=True         
                                   

        for word in temp:                           #tester chaque token si il est positif ou négatif
            if (negat):                             #si négation alors mettre faux positifs dans négatifs et faux négatis dans positifs
                if word in poswords:
                    positiveneg.append(word)          
                elif word in negwords:
                    negativeneg.append(word)
                else:
                    pass   
            else:
                if word in poswords:
                    positive.append(word)
                elif word in negwords:
                    negative.append(word)
                else:
                    pass     
        if (negat):
            positive.extend(negativeneg)
            negative.extend(positiveneg)                      
        positiveneg=[]
        negativeneg=[]        
        temp=[]
        final_words=[]     
        negat=False
        k=k+1
        print(k)

    flist=[]
    positive1=positive.copy()
    negative1=negative.copy()
    flist.append(tweetscontent)
    flist.append(positive1)
    flist.append(negative1)
    i=0
    for te in positive:
        positive[i]="Positif"
        i=i+1
    i=0
    for te in negative:
        negative[i]="Negatif"
        i=i+1    
    w=Counter(positive)
    x=Counter(negative)         
    fig,ax1=plt.subplots()
    ax1.bar(w.keys(),w.values())
    ax1.bar(x.keys(),x.values())
    fig.autofmt_xdate()
    plt.savefig('static/graph.png')    
    print(positive)
    print("\n")    
    print(negative)
    print("\n") 
    print(len(positive))
    print("\n") 
    print(len(negative))    

    return flist    


