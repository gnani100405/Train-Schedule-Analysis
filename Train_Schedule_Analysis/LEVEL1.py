import pandas as pd

# Task 1.1

df=pd.read_csv('C:\\Users\\GNANI\\projects\\Sysslan IT Solutions Project\\Train_Schedule_Analysis\\Dataset1.csv')
print(df.info())
df.columns
print(df.columns.tolist())
print(df.head())
print(df.tail())

# Task 1.2

result = df.sort_values(['Train_No', 'Distance']).groupby('Train_No', as_index=False).agg(
    Start_Station=('Station_Name', 'first'),
    End_Station=('Station_Name', 'last')
)
print('\nStart and end stations for each train:')
print(result)

# Task 1.3

stops = df.groupby('Train_No', as_index=False).agg(
    Number_of_Stops=('Station_Name', 'count')
)
print('\nNumber of stops per train:')
print(stops)

# Task 1.4

max_stops = stops['Number_of_Stops'].max()
min_stops = stops['Number_of_Stops'].min()

max_stop_trains = stops[stops['Number_of_Stops'] == max_stops]
min_stop_trains = stops[stops['Number_of_Stops'] == min_stops]

print(f'\nTrain(s) with the maximum number of stops ({max_stops}):')
print(max_stop_trains)
print(f'\nTrain(s) with the minimum number of stops ({min_stops}):')
print(min_stop_trains)
