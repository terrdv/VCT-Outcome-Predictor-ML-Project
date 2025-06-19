import pandas as pd


from sklearn.preprocessing import OrdinalEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from collections import Counter
import numpy as np



vct_data = pd.read_csv('filtered_matches.csv')

vct_data = vct_data.dropna()

classes = [False, True]

oc = OrdinalEncoder(categories=[classes])
vct_data['Team A Win'] = oc.fit_transform(vct_data[['Team A Win']])

feature_cols = [
    'Team A Winrate vs B', 'Team A Winrate', 'Team A K/D Ratio', 'Team A Average Damage',
    'Team A Average Combat Score', 'Team A Average First Kills', 'Team A Average First Deaths Per Round',
    'Team B Winrate vs A', 'Team B Winrate', 'Team B K/D Ratio', 'Team B Average Damage',
    'Team B Average Combat Score', 'Team B Average First Kills', 'Team B Average First Deaths Per Round'
]

x = vct_data[feature_cols]
y = vct_data['Team A Win']

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

log_reg = LogisticRegression(max_iter=1000, random_state=42)

log_reg.fit(X_train, y_train)


y_pred = log_reg.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

def predictionLog(df):
    preds = []

    for _ in range(50):
        pred = log_reg.predict(df)
        preds.append(pred[0])  # Assuming df is a single-row DataFrame

    majority_vote = Counter(preds).most_common(1)[0][0]
    return majority_vote