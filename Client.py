import requests
from bs4 import BeautifulSoup
class Client:
    summonerId = -1
    summonerIdx = -1
    currentChamp = -1
    champIds = {}
    champData = {}
    
    def __init__(self):
        self.champIds = self.sourceChampIds()
        self.champData = self.sourceChampData()
        
    def sourceChampIds(self):
        #TODO maybe get game version and pass in as argument to get most updated?
        response = requests.get('http://ddragon.leagueoflegends.com/cdn/13.13.1/data/en_US/champion.json')
        res = response.json()

        champIdDict = {}
        for champ in res['data']:
            champIdDict[int(res['data'][champ]['key'])] = champ
        return champIdDict
    
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