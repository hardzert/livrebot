
# -*- coding: utf-8 -*-

import sys

import tweepy
import json

information = open('info.json','rt')
informe = information.read()
info = json.loads(informe)


index_debut = int(info["index_debut"])
index_fin = int(index_debut)+234
chapitre = int(info["chapitre"])
partie = int(info["partie"])

livre = open(info['livre'],'r+')
texte = livre.read()

response = texte[index_debut]
print(response)


#  ------------- livre part -----------

if(response.find("h2") !=-1):
    
    chapitre = chapitre+1
    titre1 = response.find("h2")
    titre2 = response.find("h2",titre1+2)
    response = response[titre1-1:titre2+1]
    
while texte.replace('<p class=MsoNormal>', "").replace('</p>', "").replace('&nbsp;', " ")[index_fin-1:index_fin] != " ":
    index_fin -=1

print(informe)
response = texte.replace('<p class=MsoNormal>', "").replace('</p>', "").replace('&nbsp;', " ").replace("<p class=MsoNormal style='margin-left:1.0cm;text-indent:0cm'><i>Pour le petit","").replace('<a href="#_ftn2"name="_ftnref2" title="">',"").replace("<span class=MsoFootnoteReference><spanstyle='font-size:11.0pt'>","") [index_debut:index_fin]
informe = informe.replace('"index_debut" :"'+str(index_debut)+'"','"index_debut" :"' + str(index_fin-1)+'"' ).replace('"chapitre" :"'+str(chapitre)+'"','"chapitre" :"'+ str(chapitre)+'"').replace('"partie" :"'+str(1)+'"' ,'"partie" :"'+str(partie+1)+'"' )
#  39 212 index 0
information.close()
print(response)
information = open('info.json','wt')

information.write(informe)
information.close()



#   -----------------------  twitter part ---------------


token_file = open('token.json','rt')
token_info = token_file.read()
token = json.loads(token_info)
token_file.close()
tweet_id = token['tweet_id']


client = tweepy.Client(
    consumer_key=token["consumer_key"], consumer_secret=token["consumer_secret"],
    access_token=token["access_token"], access_token_secret=token["access_token_secret"]
)
reponse = client.create_tweet(
    # in_reply_to_tweet_id=tweet_id,
    text="Victor Hugo, Les misérables chapitre " +str(chapitre) + "\n" + response + "\n" + str(partie)+"/?"
)
client.retweet(reponse.data['id'])
print(f"https://twitter.com/user/status/{reponse.data['id']}")

token_file = open('token.json','wt')

token_file.write(token_info.replace(tweet_id,reponse.data['id']))
token_file.close()
