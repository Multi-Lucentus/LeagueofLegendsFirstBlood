# Imports
import json
import requests
import time

# Important constants
RIOT_WEBSITE = "https://na1.api.riotgames.com"
STATIC_WEBSITE = "http://static.developer.riotgames.com"


# Classes
class RequestError(Exception):
    """Raised when an error comes up with a request"""
    pass


# Functions
"""
A function that will make an HTTP request to a given URL
Will return the raw string returned from the website
"""
def makeRequest(stringRequest):

    try:
        response = requests.get(stringRequest)

        # Check for issues with the response code
        if response.status_code != 200:
            if response.status_code == 400:
                time.sleep(5)
                makeRequest(stringRequest)
            else:
                raise RequestError

    except RequestError as error:
        print("Issue with response code.\n")
    else:
        # Sleep for a second to avoid issues
        time.sleep(0.5)

    return response


def getSummonerID(summonerName):
    # Get all of a Summoner's JSON data
    url = ""
    summoner_data = makeRequest(url)

    # Parse the data and find the account ID


    return


def getMatchList(summonerID):
    return


def getPatchNumber():
    return


# Start of Program Logic
# TODO: Put in API Key manually, will keep in this string version for testing purposes
api_key = "RGAPI-caa14093-8bba-47c7-b82c-7eb65f2074f1"


summoner_name = input("Summoner Name: ")
summ_ID = getSummonerID(summoner_name)