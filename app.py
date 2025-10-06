import streamlit as st
import pickle
import pandas as pd
import requests
import os
import joblib
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv("API_KEY")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #708090
        
    }
    </style>
    """,
    unsafe_allow_html=True
)

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{(movie_id)}?api_key={api_key}&language=en-US"
    response = requests.get(url)
    # Dont hardcode api
    data=response.json()
    
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']





def recommend(movie):
    movie_index = m_list[m_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies=[]
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = m_list.iloc[i[0]].movie_id
        
        recommended_movies.append(m_list.iloc[i[0]].title)
        #fetch poster using Api
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters



m_list = joblib.load('movies.joblib')
movies_list=m_list['title'].values

similarity = joblib.load('similarity.joblib')

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "Select Movies",movies_list
)


if st.button("Recommend"):
    names,posters = recommend(selected_movie_name)
    
    # col1, col2, col3, col4, col5 = st.columns(5)

    # with col1:
    #     st.text(names[0])
    #     st.image(posters[0])

    # with col2:
    #     st.text(names[1])
    #     st.image(posters[1])

    # with col3:
    #     st.text(names[2])
    #     st.image(posters[2]
    # with col4:
    #     st.text(names[3])
    #     st.image(posters[3])
    # with col5:
    #     st.text(names[4])
    #     st.image(posters[4])

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(posters[i], width='stretch')
            st.markdown(f"""
            <div style="text-align:center; font-size:16px; font-weight:bold; margin-top:10px;">
                {names[i]}
            </div>
            """,unsafe_allow_html=True)



