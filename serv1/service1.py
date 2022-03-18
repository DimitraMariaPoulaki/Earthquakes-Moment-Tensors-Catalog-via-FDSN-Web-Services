from flask import Flask
from flask import request, jsonify, render_template, redirect
from obspy import read_events, Catalog, UTCDateTime
from obspy.core.event import read_events
import requests
from datetime import time, datetime
import os
from flask_cors import CORS
from flask import send_from_directory 
app = Flask(__name__)
cors = CORS(app)




@app.route('/index')
@app.route('/')
def index():
    return render_template("index.html")

@app.route("/query", methods=['POST','GET']) 
def minmag():

    starttime = request.args.get('starttime')
    endtime = request.args.get('endtime')
    

    
    
    r = requests.get('http://orfeus.gein.noa.gr:8085/fdsnws/event/1/query?starttime='+starttime+'T00%3A00%3A00&endtime='+endtime+'T00%3A00%3A00&includeallorigins=false&includeallmagnitudes=false&includefocalmechanism=true&minmagnitude=3.5&nodata=404')
  
    file=(starttime)+"_"+(endtime)+'.xml'
    with open(file, 'wb') as f: 
       f.write(r.content)
      

   
    
    data={'data':[]}
    try:

        for evt in read_events(file):
            try:
            
                org=evt.preferred_origin()
                if not org: raise
            
            except:
                try:
                    org=sorted(evt.origins, key=lambda o: o.creation_info.creation_time)[-1]
                except:
                    org=evt.origins[-1]

            try:
                # get moment tensor
                fm=evt.preferred_focal_mechanism()

                # get origin of moment tensor (mt)
                cent_org_id=fm.moment_tensor.derived_origin_id

                # get magnitude associated with the mt's origin
                cent_mag=[m for m in evt.magnitudes if m.origin_id==org.resource_id][0]
               
            except:
                continue
        
            d = {
                "time" : str(org.time).split('.')[0] ,
                "Mw" : round(cent_mag.mag,1),
                "longitude": round(org.longitude,4),
                "latitude": round(org.latitude,4),
                "depth": round(org.depth/1000,0),
                "id": str("{:.2e}".format(fm.moment_tensor.scalar_moment)),
                "try": str(evt.resource_id).split("geofon/")[1],
                "mt" : str(org.time).split('.')[0]+"_"+str(evt.resource_id).split("geofon/")[1],
                "mwa" : str(org.time).split('-')[0]+'_'+str(org.time).split('-')[1]+"_"+str(evt.resource_id).split("geofon/")[1]+"_"+str(round(cent_mag.mag,1)),
                }
            if org.depth > 1000000:
                continue
            if org.depth_errors.uncertainty :
                if org.depth_errors.uncertainty > 100000 :
                    continue
                 
            data["data"].append(d)
            print(org.depth_errors.uncertainty)

    except:
        pass

   


   
    os.remove(file) 
    return jsonify(data)
    
    
   


if __name__ == "__main__":
    app.debug=True
    app.run("0.0.0.0", port=5001)

    



