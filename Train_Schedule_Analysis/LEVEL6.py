import pandas as pd
df=pd.read_csv(r'C:\Users\GNANI\projects\Sysslan IT Solutions Project\Train_Schedule_Analysis\Dataset1.csv')

#Task 6.1

pivot=df.pivot_table(index='Station_Name',values='Train_No',aggfunc=['count','nunique'])
pivot.columns=['total_trains','unique_trains']
pivot=pivot.sort_values(by='total_trains',ascending=False)
pivot.to_csv('station_wise_train_distribution.csv')
crosstab=pd.crosstab(df['Station_Name'],df['Route_Number'])
crosstab=crosstab.sort_values(by=1,ascending=False)
crosstab.to_csv('station_route_crosstab.csv')
