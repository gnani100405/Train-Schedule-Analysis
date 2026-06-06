import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv(r'C:\Users\GNANI\projects\Sysslan IT Solutions Project\Train_Schedule_Analysis\Dataset1.csv')

#Task 5.1

station_pivot=df.pivot_table(
    index="Station_Name",values="Train_No",aggfunc=['count','nunique']
)
station_pivot.columns=['total_trains_count','unique_trains_count']
station_pivot=station_pivot.sort_values(by='unique_trains_count',ascending=False)
print("Top 10 busiest Stations: ")
print(station_pivot.head(10))
station_pivot.to_csv('Station_wise_train_distribution.csv')

#Task 5.2

route_crosstab=pd.crosstab(df['Station_Name'],
df['Route_Number'])
route_crosstab=route_crosstab.sort_values(by=1,ascending=False)
print("station vs Route frequency matrix (Top 10): ")
print(route_crosstab.head(10))
route_crosstab.to_csv('station_vs_route_frequency_matrix.csv')
print("\n the cross tabulation matrix is successfully saved")

#TASK 5.3

top_stations = df['Station_Name'].value_counts().head(10)
sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=top_stations.values, y=top_stations.index, hue=top_stations.index, ax=ax, palette="Blues_r", legend=False)
ax.set_title('Top 10 Busiest Stations by Train Frequency', fontsize=14, weight="bold")
ax.set_xlabel("Number of Trains")
ax.set_ylabel('Station Name')
plt.tight_layout()
plt.savefig('station_frequency_barchart.png', dpi=300)
plt.show()
print("Chart 1 saved: station_frequency_barchart.png")
top_pivot = station_pivot.head(10).copy()
fig, ax = plt.subplots(figsize=(12, 6))
x = range(len(top_pivot.index))
bar_width = 0.35
bars1 = ax.bar([i - bar_width/2 for i in x], top_pivot['total_trains_count'], width=bar_width,
               label='Total Train Stops', color='steelblue')
bars2 = ax.bar([i + bar_width/2 for i in x], top_pivot['unique_trains_count'], width=bar_width,
               label='Unique Trains', color='coral')
ax.set_title('Top 10 Stations: Total Train Stops vs Unique Trains (Pivot Table)', fontsize=14, weight='bold')
ax.set_xlabel('Station Name')
ax.set_ylabel('Count')
ax.set_xticks(list(x))
ax.set_xticklabels(top_pivot.index, rotation=45, ha='right', fontsize=9)
ax.legend()
plt.tight_layout()
plt.savefig('pivot_comparative_chart.png', dpi=300)
plt.show()
print("Chart 2 saved: pivot_comparative_chart.png")
top_crosstab = route_crosstab.head(10).iloc[:, :10]
fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(top_crosstab, annot=True, fmt='d', cmap='YlOrRd', ax=ax, linewidths=0.5)
ax.set_title('Cross-Tab Heatmap: Top 10 Stations vs Top 10 Routes', fontsize=14, weight='bold')
ax.set_xlabel('Route Number')
ax.set_ylabel('Station Name')
plt.tight_layout()
plt.savefig('crosstab_heatmap.png', dpi=300)
plt.show()
print("Chart 3 saved: crosstab_heatmap.png")

#Task 5.4

origin_stations=df[df['Distance']==0]['Station_Name'].value_counts().head(10)
print(origin_stations.to_string())

longest_route=df.loc[df['Distance'].idxmax()]
print(f"Train No: {longest_route['Train_No']} | Destination: {longest_route['Station_Name']} | Distance: {longest_route['Distance']} km")

departure_hours=df['Departure_Time'].str.split(':').str[0]
print(departure_hours.value_counts().head(3).rename_axis('Hour_of_Day').reset_index(name='Train_Count').to_string(index=False))