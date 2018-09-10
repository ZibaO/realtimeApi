from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .serializers import RequestSerializer
from .models import Request
from django.shortcuts import render
import requests
import time
import datetime
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
import pickle
import sqlite3
from sqlite3 import Error

from django.http import JsonResponse


class CreateViewGaussian(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Request.objects.all()
    serializer_class = RequestSerializer


    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        #create_and_save_model()
        serializer.save()



class CreateViewMultinomial(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()

class CreateViewBernoulli(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()


def home(request):
    create_and_save_model()
    return render(request, 'home.html', {
    })

def create_connection(db_file):#     create a database connection to the SQLite database specified by db_file
    try:
        conn = sqlite3.connect(db_file)
        return conn #return Connection object or None
    except Error as e:
        print (e)
    return None

def create_table(conn, create_table_sql):#     create a table from the create_table_sql statement
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
def insert_model(conn,modelName,model):#       insert models to table
    cur = conn.cursor()
    # Here we force pickle to use the efficient binary protocol
    # (protocol=2). This means you absolutely must use an SQLite BLOB field
    # and make sure you use sqlite3.Binary() to bind a BLOB parameter.
    cur.execute("insert into models(name,model) values (?,?)", (modelName,sqlite3.Binary(pickle.dumps(model, protocol=2)),))
    # If we use old pickle protocol (protocol=0, which is also the default),
    # we get away with sending ASCII bytestrings to SQLite.
    #cur.execute("insert into models(name,model) values (?,?)", (pickle.dumps(gnb1, protocol=0),))

def create_and_save_model():

    # In[3]:

    data = pd.read_csv('character-predictions_pose.csv')
    data4 = pd.read_csv('uci-news-aggregator.csv')

    # In[4]:

    # to avoid 'Could not convert string to float on dataset' error
    for column in data.columns:
        le = LabelEncoder()
        data[column] = le.fit_transform(data[column].astype(str))
        if data[column].dtype == type(object):
            data[column] = le.fit_transform(data[column])  # Fit label encoder and return encoded labels

    for column in data4.columns:
        le = LabelEncoder()
        data4[column] = le.fit_transform(data4[column].astype(str))
        if data4[column].dtype == type(object):
            data4[column] = le.fit_transform(data4[column])  # Fit label encoder and return encoded labels

    # In[5]:

    x = data.drop('isAlive', axis=1)
    y = data['isAlive']
    x2 = data4.drop('CATEGORY', axis=1)
    y2 = data4['CATEGORY']

    # In[6]:

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    x2_train, x2_test, y2_train, y2_test = train_test_split(x2, y2, test_size=0.2)

    # In[7]:

    gnb1 = GaussianNB()
    gnb2 = MultinomialNB()
    gnb3 = BernoulliNB()

    gnb1.fit(x_train, y_train)
    y_pred = gnb1.predict(x_test)
    print(gnb1.score(x_test, y_test))

    # In[8]:

    gnb2.fit(x2_train, y2_train)
    y2_pred = gnb2.predict(x2_test)
    print(gnb2.score(x2_test, y2_test))

    # In[9]:

    gnb3.fit(x_train, y_train)
    y_pred = gnb3.predict(x_test)
    print(gnb3.score(x_test, y_test))

    gnb3.fit(x2_train, y2_train)
    y3_pred = gnb3.predict(x2_test)
    print(gnb3.score(x2_test, y2_test))
    y3_pred

    # In[17]:
    # "DROP TABLE models;"
    data = pd.read_csv('character-predictions_pose.csv')
    data4 = pd.read_csv('uci-news-aggregator.csv')




    x = data.drop('isAlive', axis=1)
    y = data['isAlive']
    x2 = data4.drop('CATEGORY', axis=1)
    y2 = data4['CATEGORY']

    # In[6]:

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    x2_train, x2_test, y2_train, y2_test = train_test_split(x2, y2, test_size=0.2)
    database = "/Users/ziba/PycharmProjects/try6/realtime/database.db"
    sql_create_models_table = """CREATE TABLE IF NOT EXISTS models(
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    model BLOB NOT NULL);"""
    conn = sqlite3.connect(database)
    # create models table
    cur = conn.cursor()
    cur.execute(sql_create_models_table)
    # Here we force pickle to use the efficient binary protocol
    # (protocol=2). This means you absolutely must use an SQLite BLOB field
    # and make sure you use sqlite3.Binary() to bind a BLOB parameter.
    modelName1 = "Gaussian"
    modelName2 = "Multinomial"
    modelName3 = "Bernoulli"
    cur.execute("insert into models(name,model) values (?,?)",
                (modelName1, sqlite3.Binary(pickle.dumps(gnb1, protocol=2)),))
    cur.execute("insert into models(name,model) values (?,?)",
                (modelName2, sqlite3.Binary(pickle.dumps(gnb2, protocol=2)),))
    cur.execute("insert into models(name,model) values (?,?)",
                (modelName3, sqlite3.Binary(pickle.dumps(gnb3, protocol=2)),))
    # If we use old pickle protocol (protocol=0, which is also the default),
    # we get away with sending ASCII bytestrings to SQLite.
    # cur.execute("insert into models(name,model) values (?,?)", (pickle.dumps(gnb1, protocol=0),))

    # Fetch the BLOBs back from SQLite

    nameOfModel = "Gaussian"
    cur.execute("select model from models")
   # cur.execute("SELECT model FROM models WHERE name=?", (nameOfModel,))
    for row in cur:
        serializedModel = row[0]
        # Deserialize the BLOB to a Python object - # pickle.loads() needs a
        # bytestring.
        loadedModel = pickle.loads(serializedModel)  # (str(serialized_point))
        # print("got model back from database", loadedModel)
        y_pred = loadedModel.predict(x2_test)
        return y_pred


    # sql_create_models_table = """CREATE TABLE IF NOT EXISTS models(
    #                                 id integer PRIMARY KEY,
    #                                 name text NOT NULL,
    #                                 model BLOB NOT NULL);"""

    # create a database connection
    # conn = create_connection(database)
    # if conn is not None:
    #     # create models table
    #     create_table(conn, sql_create_models_table)
    #     insert_model(conn, "Gaussian", gnb1)
    #     insert_model(conn, "Multinomial", gnb2)
    #     insert_model(conn, "Bernoulli", gnb3)
    # else:
    #     print("Error! cannot create the database connection.")

    # "DROP TABLE models;"
def load_model(name_of_model,input):


    # rows = cur.fetchall()

    data = pd.read_csv('character-predictions_pose.csv')
    data4 = pd.read_csv('uci-news-aggregator.csv')




    x = data.drop('isAlive', axis=1)
    y = data['isAlive']
    x2 = data4.drop('CATEGORY', axis=1)
    y2 = data4['CATEGORY']

    # In[6]:

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    x2_train, x2_test, y2_train, y2_test = train_test_split(x2, y2, test_size=0.2)



    database = "/Users/ziba/PycharmProjects/try6/realtime/db.sqlite3"
    conn = sqlite3.connect(database)
    # create models table
    cur = conn.cursor()
    #conn = create_connection(database)
    #cur = conn.cursor()
    nameOfModel = name_of_model
    cur.execute("SELECT model FROM models WHERE name=?", (nameOfModel,))
    for row in cur:
        serializedModel = row[0]
        # Deserialize the BLOB to a Python object - # pickle.loads() needs a
        # bytestring.
        loadedModel = pickle.loads(serializedModel)  # (str(serialized_point))
        #print("got model back from database", loadedModel)
        y_pred=loadedModel.predict(x2_test)
        return  y_pred







def predictRequestGaussian(request):


    response = requests.get('http://127.0.0.1:8000/requestsGaussian/?format=json')
    data = response.json()
    count = len(data)
    input_string = data[count-1]['string']
    _input = data[count-1]['string'].split(',')
    request_time = data[count-1]['date_created']
    id = data[count-1]['id']
    pred=create_and_save_model()
    #pred=load_model("Multinomial",_input)

    return render(request, 'Gaussian.html', {
        'input_string' : input_string,
        'string' : _input,
        'prediction' : pred ,
        'request_time' : request_time,
        'id' : id,

    })




def predictRequestMultinomial(request):

    response = requests.get('http://127.0.0.1:8000/requestsMultinomial/?format=json')
    data = response.json()
    count = len(data)
    input_string = data[count-1]['string']
    string = data[count-1]['string'].split(',')
    request_time = data[count-1]['date_created']
    id = data[count-1]['id']
    y_pred=load_model("Multinomial",string)

    return render(request, 'Gaussian.html', {
        'input_string' : input_string,
        'string' : string,
        'prediction' : y_pred ,
        'request_time' : request_time,
        'id' : id,

    })
def predictRequestBernoull(request):

    response = requests.get('http://127.0.0.1:8000/requestsBernoulli/?format=json')
    data = response.json()
    count = len(data)
    input_string = data[0]['string']
    string = data[0]['string'].split(',')
    request_time = data[0]['date_created']
    id = data[0]['id']
    y_pred=load_model("Bernoulli",string)

    return render(request, 'Gaussian.html', {
        'input_string' : input_string,
        'string' : string,
        'prediction' : y_pred ,
        'request_time' : request_time,
        'id' : id,

    })

