from flask import Flask
from flask import request, redirect
import requests
import os
from flask_cors import CORS
from bs4 import BeautifulSoup
app = Flask(__name__)
cors = CORS(app)



       
@app.route("/query", methods=['POST','GET']) 
def tm():
    year = request.args.get('year')
    eventid = request.args.get('eventid') 

   
    url = 'http://orfeus.gein.noa.gr/gisola/realtime/'+year+'/list_all.html'''
    
    
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    events= soup.select('a[href^="noa"]')
    page="output"+(year)+'.html'
    with open(page, "w") as file:
        file.write(str(events))
    searchfile = open(page, "r")
    for line in searchfile:
        if eventid in line and "output/index.html" in line:
            lastmod=line.split('/')[6]
            print(lastmod)
            
             
                
    url2 = 'http://orfeus.gein.noa.gr/gisola/realtime/'+year+'/'+eventid+'/'+lastmod+'/output/index.html'
    
        

    return redirect(url2)
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
    



