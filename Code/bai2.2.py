import pandas as pd


df = pd.read_csv('results.csv', delimiter=';')

output_data = {'Team': ['All']}

numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns

for column in numeric_columns:
    output_data[f'Median of {column}'] = [df[column].median()]
    output_data[f'Mean of {column}'] = [df[column].mean()]
    output_data[f'Std of {column}'] = [df[column].std()]

for team, team_df in df.groupby('Squad'):
    team_stats = {'Team': team}
    for column in numeric_columns:
        team_stats[f'Median of {column}'] = team_df[column].median()
        team_stats[f'Mean of {column}'] = team_df[column].mean()
        team_stats[f'Std of {column}'] = team_df[column].std()
    output_data = pd.concat([pd.DataFrame(output_data), pd.DataFrame([team_stats])])

output_data.reset_index(drop=True).to_csv('results2.csv', index=False)
