import valorant_data_cleaning
import pandas as pd
from randomforest import prediction_probability
from logreg import predictionLog_probability_order_invariant


data = pd.read_csv("vct_2025/matches/team_mapping.csv")
print("Type ABBREVIATIONS for each team \n")
while True:
    predictTeamToWin = input("Predict outcome for this team: ")
    if predictTeamToWin in data['Abbreviated'].values:
        break
    else:
        print("Invalid Input \n")

while True:
    opposing = input("Opposing Team: ")
    if opposing in data['Abbreviated'].values:
        break
    else:
        print("Invalid Input \n")


teamdata = valorant_data_cleaning.build_dataframe(predictTeamToWin, opposing)

if prediction_probability(teamdata) == 1:
    print(predictTeamToWin + " will win (Random Forest Classification)")
    
else:
    print(opposing + " will win (Random Forest Classification)")

if predictionLog_probability_order_invariant(teamdata) == 1:
    print(predictTeamToWin + " will win (Logistic Regression)")
else:
    print(opposing + " will win (Logistic Regression)")


