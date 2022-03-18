from flask import Flask
from flask import request, redirect
import requests
import os
from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app)



       
@app.route("/query", methods=['POST','GET']) 
def mw():
    year = request.args.get('year')
    month = request.args.get('month')
    eventid = request.args.get('eventid') 

   
    url = 'http://bbnet.gein.noa.gr/Events/'+year+'/'+month+'/'+eventid+'_info.html'

    
        

    return redirect(url)
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
    



