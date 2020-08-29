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
                # Checks for the specific response code that too many requests have been made
                # TODO: Gather the specific number of requests and sleep for needed number of seconds
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
    url = RIOT_WEBSITE + "/lol/summoner/v4/summoners/by-name/" + summonerName + "?api_key=" + api_key
    summoner_data = makeRequest(url)

    # Parse the data and find the account ID
    datas = json.loads(summoner_data.text)
    summID = datas["accountId"]

    # Return the account ID
    return summID


def getMatchIDList(summonerID):
    # Gather the user's match history and return a list of the match IDs
    url = RIOT_WEBSITE + "/lol/match/v4/matchlists/by-account/" + summonerID + "?api_key=" + api_key
    matchlist = makeRequest(url)

    # Go through each match and get the match ID
    matches = json.loads(matchlist.text)
    matches_list = matches["matches"]

    match_ids = []
    for match in matches_list:
        match_ids.append(match["gameId"])
    
    return match_ids
    

# Start of Program Logic
# TODO: Put in API Key manually, will keep in this string version for testing purposes
api_key = "RGAPI-caa14093-8bba-47c7-b82c-7eb65f2074f1"

# Get the wanted summoner name, and then start gathering specific data
summoner_name = input("Summoner Name: ")
summID = getSummonerID(summoner_name)

# Gather the summoner's matchlist to parse through
match_ids = getMatchIDList(summID)