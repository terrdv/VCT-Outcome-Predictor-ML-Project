import valorant_data_cleaning 
from randomforest import prediction
print("Type ABBREVIATIONS for each team \n")
predictTeamToWin = input("Predict outcome for this team: ")
opposing = input("Opposing Team: ")

teamdata = valorant_data_cleaning.build_dataframe(predictTeamToWin, opposing)

if prediction(teamdata) == 1:
    print(predictTeamToWin + " will win")
else:
    print(opposing + " will win")
