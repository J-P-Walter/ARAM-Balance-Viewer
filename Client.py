import requests
from bs4 import BeautifulSoup

#Class to basically just gather and hold data so its easier to access
#for the main program
class Client:
    summonerId = -1
    summonerIdx = -1
    currentChamp = -1
    champIds = {}
    champData = {}
    
    def __init__(self):
        self.champIds = self.sourceChampIds()
        self.champData = self.sourceChampData()
        
    #Uses community hosted data on all champs, only interested in the champion ids
    #TODO maybe get game version and pass in as argument to get most updated data ie. if a champ is added to the game

    def sourceChampIds(self):
        response = requests.get('http://ddragon.leagueoflegends.com/cdn/13.13.1/data/en_US/champion.json')
        res = response.json()

        champIdDict = {}
        for champ in res['data']:
            champIdDict[int(res['data'][champ]['key'])] = champ
        return champIdDict
    
    #Scrapes the ARAM wiki for champion data, unfortunately it looks like it has a lot of gaps
    #so maybe look into own database as an alternative
    def sourceChampData(self):
        page = requests.get('https://leagueoflegends.fandom.com/wiki/ARAM')
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find_all('tbody')[1]

        champs = {}

        rows = table.find_all('tr')[1:]
        for row in rows:
            data = row.find_all('td')
            champData = {}
            champData['name'] = data[0].text.strip()
            champData['damageDealt'] = data[1].text.strip()
            champData['damageReceived'] = data[2].text.strip()
            champData['otherEffects'] = data[3].text.strip()

            champs[data[0].text.strip().replace('\'','').lower()] = champData
        return champs
    
    def getSummonerId(self):
        return self.summonerId
    def setSummonerId(self, summonerId):
        self.summonerId = summonerId

    def getChampIds(self):
        return self.champIds
    def getChampData(self):
        return self.champData
    
    def getSummonerIdx(self):
        return self.summonerIdx
    def setSummonerIdx(self, summonerIdx):
        self.summonerIdx = summonerIdx

    def getCurrentChamp(self):
        return self.currentChamp
    def setCurrentChamp(self, currentChamp):
        self.currentChamp = currentChamp