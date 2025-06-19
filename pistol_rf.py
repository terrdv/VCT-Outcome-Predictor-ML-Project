# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import accuracy_score, classification_report

# from collections import Counter
# import numpy as np


# vct_data = pd.read_csv('pistol_rounds.csv')

# feature_cols = [
#     'Team A Pistol Winrate vs B', 'Team A Pistol Winrate', 'Team B Pistol Winrate vs A', 'Team B Pistol Winrate', 
#     'Team A K/D Ratio', 'Team A Average Damage', 'Team A Average Combat Score' , 'Team A Average First Kills',
#     'Team A Average First Deaths Per Round', 'Team B K/D Ratio','Team B Average Damage','Team B Average Combat Score',
#     'Team B Average First Kills','Team B Average First Deaths Per Round'
# ]

# x = vct_data[feature_cols]
# y = vct_data['Outcome'].astype(int)

# X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

# from sklearn.ensemble import RandomForestClassifier
# rf = RandomForestClassifier(n_estimators=50, random_state=42)

# rf.fit(X_train, y_train)

# y_pred = rf.predict(X_test)

# rf.score(X_test, y_test)

# #Evaluate the model
# print("Accuracy:", accuracy_score(y_test, y_pred))