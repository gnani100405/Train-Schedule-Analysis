import pandas as pd

df = pd.read_csv(r'C:\Users\GNANI\projects\Sysslan IT Solutions Project\Train_Schedule_Analysis\Dataset1.csv')

# Task 2.1

df['Arrival_time'] = df['Arrival_time'].str.strip()
df['Departure_Time'] = df['Departure_Time'].str.strip()
df['Arrival_time'] = pd.to_datetime(df['Arrival_time'], errors='coerce')
df['Departure_Time'] = pd.to_datetime(df['Departure_Time'], errors='coerce')
print('--- Task 2.1: arrival and departure times ---')
print(df[['Arrival_time', 'Departure_Time']].head(10).to_string(index=False))

# Task 2.2

df = df.sort_values(['Train_No', 'Distance'])
journey = df.groupby('Train_No', as_index=False).agg(
    Start_Time=('Departure_Time', 'first'),
    End_Time=('Arrival_time', 'last')
)
journey['Total_Duration'] = journey['End_Time'] - journey['Start_Time']
journey.loc[journey['Total_Duration'] < pd.Timedelta(0), 'Total_Duration'] += pd.Timedelta(days=1)

def format_duration(td):
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes = remainder // 60
    if hours:
        return f"{hours} hours and {minutes} minutes"
    return f"{minutes} minutes"

journey['Total_Duration'] = journey['Total_Duration'].apply(format_duration)
print('--- Task 2.2: total train duration ---')
print(journey[['Train_No', 'Total_Duration']].head(10).to_string(index=False))

# Task 2.3

route_distance = df.groupby('Train_No', as_index=False).agg(
    Total_Route_Distance=('Distance', 'max')
)

def classify_route(distance):
    if pd.isna(distance):
        return 'Unknown'
    if distance <= 100:
        return 'Short'
    if distance <= 500:
        return 'Medium'
    return 'Long'

route_distance['Route_Type'] = route_distance['Total_Route_Distance'].apply(classify_route)
print(route_distance[['Train_No', 'Total_Route_Distance', 'Route_Type']].head(20).to_string(index=False))
print(route_distance['Route_Type'].value_counts())

# Task 2.4

station_frequency = df.groupby('Station_Name', as_index=False).agg(
    Train_Count=('Train_No', 'nunique')
).sort_values('Train_Count', ascending=False)
print(station_frequency.head(20).to_string(index=False))