from flask import Flask,render_template,url_for,request,redirect, make_response
import os
import binascii
import sys
import datetime
import boto3
import Adafruit_DHT
import threading
import json
from time import time
import datetime
from random import random

app = Flask(__name__)

class MyDb(object):

    def __init__(self, Table_Name='DHT'):
        self.Table_Name=Table_Name

        self.db = boto3.resource('dynamodb')
        self.table = self.db.Table(Table_Name)

        self.client = boto3.client('dynamodb')

    @property
    def get(self):
        response = self.table.get_item(
            Key={
                'Sensor_Id':"1"
            }
        )

        return response

    def put(self, Sensor_Id='' , Temperature='', Humidity='', R_Day='', R_Hour=''):
        self.table.put_item(
            Item={
                'Sensor_Id':Sensor_Id,
                'Temperature':Temperature,
                'Humidity' :Humidity,
                'R_Day': R_Day,
                'R_Hour': R_Hour
            }
        )

    def delete(self,Sensor_Id=''):
        self.table.delete_item(
            Key={
                'Sensor_Id': Sensor_Id
            }
        )

    def describe_table(self):
        response = self.client.describe_table(
            TableName='Sensor'
        )
        return response

    @staticmethod
    def sensor_value():

        pin = 4
        sensor = Adafruit_DHT.DHT22

        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        else:
            print('Failed to get reading. Try again!')
        return temperature, humidity


@app.route('/', methods=["GET", "POST"])
def main():
    return render_template('index.html')



@app.route('/data', methods=["GET", "POST"])
def data():
    
    now = datetime.datetime.now()
    R_Day = now.strftime("%m/%d/%Y")
    R_Hour = now.strftime("%H:%M:%S")
    #threading.Timer(interval=6, function=main).start() #### REVER!
    obj = MyDb()
    Temperature , Humidity = obj.sensor_value()
    randomHash=binascii.hexlify(os.urandom(16)).decode()
    if R_Day and R_Hour is not None:   #alterar para: se dia e hora for nulo, obter dia e hora, talvez em while...
        obj.put(Sensor_Id=str(randomHash), Temperature=str(round(Temperature,3)), Humidity=str(round(Humidity,3)), R_Day=R_Day, R_Hour=R_Hour)
        print(randomHash,"Uploaded Sample on Cloud T:{0:0.1f},H:{1:0.1f} ".format(Temperature, Humidity))
   
    data = [time()*1000, Temperature]   #  data = [time()*1000, random()]
    #stamp=datetime.datetime.fromtimestamp(time())
    #print(stamp)


    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response


if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host="0.0.0.0")