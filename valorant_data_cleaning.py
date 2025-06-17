#import kaggle
import pandas as pd

from sklearn.model_selection import train_test_split

#team1 = input("Enter the first team name: ")
#team2 = input("Enter the second team name: ")

# Read the CSV file

pstats25 = pd.read_csv('vct_2025/players_stats/players_stats.csv')
df25 = pd.read_csv('vct_2025/matches/scores.csv')
teammap = pd.read_csv('vct_2025/matches/team_mapping.csv')


df = pd.read_csv("vct_2025/matches/scores.csv")

# Keep only the desired columns
df = df[['Team A', 'Team B', 'Match Result']]

# Save the cleaned data to a new CSV
#df.to_csv("filtered_matches.csv", index=False)




#RETRIEVES FULL TEAM NAME FROM ABBREVIATED NAME
def get_full_team_name(team):
    filtered_df = teammap[teammap['Abbreviated'] == team]

    return filtered_df.iloc[0]['Full Name'] if not filtered_df.empty else None


#RETRIEVES TEAM ROSTER FOR A GIVEN TEAM
def get_team_roster(team):
    roster = set()
    filtered_df = pstats25[pstats25['Teams'] == team]

    for i in range(len(filtered_df) -1, -1, -1):
        roster.add(filtered_df.iloc[i]['Player'])
        if len(roster) == 5:
            break
            
    return roster


#RETRIEVES PAST MATCHES BETWEEN TWO TEAMS
def get_past_matches(team1, team2):
    filtered_df = df25[(df25['Match Name'] == team1 + " vs " + team2) | (df25['Match Name'] == team2 + " vs " + team1)]
    matches = set()
    for i in range(len(filtered_df) - 1, -1, -1):
        matches.add((filtered_df.iloc[i]['Match Result']))


    return matches


#RETRIEVES WINRATE FOR TEAM 1 AGAINST TEAM 2
def get_winrate_team1(team1, team2):
    match_set = get_past_matches(team1, team2)
    if len(match_set) == 0:
        return None
    wins = 0
    for match in match_set:
        if match ==(team1 + " won"):
            wins += 1
    return wins/len(match_set) * 100


#RETRIEVES TEAM WINRATE OVERALL
def get_team_winrate(team):
    filtered_df = df25[df25['Match Name'].str.contains(team)]
    total_matches = len(filtered_df)
    wins = len(filtered_df[filtered_df['Match Result'].str.contains(team)])
    
    if total_matches == 0:
        return 0.0
    
    return wins / total_matches * 100



#RETRIEVES AVERAGE PLAYER STATS FOR A GIVEN TEAM
def get_average_player_stats(team):
    filtered_df = pstats25[pstats25['Teams'] == team]
    
    if filtered_df.empty:
        return None
    
    average_stats = {
        'K/D Ratio': filtered_df['Kills:Deaths'].mean(),
        'Average Damage': filtered_df['Average Damage Per Round'].mean(),
        'Average Combat Score': filtered_df['Average Combat Score'].mean(),
        'Average First Kills': filtered_df['First Kills'].mean(),

    }
    
    return average_stats


#def build_dataframe(team1, team2):
    team1_full = get_full_team_name(team1)
    team2_full = get_full_team_name(team2)

    if not team1_full or not team2_full:
        return None

    team1_roster = get_team_roster(team1_full)
    team2_roster = get_team_roster(team2_full)

    if not team1_roster or not team2_roster:
        return None


    winrate_team1 = get_winrate_team1(team1_full, team2_full)
    if winrate_team1 is None:
        winrate_team1 = 0
        winrate_team2 = 0
    else:
        winrate_team2 = 100 - winrate_team1


    overall_winrate_team1 = get_team_winrate(team1_full)
    overall_winrate_team2 = get_team_winrate(team2_full)

    average_stats_team1 = get_average_player_stats(team1_roster)
    average_stats_team2 = get_average_player_stats(team2_roster)

    data = {
        'Team': [team1_full, team2_full],
        'Roster': [team1_roster, team2_roster],
        'Win Rate vs Opponent': [winrate_team1, winrate_team2],
        'Overall Win Rate': [overall_winrate_team1, overall_winrate_team2],
        'Average KD': [average_stats_team1['K/D Ratio'], average_stats_team2['K/D Ratio']],
        'Average Damage': [average_stats_team1['Average Damage'], average_stats_team2['Average Damage']],
        'Average Combat Score': [average_stats_team1['Average Combat Score'], average_stats_team2['Average Combat Score']],
        'Average First Kills': [average_stats_team1['Average First Kills'], average_stats_team2['Average First Kills']],
    }

    df = pd.DataFrame(data)
    
    return df


#bothteamsdata = build_dataframe("FNC", "G2")

#x = df25[:, 0:8]
#y = df25[:, 8]

#X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier()





#add avg stats to filtered_matches.csv
df['Team A winrate vs B'] = df.apply(lambda row: get_winrate_team1(row['Team A'], row['Team B']), axis=1)
df['Team A Average Stats'] = df['Team A'].apply(get_average_player_stats)
df['Team A Winrate'] = df['Team A'].apply(get_team_winrate)
df['Team B Average Stats'] = df['Team B'].apply(get_average_player_stats)
# Normalize Team A stats
team_a_stats_df = df['Team A Average Stats'].apply(pd.Series).round(2)
team_a_stats_df.columns = ['Team A ' + col for col in team_a_stats_df.columns]
# Join back to original dataframe
df = pd.concat([df, team_a_stats_df], axis=1)

#add winrate to filtered_matches.csv
df['Team B winrate vs A'] = df.apply(lambda row: get_winrate_team1(row['Team B'], row['Team A']), axis=1)
df['Team B Average Stats'] = df['Team B'].apply(get_average_player_stats)
df['Team B Winrate'] = df['Team B'].apply(get_team_winrate)
# Normalize Team B stats
team_b_stats_df = df['Team B Average Stats'].apply(pd.Series).round(2)
team_b_stats_df.columns = ['Team B ' + col for col in team_b_stats_df.columns]

# Join back to original dataframe
df = pd.concat([df, team_b_stats_df], axis=1)

# Keep as boolean
df['Team A Win'] = df['Match Result'].str.replace(' won', '', regex=False) == df['Team A']

df.drop(columns=['Match Result','Team A Average Stats', 'Team B Average Stats'], inplace=True)




df.to_csv("filtered_matches.csv", index=False)



            
        








