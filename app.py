# coding: utf-8
from flask import Flask,render_template,request,url_for,redirect

from sentiment import sentimentanalysistext2, sentimentanalysistextnegation, sentimentanalysistwitter2, sentimentanalysistwitternegation

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index2.html")


#Sachant que sur HEROKUAPP, si une requète au server dure plus de 30 secondes, elle sera automatiquement 
#annulée, par conséquent si on souhaite faire du scrapping depuis le serv heroku app ou qu'un traitement dure, ça sera impossible
#l'idée serait de lancer un thread qui ferait des traitements sans retourner un résultat à l'utilisateur
#Ou lancer depuis une machine locale, dans notre miniprojet on a téléchargé des tweets mentionnant "Zemmour"
#entre le 20 et 27 novembre, plus de 120.000 et sont directement stockés dans a_file.txt


@app.route("/results",methods=["POST","GET"])
def results():
    
#premier formulaire

    var=request.form.get("nm")                          
    t=request.form.get("negat")
    u=request.form.get("tw")
    if (t=="oui"):              #si négation cochée
        if(u=="zemoui"):      #si Zemm coché on lance l'algo sur le fichier a_file.txt sinon sur l'input de l'utilisateur
            test=open('a_file.txt',encoding="UTF-8").read() 
            recupa=sentimentanalysistextnegation(test)
            return render_template("results.html",recup=recupa)
        else:
            recupa=sentimentanalysistextnegation(var)
            return render_template("results.html",recup=recupa)
    else:
        if(u=="zemoui"):
            test=open('a_file.txt',encoding="UTF-8").read()
            recupa=sentimentanalysistext2(test)
            return render_template("results.html",recup=recupa)
        else:
            recupa=sentimentanalysistext2(var)
            return render_template("results.html",recup=recupa)       

@app.route("/resultstw",methods=["POST","GET"])
def resultstw():
    #deuxème formulaire
    var=request.form.get("ab")
    t=request.form.get("negat1")
    if (t=="oui"):   #si négation cochée, on lance  sentimentanalysistwitternegation sur la requète
        recupa=sentimentanalysistwitternegation(var)
        
        return render_template("resultstw.html",recup=recupa)
    else:
        recupa=sentimentanalysistwitter2(var) #sinon lancer sentimentanalysistwitter
        return render_template("resultstw.html",recup=recupa)          



    



if __name__ == "__main__":
    app.debug=True
    app.run()
    