import pymongo
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px

#Mongodb Atlas Connection details
mongodb_username="Revathy"
mongodb_password="guvi2024"
mongodb_cluster="Cluster0"
mongodb_database="sample_airbnb"
mongodb_collection="listingsAndReviews"

#Mongodb connection
client = pymongo.MongoClient("mongodb://Revathy:guvi2024@ac-5n8fsfk-shard-00-00.berjwr1.mongodb.net:27017,ac-5n8fsfk-shard-00-01.berjwr1.mongodb.net:27017,ac-5n8fsfk-shard-00-02.berjwr1.mongodb.net:27017/?ssl=true&replicaSet=atlas-11ihco-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0")
db = client[mongodb_database]
coll = db[mongodb_collection]

#Retrieving dataset from Mongodb and converting it into DataFrame
dataset=[]
for i in coll.find():
    data={
        "ID": i['_id'],
        "Listing_URL": i['listing_url'],
        "Name": i['name'],
        "Description": i['description'],
        "Neighborhood overview": i['neighborhood_overview'],
        "House Rules": i.get('house_rules'),
        "Property Type": i ['property_type'],
        "Room Type": i['room_type'],
        "Bed Type": i ['bed_type'],
        "Minimum Nights": int(i['minimum_nights']),
        "Maximum Nights": int(i['maximum_nights']),
        "Cancellation_policy": i['cancellation_policy'],
        "Last_Scraped": i['last_scraped'],
        "Calendar Last Scraped": i['calendar_last_scraped'],
        "Number of Review": i['number_of_reviews'],
        "Amenities": i['amenities'],
        "Price": i['price'],
        "Security Deposit": i.get('security_deposit'),
        "Host ID": i['host']['host_id'],
        "Host Name": i['host']['host_name'],
        "Street": i['address']['street'],
        "Country": i['address']['country'],
        "Country code": i['address']['country_code'],
        "Longitude": i['address']['location']['coordinates'][0],
        "Latitude": i['address']['location']['coordinates'][1],
        "Availability": i['availability']['availability_365'],
        "Review Scores": i['review_scores']
    }
    dataset.append(data)

df=pd.DataFrame(dataset)
