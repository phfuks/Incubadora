from flask import Flask, render_template
import boto3
import re
import time

#Database Connection
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('DHT')

#Scan
resp_Scan = table.scan(ProjectionExpression="R_Day, R_Hour, Temperature")
    

#Start

app=Flask(__name__)

@app.route("/")
def home():
    
    print(type(resp_Scan['Items']))
    
    ScanList=[]    
    for elem in resp_Scan['Items']:
        ScanList.append(elem.values())

    PairedList =[]
    for items in ScanList:
        PairedList.append(list(items))
        
    for i in PairedList:
        print (i[0],":",i[1],":",i[2])
        
    print(type(PairedList))
    
    PairedList.sort()  #ordena as informações

    labels = []
    values = []
    for row in PairedList:
        print (row[0],":",row[1],":",row[2])
        labels.append(row[1])
        values.append(row[2])
       

    return render_template("graph.html", labels=labels, values=values)

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port="5000")