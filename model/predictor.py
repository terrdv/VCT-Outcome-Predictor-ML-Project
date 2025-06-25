from model.valorant_data_cleaning import build_dataframe
import pandas as pd
from model.randomforest import prediction_probability
from model.logreg import predictionLog_probability_order_invariant


data = pd.read_csv("vct_2025/matches/team_mapping.csv")
# print("Type ABBREVIATIONS for each team \n")
# while True:
#     predictTeamToWin = input("Predict outcome for this team: ")
#     if predictTeamToWin in data['Abbreviated'].values:
#         break
#     else:
#         print("Invalid Input \n")

# while True:
#     opposing = input("Opposing Team: ")
#     if opposing in data['Abbreviated'].values:
#         break
#     else:
#         print("Invalid Input \n")


def getdf(teama, teamb):
    teamdata = build_dataframe(teama, teamb)
    return teamdata

def finalpred_rfc(teama,teamb):
    teamdata = getdf(teama, teamb)

    if prediction_probability(teamdata) == 1:
        return teama + " will win (Random Forest Classification)"
        
    else:
        return teamb + " will win (Random Forest Classification)"


def finalpred_logreg(teama,teamb):
    teamdata = getdf(teama, teamb)
    if predictionLog_probability_order_invariant(teamdata) == 1:
        return teama + " will win (Logistic Regression)"
    else:
        return teamb + " will win (Logistic Regression)"


