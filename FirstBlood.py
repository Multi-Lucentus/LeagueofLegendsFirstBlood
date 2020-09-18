# Imports
import json
import requests
import time

# Important constants
RIOT_WEBSITE = "https://na1.api.riotgames.com"


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
        print("Issue with response code: " + str(response.status_code) + "\n")
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


def getFirstBloodData(summoner_name, matchlist):
    # Parameter should be a list of match IDs
    # Function will go through each match (by ID) and figure out if the intended user got first blood or killed for first blood
    num_games = len(matchlist)

    num_first_bloods = 0

    # Check the number of games and if we'll need to wait between requests
    # Max requests is 20 requests every 1 second (prbly wont need to worry about) or 
    # 100 requests every 2 minutes
    # Wait 5 seconds between every 20 requests
    counter = 0

    print(summoner_name + "'s Matches (" + str(num_games) + ")")

    for matchId in matchlist:
        # Check the counter number
        if counter == 20:
            print("Sleeeep")
            time.sleep(2)
            counter = 0

        # Make a request to get all of the information for that specific game
        url = RIOT_WEBSITE + "/lol/match/v4/matches/" + str(matchId) + "?api_key=" + api_key
        match_datas = makeRequest(url)
        
        print("Match ID: " + str(matchId))

        # Get the data for that specific match
        match_data = json.loads(match_datas.text)

        # Now to determine who got first blood
        participant_data = match_data["participants"]
        participant_ids = match_data["participantIdentities"]

        part_ID = 0

        for participant in participant_ids:
            player_data = participant["player"]
            if player_data["summonerName"] == summoner_name:
                part_ID = participant["participantId"]

        print("\tParticipant ID: " + str(part_ID))

        # Check what participant got first blood and see if that matches w/ the participant id for entered summoner
        # TODO: Check if enemy laner was the one to get first blood
        for participant in participant_data:
            test_id = participant["participantId"]
            if test_id == part_ID:
                # Check for first blood
                stats = participant["stats"]
                did_first_blood = stats["firstBloodKill"]

                print("\tFirst Blood? " + str(did_first_blood))

                if did_first_blood:
                    num_first_bloods += 1

        counter += 1

    return num_first_bloods


# Start of Program Logic
# TODO: Put in API Key manually, will keep in this string version for testing purposes
api_key = "RGAPI-caa14093-8bba-47c7-b82c-7eb65f2074f1"

# Get the wanted summoner name, and then start gathering specific data
summoner_name = input("Summoner Name: ")

#TODO: Check if summoner name has any spaces and fix

summID = getSummonerID(summoner_name)

# Gather the summoner's matchlist to parse through
match_ids = getMatchIDList(summID)
num_first_bloods = getFirstBloodData(summoner_name, match_ids)

print(summoner_name + " has gotten " + str(num_first_bloods) + " first bloods in their last" + str(len(match_ids)) + "games")