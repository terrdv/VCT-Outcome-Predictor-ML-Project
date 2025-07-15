import pandas as pd


pstats25 = pd.read_csv('vct_2025/players_stats/players_stats.csv')
teams = pd.read_csv('vct_2025/ids/teams_ids.csv')
df25 = pd.read_csv('vct_2025/matches/scores.csv')


def get_team_roster(team):
    roster = set()
    filtered_df = pstats25[pstats25['Teams'] == team]

    for i in range(len(filtered_df) -1, -1, -1):
        roster.add(filtered_df.iloc[i]['Player'])
        if len(roster) == 5:
            break
            
    return roster

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

#RETRIEVES TEAM WINRATE OVERALL
def get_team_winrate(team):
    filtered_df = df25[df25['Match Name'].str.contains(team)]
    total_matches = len(filtered_df)
    wins = len(filtered_df[filtered_df['Match Result'].str.contains(team)])
    
    if total_matches == 0:
        return 0.0
    
    return wins / total_matches * 100

team_data = []
for i in range(len(teams)):
    if teams.iloc[i]["Team"] == "NRG":
        team = "NRG"

        roster = get_team_roster("Mega Minors")

        stats = get_average_player_stats_list(roster)
        if stats is None:
            continue
        winrate = get_team_winrate("NRG")

    else:
        team = teams.iloc[i]['Team']

        roster = get_team_roster(team)

        stats = get_average_player_stats_list(roster)
        if stats is None:
            continue
        winrate = get_team_winrate(team)

    team_info = {
        'Team': team,
        'Winrate': winrate,
        **stats
    }

    team_data.append(team_info)

team_df = pd.DataFrame(team_data)

team_df.to_csv("team_data.csv", index=False)



