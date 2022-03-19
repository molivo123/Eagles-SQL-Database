import mysql.connector
import csv
from tabulate import tabulate

EaglesDB_conn = mysql.connector.connect(host="localhost",
                                       user="root",
                                       password="Aa262626!",
                                       database='EaglesDB')

cursor = EaglesDB_conn.cursor(buffered=True)


def viewOption1():
#total view options, allow user to see entire table
    while True:
    #continuous prompt for selection input
        try:
            print("type 'player' to view All players that have recorded a statistic for The Philadelphia Eagles Organization.")
            print("type 'playerav' to view players that have been part of The Philadelphia Eagles Organization and their VALUE since 1960")
            print("type 'coach' to view All coaches that have coached for The Philadelphia Eagles Organization.")
            print("type 'gm' to view All GMs that have worked for The Philadelphia Eagles Organization.")
            print("type 'owner' to view All Owners that have owned for The Philadelphia Eagles Organization.")
            print("type 'teamseason' to view every Season Result for the Philadelphia Eagles.")
            print("type 'quit' to return to options")
            user_choice = input("Please enter your selection here: ")

            if user_choice == 'player':

                user_viewplayer_choice = input("would you like to view the whole player table (type 'player') or view filtered options (type 'filter'): ")

                if user_viewplayer_choice == 'player':
                    # views whole table
                    query = "select * from EaglesDB.Players;"

                    cursor.execute(query)
                    result = cursor.fetchall()
                    print(tabulate(result,headers=["PlayerName\ID","YearFrom","YearTo","GamesPlayed","Position","DidTheyPlayAfter1960"]))

                elif user_viewplayer_choice == 'filter':
                    #opens up other options for viewing
                    player_filter_choice = input("which variables would you like to filter by: gamesplayed or av? ")
                    group_or_limit_choice = input("do you want to see grouped averages (type 'group') or limited views (type 'limit'): ")
                    if player_filter_choice.lower() not in ('gamesplayed','av'):
                        if group_or_limit_choice.lower() not in ('group', 'limit'):
                            print("Not an appropriate choice.")
                    else:

                        if player_filter_choice == 'gamesplayed':
                            #sort option
                            if group_or_limit_choice == 'limit':
                                try:
                                    limitChoice = (int(input("how many players would you like to limit this to? ")),)
                                except ValueError:
                                    print("That's not an int!")
                                    continue
                                if limitChoice != 0:
                                    query = "select * from EaglesDB.Players order by GamesPlayed desc LIMIT %s;"
                                    cursor.execute(query, limitChoice)
                                    result = cursor.fetchall()
                                    print(tabulate(result, headers=["PlayerName\ID", "YearFrom", "YearTo", "GamesPlayed","Position", "DidTheyPlayAfter1960"]))
                            elif group_or_limit_choice == 'group':
                                query = '''select PL.Position,avg(PL.GamesPlayed) from EaglesDB.Players PL left join EaglesDB.PlayersAV AV on PL.PlayerName = AV.PlayerName
                                            group by PL.Position;'''
                                #group by/aggregated query
                                cursor.execute(query)
                                result = cursor.fetchall()
                                print(tabulate(result, headers=["Position", "Number of Gamesplayed"]))

                        elif player_filter_choice == 'av':
                            #sort option
                            if group_or_limit_choice == 'limit':
                                try:
                                    limitChoice = (int(input("how many players would you like to limit this to? ")),)
                                except ValueError:
                                    print("That's not an int!")
                                    continue
                                if limitChoice != 0:
                                    query = "select PL.PlayerName, PL.YearFrom, PL.YearTo, PL.GamesPlayed,PL.Position,AV.AV from EaglesDB.Players PL left join EaglesDB.PlayersAV AV on PL.PlayerName = AV.PlayerName order by AV.AV desc LIMIT %s;"
                                    cursor.execute(query, limitChoice)
                                    result = cursor.fetchall()
                                    print(tabulate(result,headers=["PlayerName\ID", "YearFrom", "YearTo", "GamesPlayed","Position", "AV"]))
                            elif group_or_limit_choice == 'group':
                                group_choice = input("Do you want to group by position or yearfrom? ")

                                if group_choice not in ('position','yeafrom'):
                                    print("Not an appropriate choice.")

                                else:

                                    query = '''select PL.Position,avg(AV.AV) from EaglesDB.Players PL left join EaglesDB.PlayersAV AV on PL.PlayerName = AV.PlayerName
                                                                                group by PL.Position;'''
                                    cursor.execute(query)
                                    result = cursor.fetchall()
                                    print(tabulate(result, headers=["Position", " AverageAV"]))

            elif user_choice == 'playerav':
                #view another entire table
                query = "select * from EaglesDB.PlayersAV;"

                cursor.execute(query)
                result = cursor.fetchall()
                print(tabulate(result, headers=["PlayerName\ID", "AV"]))

            elif user_choice == 'coach':
                #view another entire table

                query = "select * from EaglesDB.HeadCoaches;"

                cursor.execute(query)
                result = cursor.fetchall()
                print(tabulate(result, headers=["CoachName","YearFrom","YearTo","GamesCoached","Wins","Losses","Ties"]))


            elif user_choice == 'gm':
                #view another entire table

                query = "select * from EaglesDB.Executives;"

                cursor.execute(query)
                result = cursor.fetchall()
                print(tabulate(result,headers=["GMName","YearFrom","YearTo"]))

            elif user_choice == 'owner':
                #view another entire table

                query = "select * from EaglesDB.Executives;"

                cursor.execute(query)
                result = cursor.fetchall()
                print(tabulate(result,headers=["OwnerName","YearFrom","YearTo"]))

            elif user_choice == 'teamseason':
                #view another entire table

                query = "select * from EaglesDB.SeasonResults;"

                cursor.execute(query)
                result = cursor.fetchall()
                print(tabulate(result, headers=["SeasonYear","Wins","Losses","Ties","PlayoffRun","PtsFor","PtsAgainst","PtsDifferential"]))

            elif user_choice == 'quit':
                MenuOptions()

            else:
                print("Sorry that wasn't a valid option")
                #error checking

        except ValueError:
            #invalid input handling
            print("invalid input try again")
            continue

def viewOption2():
    #more advanced view option
    while True:
        user_choice1 = input("Do you want to view player's by coach, owner, GM, teamseason ,all, or type 'quit' to return to menu? ")
        #prompt to choose filter option
        if user_choice1.lower() in ('coach', 'owner', 'gm', 'teamseason' ,'all'):
            break

        elif user_choice1 == 'quit':
            MenuOptions()

    while True:
        if user_choice1 == 'coach':
            query = "select * from EaglesDB.HeadCoaches;"
            cursor.execute(query)
            result = cursor.fetchall()
            print(
                tabulate(result, headers=["CoachName", "YearFrom", "YearTo", "GamesCoached", "Wins", "Losses", "Ties"]))

            print("I printed all coaches above to help you copy and paste the correct ID")

            coach_choice = input(("Which coach's players, GMs, and owners would you like to view? Please enter the valid Coach ID from above and see their players (or type 'quit to exit'): "), )
            if coach_choice != '':
                #big join to find every record that was on the team at the same time as a praticular coach
                query = '''
                            select PL.PlayerName, PL.YearFrom, PL.YearTo,AV.AV, GM.Name,GM.YearFrom,GM.YearTo,O.Name,O.YearFrom,O.YearTo
                            from EaglesDB.Players PL left join EaglesDB.PlayersAV AV on PL.PlayerName = AV.PlayerName 
                            left join EaglesDB.GMs GM on PL.YearFrom >= GM.YearFrom and PL.YearFrom <= GM.YearTo or PL.YearTo >= GM.YearTo and PL.YearTo <= GM.YearFrom
                            left join EaglesDB.Owners O on PL.YearFrom >= O.YearFrom and PL.YearFrom <= O.YearTo or PL.YearTo >= O.YearTo and PL.YearTo <= O.YearFrom
                            
                            WHERE PL.YearFrom  >= (SELECT HC.YearFrom FROM EaglesDB.HeadCoaches HC
                            WHERE HC.Name = %s) and PL.YearFrom <= (SELECT HC.YearTo FROM EaglesDB.HeadCoaches HC
                            WHERE HC.Name = %s);'''

                cursor.execute(query, (coach_choice, coach_choice))
                result = cursor.fetchall()
                print(tabulate(result, headers=["PlayerName\ID", "YearFrom", "YearTo", "AV", 'GMName','YearFrom','YearTo','OwnerName','YearFrom','YearTo']))

                again_input = input("press enter to run another similar query or type 'quit' return to the menu: ")

                if again_input == 'quit':
                    MenuOptions()
                else:
                    pass

            elif coach_choice == 'quit':
                MenuOptions()

        elif user_choice1 == 'gm':
            query = "select * from EaglesDB.GMs;"
            cursor.execute(query)
            result = cursor.fetchall()
            print(tabulate(result, headers=["GMName", "YearFrom", "YearTo"]))

            print("I printed all GMs above to help you copy and paste the correct ID")

            gm_choice = input(("Which GM's coach, owners, and players would you like to view? Please enter the valid GM ID from above and see their players (or type 'quit to exit'): "), )
            if gm_choice != '':
                #big join to find every record that was on the team at the same time as a praticular gm
                query = '''
                            select PL.PlayerName, PL.YearFrom, PL.YearTo,AV.AV, HC.Name,HC.YearFrom,HC.YearTo,O.Name,O.YearFrom,O.YearTo
                            from EaglesDB.Players PL left join EaglesDB.PlayersAV AV on PL.PlayerName = AV.PlayerName 
                            left join EaglesDB.HeadCoaches HC on PL.YearFrom >= HC.YearFrom and PL.YearFrom <= HC.YearTo or PL.YearTo >= HC.YearTo and PL.YearTo <= HC.YearFrom
                            left join EaglesDB.Owners O on PL.YearFrom >= O.YearFrom and PL.YearFrom <= O.YearTo or PL.YearTo >= O.YearTo and PL.YearTo <= O.YearFrom

                            WHERE PL.YearFrom  >= (SELECT GM.YearFrom FROM EaglesDB.GMs GM
                            WHERE GM.Name = %s) and PL.YearFrom <= (SELECT GM.YearTo FROM EaglesDB.GMs GM
                            WHERE GM.Name = %s);'''

                cursor.execute(query, (gm_choice, gm_choice))
                result = cursor.fetchall()
                print(tabulate(result,headers=["PlayerName\ID", "YearFrom", "YearTo", "AV", 'HCName', 'YearFrom', 'YearTo','OwnerName', 'YearFrom', 'YearTo']))

                again_input = input("press enter to run another similar query or type 'quit' return to the menu: ")

                if again_input == 'quit':
                    MenuOptions()
                else:
                    pass

            elif gm_choice == 'quit':
                MenuOptions()

        elif user_choice1 == 'owner':
            query = "select * from EaglesDB.Owners;"
            cursor.execute(query)
            result = cursor.fetchall()
            print(tabulate(result, headers=["OwnerName", "YearFrom", "YearTo"]))

            print("I printed all Owners above to help you copy and paste the correct ID")

            owner_choice = input(("Which Owners' players would you like to view? Please enter the valid Owner ID from above and see their players (or type 'quit to exit'): "), )
            if owner_choice != '':
                #big join to find every record that was on the team at the same time as a praticular owner
                query = '''
                            select PL.PlayerName, PL.YearFrom, PL.YearTo,AV.AV, HC.Name,HC.YearFrom,HC.YearTo,GM.Name,GM.YearFrom,GM.YearTo
                            from EaglesDB.Players PL left join EaglesDB.PlayersAV AV on PL.PlayerName = AV.PlayerName 
                            left join EaglesDB.HeadCoaches HC on PL.YearFrom >= HC.YearFrom and PL.YearFrom <= HC.YearTo or PL.YearTo >= HC.YearTo and PL.YearTo <= HC.YearFrom
                            left join EaglesDB.GMs GM on PL.YearFrom >= GM.YearFrom and PL.YearFrom <= GM.YearTo or PL.YearTo >= GM.YearTo and PL.YearTo <= GM.YearFrom

                            WHERE PL.YearFrom  >= (SELECT O.YearFrom FROM EaglesDB.Owners O
                            WHERE O.Name = %s) and PL.YearFrom <= (SELECT O.YearTo FROM EaglesDB.Owners O
                            WHERE O.Name = %s);'''

                cursor.execute(query, (owner_choice, owner_choice))
                result = cursor.fetchall()
                print(tabulate(result,headers=["PlayerName\ID", "YearFrom", "YearTo", "AV", 'HCName', 'YearFrom', 'YearTo','GMName', 'YearFrom', 'YearTo']))

                again_input = input("press enter to run another similar query or type 'quit' return to the menu: ")

                if again_input == 'quit':
                    MenuOptions()
                else:
                    pass

            elif owner_choice == 'quit':
                MenuOptions()

        elif user_choice1 == 'teamseason':
            season_choice = int(input("Enter a season year between 1933-2020 to view it's players: "))
            if season_choice != 0:
                query = '''select Players.PlayerName, Players.YearFrom, Players.YearTo, GamesPlayed, Position, After1960 from EaglesDB.Players
                WHERE (SELECT SeasonResults.Year FROM EaglesDB.SeasonResults
                WHERE SeasonResults.Year = '%s') between Players.YearFrom and Players.YearTo;
                '''
                cursor.execute(query, season_choice)
                result = cursor.fetchall()
                print(tabulate(result, headers=["PlayerName\ID", "YearFrom", "YearTo", "GamesPlayed", "Position","DidTheyPlayAfter1960"]))

                again_input = input("press enter to run another similar query or type 'quit' return to the menu: ")

                if again_input == 'quit':
                    MenuOptions()
                else:
                    pass

        elif user_choice1 == 'all':
            # big join to find every record that has every combination of player coach gm owner
            query = '''
            select PlayerName,PL.YearFrom,PL.YearTo,HC.Name,HC.YearFrom,HC.YearTo,GM.Name,GM.YearFrom,GM.YearTo,O.Name,O.YearFrom,O.YearTo
            from EaglesDB.Players PL left outer join EaglesDB.HeadCoaches HC on PL.YearFrom >= HC.YearFrom and PL.YearFrom <= HC.YearTo or PL.YearTo >= HC.YearTo and PL.YearTo <= HC.YearFrom
                left outer join EaglesDB.GMs GM on PL.YearFrom >= GM.YearFrom and PL.YearFrom <= GM.YearTo or PL.YearTo >= GM.YearTo and PL.YearTo <= GM.YearFrom
                left outer join EaglesDB.Owners O on PL.YearFrom >= O.YearFrom and PL.YearFrom <= O.YearTo or PL.YearTo >= O.YearTo and PL.YearTo <= O.YearFrom
                union all
            select PlayerName,PL.YearFrom,PL.YearTo,HC.Name,HC.YearFrom,HC.YearTo,GM.Name,GM.YearFrom,GM.YearTo,O.Name,O.YearFrom,O.YearTo
            from EaglesDB.Players PL right outer join EaglesDB.HeadCoaches HC on PL.YearFrom >= HC.YearFrom and PL.YearFrom <= HC.YearTo or PL.YearTo >= HC.YearTo and PL.YearTo <= HC.YearFrom
                right outer join EaglesDB.GMs GM on PL.YearFrom >= GM.YearFrom and PL.YearFrom <= GM.YearTo or PL.YearTo >= GM.YearTo and PL.YearTo <= GM.YearFrom
                right outer join EaglesDB.Owners O on PL.YearFrom >= O.YearFrom and PL.YearFrom <= O.YearTo or PL.YearTo >= O.YearTo and PL.YearTo <= O.YearFrom;
            '''
            cursor.execute(query)
            result = cursor.fetchall()
            print(tabulate(result,
                               headers=["PlayerName\ID", "YearFrom", "YearTo", "HeadCoachName", "YearFrom", "YearTo",
                                        "GMName", "YearFrom", "YearTo", "OwnerName", "YearFrom", "YearTo"]))

            again_input = input("press enter to run another similar query or type 'quit' return to the menu: ")

            if again_input == 'quit':
                MenuOptions()
            else:
                break

        elif user_choice1 == 'quit':
            MenuOptions()

        else:
            print("Sorry that wasn't a valid option")



def createOption3():
    while True:
        try:
            user_choice = input("Would you like to create a player, coach, owner, gm, teamseason, or quit? ")

            if user_choice == 'player':
                user_inputName = input("Enter name here: ")
                user_startYear = int(input("Enter start year here: "))
                if len(str(user_startYear)) == 4 and user_startYear < 2020 and user_startYear > 1900:
                    #checking for valid year
                    pass
                else:
                    print("That is an invalid year, please try again.")
                    continue
                user_endYear = int(input("Enter last year here: "))
                if len(str(user_endYear)) == 4 and user_startYear < user_endYear and user_startYear < 2020 and user_startYear > 1900 and user_endYear < 2020 :
                    pass
                else:
                    print("That is an invalid year, please try again.")
                    continue

                user_inputGamesPlayed = int(input("Enter number of games played here: "))

                user_inputPosition = input("Enter position here: ")

                after1960 = 0

                if user_endYear > 1959:
                    after1960 = 1
                else:
                    pass
                #insert into particular table a custom entry

                query = ("INSERT INTO EaglesDB.Players(PlayerName, YearFrom, YearTo, Gamesplayed,Position, After1960) values(%s,%s,%s,%s,%s,%s)")
                new_player = (user_inputName, user_startYear, user_endYear, user_inputGamesPlayed,user_inputPosition,after1960)

                cursor.execute(query, new_player)
                EaglesDB_conn.commit()
                print("Record has been created")


            elif user_choice == 'coach':
                #same as player with similar year checking but different other fields
                user_inputName = input("Enter name here: ")
                user_startYear = int(input("Enter start year here: "))
                if len(str(user_startYear)) == 4 and user_startYear < 2020 and user_startYear > 1900 :
                    pass
                else:
                    print("That is an invalid year, please try again.")
                    continue
                user_endYear = int(input("Enter last year here: "))
                if len(str(user_endYear)) == 4 and user_startYear < user_endYear and user_startYear < 2020 and user_startYear > 1900 and user_endYear < 2020:
                    pass
                else:
                    print("That is an invalid year, please try again.")
                    continue
                user_inputGamesCoached = int(input("Enter number of games coached here: "))
                user_inputWins = int(input("Enter number of wins here: "))
                user_inputLosses = int(input("Enter number of losses here: "))
                user_inputTies = int(input("Enter number of ties here: "))

                if (user_inputWins + user_inputLosses+ user_inputTies !=user_inputGamesCoached):
                    print("The number of wins losses and ties do not equal the number of games coached, please try again.")
                    continue

                query = ("INSERT INTO EaglesDB.HeadCoaches(Name, YearFrom, YearTo, GamesCoached,Wins, Losses,Ties) values(%s,%s,%s,%s,%s,%s,%s)")
                new_coach = (user_inputName, user_startYear, user_endYear, user_inputGamesCoached, user_inputWins, user_inputLosses,user_inputTies)

                cursor.execute(query, new_coach)
                EaglesDB_conn.commit()
                print("Record has been created")


            elif user_choice == 'gm':
                user_inputName = input("Enter name here: ")
                user_startYear = int(input("Enter start year here: "))
                if len(str(user_startYear)) == 4 and user_startYear < 2020 and user_startYear > 1900:
                    pass
                else:
                    print("That is an invalid year, please try again.")
                    continue
                user_endYear = int(input("Enter last year here: "))
                if len(str(user_endYear)) == 4 and user_startYear < user_endYear and user_startYear < 2020 and user_startYear > 1900 and user_endYear < 2020:
                    pass
                else:
                    print("That is an invalid year, please try again.")
                    continue

                query = ("INSERT INTO EaglesDB.GMs(Name, YearFrom, YearTo) values(%s,%s,%s)")
                new_GM = (user_inputName, user_startYear, user_endYear)

                cursor.execute(query, new_GM)
                EaglesDB_conn.commit()
                print("Record has been created")

            elif user_choice == 'owner':
                user_inputName = input("Enter name here: ")
                user_startYear = int(input("Enter start year here: "))
                if len(str(user_startYear)) == 4 and user_startYear < 2020 and user_startYear > 1900:
                    pass
                else:
                    print("That is an invalid year, please try again.")
                    continue
                user_endYear = int(input("Enter last year here: "))
                if len(str(user_endYear)) == 4 and user_startYear < user_endYear and user_startYear < 2020 and user_startYear > 1900 and user_endYear < 2020:
                    pass
                else:
                    print("That is an invalid year, please try again.")
                    continue

                query = ("INSERT INTO EaglesDB.Owners(Name, YearFrom, YearTo) values(%s,%s,%s)")
                new_Owner = (user_inputName, user_startYear, user_endYear)

                cursor.execute(query, new_Owner)
                EaglesDB_conn.commit()
                print("Record has been created")


            elif user_choice == 'teamseason':
                # different fields from the rest, but primary key is a year so error checking is a little more intensive
                user_Year = int(input("Enter team year here: "))
                if len(str(user_Year)) == 4 and user_Year < 2020 and user_Year > 1900 and user_Year < 2020:
                    pass
                else:
                    print("That is an incorrect year, please try again.")
                    continue

                user_inputWins = int(input("Enter number of wins here: "))
                user_inputLosses = int(input("Enter number of losses here: "))
                user_inputTies = int(input("Enter number of ties here: "))

                user_PlayoffRun = 0

                user_inputPtsFor = int(input("How many points did the team score this year? "))
                user_inputPtsAgainst = int(input("How many points did the team have scored on them this year? "))
                user_inputPtsDifferential = user_inputPtsFor - user_inputPtsAgainst


                query = ("INSERT INTO EaglesDB.SeasonResults(Year, Wins, Losses,Ties, PlayoffRun,PtsFor,PtsAgainst, PtsDifferential) values(%s,%s,%s,%s,%s,%s,%s,%s)")
                new_year = (user_Year, user_inputWins, user_inputLosses, user_inputTies,user_PlayoffRun ,user_inputPtsFor, user_inputPtsAgainst, user_inputPtsDifferential)

                cursor.execute(query, new_year)
                EaglesDB_conn.commit()
                print("Record has been created")


            elif user_choice == 'quit':
                MenuOptions()

            else:
                print("Not a valid option, please try again")

        except ValueError:
            print("invalid input try again")
            continue


def deleteOption4():
    #hard delete function that requires primary key
    while True:
        try:
            user_choice = input("Would you like to delete a player, coach, owner, GM, teamseason, or quit? ")

            if user_choice == 'player':
                input_deletePlayer = input("Enter the exact name and playerID of the player record you wish to delete: ")

                query = "DELETE FROM EaglesDB.Players WHERE PlayerName = '%s'" % (input_deletePlayer)

                cursor.execute(query)
                EaglesDB_conn.commit()
                print("The delete was processed successfully")
                #print("The delete was processed successfully, check to see if the record remains and if so, retype with correct name/ID")


            elif user_choice == 'coach':
                input_deleteCoach = input("Enter the exact name and coachID of the coach record you wish to delete: ")

                query = "DELETE FROM EaglesDB.HeadCoaches WHERE Name = '%s'" % (input_deleteCoach)

                cursor.execute(query)
                EaglesDB_conn.commit()
                print("The delete was processed successfully")
                #print("The delete was processed successfully, check to see if the record remains and if so, retype with correct name/ID")


            elif user_choice == 'gm':
                input_deleteGM = input("Enter the exact name and gmID of the executive record you wish to delete: ")

                query = "DELETE FROM EaglesDB.GMs WHERE Name = '%s'" % (input_deleteGM)

                cursor.execute(query)
                EaglesDB_conn.commit()
                print("The delete was processed successfully")
                #print("The delete was processed successfully, check to see if the record remains and if so, retype with correct name/ID")

            elif user_choice == 'owner':
                input_deleteOwner = input("Enter the exact name and ownerID of the executive record you wish to delete: ")

                query = "DELETE FROM EaglesDB.Owners WHERE Name = '%s'" % (input_deleteOwner)

                cursor.execute(query)
                EaglesDB_conn.commit()
                print("The delete was processed successfully")
                #print("The delete was processed successfully, check to see if the record remains and if so, retype with correct name/ID")


            elif user_choice == 'teamseason':
                input_deleteSeason = input("Enter the exact year of the season you wish to delete: ")

                query = "DELETE FROM EaglesDB.SeasonResults WHERE Year = '%s'" % (input_deleteSeason)

                cursor.execute(query)
                EaglesDB_conn.commit()
                print("The delete was processed successfully")
                #print("The delete was processed successfully, check to see if the record remains and if so, retype with correct name/ID")


            elif user_choice == 'quit':
                MenuOptions()

        except ValueError:
            print("invalid input try again")
            continue

def updateOption5():
    #update method which allows you to update any option that's not a primary key
    while True:
        try:
            user_choice = input("Would you like to update a player, coach, gm, owner, teamseason, or quit? ")

            if user_choice == 'player':
                input_updatePlayer = input("Enter the exact name and/or playerID of the record you wish to update or change: ")

                input_updateField = input("Do you want to update their 'yearfrom', 'yearto', 'gamesplayed', or 'position' ")


                if input_updateField == 'yearfrom':
                    user_newyearfrom = input("What should the new yearfrom be? ")
                    query = "UPDATE EaglesDB.Players SET YearFrom= '%s' WHERE PlayerName= '%s'" % (user_newyearfrom, input_updatePlayer)
                    cursor.execute(query)
                    EaglesDB_conn.commit()
                    print("Record has been updated")
                    continue

                elif input_updateField == 'yearto':
                    user_newyearto = input("What should the new yearto be? ")
                    query = "UPDATE EaglesDB.Players SET YearTo= '%s' WHERE PlayerName= '%s'" % (user_newyearto, input_updatePlayer)
                    cursor.execute(query)
                    EaglesDB_conn.commit()
                    print("Record has been updated")
                    continue

                elif input_updateField == 'gamesplayed':
                    user_newgamesplayed = input("What should the new gamesplayed be? ")
                    query = "UPDATE EaglesDB.Players SET GamesPlayed= '%s' WHERE PlayerName= '%s'" % (user_newgamesplayed, input_updatePlayer)
                    cursor.execute(query)
                    EaglesDB_conn.commit()
                    print("Record has been updated")
                    continue

                elif input_updateField == 'position':
                    user_newposition = input("What should the new position be? ")
                    query = "UPDATE EaglesDB.Players SET Position= '%s' WHERE PlayerName= '%s'" % (user_newposition, input_updatePlayer)
                    cursor.execute(query)
                    EaglesDB_conn.commit()
                    print("Record has been updated")
                    continue

                else:
                    print("Not a valid selection, please try again")
                    continue


            elif user_choice == 'coach':
                input_updateCoach = input("Enter the exact name and/or coachID of the record you wish to update or change: ")

                input_updateField = input("Do you want to update their 'yearfrom', 'yearto', 'gamescoached', 'wins', 'losses', 'ties' ")

                if input_updateField == 'yearfrom':
                    user_newyearfrom = input("What should the new yearfrom be? ")
                    query = "UPDATE EaglesDB.HeadCoaches SET YearFrom= '%s' WHERE Name= '%s'" % (user_newyearfrom, input_updateCoach)
                    cursor.execute(query)
                    EaglesDB_conn.commit()
                    print("Record has been updated")
                    continue

                elif input_updateField == 'yearto':
                    user_newyearto = input("What should the new yearto be? ")
                    query = "UPDATE EaglesDB.HeadCoaches SET YearTo= '%s' WHERE Name= '%s'" % (user_newyearto, input_updateCoach)
                    cursor.execute(query)
                    EaglesDB_conn.commit()
                    print("Record has been updated")
                    continue

                elif input_updateField == 'gamescoached':
                    user_newgamescoached = input("What should the new gamescoached be? ")
                    query = "UPDATE EaglesDB.HeadCoaches SET GamesPlayed= '%s' WHERE Name= '%s'" % (user_newgamescoached, input_updateCoach)
                    cursor.execute(query)
                    EaglesDB_conn.commit()
                    print("Record has been updated")
                    continue

                elif input_updateField == 'wins':
                    user_newwins = input("What should the new wins be? ")
                    query = "UPDATE EaglesDB.HeadCoaches SET Wins= '%s' WHERE Name= '%s'" % (user_newwins, input_updateCoach)
                    cursor.execute(query)
                    EaglesDB_conn.commit()
                    print("Record has been updated")
                    continue

                elif input_updateField == 'losses':
                    user_newlosses = input("What should the new losses be? ")
                    query = "UPDATE EaglesDB.HeadCoaches SET Losses= '%s' WHERE Name= '%s'" % (user_newlosses, input_updateCoach)
                    cursor.execute(query)
                    EaglesDB_conn.commit()
                    print("Record has been updated")
                    continue

                elif input_updateField == 'ties':
                    user_newties = input("What should the new ties be? ")
                    query = "UPDATE EaglesDB.HeadCoaches SET Ties= '%s' WHERE Name= '%s'" % (user_newties, input_updateCoach)
                    cursor.execute(query)
                    EaglesDB_conn.commit()
                    print("Record has been updated")
                    continue

                else:
                    print("Not a valid selection, please try again")
                    continue


            elif user_choice == 'gm':
                input_updateGMs = input("Enter the exact name and gmID of the executive record you wish to update or change: ")

                input_updateField = input("Do you want to update their 'yearfrom' or 'yearto'")

                if input_updateField == 'yearfrom':
                    user_newyearfrom = input("What should the new yearfrom be? ")
                    query = "UPDATE EaglesDB.GMs SET YearFrom= '%s' WHERE Name= '%s'" % (user_newyearfrom, input_updateGMs)
                    cursor.execute(query)
                    EaglesDB_conn.commit()
                    print("Record has been updated")
                    continue

                elif input_updateField == 'yearto':
                    user_newyearto = input("What should the new yearto be? ")
                    query = "UPDATE EaglesDB.GMs SET YearTo= '%s' WHERE Name= '%s'" % (user_newyearto, input_updateGMs)
                    cursor.execute(query)
                    EaglesDB_conn.commit()
                    print("Record has been updated")
                    continue

            elif user_choice == 'owner':
                input_updateOwners = input("Enter the exact name and executiveID of the executive record you wish to update or change: ")

                input_updateField = input("Do you want to update their 'yearfrom', 'yearto', 'wasOwner', 'wasGM', 'wasCoach' ")

                if input_updateField == 'yearfrom':
                    user_newyearfrom = input("What should the new yearfrom be? ")
                    query = "UPDATE EaglesDB.Owners SET YearFrom= '%s' WHERE Name= '%s'" % (user_newyearfrom, input_updateOwners)
                    cursor.execute(query)
                    EaglesDB_conn.commit()
                    print("Record has been updated")
                    continue

                elif input_updateField == 'yearto':
                    user_newyearto = input("What should the new yearto be? ")
                    query = "UPDATE EaglesDB.Owners SET YearTo= '%s' WHERE Name= '%s'" % (user_newyearto, input_updateOwners)
                    cursor.execute(query)
                    EaglesDB_conn.commit()
                    print("Record has been updated")
                    continue


            elif user_choice == 'teamseason':
                input_updateTeamSeason = input("Enter the exact year of the season you wish to update or change: ")

                input_updateField = input("Do you want to update this year's 'wins', 'losses', 'ties', 'ptsfor', or 'ptsagainst' field? ")

                if input_updateField == 'wins':
                    user_newWins = int(input("What should the new wins be for this year? "))
                    query = "UPDATE EaglesDB.SeasonResults SET Wins= '%s' WHERE Year= '%s'" % (user_newWins, input_updateTeamSeason)
                    cursor.execute(query)
                    EaglesDB_conn.commit()
                    print("Record has been updated")

                elif input_updateField == 'losses':
                    user_newLosses = int(input("What should the new losses be for this year? "))
                    query = "UPDATE EaglesDB.SeasonResults SET Losses= '%s' WHERE Year= '%s'" % (user_newLosses, input_updateTeamSeason)
                    cursor.execute(query)
                    EaglesDB_conn.commit()
                    print("Record has been updated")

                elif input_updateField == 'ties':
                    user_newTies = int(input("What should the new ties be for this year? "))
                    query = "UPDATE EaglesDB.SeasonResults SET Ties= '%s' WHERE Year= '%s'" % (user_newTies, input_updateTeamSeason)
                    cursor.execute(query)
                    EaglesDB_conn.commit()
                    print("Record has been updated")

                elif input_updateField == 'ptsfor':
                    user_newPtsFor = int(input("What should the new ptsfor be for this year? "))
                    query = "UPDATE EaglesDB.SeasonResults SET PtsFor= '%s' WHERE Year= '%s'" % (user_newPtsFor, input_updateTeamSeason)
                    cursor.execute(query)
                    EaglesDB_conn.commit()
                    print("Record has been updated")
                    query = "UPDATE EaglesDB.SeasonResults SET PtsDifferential= PtsFor-PtsAgainst WHERE Year= '%s'" % (input_updateTeamSeason)
                    cursor.execute(query)
                    EaglesDB_conn.commit()
                    print("Record has been updated")

                elif input_updateField == 'ptsagainst':
                    user_newPtsAgainst = int(input("What should the new ptsagainst be for this year? "))
                    query = "UPDATE EaglesDB.SeasonResults SET PtsAgainst= '%s' WHERE Year= '%s'" % (user_newPtsAgainst, input_updateTeamSeason)
                    cursor.execute(query)
                    EaglesDB_conn.commit()
                    print("Record has been updated")
                    query = "UPDATE EaglesDB.SeasonResults SET PtsDifferential= PtsFor-PtsAgainst WHERE Year= '%s'" % (input_updateTeamSeason)
                    cursor.execute(query)
                    EaglesDB_conn.commit()
                    print("Record has been updated")


                #cursor.execute(query)
                #EaglesDB_conn.commit()


            elif user_choice == 'quit':
                MenuOptions()

        except ValueError:
            print("invalid input try again")
            continue

def createCSVOptions6():
    while True:
    #continuous prompt for selection input
        try:
            user_input = input("Do you want players (type 'player'), coaches (type 'coach'), owners (type 'owner'), or gm (type 'gm') to be outputted to a csv file, or type 'quit' to return to menu': ")

            if user_input == 'player':
                cursor.execute("select * from EaglesDB.Players")

                csvResult = cursor.fetchall()
                print("Output successful")


                with open('outputCSV.csv', 'w', newline='') as file:
                    for x in csvResult:
                        writer = csv.writer(file)
                        writer.writerow(x)

            elif user_input == 'coach':
                cursor.execute("select * from EaglesDB.HeadCoaches")

                csvResult = cursor.fetchall()
                print("Output successful")


                with open('outputCSV.csv', 'w', newline='') as file:
                    for x in csvResult:
                        writer = csv.writer(file)
                        writer.writerow(x)

            elif user_input == 'gm':
                cursor.execute("select * from EaglesDB.GMs")

                csvResult = cursor.fetchall()
                print("Output successful")


                with open('outputCSV.csv', 'w', newline='') as file:
                    for x in csvResult:
                        writer = csv.writer(file)
                        writer.writerow(x)

            elif user_input == 'owner':
                cursor.execute("select * from EaglesDB.Owners")

                csvResult = cursor.fetchall()
                print("Output successful")

                with open('outputCSV.csv', 'w', newline='') as file:
                    for x in csvResult:
                        writer = csv.writer(file)
                        writer.writerow(x)


            elif user_input == 'quit':
                MenuOptions()

        except ValueError:
            print("invalid input try again")
            continue


def MenuOptions():
    #hub for all main database operations

    while True:
    #continuous prompt for selection input
        try:
            print("Welcome to The Philadelphia Eagles Database, below I have listed some options to allow you to view, create, delete, and update records: \n")

            print("enter 1 to view either the player, playerav, headcoach, gm, owner, or teamseason tables by limits and filters. ")
            print("enter 2 to view players by another table. ")
            print("enter 3 to create a new player, coach, gm, owner, or teamseason. ")
            print("enter 4 to delete a player, coach, gm, owner, or teamseason. ")
            print("enter 5 to update a player, coach, gm, owner, or teamseason. ")
            print("enter 6 to output to a CSV file. ")
            print("enter 0 to exit the program.")

            user_choice = int(input("Enter option here: "))
        except ValueError:
            print("invalid input try again")
            continue


        if user_choice == 1:
            viewOption1()
        if user_choice == 2:
            viewOption2()
        elif user_choice == 3:
            createOption3()
        elif user_choice == 4:
            deleteOption4()
        elif user_choice == 5:
            updateOption5()
        elif user_choice == 6:
            createCSVOptions6()
        elif user_choice == 0:
            print("Goodbye")
            quit()


if 1<2:
    MenuOptions()


EaglesDB_conn.commit()

cursor.close()