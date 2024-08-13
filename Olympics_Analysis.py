import streamlit as st 
import pandas as pd 
import plotly.express as px
import seaborn as sns 
import matplotlib.pyplot as plt
import plotly.figure_factory as ff 
import scipy

import preprocessor
import helper

def wide_space_default():
    st.set_page_config(layout="wide")

wide_space_default()

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
tokyo_df = pd.read_csv('2020 Tokyo extension.csv')

old_df = df
df = pd.concat([df,tokyo_df],axis=0)

df = preprocessor.preprocess(df,region_df)
old_df = preprocessor.preprocess(old_df,region_df)
df_no_duplicate_medal = preprocessor.remove_duplicate_medals(df)

st.sidebar.title("Olympics Analysis")

user_menu =st.sidebar.radio(
    'Select Option', 
    ('Medal Tally','Country-Wise Analysis','Most Successful Athletes', 'Overall Analysis','Athlete wise Analysis')
)


# st.dataframe(df)

if user_menu == 'Medal Tally':
    st.subheader("**This data analysis tool covers 124 years of Olympic history (1896-2020). It offers the following features:**")
    st.write("***Select the option from left side-bar***")
    st.markdown('''1. :blue-background[MEDAL TALLY]: View country-wise and year-wise medal counts.''')
    st.markdown('''2. :blue-background[COUNTRY-WISE ANALYSIS]:Track the performance of a specific country over the years and discover its most successful athletes.''')
    st.markdown('''3. :blue-background[MOST SUCCESSFUL ATHLETES]:Discover most successful athletes in particular sport.''')
    st.markdown('''4. :blue-background[OVERALL OLYMPIC ANALYSIS]: Explore the number of events, events over time, and identify the most successful athletes in each sport.  ''')
    st.markdown('''5. :blue-background[ATHELETE-WISE ANALYSIS]:  Analyze the age distribution of medalists, compare male vs. female participation, and examine height vs. weight trends.''')
    # st.text("This is mahesh")
    # temp_df = # df0 =df.drop_duplicates(subset=['City','Sport','Event','Medal','NOC','Year','Games'])
    temp_df = df_no_duplicate_medal[['region','Year','Gold','Silver','Bronze']]
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)
    

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country",country)
    # medal_tally = helper.medal_tally(df)
    if selected_year == 'Overall' and selected_country == 'Overall' : 
        st.title("Overall Tally (1896 - 2020)")
    elif selected_year != 'Overall' and selected_country == 'Overall' : 
        st.title("Medal Tally in year " + str(selected_year))
    elif selected_year == 'Overall' and selected_country != 'Overall' :
         st.title(selected_country + "'s overall performance") 
    elif selected_year != 'Overall' and selected_country != 'Overall' :
         st.title(selected_country + "'s performance in " + str(selected_year)) 
    st.divider()
    medal_tally = helper.fetch_medal_tally(selected_year,selected_country,temp_df)
    medal_tally.rename(columns = {'region':'Country'},inplace =True)
    st.table(medal_tally)

if user_menu == 'Most Successful Athletes':
    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.remove('Swimming')
    sport_list.insert(0,'Overall')
    sport_list.insert(0,'Swimming')
    st.header('Select Sport')
    selected_sport = st.selectbox('',sport_list)
    x = helper.most_successful(selected_sport,df)
    st.table(x)
    st.divider()



if user_menu == 'Overall Analysis':
    editions =  df['Year'].unique().shape[0]
    cities =  df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = old_df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]
    st.title("Overall Stats")
    st.divider()
    col1,col2,col3 = st.columns(3)
    with col1: 
        st.header("Editions")
        st.title(editions)
    with col2: 
        st.header("Host Cities")
        st.title(cities)
    with col3: 
        st.header("Sports")
        st.title(sports)

    col1,col2,col3 = st.columns(3)
    with col1: 
        st.header("Events")
        st.title(events)
    with col2: 
        st.header("Athletes")
        st.title(athletes)
    with col3: 
        st.header("Countries")
        st.title(nations)

    st.divider()

    nations_over_time = helper.data_over_time(old_df,'region')
    nations_over_time.rename(columns={'count': 'No of Countries'},inplace=True)
    fig = px.line(nations_over_time, x="Year", y="No of Countries")
    st.title("Participating Nations Over Time")
    st.plotly_chart(fig)
    st.divider()

    events_over_time = helper.data_over_time(old_df,'Event')
    events_over_time.rename(columns={'count': 'No of Events'},inplace=True)
    fig = px.line(events_over_time, x="Year", y="No of Events")
    st.title("No. of Events Over Time")
    st.plotly_chart(fig)
    st.divider()

    athletes_over_time = helper.data_over_time(old_df,'Name')
    athletes_over_time.rename(columns={'count': 'No of Athletes'},inplace=True)
    fig = px.line(athletes_over_time, x="Year", y="No of Athletes")
    st.title("Participating Athletes Over Time")
    st.plotly_chart(fig)
    st.divider()


    st.title("No of events over time (every sport)")
    st.subheader("The heatmap below shows the number of events that took place in each sport during different editions of the Olympics.")
    st.markdown(''':red-background[Funfact] :  Cricket was included in the Olympics in 1900, marking its only appearance in the Olympics. It's set to make a comeback in the 2028 Los Angeles Olympics.''')
    x = df.drop_duplicates(['Year','Event', 'Sport'])[['Year','Event','Sport']]
    fig,ax = plt.subplots(figsize = (25,20))
    ax = sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'), annot= True,cmap = 'Blues')
    st.pyplot(fig)


if user_menu == 'Country-Wise Analysis' : 
    st.title('Country-Wise Analysis')
    st.divider()
    year,country = helper.country_year_list(df)
    country.remove('Overall')
    selected_country = st.sidebar.selectbox('Select a country',country)
    country_over_time = helper.yearwise_medal_analysis(df_no_duplicate_medal,selected_country)

    fig = px.line(country_over_time, x="Year", y="Total Medals")
    st.header(selected_country +"'s Olympic performance over the years")
    st.plotly_chart(fig)
    st.divider()

    st.header(selected_country + "'s sport-wise analysis over the years")
    st.subheader("The numbers represent " + selected_country + "'s medal count in a particular sport for a specific year.")
    st.write("Choose a different country from left side-bar to see stats :)")
    sport_wise_analysis = helper.countrys_sport_analysis(df_no_duplicate_medal,selected_country)
    fig,ax= plt.subplots(figsize = (25,15))
    ax = sns.heatmap(sport_wise_analysis, annot=True, cmap="Blues",annot_kws={"size": 10})
    st.pyplot(fig)
    st.divider()

    st.header('Most successful atheletes in '+ selected_country)
    most_successful = helper.most_successful_in_country(selected_country,df)
    st.table(most_successful)
    st.divider()


if user_menu == 'Athlete wise Analysis': 
    st.title('Athlete wise Analysis')
    st.divider()
    athelete_df = old_df.drop_duplicates(subset=['Name','region'])
    x1 = athelete_df['Age'].dropna()
    x2 = athelete_df[athelete_df['Medal'] == 'Gold'] ['Age'].dropna()
    x3 = athelete_df[athelete_df['Medal'] == 'Silver'] ['Age'].dropna()
    x4 = athelete_df[athelete_df['Medal'] == 'Bronze'] ['Age'].dropna()
    fig = ff.create_distplot([x1,x2,x3,x4],['Overall Age', 'Gold Medalist', 'Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)
    fig.update_layout(autosize = False,width = 1000,height = 600)
    st.header('Age Distribution')
    st.plotly_chart(fig)

    st.divider()

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Athletics',
                     'Swimming', 'Badminton', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling', 'Hockey',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving',
                     'Tennis', 'Golf', 'Archery',
                     'Volleyball', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athelete_df[athelete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.header("Distribution of Age with respect to Sports (Gold Medalists)")
    st.plotly_chart(fig)

    st.divider()

    st.header("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(old_df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

    sport_list = old_df['Sport'].unique().tolist()
    sport_list.remove('Aeronautics')
    sport_list.remove('Golf')
    sport_list.remove('Badminton')
    sport_list.remove('Diving')
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    sport_list.insert(0,'Badminton')
    sport_list.insert(0,'Diving')
    st.header('Height Vs Weight chart for specific sport')
    st.subheader('Select a sport')
    selected_sport = st.selectbox('', sport_list)
    temp_df = helper.weight_v_height(old_df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(data = temp_df, x = 'Weight', y = 'Height',hue=temp_df['Medal'],style=temp_df['Sex'],s=40)
    st.pyplot(fig)

    st.divider()

    



    



