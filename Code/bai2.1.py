import pandas as pd

# Read the CSV file
file_path = 'results.csv'
df = pd.read_csv(file_path, delimiter=';')

# Initialize a dictionary to store the results
results = {}

# Loop through the columns (assuming statistics start from the 8th column)
for col in df.columns[7:]:
    # Get top 3 players with highest scores for this statistic
    top_players = df.nlargest(3, col)['Player'].tolist()
    results[f'Highest_{col}'] = top_players
    
    # Get top 3 players with lowest scores for this statistic
    bottom_players = df.nsmallest(3, col)['Player'].tolist()
    results[f'Lowest_{col}'] = bottom_players

# Create a DataFrame from the results dictionary
results_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in results.items()]))

# Save the results DataFrame to a new CSV file
output_file_path = 'top_bottom_players.csv'
results_df.to_csv(output_file_path, index=False)

print(f'Results saved to {output_file_path}')
