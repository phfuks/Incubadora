from flask import Flask, render_template
import boto3
import re

#Database Connection
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('DHT')

#Scan
resp_R_Hour = table.scan(ProjectionExpression="R_Hour")
resp_Temperature = table.scan(ProjectionExpression="Temperature")
    

#Start

app=Flask(__name__)

@app.route("/")
def home():         
    
    resp_Temperature['Items']=re.sub("{|}|'","",str(resp_Temperature['Items']))
    resp_Temperature['Items']=re.sub("Temperature: ","",str(resp_Temperature['Items']))

    print(resp_R_Hour['Items'])
    print(resp_Temperature['Items'])
    
    #print(type(resp_R_Hour['Items']))
    #print(type(labels))
    
    #print(type(resp_Temperature['Items']))
    #print(type(values))
    
    labels = []
    for row in resp_R_Hour['Items']:
        row=re.sub("{|}|'","",str(row))
        row=re.sub("R_Hour: ","",str(row))
        labels.append(row)
        print (row)

    return render_template("graph.html", labels=labels, values=resp_Temperature['Items'])

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port="5001")