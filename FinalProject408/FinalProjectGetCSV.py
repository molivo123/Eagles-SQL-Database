import pandas as pd
import mysql.connector


EaglesDB_conn = mysql.connector.connect(host="localhost",
                                       user="root",
                                       password="Aa262626!",
                                       database='EaglesDB')

cursor = EaglesDB_conn.cursor(buffered=True)

dataP = pd.read_csv (r'/Users/matthew/Desktop/School/CPSC408/FinalProject408/CPSC408ProjectDatasets/EaglesPlayersTable.csv', sep=', ', delimiter=',',header=0, engine='python')
dataPAV = pd.read_csv (r'/Users/matthew/Desktop/School/CPSC408/FinalProject408/CPSC408ProjectDatasets/EaglesPlayersAV.csv', sep=', ', delimiter=',',header=0, engine='python')
dataSR = pd.read_csv (r'/Users/matthew/Desktop/School/CPSC408/FinalProject408/CPSC408ProjectDatasets/EaglesTeamSeasonResults.csv', sep=', ', delimiter=',',header=0, engine='python')
dataHC = pd.read_csv (r'/Users/matthew/Desktop/School/CPSC408/FinalProject408/CPSC408ProjectDatasets/EaglesHeadCoachTable.csv', sep=', ', delimiter=',',header=0, engine='python')
dataGM = pd.read_csv (r'/Users/matthew/Desktop/School/CPSC408/FinalProject408/CPSC408ProjectDatasets/EaglesGMsTable.csv', sep=', ', delimiter=',', header=0, engine='python')
dataO = pd.read_csv (r'/Users/matthew/Desktop/School/CPSC408/FinalProject408/CPSC408ProjectDatasets/EaglesOwnersTable.csv', sep=', ', delimiter=',', header=0, engine='python')


dfP = pd.DataFrame(data=dataP)
#print(dfP)

dfPAV = pd.DataFrame(data=dataPAV)
#print(dfPAV)
dfSR = pd.DataFrame(data=dataSR)
dfHC = pd.DataFrame(data=dataHC)
dfGM = pd.DataFrame(data=dataGM)
dfO = pd.DataFrame(data=dataO)

#print(df)

#print(df.shape)
#print(df.columns)


#print(df)


#cursor.execute('CREATE TABLE people_info (Name nvarchar(50), Country nvarchar(50), Age int)')

def Players():
    for row in dfP.itertuples():
        #print(row)
        queryP = "INSERT INTO EaglesDB.Players (PlayerName, YearFrom, YearTo, GamesPlayed, Position, After1960) VALUES (%s,%s,%s,%s,%s,%s)"

        valueP = (row.PlayerName, row.YearFrom, row.YearTo, row.GamesPlayed, row.Position,row.After1960)

        cursor.execute(queryP, valueP)

def PlayersAV():
    for row in dfPAV.itertuples():
        queryPAV = "INSERT INTO EaglesDB.PlayersAV (PlayerName, AV) VALUES (%s,%s)"
        valuePAV = (row.PlayerName, row.AV)

        cursor.execute(queryPAV, valuePAV)

def SeasonResult():
    for row in dfSR.itertuples():
        querySR = "INSERT INTO EaglesDB.SeasonResults (Year, Wins, Losses, Ties, PlayoffRun, PtsFor,PtsAgainst, PtsDifferential) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        valueSR = (
        row.Year, row.W, row.L, row.T, row.Playoffs, row.PF, row.PA, row.PD)

        cursor.execute(querySR, valueSR)

def HeadCoaches():
    for row in dfHC.itertuples():
        queryHC = "INSERT INTO EaglesDB.HeadCoaches (Name, YearFrom, YearTo,GamesCoached,Wins,Losses, Ties) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        valueHC = (row.Name, row.From, row.To, row.Games, row.Wins, row.Losses, row.Ties)

        cursor.execute(queryHC, valueHC)

def GMs():
    for row in dfGM.itertuples():
        queryE = "INSERT INTO EaglesDB.GMs (Name, YearFrom, YearTo) VALUES (%s,%s,%s)"
        valueE = (row.Name, row.From, row.To)

        cursor.execute(queryE, valueE)

def Owners():
    for row in dfO.itertuples():
        queryE = "INSERT INTO EaglesDB.Owners (Name, YearFrom, YearTo) VALUES (%s,%s,%s)"
        valueE = (row.Name, row.From, row.To)

        cursor.execute(queryE, valueE)



Players()
PlayersAV()
SeasonResult()
HeadCoaches()
GMs()
Owners()

print("Done")


select_players_query = "SELECT * FROM EaglesDB.Players"
select_playersAV_query = "SELECT * FROM EaglesDB.PlayersAV"
select_Team_query = "SELECT * FROM EaglesDB.SeasonResults"
select_Coaches_query = "SELECT * FROM EaglesDB.HeadCoaches"
select_GMs_query = "SELECT * FROM EaglesDB.GMs"
select_Owners_query = "SELECT * FROM EaglesDB.Owners"


#cursor.execute(select_players_query)
#records = cursor.fetchall()

'''for row in records:
    print("PlayerName= ", row[0], )
    print("YearFrom = ", row[1])
    print("YearTo = ", row[2])
    print("GamesPlayed = ", row[3])
    print("Position = ", row[4])
    print("After1960= ", row[5], "\n")
    '''

#cursor.execute(select_playersAV_query)
#records = cursor.fetchall()

#for row in records:
#    print("PlayerName= ", row[0], )
#    print("AV = ", row[1],"\n")


EaglesDB_conn.commit()

cursor.close()

