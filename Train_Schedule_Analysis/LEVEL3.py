import pandas as pd
df = pd.read_csv(r'C:\Users\GNANI\projects\Sysslan IT Solutions Project\Train_Schedule_Analysis\Dataset1.csv')

# Task 3.1

print("Missing values before cleaning:")
print("Arrival_time '00:00:00' count:", (df['Arrival_time'].astype(str).str.strip() == '00:00:00').sum())
print("Departure_Time '00:00:00' count:", (df['Departure_Time'].astype(str).str.strip() == '00:00:00').sum())
df['Arrival_time'] = df['Arrival_time'].astype(str).str.strip()
df['Departure_Time'] = df['Departure_Time'].astype(str).str.strip()
df = df.sort_values(['Train_No', 'Distance'])
df['is_start'] = df.groupby('Train_No').cumcount() == 0
df['is_end'] = df.groupby('Train_No').cumcount(ascending=False) == 0
df.loc[df['is_start'] & (df['Arrival_time'] == '00:00:00'), 'Arrival_time'] = pd.NA
df.loc[df['is_end'] & (df['Departure_Time'] == '00:00:00'), 'Departure_Time'] = pd.NA
df['Arrival_time'] = pd.to_datetime(df['Arrival_time'], format='%H:%M:%S', errors='coerce')
df['Departure_Time'] = pd.to_datetime(df['Departure_Time'], format='%H:%M:%S', errors='coerce')
df.loc[df['is_start'] & df['Arrival_time'].isna(), 'Arrival_time'] = df.loc[df['is_start'], 'Departure_Time']
df.loc[df['is_end'] & df['Departure_Time'].isna(), 'Departure_Time'] = df.loc[df['is_end'], 'Arrival_time']
df['Departure_Time'] = df.groupby('Train_No')['Departure_Time'].transform(lambda x: x.ffill().bfill())
df['Arrival_time'] = df.groupby('Train_No')['Arrival_time'].transform(lambda x: x.bfill().ffill())
df = df.drop(columns=['is_start', 'is_end'])
print("\nMissing values after cleaning:")
print("Arrival_time null/NaT count:", df['Arrival_time'].isna().sum())
print("Departure_Time null/NaT count:", df['Departure_Time'].isna().sum())
print("\nFirst 10 rows of processed schedule times:")
print(df[['Train_No', 'Station_Name', 'Arrival_time', 'Departure_Time', 'Distance']].head(10).to_string(index=False))
print("="*50)

# Task 3.2

print("--- TASK 3.2: REMOVE DUPLICATE TRAIN RECORDS ---")
initial_rows = len(df)
df = df.drop_duplicates()
final_rows = len(df)
print(f"Initial row count: {initial_rows}")
print(f"Removed {initial_rows - final_rows} duplicate records.")
print(f"Total rows remaining after deduplication: {final_rows}")
print("="*50)

# Task 3.3

print("--- TASK 3.3: VERIFY CORRECT STATION ORDER ---")
is_ordered = df.groupby('Train_No')['Distance'].diff().dropna() >= 0
if is_ordered.all():
    print("Verification Success: All station sequences are correctly ordered by distance.")
else:
    print("Verification Failure: Some routes have incorrect station order.")
print("="*50)
# Task 3.4

print("--- TASK 3.4: SAVE THE VERIFIED DATASET ---")
output_path = r'C:\Users\GNANI\projects\Sysslan IT Solutions Project\Train_Schedule_Analysis\Cleaned_Dataset.csv'
df.to_csv(output_path, index=False)
print(f"Verified dataset saved successfully to: {output_path}")
