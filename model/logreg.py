import pandas as pd


from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler


vct_data = pd.read_csv('filtered_matches.csv')

vct_data = vct_data.dropna()

vct_data['Team A Win'] = vct_data['Team A Win'].astype(int)

feature_cols = [
    'Team A Winrate vs B', 'Team A Winrate', 'Team A K/D Ratio', 'Team A Average Damage',
    'Team A Average Combat Score', 'Team A Average First Kills', 'Team A Average First Deaths Per Round',
    'Team B Winrate vs A', 'Team B Winrate', 'Team B K/D Ratio', 'Team B Average Damage',
    'Team B Average Combat Score', 'Team B Average First Kills', 'Team B Average First Deaths Per Round'
]

def create_order_invariant_data(df):
    """Create order-invariant dataset by swapping team positions"""
    original_data = df.copy()
    

    swapped_data = df.copy()
    

    team_a_cols = [col for col in feature_cols if 'Team A' in col]
    team_b_cols = [col for col in feature_cols if 'Team B' in col]
    
    for a_col, b_col in zip(team_a_cols, team_b_cols):
        swapped_data[a_col] = df[b_col]
        swapped_data[b_col] = df[a_col]
    
    # Flip the target variable for swapped data
    swapped_data['Team A Win'] = 1 - df['Team A Win']
    
    # Combine original and swapped data
    augmented_data = pd.concat([original_data, swapped_data], ignore_index=True)
    return augmented_data


augmented_vct_data = create_order_invariant_data(vct_data)

x_augmented = augmented_vct_data[feature_cols]
y_augmented = augmented_vct_data['Team A Win']

X_train, X_test, y_train, y_test = train_test_split(x_augmented, y_augmented, test_size=0.2, random_state=42)


scaler = StandardScaler()
X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=feature_cols)
X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=feature_cols)

log_reg = LogisticRegression(max_iter=5000, random_state=42)

log_reg.fit(X_train_scaled, y_train)


y_pred = log_reg.predict(X_test_scaled)
print("Accuracy:", accuracy_score(y_test, y_pred))
def predictionLog(df):
    data_scaled = pd.DataFrame(scaler.transform(df), columns=feature_cols)
    pred = log_reg.predict(data_scaled)
    return pred[0]

def predictionLog_probability_order_invariant(df, threshold=0.5):
    """Order-invariant probability-based prediction"""
    # Make prediction with original order
    data_scaled = pd.DataFrame(scaler.transform(df), columns=feature_cols)
    prob_original = log_reg.predict_proba(data_scaled)[0][1]
    
    # Create swapped version
    df_swapped = df.copy()
    team_a_cols = [col for col in feature_cols if 'Team A' in col]
    team_b_cols = [col for col in feature_cols if 'Team B' in col]
    
    for a_col, b_col in zip(team_a_cols, team_b_cols):
        df_swapped[a_col] = df[b_col]
        df_swapped[b_col] = df[a_col]
    
    # Make prediction with swapped order
    data_swapped_scaled = pd.DataFrame(scaler.transform(df_swapped), columns=feature_cols)
    prob_swapped = log_reg.predict_proba(data_swapped_scaled)[0][1]
    
    # Average the predictions
    final_team_a_prob = (prob_original + (1 - prob_swapped)) / 2
    
    return 1 if final_team_a_prob >= threshold else 0