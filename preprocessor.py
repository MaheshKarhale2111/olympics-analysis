import pandas as pd 
import streamlit as st




def preprocess(df,region_df) : 
    #filtering out oympics happened in summer 
    df = df[df['Season'] == 'Summer']
    # drop 1906 olympics as it's not official 
    df = df.drop(df[df['Year'] == 1906].index)
    #merging 
    df=  df.merge(region_df,on='NOC', how='left')
    # st.table(df)
    df = df.drop(['ID','Season','notes','NOC'], axis=1)
    #drop duplicates 
    df.drop_duplicates(inplace=True)
    #one-hot encode medals 
    df = pd.concat([df,pd.get_dummies(df['Medal'])], axis=1)
    
    return df

def remove_duplicate_medals(df):
    df0 = df.drop_duplicates(subset=['City','Sport','Event','Medal','region', 'Team','Year',])
    return df0
