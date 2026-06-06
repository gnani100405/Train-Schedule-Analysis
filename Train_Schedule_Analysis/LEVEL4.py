from pandas import plotting
from dataclasses import dataclass
import pandas as pd
df = pd.read_csv(r'C:\Users\GNANI\projects\Sysslan IT Solutions Project\Train_Schedule_Analysis\Dataset1.csv')

#Task 4.1

idx_min = df.groupby('Train_No')['Distance'].idxmin()
idx_max = df.groupby('Train_No')['Distance'].idxmax()
df_start = df.loc[idx_min, ["Train_No", "Departure_Time"]].rename(columns={"Departure_Time": "Start_Time"})
df_end = df.loc[idx_max, ["Train_No", "Arrival_time", "Distance"]].rename(columns={"Arrival_time": "End_Time", "Distance": "Total_Distance"})
merged = pd.merge(df_start, df_end, on="Train_No")
def classify_route(distance):
    if pd.isna(distance):
        return 'Unknown'
    if distance <= 100:
        return 'Short'
    if distance <= 500:
        return 'Medium'
    return 'Long'
merged['Route_Type'] = merged['Total_Distance'].apply(classify_route)
def cal_duration(row):
    t_start = pd.to_datetime(row['Start_Time'], format='%H:%M:%S', errors='coerce')
    t_end = pd.to_datetime(row['End_Time'], format='%H:%M:%S', errors='coerce')
    
    if pd.isna(t_start) or pd.isna(t_end):
        return None
        
    if t_end < t_start:
        t_end += pd.Timedelta(days=1)
    return (t_end - t_start).total_seconds() / 3600.0

merged['duration_hours'] = merged.apply(cal_duration, axis=1)
avg_duration = merged.groupby("Route_Type")["duration_hours"].mean().reset_index()
print(avg_duration)

#Task 4.2

station_counts=df.groupby(["Station_Name","Station_Code"]).size().reset_index(name="Total_Trains")
high_traffic=station_counts.sort_values(by="Total_Trains",ascending=False)
print("Top Hight Traffic Station: ")
print(high_traffic.head(10).to_string(index=False))

#Task 4.3

print("\n" + "="*55 + "\nSTATION TRAFFIC (TOP 10 STATIONS)\n" + "-"*55)
top_10 = high_traffic.head(10)
for _, r in top_10.iterrows():
    print(f"{r['Station_Name'] + ' (' + r['Station_Code'] + ')':<25} | {'#' * int(r['Total_Trains']/35):<30} | {r['Total_Trains']} trains")
print("\n" + "-"*55 + "\nJOURNEY DURATION DISTRIBUTION\n" + "-"*55)
durations = merged['duration_hours'].dropna()
for h in range(0, 24, 2):
    count = ((durations >= h) & (durations < h+2)).sum()
    if count > 0:
        print(f"Duration {h:02d}-{h+2:02d}h : {'#' * int(count/180):<30} | {count} trains")
print("="*55 + "\n")
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.figure(figsize=(8, 5))
    top_10.sort_values(by="Total_Trains").plot(kind='barh', x='Station_Name', y='Total_Trains', color='teal', legend=False)
    plt.title("Top 10 High Traffic Stations")
    plt.tight_layout()
    plt.savefig("station_traffic.png")
    plt.savefig(r"C:\Users\GNANI\projects\Sysslan IT Solutions Project\Train_Schedule_Analysis\station_traffic.png")
    plt.close()
    plt.figure(figsize=(8, 5))
    plt.hist(durations, bins=15, color='coral', edgecolor='black')
    plt.title("Distribution of Journey Durations")
    plt.xlabel("Duration (Hours)")
    plt.tight_layout()
    plt.savefig("journey_duration.png")
    plt.savefig(r"C:\Users\GNANI\projects\Sysslan IT Solutions Project\Train_Schedule_Analysis\journey_duration.png")
    plt.close()
    
    print("[SUCCESS] Plots saved as station_traffic.png and journey_duration.png")
except:
    pass

#Task 4.4

num_trains = df["Train_No"].nunique()
num_stations = df["Station_Code"].nunique()
avg_stops = df.groupby("Train_No").size().mean()
route_distances = df.groupby("Train_No")["Distance"].max()
longest_run = route_distances.max()
avg_run = route_distances.mean()
print("Dataset Summary Observations:")
print(f"Total Unique Trains: {num_trains}")
print(f"Total Unique Stations: {num_stations}")
print(f"Average Stops Per Train: {avg_stops:.2f}")
print(f"Maximum Journey Distance: {longest_run} km")
print(f"Average Journey Distance: {avg_run:.2f} km")