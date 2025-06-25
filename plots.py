
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
from PIL import Image


def pie(teama, teamb, df):
    labels = [teama, teamb]
    a = df.iloc[0]["Team A Winrate vs B"]
    b = df.iloc[0]["Team B Winrate vs A"]
    if a == 0 and b == 0:
        a = 50
        b = 50
    vals = [a,b]

    plt.pie(vals, labels=labels, autopct='%1.1f%%', startangle=90, colors=["#5380a0", "#6C5F9B"], wedgeprops={'edgecolor': 'white'}, textprops={'color': 'white'})
    plt.title(f"{teama} vs {teamb} Winrates", fontsize=16, color = "white")


    buf = BytesIO()
    fig = plt.gcf() 
    fig.set_size_inches(3.5,3.5)
    plt.savefig(buf, format='png', transparent=True, bbox_inches='tight')
    plt.close(fig)  # Close to free memory
    plt.xticks(fontsize=10, color="white")
    plt.yticks(fontsize=10, color="white")
    buf.seek(0)

    # Return as a PIL image
    return Image.open(buf)


def barplot(teama, teamb, df):
    x = ['Overall Winrate', 'Damage per Round', 'Combat Score']

    team_a_stats = [
        df.iloc[0]["Team A Winrate"],
        df.iloc[0]["Team A Average Damage"],
        df.iloc[0]["Team A Average Combat Score"]
    ]

    team_b_stats = [
        df.iloc[0]["Team B Winrate"],
        df.iloc[0]["Team B Average Damage"],
        df.iloc[0]["Team B Average Combat Score"]
    ]
    plt.bar(x, team_a_stats, width=0.4, label=teama, color="#5380a0", align='center')
    plt.bar(x, team_b_stats, width=0.4, label=teamb, color="#6C5F9B", align='edge')
    plt.title(f"{teama} vs {teamb} Stats Comparison", fontsize=14, color = "white")
    plt.xlabel("Average Metrics", fontsize=12, color = "white")
    plt.ylabel("Value",fontsize=12, color="white")
    plt.xticks(fontsize=7, color="white")
    plt.yticks(fontsize=8, color="white")
    
    

    buf = BytesIO()
    fig = plt.gcf() 
    fig.set_size_inches(3.5,3.5)
    plt.savefig(buf, format='png', transparent=True, bbox_inches='tight')
    plt.close(fig)  # Close to free memory
    buf.seek(0)

    # Return as a PIL image
    return Image.open(buf)

    
