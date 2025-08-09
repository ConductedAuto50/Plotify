from flask import Flask, render_template, request, session, jsonify
from flask_cors import CORS
import pandas as pd
import json
from zipfile import ZipFile
from analysis import MusicData
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])  # Updated for credentials and specific origin
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True


@app.route('/',methods=['GET', 'POST'])
def index():
    return jsonify({"message": "Hola amigos"})

@app.route('/upload', methods=['GET','POST'])
def upload_file():
    if 'file' not in request.files:
        return {"No file part"}, 400
    file = request.files['file']

    if file.filename == '':
        return "No selected file", 400

    if file and file.filename.endswith('.zip'):
        df= pd.DataFrame()
        with ZipFile(file) as zip_file:
            for filename in zip_file.namelist():
                if filename.startswith('Spotify Extended Streaming History') and filename.endswith('.json'):
                    with zip_file.open(filename) as json_file:
                        data = pd.read_json(json_file)
                        df = pd.concat([df, data], ignore_index=True)
        tz=session.get('timezone',0)
        data=MusicData(df,tz)

        topsong=data.topsong() #dict
        topsinger=data.topsinger() #dict
        tot=data.totalhours() #str
        tod=data.timeofday() #str
        
        session['topsong']=topsong
        session['topsinger']=topsinger
        session['totalhours']=tot
        session['timeofday']=tod
        print(session)
        session.modified = True
        return jsonify("should be saved in session")

#     if file and file.filename.endswith('.json'):

#         df=pd.read_json(file)
#         tz=session.get('timezone',0)
#         data=MusicData(df,tz)
# ##########################################################        #TODO change this 
#         topson,artis,imgurl,songurl=data.topsong()
#         topsinge,imgurl1,songurl1=data.topsinger()
#         tot=data.totalhours()
#         tod=data.timeofday()
        
#         return render_template('result.html',topsing=topsinge,totalh=tot,topso=topson,arti=artis,imgurl=imgurl,songurl=songurl,imgurl1=imgurl1,songurl1=songurl1,tod=tod)
    else:
        return {"Invalid file type. Please upload a .zip or .json file."}, 400


@app.route('/get_insights', methods=['GET'])
def get_insights():
    topsong = session.get('topsong', {})
    topsinger = session.get('topsinger', {})
    totalhours = session.get('totalhours', '')
    timeofday = session.get('timeofday', '')
    print("checkin again")
    print(session)
    return jsonify({
        'topsong': topsong,
        'topsinger': topsinger,
        'totalhours': totalhours,
        'timeofday': timeofday
    })


@app.route('/set_timezone', methods=['POST'])
def set_timezone():
    # Get the time zone from the JSON data sent by JavaScript
    data = request.get_json()
    timezone = data.get('timezone')
    session['timezone'] = timezone    
    return ""


if __name__ == '__main__':
    app.run(debug=True)
