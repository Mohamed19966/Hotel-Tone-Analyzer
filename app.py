from flask import Flask
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import pandas as pd 
import numpy as np
import json
df = pd.read_csv('7282_1.csv')
apikey='9d_xot7IbgklVQ3j6cEieTfozGgDh4ojZ9snN_MVuIQH'
URL='https://gateway-lon.watsonplatform.net/tone-analyzer/api'
version='2019-10-23'
authenticator = IAMAuthenticator(apikey)
tone_analyzer = ToneAnalyzerV3(
    version=version,
    authenticator=authenticator
)
tone_analyzer.set_service_url(URL)


app = Flask(__name__)

@app.route('/hotels/<hotel_name>')
def hello_world(hotel_name):
    #tones=[]
    hotel_analysis=[]
    tones_dict = {
		"Anger" : 0,
		"Fear" : 0,
		"Joy" : 0,
		"Sadness" : 0,
		"Analytical" : 0,
		"Confident" : 0
	}
    hotels = df['name'] == hotel_name
    
    hotel_df=df[hotels]
    text=hotel_df['reviews.text'].tolist()
    size = np.shape(text)[0]
    count_joy=0;count_fear=0;count_anger=0; count_sadness=0;count_analytical=0;count_confident=0
    for i in range(size):
        tone_analysis = tone_analyzer.tone(
            {'text': text[i]},
            content_type='text/plain',
            sentences=False
        ).get_result()
        if(tone_analysis['document_tone']['tones']):
            tones=tone_analysis['document_tone']['tones']
            hotel_analysis.append(tone_analysis['document_tone']['tones'])
            for j in range(np.shape(tones)[0]):
                if tones[j]['tone_id']=='anger':
                    tones_dict['Anger']+=tones[j]['score']
                    count_anger = count_anger+1
                elif tones[j]['tone_id']=='fear':
                    tones_dict['Fear']+=tones[j]['score']
                    count_fear = count_fear+1
                elif tones[j]['tone_id']=='joy':
                    tones_dict['Joy']+=tones[j]['score']
                    count_joy = count_joy+1
                elif tones[j]['tone_id']=='sadness':
                    tones_dict['Sadness']+=tones[j]['score']
                    count_sadness = count_sadness+1
                elif tones[j]['tone_id']=='analytical':
                    tones_dict['Analytical']+=tones[j]['score']
                    count_analytical = count_analytical+1
                elif tones[j]['tone_id']=='confident':
                    tones_dict['Confident']+=tones[j]['score']
                    count_confident = count_confident+1
    tones_dict['Anger'] = round(tones_dict['Anger']/count_anger,2) if count_anger !=0  else 0
    tones_dict['Fear']  = round(tones_dict['Fear']/count_fear,2) if count_fear  !=0 else  0
    tones_dict['Joy']   = round(tones_dict['Joy']/count_joy,2)   if count_joy   !=0 else  0
    tones_dict['Sadness']=round(tones_dict['Sadness']/count_sadness,2) if count_sadness != 0 else 0
    tones_dict['Analytical']=round(tones_dict['Analytical']/count_analytical,2) if count_analytical !=0 else 0
    tones_dict['Confident']=round(tones_dict['Confident']/count_confident,2) if count_confident  !=0 else 0


    
        
    return json.dumps(tones_dict, indent=2)

if __name__ == '__main__':
   app.run()