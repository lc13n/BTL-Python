import pandas as pd
from collections import Counter


file_path = 'results.csv'  
df = pd.read_csv(file_path, delimiter=';')


stats_columns = df.columns[2:]  


top_teams = {}
for col in stats_columns:
    top_team = df.loc[df[col].idxmax(), 'Squad']
    top_teams[col] = top_team

print("Đội có điểm số cao nhất ở mỗi chỉ số:")
for stat, team in top_teams.items():
    print(f"{stat}: {team}")

team_performance = Counter(top_teams.values())

best_team = team_performance.most_common(1)[0]
print("\nĐội có phong độ tốt nhất:")
print(f"{best_team[0]} với {best_team[1]} lần dẫn đầu các chỉ số")

print("\nSố lần dẫn đầu các chỉ số của mỗi đội:")
for team, count in team_performance.items():
    print(f"{team}: {count} lần")
