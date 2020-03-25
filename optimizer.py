import timeit, sys, animation, time, pickle, os, datetime
import pandas as pd
from progress.bar import IncrementalBar
from statistics import *
from sportsreference.nba.teams import Teams
from basketball_reference_scraper.teams import get_roster, get_roster_stats
from basketball_reference_scraper.players import get_stats
#pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

class DF:
    players = pd.DataFrame()
    avg = pd.DataFrame()
    p36 = pd.DataFrame()
    adv = pd.DataFrame()
    year = 0

    def rank(self, df):
        sum_pts = df['PTS'].sum(skipna=True)
        sum_3 = df['3P'].sum(skipna=True)
        sum_reb = df['TRB'].sum(skipna=True)
        sum_ast = df['AST'].sum(skipna=True)
        sum_stl = df['STL'].sum(skipna=True)
        sum_blk = df['BLK'].sum(skipna=True)
        mean_fg = df['FG%'].mean(skipna=True)
        mean_ft = df['FT%'].mean(skipna=True)
        std_fg = df['FG%'].std(skipna=True)
        std_ft = df['FT%'].std(skipna=True)
        values = [0] * 530
        #countfg = 0
        #countft = 0
        for i in range(len(df)):
            fg = ((df.at[i, 'FG%'] - mean_fg)/std_fg)
            ft = ((df.at[i, 'FT%'] - mean_ft)/std_ft)
            """if fg > 0:
                countfg += 1
            if ft > 0:
                countft += 1"""
                
            values[i] = (df.at[i, 'PTS'] + ((sum_pts/sum_3)*df.at[i, '3P']) + ((sum_pts/sum_reb)*df.at[i, 'TRB']) + ((sum_pts/sum_ast)*df.at[i, 'AST']) + ((sum_pts/sum_stl)*df.at[i, 'STL']) + ((sum_pts/sum_blk)*df.at[i, 'BLK']) + ((sum_pts/250)*fg) + ((sum_pts/283)*ft))

        df['VALUE'] = values
        df = df.sort_values(by='VALUE', ascending=False).reset_index(drop=True)
        
        return df
    
    def remove_duplicates(self, df, data):
        dup = df.duplicated('PLAYER', False)
        i = 0
        count = 0
        while i < len(dup):
            if dup[i]:
                count += 1
                player = df.at[i, 'PLAYER']
                stats = get_stats(player, data, 2019)
                for j in range(i+1, len(dup)):
                    if not dup[j] or df.at[j, 'PLAYER'] != player:
                        df = df.drop(df.index[(i+1):j]).reset_index(drop=True)
                        dup = dup.drop(dup.index[(i+1):j]).reset_index(drop=True)
                        break
                    
                for column in df.columns:
                    if column in stats.columns and column != 'POS':
                        df.at[i, column] = stats.at[0, column]

                dup[i] = False

                if count % 10 == 0:
                    print(count, "duplicates removed.")
                
            i += 1

        print(count, "total duplicates removed.\n")
        return df

    
    def set_types(self, df):
        for col in df.columns.values:
            if 'Unnamed' in str(col):
                df = df.drop(col, axis=1)
                
            elif str(col) not in ['PLAYER', 'POS', 'AGE', 'TEAM', 'SEASON']:
                df = df.astype({col : 'float64'})

        print("Done! Column types set.\n")
        return df

    
    def fix_names(self, df):
        for start_index in range(len(df)):
            df.at[start_index, 'PLAYER'] = df.at[start_index, 'PLAYER'].replace('Ã³', 'ó')
            df.at[start_index, 'PLAYER'] = df.at[start_index, 'PLAYER'].replace('Ä‡', 'ć')
            df.at[start_index, 'PLAYER'] = df.at[start_index, 'PLAYER'].replace('Å½', 'Ž')
            df.at[start_index, 'PLAYER'] = df.at[start_index, 'PLAYER'].replace('Å¾', 'ž')
            df.at[start_index, 'PLAYER'] = df.at[start_index, 'PLAYER'].replace('Ã­', 'í')
            df.at[start_index, 'PLAYER'] = df.at[start_index, 'PLAYER'].replace('Ã©', 'é')
            df.at[start_index, 'PLAYER'] = df.at[start_index, 'PLAYER'].replace('Ã¶', 'ö')
            df.at[start_index, 'PLAYER'] = df.at[start_index, 'PLAYER'].replace('tÄ', 'tā')
            df.at[start_index, 'PLAYER'] = df.at[start_index, 'PLAYER'].replace('DÄ', 'Dā')
            df.at[start_index, 'PLAYER'] = df.at[start_index, 'PLAYER'].replace('Å ', 'Š')
            df.at[start_index, 'PLAYER'] = df.at[start_index, 'PLAYER'].replace('Ã¡', 'á')
            df.at[start_index, 'PLAYER'] = df.at[start_index, 'PLAYER'].replace('Å¡', 'š')
            df.at[start_index, 'PLAYER'] = df.at[start_index, 'PLAYER'].replace('Ã½', 'ý')
            df.at[start_index, 'PLAYER'] = df.at[start_index, 'PLAYER'].replace('Ã¨', 'è')
            df.at[start_index, 'PLAYER'] = df.at[start_index, 'PLAYER'].replace('Ãª', 'ê')
            df.at[start_index, 'PLAYER'] = df.at[start_index, 'PLAYER'].replace('Ä°', 'İ')
            df.at[start_index, 'PLAYER'] = df.at[start_index, 'PLAYER'].replace('Å«', 'ū')
            df.at[start_index, 'PLAYER'] = df.at[start_index, 'PLAYER'].replace('Ãn', 'Án')
            df.at[start_index, 'PLAYER'] = df.at[start_index, 'PLAYER'].replace('Ä', 'č')
            df.at[start_index, 'PLAYER'] = df.at[start_index, 'PLAYER'].replace('Ãl', 'Ál')
            df.at[start_index, 'PLAYER'] = df.at[start_index, 'PLAYER'].replace('\x8d', '')
            df.at[start_index, 'PLAYER'] = df.at[start_index, 'PLAYER'].replace('\x81', '')
            
            if start_index % 100 == 0 and start_index != 0:
                print("  ", start_index, "players checked.")
                
            elif start_index == len(df) - 1:
                print("Done!", start_index+1, "total players checked.")

        return df

    def construct_datasets(self, year_in):
        """Quicker approach is to get request relevant datasets by roster rather than by player (530 calls versus 30 calls).
           Although it might still be doing the same, it is somehow faster. However, list contains duplicates of a player that
           has played in multiple teams throughout the season.
                   ---TODO---
           Count the duplicates during player viability process."""
        try:
            print("Fetching DataSets: NBA per game, NBA per 36, NBA advanced stats")
            self.avg = pickle.load(open("df_avg.pickle", "rb"))
            self.p36 = pickle.load(open("df_36.pickle", "rb"))
            self.adv = pickle.load(open("df_adv.pickle", "rb"))
            
        except (OSError, IOError) as e:
            print("No pre-existing datasets found.")
            print("Constructing DataSets: NBA per game, NBA per 36, NBA advanced stats")
            nba_teams = Teams()
            print("   Fetching Milwaukee Bucks " + str(year_in-1) + "-" + str(year_in)[2:] + " per game roster stats.")
            self.avg = pd.DataFrame(get_roster_stats('MIL', year_in, 'PER_GAME'))
            print("   Fetching Milwaukee Bucks " + str(year_in-1) + "-" + str(year_in)[2:] + " per minute roster stats.")
            self.p36 = pd.DataFrame(get_roster_stats('MIL', year_in, 'PER_MINUTE'))
            print("   Fetching Milwaukee Bucks " + str(year_in-1) + "-" + str(year_in)[2:] + " advanced roster stats.\n")
            self.adv = pd.DataFrame(get_roster_stats('MIL', year_in, 'ADVANCED'))
            for team in nba_teams:
                if team.abbreviation != 'MIL':
                    print("   Fetching " + team.name + " " + str(year_in-1) + "-" + str(year_in)[2:] + " per game roster stats.")
                    self.avg = self.avg.append(get_roster_stats(team.abbreviation, year_in, 'PER_GAME'), ignore_index = True)
                    print("   Fetching " + team.name + " " + str(year_in-1) + "-" + str(year_in)[2:] + " per minute roster stats.")
                    self.p36 = self.p36.append(get_roster_stats(team.abbreviation, year_in, 'PER_MINUTE'), ignore_index = True)
                    print("   Fetching " + team.name + " " + str(year_in-1) + "-" + str(year_in)[2:] + " advanced roster stats.\n")
                    self.adv = self.adv.append(get_roster_stats(team.abbreviation, year_in, 'ADVANCED'), ignore_index = True)

        self.avg = self.avg.sort_values(by=['PLAYER']).reset_index(drop=True)
        self.p36 = self.p36.sort_values(by=['PLAYER']).reset_index(drop=True)
        self.adv = self.adv.sort_values(by=['PLAYER']).reset_index(drop=True)
        print("   NBA per game dataframe constructed and sorted by player.\n   NBA per 36 dataframe constructed and sorted by player.\n   NBA advanced stats dataframe constructed and sorted by player.\n")
        print("\nFixing player names, setting column types, and removing duplicates in NBA per game dataframe.")
        self.avg = self.fix_names(self.avg)
        self.avg = self.set_types(self.avg)
        self.avg = self.remove_duplicates(self.avg, 'PER_GAME')
        print("Fixing player names, setting column types, and removing duplicates in NBA per minute dataframe.")
        self.p36 = self.fix_names(self.p36)
        self.p36 = self.set_types(self.p36)
        self.p36 = self.remove_duplicates(self.p36, 'PER_MINUTE')
        print("Fixing player names, setting column types, and removing duplicates in NBA advanced stats dataframe.")
        self.adv = self.fix_names(self.adv)
        self.adv = self.set_types(self.adv)
        self.adv = self.remove_duplicates(self.adv, 'ADVANCED')

        print("Ranking and sorting NBA per game dataframe.")
        self.avg = self.rank(self.avg)
        
        pickle.dump(self.avg, open("df_avg.pickle", "wb"))
        pickle.dump(self.p36, open("df_36.pickle", "wb"))
        pickle.dump(self.adv, open("df_adv.pickle", "wb"))
        print(self.year, "per game dataset of size", len(self.avg), "constructed and stored successfully.")
        print(self.year, "per minute dataset of size", len(self.p36), "constructed and stored successfully.")
        print(self.year, "advanced dataset of size", len(self.adv), "constructed and stored successfully.")

    def __init__(self, year_in):
        self.year = year_in
        self.construct_datasets(self.year)
        self.players['PLAYER'] = self.avg['PLAYER'].values
        self.players = self.players.drop_duplicates().reset_index(drop=True)
        self.players['DRAFTED'] = 0

class Team:

    name = ""
    size = 0
    roster = []

    def __init__(self, name_in, size_in):
        self.name = name_in
        self.size = size_in

class Player:

    name = ""
    position = 0
    punt_cats = ["to/g"]
    team = Team("", 15)
    
    def __init__(self, name_in, pos_in, team_name, size_in, to_punt):
        self.name = name_in
        self.position = pos_in
        self.team = Team(team_name, size_in)
        self.punt_cats = to_punt    

class Pick:

    name = ""
    viability = { }
    row_num = -1
    adv_row = -1
    row = []
    
    def __init__(self, df, index, benchmarks, std_devs):
        self.row = df.avg.iloc[index]
        self.name = self.row['PLAYER']
        self.row_num = index
        
        #set viability
        self.viability["FG%"] = (self.row["FG%"] - benchmarks["FG%"])/std_devs["FG%"]
        self.viability["FT%"] = (self.row['FT%'] - benchmarks["FT%"])/std_devs["FT%"]
        self.viability["3P"] = (self.row['3P'] - benchmarks["3P"])/std_devs["3P"]
        self.viability["PTS"] = (self.row['PTS'] - benchmarks["PTS"])/std_devs["PTS"]
        self.viability["TRB"] = (self.row['TRB'] - benchmarks["TRB"])/std_devs["TRB"]
        self.viability["AST"] = (self.row['AST'] - benchmarks["AST"])/std_devs["AST"]
        self.viability["STL"] = (self.row['STL'] - benchmarks["STL"])/std_devs["STL"]
        self.viability["BLK"] = (self.row['BLK'] - benchmarks["BLK"])/std_devs["BLK"]
        self.viability["TOS"] = (self.row['TOV'] - benchmarks["TOV"])/std_devs["TOV"]
        self.viability["MP"] = (self.row['MP'] - benchmarks["MP"])/std_devs["MP"]
        self.viability["USG%"] = (df.adv.loc[df.adv.PLAYER == self.name, 'USG%'].values[0] - benchmarks["USG%"])/std_devs["USG%"]
        
    #returns true if self > pick
    def compare(self, pick, punts):
        comparison = {}
        for i in self.viability.items():
            if i[0] not in punts:
                if self.viability[i[0]] > pick.viability[i[0]]:
                    comparison[i[0]] = '+'
                else:
                    comparison[i[0]] = '-'

        plus_count = 0
        for i in comparison.items():
            if comparison[i[0]] == '+':
                plus_count += 1

        if plus_count > (len(comparison)-len(punts))//2:
            return True
        else:
            return False

class Benchmarks:

    benchmarks = {"FG%": 0.0, "FT%": 0.0, "3P": 0.0, "PTS": 0.0,
                  "TRB": 0.0, "AST": 0.0, "STL": 0.0, "BLK": 0.0,
                  "TOV": 0.0, "MP": 0.0, "USG%": 0.0, "TS%": 0.0,
                  "eFG%": 0.0, "PER": 0.0, "TRB%": 0.0, "AST%": 0.0,
                  "STL%": 0.0, "BLK%": 0.0, "TOV%": 0.0, "USG%": 0.0,
                  "BPM": 0.0}
    
    std_devs = {"FG%": 0.0, "FT%": 0.0, "3P": 0.0, "PTS": 0.0,
                "TRB": 0.0, "AST": 0.0, "STL": 0.0, "BLK": 0.0,
                "TOV": 0.0, "MP": 0.0, "USG%": 0.0, "TS%": 0.0,
                "eFG%": 0.0, "PER": 0.0, "TRB%": 0.0, "AST%": 0.0,
                "STL%": 0.0, "BLK%": 0.0, "TOV%": 0.0, "USG%": 0.0,
                "BPM": 0.0}
    
    pos_count = {"PG": 0, "SG": 0, "SF": 0, "PF": 0, "C": 0}

    players = 0

    def build(self, df):
        
        for row in range(self.players):
            for col in list(df.avg.columns.values):
                if str(col) in self.benchmarks:
                    self.benchmarks[str(col)] += df.avg.loc[df.avg.index[row], str(col)]/self.players

            for col in list(df.adv.columns.values):
                if str(col) in self.benchmarks:
                    self.benchmarks[str(col)] += df.adv.loc[df.avg.index[row], str(col)]/self.players

            self.pos_count[df.avg.loc[df.avg.index[row], 'POS']] += 1
    
        for col in list(df.avg.columns.values):
            if str(col) in self.std_devs:
                self.std_devs[col] = df.avg[str(col)].std()

        for col in list(df.adv.columns.values):
            if str(col) in self.std_devs:
                self.std_devs[col] = df.adv[str(col)].std()

    def __init__(self, draft_size):
        self.players = draft_size
        

def get_input():

    inputs = {}

    inputs['owner_name'] = input("What is your name? ")
    
    inputs['team_name'] = input("What is your team name? ")
    
    inputs['mock'] = int(input("Would you like to run a mock draft or a live optimization? (Live=1, Mock=0): "))
    while isinstance(inputs['mock'], int) == False or inputs['mock'] > 1 or inputs['mock'] < 0:
        inputs['mock'] = int(input("Answer 1 for Live or 0 for Mock: "))

    inputs['scoring_format'] = 1 #int(input("What is your league's scoring format? (1=H2H, 2=Points, 3=Roto) "))
    while isinstance(inputs['scoring_format'], int) == False or inputs['scoring_format'] > 3 or inputs['scoring_format'] < 1:
        inputs['scoring_format'] = int(input("Answer 1 for head-to-head, 2 for points, or 3 for roto: "))
    
    inputs['cats'] = 9 #int(input("How many categories does your league have?"))
    while isinstance(inputs['cats'], int) == False or inputs['cats'] > 15 or inputs['cats'] < 8:
        inputs['cats'] = int(input("Supported categories are between 8 and 15, re-enter: "))
        
    inputs['draft_format'] = 1 #int(input("Is your draft snaked? (1=Yes, 0=No) "))
    while isinstance(inputs['draft_format'], int) == False or inputs['draft_format'] > 1 or inputs['draft_format'] < 0:
        inputs['draft_format'] = int(input("Answer 1 for yes and 0 for no: "))

    inputs['league_size'] = int(input("Enter league size: "))
    while isinstance(inputs['league_size'], int) == False or inputs['league_size'] < 8 or inputs['league_size'] > 20 or inputs['league_size'] % 2 != 0:
        print("Supported league sizes are even numbers between 8 and 20.")
        inputs['league_size'] = int(input("Re-enter league size: "))

    inputs['draft_pos'] = int(input("Enter draft position: "))
    while isinstance(inputs['draft_pos'], int) == False or inputs['draft_pos'] < 0 or inputs['draft_pos'] > inputs['league_size']:
        print("Invalid draft position.")
        inputs['draft_pos'] = int(input("Re-enter draft position: "))

    inputs['team_size'] = int(input("Enter team size: "))
    while isinstance(inputs['team_size'], int) == False or inputs['team_size'] < 8 or inputs['team_size'] > 20:
        print("Unsupported team size: 8 <= size <= 20")
        inputs['team_size'] = int(input("Re-enter team size: "))

    inputs['keeper'] = int(input("Is it a keeper league? (Yes=1, No=0): "))
    while isinstance(inputs['keeper'], int) == False or inputs['keeper'] > 1 or inputs['keeper'] < 0:
        inputs['keeper'] = int(input("Answer 1 for Yes or 0 for No: "))
        
    if inputs['keeper']:
        inputs['keeper_count'] = int(input("How many keepers are there per team? "))
        while isinstance(inputs['keeper_count'], int) == False or inputs['keeper_count'] >= 0 or inputs['keeper_count'] < inputs['team_size']:
            inputs['keeper_count'] = int(input("Keeper count must be between 0 and the size of your team: "))

    else:
        inputs['keeper_count'] = 0
    
    if inputs['keeper_count'] != inputs['team_size']:
        return inputs
    
    else:
        print("Weird league, you're all set!")

def setup_draft(inputs, df):
    inputs['rounds'] = inputs['team_size'] - inputs['keeper_count']
    inputs['picks_left'] = inputs['rounds'] * inputs['league_size']
    print("Before we optimize your draft, are there any categories you wish to punt?\nFG% - FT% - 3P - PTS - REB - AST - STL - BLK - TOV")
    to_punt = str(input("Enter list of comma separated categories in uppercase: "))
    puntstr = to_punt.replace(" ", "")
    inputs['punt'] = puntstr.split(',')
    inputs['punt'] = list(set(inputs['punt']))
    while len(inputs['punt']) > inputs['cats']//2:
        print("You cannot punt a majority of categories, enter 4 or less.")
        to_punt = str(input("Enter list of comma separated categories in uppercase: "))
        puntstr = to_punt.replace(" ", "")
        inputs['punt'] = puntstr.split(',')
        inputs['punt'] = list(set(inputs['punt']))
            
    if mock:
        mock(inputs, df)

    else:
        live(inputs, df)
    
def mock(inputs, df):
    #set mock participants and draft order
    participants = []
    comp = 1
    for i in range(inputs['league_size']):
        if i != inputs['draft_pos'] - 1:
            participants += [Player("Computer" + str(comp), i + 1, "MockTeam" + str(comp), inputs['team_size'], ["TOS"])]
            comp += 1

        else:
            participants += [Player(inputs['owner_name'], inputs['draft_pos'], inputs['team_name'], inputs['team_size'], inputs['punt'])]

    print("Punting", end=" ")
    for p in inputs['punt']:
        print(p, end=" ")           
    print()
    
    #set benchmarks
    analytics = Benchmarks(inputs['picks_left'])
    analytics.build(df)

    #make sure players are set up in correct draft order
    for i in range(inputs['league_size']):
        print(participants[i].name)
        print(participants[i].team.name)

    print()
    count = 1            
    rnd = 1
    drafted = [0] * 530
    df.players['PLAYER'] = df.avg['PLAYER']
    df.players['DRAFTED'] = drafted
    while rnd < 16:
        if inputs['draft_format'] == 1 and rnd % 2 == 0:
            for i in range(inputs['league_size'] - 1, -1, -1):
                to_pick = Pick(df, df.players.DRAFTED.idxmin(), analytics.benchmarks, analytics.std_devs)
                for row in range(inputs['picks_left']):
                    if df.players.loc[row, 'DRAFTED'] == 0 and df.players.loc[row, 'PLAYER'] != to_pick.name:
                        other_pick = Pick(df, row, analytics.benchmarks, analytics.std_devs)
                        if to_pick.compare(other_pick, participants[i].punt_cats):
                            to_pick = other_pick
                
                if participants[i].name == inputs['owner_name']:
                    answer = int(input(to_pick.name + " is your optimum pick! Do you wish to draft him? "))
                    if answer:
                        print(participants[i].team.name + " selects " + to_pick.name + " with pick #" + str(count) + " in the draft.")
                        participants[i].team.roster += [to_pick.name]
                    else:
                        draft = input("Enter name of player you wish to draft: ")
                        to_pick.row_num = df.players.index[df.players['PLAYER']==draft]
                        to_pick.name = df.players.loc[df.players.index[to_pick.row_num], 'PLAYER']
                        participants[i].team.roster += [to_pick.name]
                        
                else:
                    print(participants[i].team.name + " selects " + to_pick.name + " with pick #" + str(count) + " in the draft.")
                    participants[i].team.roster += [to_pick.name]

                count += 1
                df.players.loc[df.players.index[to_pick.row_num], 'DRAFTED'] = 1

        else:
            for i in range(inputs['league_size']):
                to_pick = Pick(df, df.players.DRAFTED.idxmin(), analytics.benchmarks, analytics.std_devs)
                for row in range(inputs['picks_left']):
                    if df.players.loc[row, 'DRAFTED'] == 0 and df.players.loc[row, 'PLAYER'] != to_pick.name:
                        other_pick = Pick(df, row, analytics.benchmarks, analytics.std_devs)
                        if to_pick.compare(other_pick, participants[i].punt_cats):
                            to_pick = other_pick
                
                if participants[i].name == inputs['owner_name']:
                    answer = int(input(to_pick.name + " is your optimum pick! Do you wish to draft him? "))
                    if answer:
                        print(participants[i].team.name + " selects " + to_pick.name + " with pick #" + str(count) + " in the draft.")
                        participants[i].team.roster += [to_pick.name]
                    else:
                        draft = input("Enter name of player you wish to draft: ")
                        to_pick.row_num = df.players.index[df.players['PLAYER']==draft]
                        to_pick.name = df.players.loc[df.players.index[to_pick.row_num], 'PLAYER']
                        participants[i].team.roster += [to_pick.name]
                        
                else:
                    print(participants[i].team.name + " selects " + to_pick.name + " with pick #" + str(count) + " in the draft.")
                    participants[i].team.roster += [to_pick.name]

                count += 1
                df.players.loc[df.players.index[to_pick.row_num], 'DRAFTED'] = 1

        rnd += 1
    
def live(inputs, df):
    print("not implemented")

if __name__ == '__main__':   
    start = timeit.default_timer()
    today = datetime.datetime.today()
    
    if today.month >= 7:
        df = DF(today.year)
    else:
        df = DF(today.year - 1)
        
    print('\nWelcome to the Sixth Man, the fantasy basketball draft optimizer!')
    #print('Answer the following prompts to get started.')
    #inputs = get_input()
    inputs = {'owner_name': 'Alexis', 'team_name': 'Mario Esnu', 'mock': 0,
              'scoring_format': 1, 'cats': 9, 'draft_format': 1, 'league_size': 10,
              'draft_pos': 8, 'team_size': 15, 'keeper': 0, 'keeper_count': 0}
    setup_draft(inputs, df)
    print('Thanks for using the Sixth Man Fantasy Hoops Optimizer, good luck!')
    stop = timeit.default_timer()
    print('Time: ', stop - start)
