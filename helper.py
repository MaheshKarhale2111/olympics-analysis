import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

def medal_tally(df):
  medal_tally = df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
  medal_tally['total'] = medal_tally['Gold']  + medal_tally['Silver']+ medal_tally['Bronze']

  return medal_tally



def fetch_medal_tally(year, country,medal_df): 
    
    flag = False
    if (year == 'Overall' and country == 'Overall') :
        temp = medal_df
    elif (year == 'Overall' and country != 'Overall') :
        flag = True
        temp= medal_df[(medal_df['region'] ==  country)]
    elif (year != 'Overall' and country == 'Overall') : 
        temp= medal_df[medal_df['Year'] ==  int(year)]
    elif (year != 'Overall' and country != 'Overall') :
       temp = medal_df[(medal_df['Year'] ==  int(year)) & (medal_df['region'] == country)]

    if(flag):
        x = temp.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year',ascending=True).reset_index()
    else : 
        x = temp.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    
    x['Total'] = x['Gold'] + x['Silver']+ x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['Total'] = x['Total'].astype('int')


    return x


def country_year_list(df): 
  years = df['Year'].unique().tolist()
  years.sort(reverse = True)
  years.insert(0,'Overall')


  country = df['region'].dropna().unique().tolist()
  country.sort()
  country.remove('USA')
  country.remove('India')
  country.remove('UK')
  country.remove('China')
  country.remove('Japan')
  country.remove('France')
  country.insert(0,'France')
  country.insert(0,'UK')
  country.insert(0,'China')
  country.insert(0,'India')
  country.insert(0,'USA')
  country.insert(0,'Japan')
  country.insert(0,'Overall')

  return years,country

def data_over_time(df,col): 
   nations_over_time = df.drop_duplicates(subset=['Year',col])['Year'].value_counts().reset_index().sort_values('Year')
   return nations_over_time

def most_successful(sport,df) :
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    
    temp_df = temp_df['Name'].value_counts().reset_index().head(10).merge(df,left_on ='Name', right_on = 'Name', how ='left')
    #extracting important columns
    temp_df = temp_df[['Name','count','region','Sport']]    #drop duplicates 
    temp_df = temp_df.drop_duplicates('Name').reset_index()
    temp_df = temp_df.drop('index', axis = 1)
    temp_df.rename(columns = {'count' : 'Medals','region' : 'Country'}, inplace = True)
    return temp_df

def yearwise_medal_analysis(df,country): 
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    temp_df = temp_df.groupby('Year').count()['Medal'].reset_index()
    temp_df.rename(columns={'Medal' : 'Total Medals'},inplace=True)
    return temp_df

def countrys_sport_analysis(df,country) : 
   temp_df = df.dropna(subset=['Medal'])
   temp_df = temp_df[temp_df['region'] == country]

   return   temp_df.pivot_table(index='Sport', columns='Year',values='Medal',aggfunc='count').fillna(0).astype('int')
#    return temp_df

def most_successful_in_country(country,df) :
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]
    
    temp_df = temp_df['Name'].value_counts().reset_index().head(10).merge(df,left_on ='Name', right_on = 'Name', how ='left')
    #extracting important columsn 
    temp_df = temp_df[['Name','count','Sport']]    #drop duplicates 
    temp_df = temp_df.drop_duplicates('Name').reset_index()
    temp_df = temp_df.drop('index', axis = 1)
    temp_df.rename(columns = {'count' : 'Medals'}, inplace = True)
    return temp_df

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final