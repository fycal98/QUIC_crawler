
import csv
from concurrent import futures
import matplotlib.pyplot as plt
import csv
import pandas as pd
from tabulate import tabulate
from socket import *
from struct import * 
import binascii
import random
import os
import requests
import zipfile
from io import BytesIO 
import quic_packet_initial
sites = []
resultat = []
quic = 0
tcp = 0
#recupere la list des sites depuis le site d'alexa
url = 'https://statvoo.com/dl/top-1million-sites.csv.zip'
r = requests.get(url, stream=True)
z = zipfile.ZipFile(BytesIO(r.content))
z.extractall()

with open('top-1m.csv', newline='') as f:
    reader = csv.reader(f)
    i = 0
    for line in reader : 
        sites.append(line[1])
        i+=1
        if i == 10 : break


#crée un example d'une message quic de type initial
packet = quic_packet_initial.Quic().header
#packet = 'ce000000010862e114195928091a004046006654c99fc9e601a3a8a89c596bffff21d131800ec744fa5e5ae06b3a084b3a455e9a8b3a765e850368d87fbc7fbb350903419cacf8c387ea39b0c5a2dfe16d3383c70bc4094489b63e08b1dafeaac768a8a68a989bbf61a5ffcc4417c3c84382df5c93236a143207d21404ff1076919c9473d3084ee226621d9e613cb09f4cd1947ae34d2cc7ff925680b2b7cba822755ed107371c369c265c41a070955e979978256b8b5d8f3941140dc52350a9abbdaf90b6eb3b074ba0e266863d192bd292fcaf8d8e11765adde0e5163253eb141702db68bae523353d0a2ee17fb26eb619fe850cbc0026813b24c53cafdeeb080cac13e9a1fc02417244b5d6fdd7a9235f5959b6c1ab2f850ce82c93d36e4d78a08b0c368f45ddd7bfc1d24bc713bcfb867bea5a9b74a9540cff8d999bdf55822e72bbe60cf9268bb67bc942c655332c56344c438292dad0d5b18c62cb6b59442542e215979b5ad83a2d2093f5f193a557f9cbe39b744311bb263bd87d701f4399b15a86ffaeedb9f6bdb95e3926b166d72620c7e05fb40f0daad0389a82b78094d755ae1efcce3b44a796c6396b15c1a0e77cd8e5b12bc8cef378c7cfdf2c733f4cb18d49f012a6e392f573017737e97ed8fff2928aa877d06cb29ebcd717cfab2f86414594408434d5d693ea2fd57e9f3f80be4d2a6e8cc19d76d5f7f130f2c8458de4a216d9523b4bfc22017f70572ac97877ef20b25bf9267a92a6dc6c9b8c28622731efbb210972903d1515a608f79a0384a8242b4b3611c4603278d2887a7f875f5790e1ad3cc78048a33c443984463a60e7df322f93bd2de7277d0102283c4bc1e1c84eb205f352e196ea37123611595b82fd3f5e4f84a082731abf1ef40ef8b87b4b98aee93159d7b511da40eec5a305abdaaa7d78b2a2445371bfce80ad2b41c5f972cab34adf72d92fc4d12cafbe9cec6869b5bc8a8cf5766f33dc6bf1b78d418d42478fc71e28c6451201124343fbbd1fa2e92043e4cd86f4cb2f457da6674c58e9ff35076d1ca13722cf6a2b3637d55568ddda049dde135295cf33634744c07cae0daf640e3c08511f8899a716317fe3ccbfb459c5ef5e6f47f62249b5c39333b85c11549aa12f03765cd37136083c8d66e1340d46f639ccb67fe6af73b25b6a2ca10b2253d59c12e64428ff5c4933e41b98c9d39c1b104968781b022b51a1d3c8484e14ef7fdb6e18c4485bf2bb0222e22ec5160120b1996797577b14a0fc3d88aa669116d2eee8bd1fb2574eb6e6f19afc262f31af13634b8d96aba09cefe2a79a7c5ccdbeadf943ed48ed4bfc179ff9b8fc7da01b40994163a998f153c4f65fcdb053435920ea6b4a4c085bd5f714aee15bf29b5d3703b9f64b06772e56d8449a094207294a5b2fe94db64e6254fc6f049fb376f121f56369c13104b1d367a6b4ea57a356bb06f8b63bc4bc3529c0d031e3426d314be7d3a480e7638dbd5aa5f6059c6d06e7a4c2077ed7c95ea7c6d2d4c0a8d363c4c1a17f1ce31450311df0455b45e9b55589299bb0370dcddb097aac880ea6aeba6f15abb7de8b8458a5fd397b8c5723a274ec480f43fe63f3ca97069ddfaaaa11871bdfa1693aee92e72c1ad154e711d82edc440fcf16343e429a7483a005f20fa3336f4c56d411264b0184cc77b54f35669de3d5363777e528db696c410e9a9c25ff4f352e2b2172c552b972d0cc1859e12b5de19da24781fee8633e47f65cec17e8398d'
packet = binascii.unhexlify(packet)

#la fonction check verifi si le site support le protocole quic est rend True si c'est le cas
def check(url) :
    s = socket(AF_INET,SOCK_DGRAM)
    s.bind(('',random.randint(1000,65535)))
    s.sendto(packet,(url,443))
    s.settimeout(1)
    try :     
        result = s.recv(1000)
        print(url+ ' : '+'quic')
        global quic
        quic+=1
        global resultat
        resultat.append({'url' : url ,'protocole': 'quic'})
        return True
    except : 
        print(url+ ' : '+'tcp')
        resultat.append({'url' : url ,'protocole': 'tcp'})
        global tcp
        tcp+=1
       
        return False

#utliser une pool de thread pour executer la functiion check pour reduire le temps d'attente
executor = futures.ThreadPoolExecutor(max_workers=2)

#executer la fonction check pour chaque site
for site in sites : 
    a = executor.submit(check,site)

#attendre la fin de l'execution
executor.shutdown(wait=True)

#nous supprimons le fichier du resultat precedente s'il existe
try:
    os.remove("resultat.csv'")
except OSError:
    pass

#on crée un nouveau fichier de resultat 
file  = open('resultat.csv','w')
writer = csv.DictWriter(file , fieldnames=['url' , 'protocole'])
writer.writeheader()
for data in resultat:
            writer.writerow(data)
file.close()
df = pd.read_csv('resultat.csv',)

#présenter les resultat dans un tablau
print(tabulate(df, headers = 'keys', tablefmt = 'pretty'))

#présenter les resultat dans un graph
sizes = [quic, tcp,]
labels = 'Quic', 'Tcp',
explode = (0, 0.1,)  
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  
plt.show()
    