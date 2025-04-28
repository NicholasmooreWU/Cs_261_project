#simlogic
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv(r'C:\Users\caden\Cs_261_project\Soccer_data\lineup_data\lineup_2024_AFC.CHAMPIONS.csv')

# Create a new DataFrame to store formation and win information
formation_wins = []

# Iterate through each unique eventId
for event_id in df['eventId'].unique():
    # Get data for the current event
    event_data = df[df['eventId'] == event_id]

    # Extract formation and winner for home team
    formation_wins.append({
        'eventId': event_id,
        'formation': event_data[event_data['homeAway'] == 'home']['formation'].values[0],
        'win': 1 if event_data[event_data['homeAway'] == 'home']['winner'].values[0] == 1 else 0
    })

    # Extract formation and winner for away team
    formation_wins.append({
        'eventId': event_id,
        'formation': event_data[event_data['homeAway'] == 'away']['formation'].values[0],
        'win': 1 if event_data[event_data['homeAway'] == 'away']['winner'].values[0] == 1 else 0
    })

formation_wins_df = pd.DataFrame(formation_wins)

# Group by formation and calculate win percentage and count
formation_stats = formation_wins_df.groupby('formation').agg(
    total_count=('formation', 'size'),
    win_count=('win', 'sum')
).reset_index()

# Calculate win percentage
formation_stats['win_percentage'] = (formation_stats['win_count'] / formation_stats['total_count']) * 100

# Sort by win percentage in descending order
formation_stats = formation_stats.sort_values(by='win_percentage', ascending=False)

# Display the results
print(formation_stats)

plt.figure(figsize=(10, 6))
sns.scatterplot(x='total_count', y='win_percentage', data=formation_stats,
                hue='formation', size='total_count', sizes=(50, 500),
                palette='viridis', alpha=0.7)

# Customize the plot
plt.title('Win Percentage vs. Total Count by Formation (Bubble Chart)')
plt.xlabel('Total Count')
plt.ylabel('Win Percentage')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # Place legend outside
plt.tight_layout()

# Show the plot
plt.show()