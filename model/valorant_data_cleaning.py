
import pandas as pd


pstats25 = pd.read_csv('vct_2025/players_stats/players_stats.csv')
df25 = pd.read_csv('vct_2025/matches/scores.csv')
df24 = pd.read_csv('vct_2024/matches/scores.csv')
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
        'Average First Deaths Per Round': filtered_df['First Deaths Per Round'].mean(),

    }
    
    return average_stats


def get_average_player_stats_list(team):
    filtered_df = pstats25[pstats25['Player'].isin(team)]
    
    if filtered_df.empty:
        return None
    
    average_stats = {
        'K/D Ratio': filtered_df['Kills:Deaths'].mean(),
        'Average Damage': filtered_df['Average Damage Per Round'].mean(),
        'Average Combat Score': filtered_df['Average Combat Score'].mean(),
        'Average First Kills': filtered_df['First Kills'].mean(),
        'Average First Deaths Per Round': filtered_df['First Deaths Per Round'].mean(),

    }
    



    return average_stats


def build_dataframe(team1, team2):
    if team1 == "NRG":
        team1_full = "Mega Minors"
    else: 
        team1_full = get_full_team_name(team1)

    if team2 == "NRG":
        team2_full = "Mega Minors"
    else: 
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

    average_stats_team1 = get_average_player_stats_list(team1_roster)
    average_stats_team2 = get_average_player_stats_list(team2_roster)
    data = {
        'Team A Winrate vs B': [winrate_team1],
        'Team A Winrate': [overall_winrate_team1],
        'Team A K/D Ratio': [average_stats_team1['K/D Ratio']],
        'Team A Average Damage': [average_stats_team1['Average Damage']],
        'Team A Average Combat Score': [average_stats_team1['Average Combat Score']],
        'Team A Average First Kills': [average_stats_team1['Average First Kills']],
        'Team A Average First Deaths Per Round': [average_stats_team1['Average First Deaths Per Round']],
        'Team B Winrate vs A': [winrate_team2],
        'Team B Winrate': [overall_winrate_team2],
        'Team B K/D Ratio': [average_stats_team2['K/D Ratio']],
        'Team B Average Damage': [average_stats_team2['Average Damage']],
        'Team B Average Combat Score': [average_stats_team2['Average Combat Score']],
        'Team B Average First Kills': [average_stats_team2['Average First Kills']],
        'Team B Average First Deaths Per Round': [average_stats_team2['Average First Deaths Per Round']],
        
    }

    df = pd.DataFrame(data)
    return df

    


#add avg stats to filtered_matches.csv
df['Team A Winrate vs B'] = df.apply(lambda row: get_winrate_team1(row['Team A'], row['Team B']), axis=1)
df['Team A Average Stats'] = df['Team A'].apply(get_average_player_stats)
df['Team A Winrate'] = df['Team A'].apply(get_team_winrate)
df['Team B Average Stats'] = df['Team B'].apply(get_average_player_stats)
# Normalize Team A stats
team_a_stats_df = df['Team A Average Stats'].apply(pd.Series).round(2)
team_a_stats_df.columns = ['Team A ' + col for col in team_a_stats_df.columns]
# Join back to original dataframe
df = pd.concat([df, team_a_stats_df], axis=1)

#add winrate to filtered_matches.csv
df['Team B Winrate vs A'] = df.apply(lambda row: get_winrate_team1(row['Team B'], row['Team A']), axis=1)
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




#Build dataframe to predict pistol round win

# def get_past_pistol_matches(team1, team2):
#     filtered_df = pistolrounds[((pistolrounds['Match Name'] == team1 + " vs " + team2) | (pistolrounds['Match Name'] == team2 + " vs " + team1)) & (pistolrounds['Team'] == team1)]
#     matches = []
#     for i in range(len(filtered_df) - 1, -1, -1):
#         matches.append((filtered_df.iloc[i]['Outcome']))

#     return matches


# #RETRIEVES WINRATE FOR TEAM 1 AGAINST TEAM 2
# def get_pwinrate_team1(team1, team2):
#     match_set = get_past_pistol_matches(team1, team2)
#     if len(match_set) == 0:
#         return None
#     wins = 0
#     for match in match_set:
#         if match ==("Win"):
#             wins += 1
#     return wins/(len(match_set)) * 100


# #RETRIEVES TEAM PISTOL WINRATE OVERALL
# def get_team_pwinrate(team):
#     filtered_df = pistolrounds[pistolrounds['Team'] == team]
#     total_matches = len(filtered_df)
#     wins = len(filtered_df[filtered_df['Outcome'] == 'Win'])
    
#     if total_matches == 0:
#         return 0.0
    
#     return wins / total_matches * 100

# def winlosstoInt(outcome):
#     if outcome == 'Win':
#         return 1
#     elif outcome == 'Loss':
#         return 0
#     else:
#         return None

# pistolrounds = pd.read_csv('vct_2025/matches/eco_rounds.csv')
# # Filter for pistol rounds (round 1)
# pistolrounds = pistolrounds[pistolrounds['Round Number'] == 1]
        
# pistolrounds = pistolrounds[['Match Name', 'Team','Outcome']]



# pistolrounds[['Team A', 'Team B']] = pistolrounds['Match Name'].str.split(' vs ', expand=True)
# pistolrounds['Team A Pistol Winrate vs B'] = pistolrounds.apply(lambda row: get_pwinrate_team1(row['Team A'], row['Team B']), axis=1)
# pistolrounds['Team B Pistol Winrate vs A'] = pistolrounds.apply(lambda row: get_pwinrate_team1(row['Team B'], row['Team A']), axis=1)
# pistolrounds['Team A Pistol Winrate'] = pistolrounds['Team A'].apply(get_team_pwinrate)
# pistolrounds['Team B Pistol Winrate'] = pistolrounds['Team B'].apply(get_team_pwinrate)
# pistolrounds['Outcome'] = pistolrounds['Outcome'].apply(winlosstoInt)

# pistolrounds['Team A Average Stats'] = pistolrounds['Team A'].apply(get_average_player_stats)
# pistolrounds['Team B Average Stats'] = pistolrounds['Team B'].apply(get_average_player_stats)

# team_a_stats_df = pistolrounds['Team A Average Stats'].apply(pd.Series).round(2)
# team_a_stats_df.columns = ['Team A ' + col for col in team_a_stats_df.columns]

# pistolrounds = pd.concat([pistolrounds, team_a_stats_df], axis=1)

# team_b_stats_df = pistolrounds['Team B Average Stats'].apply(pd.Series).round(2)
# team_b_stats_df.columns = ['Team B ' + col for col in team_b_stats_df.columns]

# pistolrounds = pd.concat([pistolrounds, team_b_stats_df], axis=1)

# pistolrounds.drop(columns=['Team A Average Stats', 'Team B Average Stats'], inplace=True)

# pistolrounds.to_csv("pistol_rounds.csv", index=False)

#print(get_pwinrate_team1("Sentinels", "G2 Esports"))











