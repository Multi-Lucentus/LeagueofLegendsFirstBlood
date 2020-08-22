# Imports
import json
import requests
import time

# Classes
class RequestError:
    except_string = "Request Error"



# Functions
"""
A function that will make an HTTP request to a given URL
Will return the raw string returned from the website
"""
def makeRequest(stringRequest):

    try:
        response = requests.get(stringRequest)

        if response.status_code != 200:
            raise RequestError
    except RequestError as error:
        print("An exception occurred.\n")
        time.sleep(5)
    else:
        time.sleep(0.5)

    return


def getSummonerID(summonerName):
    # Get all of a Summoner's JSON data
    url = ""
    summoner_data = makeRequest(url)

    # Parse the data and find the account ID


    return


def getMatchList(summonerID):
    return




# Start of Program Logic
api_key = "RGAPI-caa14093-8bba-47c7-b82c-7eb65f2074f1"


summoner_name = input("Summoner Name: ")
summ_ID = getSummonerID(summoner_name)