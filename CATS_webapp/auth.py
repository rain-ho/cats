import streamlit as st
import streamlit.components.v1 as com
import string
import random
from email.message import EmailMessage
import ssl
import smtplib
import pandas as pd
import hashlib 
from supabase.client import create_client, Client
from datetime import datetime
from venv import create
from PIL import Image
import datetime
import re
import requests
from datetime import datetime

import base64
import os
import streamlit as st
from supabase import create_client, Client
import re
import string
import hashlib
import json
import hashlib

st.set_page_config(layout="wide")


encrypt = lambda input_string: hashlib.sha256(hashlib.md5(input_string.encode('utf-8')).hexdigest().encode('utf-8')).hexdigest()

#######################################################################################################################################################
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)





#######################################################################################################################################################
def turnRegisterPage():
    st.session_state.page  = 1
    st.session_state.museumId = None

def turnMuseumPage(museumId):
    st.session_state.page = 2
    st.session_state.museumId = museumId
    st.session_state.toggle = False


def turnLoginPage():
    st.session_state.page = 0
    st.session_state.museumId = None

def turnRiskPage(museumId, artId):
    st.session_state.page = 3
    st.session_state.museumId = museumId
    st.session_state.artId = artId

def turnAddPaint(museumId):
    st.session_state.page = 4
    st.session_state.museumId = museumId
    st.session_state.artId = None

def turnHistoryPage(museumId, ArtId):
    st.session_state.page = 5
    st.session_state.museumId = museumId
    st.session_state.artId = ArtId    




            

    




def background(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
            background-size: cover
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


def urlBackground(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url('{image_url}');
            background-size: cover;
            background-color: rgba(255, 255, 255, .5);

        }}
        </style>
        """,
        unsafe_allow_html=True
    )





#   pradomuseo
#   E1.Prad0




def check_password(input_string):
    special_chars = "!@#$%^&*(),.?\":{}|<>"
    if (
        len(input_string) >= 8 and
        any(char.isdigit() for char in input_string) and
        any(char.islower() for char in input_string) and
        any(char.isupper() for char in input_string) and
        any(char in special_chars for char in input_string)
    ):
        return True
    else:
        return False

        

def registerPage():


    supabase = init_connection()
    background('imgs/adam_cat.jpg')

    coll1,coll2, coll3 = st.columns([1.5,3,1.5])

    with coll2:
        st.markdown("<h1 class='LoginTitle'>CATS<br>Register your museum</h1>", unsafe_allow_html=True)

        register_form = st.form(key = 'loginPage')
        with register_form:
            
        #Get User Credentials
            register_name = st.text_input("Name")
            register_username = st.text_input("Username")
            register_email = st.text_input("Email")
            register_password = st.text_input("Password", type = 'password')
            register_verifypassword = st.text_input("Repeat password", type = 'password')
            register_address = st.text_input("Address")

            col1, col2, col3= st.columns([2, 1, 1])
            with col2:
                register_button = st.form_submit_button("Register")
            with col3:
                back_button = st.form_submit_button("Return")
            
            if back_button:
                turnLoginPage()     
                st.experimental_rerun()
            

            if register_button:

                valid_register = True

                if register_name == '':
                    st.text("NAME CAN NOT BE EMPTY")
                    valid_register = False

                if valid_register:
                    if register_username == '':
                        st.text("USERNAME CAN NOT BE EMPTY")
                        valid_register = False

                email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if valid_register:
                    if register_email == '':
                        st.text("EMAIL CAN NOT BE EMPTY")
                        valid_register = False

                if valid_register:
                    if not re.match(email_regex, register_email):
                        st.text("EMAIL IS INVALID")
                        valid_register = False

                if valid_register:
                    if register_password == '':
                        st.text("PASSWORD CAN NOT BE EMPTY")
                        valid_register = False

                if valid_register:
                    if not check_password(register_password):
                        st.text("PASSWORD MUST BE 8 DIGITS LENGHT, HAVE ONE NUMBER, ONE SPECIAL CHARACTER,")
                        st.text("ONE UPPERCASE AND ONE LOWERCASE LETTER")
                        valid_register = False

                if valid_register:
                    if register_address == '':
                        st.text("ADDRESS CAN NOT BE EMPTY")
                        valid_register = False

                if valid_register:
                    if register_password != register_verifypassword:
                        st.text("PASSWORDS DO NOT MATCH")
                        valid_register = False

                if valid_register:
                    register_password = encrypt(register_password)
                    register_verifypassword = ''

                    response, count = supabase.table('museum').select('*').eq('username', register_username).execute()    
                    
                    if len(response[1]) > 0:
                        st.text("THAT USERNAME IS ALREADY TAKEN. CHOOSE ANOTHER.")


                    else:
                        supabase.table('museum').insert({"username": register_username, "email": register_email, "password": register_password, "name": register_name, "address": register_address}).execute()
                        turnLoginPage()     
                        st.experimental_rerun()
                #Louvre.1 ->Password
                #Rikjs -> asAS12.-
                #pradomuseo -> E1.Prad0

                # response, count = supabase.table('museum').select('*').eq('username', username).execute()    
                
                # if len(response[1]) > 0:
                #     loginId =response[1][0]['m_id']
                #    

def landPage():
    supabase = init_connection()

    background('imgs/adam_cat.jpg')

    coll1,coll2, coll3 = st.columns([1.5,3,1.5])
    with coll2:

        st.markdown("<h1 class='LoginTitle'>CATS<br>Creative Art Tracking & Surveillance</h1>", unsafe_allow_html=True)
    
        login_form = st.form(key = 'loginPage')
        with login_form:
            
        #Get User Credentials
            username = st.text_input("Username")
            password = st.text_input("Password", type = 'password')

            col1, col2, col3 = st.columns([2,1,1])
            with col2:
                login_button = st.form_submit_button("Login")
            with col3:
                register_button = st.form_submit_button("Register")

            if register_button:
                turnRegisterPage()     
                st.experimental_rerun()

            if login_button:
                #loginId, loginUsername, loginEmail, loginPassword, loginName, loginAddress, loginAwCNT = spabuase.table('museum').select("*").execute()
                #print (loginUsername, loginPassword)

                #response, count = supabase.table('museum').select('*').execute()
                
                response, count = supabase.table('museum').select('*').eq('username', username).execute()    
                
                if len(response[1]) > 0:
                    loginId =response[1][0]['m_id']
                    loginUsername =response[1][0]['username']
                    loginEmail =response[1][0]['email']
                    loginPassword =response[1][0]['password']
                    loginName =response[1][0]['name']
                    loginAddress =response[1][0]['address']
                    loginAwCNT =response[1][0]['aw_cnt']

                    password = encrypt(password)
                    if loginPassword == password:

                        st.text("SUCCESS")
                        turnMuseumPage(loginId)
                        st.experimental_rerun()

                    #LOGIN

                    else:
                        st.text("USERNAME AND PASSWORD DO NOT MATCH. TRY AGAIN.")
                else:
                    st.text("USERNAME AND PASSWORD DO NOT MATCH. TRY AGAIN.")
  
def loginPage():

    supabase = init_connection()
    museumId = st.session_state.museumId
    
    
    response, count = supabase.table('museum').select('*').eq('m_id', museumId).execute()
    museumName = response[1][0]['name']
    image_url = response[1][0]['image_url']
    museumEmail = response[1][0]['email']
    museumAddress = response[1][0]['address']


    urlBackground(image_url)

    
    st.markdown(f"<h1 class='LoginTitle'>CATS<br>WELCOME {museumName}</h1>", unsafe_allow_html=True)

    response, count = supabase.table('artwork').select('*').eq('museum_m_id', museumId).execute()
    
 
    col1, col2= st.columns([6, 1])     
   
    with col2:
            
        if st.button("REFRESH", key="refreshArtkey}"):
            turnMuseumPage(museumId)
            st.experimental_rerun()


        if st.button("LOGOUT",key="LogoutMuseumkey"):
            turnLoginPage()
            st.experimental_rerun()
            
        if st.button("MANAGEMENT", key="newArtWork"):
            turnAddPaint(museumId)
            st.experimental_rerun()


    if response [1] != []:
        artTitle = response[1][0]['title']
        artArtist = response[1][0]['artist']
        # for i in range(0, 1 + len(response)):
        #     print(response[1][i]['title'] + '--->' + response[1][i]['artist'] + '\n\n')

        # Define the sizes as percentages
        col1_width = 35
        col2_width = 45
        col3_width = 15


        col1, col2= st.columns([6, 1])     
        with col1:
            st.markdown(f'<div class= "museumId"> ARTWORKS </div>', unsafe_allow_html=True)   
        

        for i in range(0, len(response[1])):
            
            title = response[1][i]['title'] + "  by  " + response[1][i]['artist']

            st.markdown(f'<div class="titleMuseumPage">{title}</div>', unsafe_allow_html=True)
                        


            col1, col2, col3 = st.columns([col1_width, col2_width, col3_width])
            
            with col1:
                imageURL = response[1][i]['img_url']
                st.image(imageURL)  

            with col2:
                markdown_text = f"<strong>Title:</strong> {response[1][i]['title'] or 'No information'}<br>" \
                                f"<strong>Artist:</strong> {response[1][i]['artist'] or 'No information'}<br>" \
                                f"<strong>Board ID:</strong> {response[1][i]['board_id'] or 'No information'}<br>" \
                                f"<strong>Description:</strong> {response[1][i]['description'] or 'No information'}<br>" \
                                f"<strong>Year Made:</strong> {response[1][i]['year_made'] or 'No information'}<br>" \
                                f"<strong>Style:</strong> {response[1][i]['style'] or 'No information'}<br>" \
                                f"<strong>Medium:</strong> {response[1][i]['medium'] or 'No information'}<br>" \
                                f"<strong>Height:</strong> {str(response[1][i]['height']) + ' m' if response[1][i]['height'] else 'No information'}<br>" \
                                f"<strong>Width:</strong> {str(response[1][i]['width']) + ' m' if response[1][i]['width'] else 'No information'}<br>" \
                                f"<strong>Worth:</strong> {response[1][i]['worth'] or 'No information'}<br>" \
                                f"<strong>Acquisition Date:</strong> {response[1][i]['acq_date'] or 'No information'}<br>" \
                                f"<strong>Acquisition Price:</strong> {response[1][i]['acq_price'] or 'No information'}<br>" \
                                f"<strong>Owner:</strong> {response[1][i]['owner'] or 'No information'}<br>" \
                                f"<strong>Status:</strong> {response[1][i]['status'] or 'No information'}<br>" 
                                

                with st.expander("Click to view details"):
                    st.markdown(f'<div class="descryptBoxArtwork">{markdown_text}</div>', unsafe_allow_html=True)

                    risk_button = st.button("RISK ANALYSIS", key={i + 1})
                    if risk_button:
                        turnRiskPage(museumId, response[1][i]['a_id'])
                        st.experimental_rerun()
            

                    

    return

def addPaint():
    supabase = init_connection()
    museumId = st.session_state.museumId
    
    
    response, count = supabase.table('museum').select('*').eq('m_id', museumId).execute()
    museumName = response[1][0]['name']
    image_url = response[1][0]['image_url']
    museumEmail = response[1][0]['email']
    museumAddress = response[1][0]['address']
    urlBackground(image_url)

    if st.button("ADD NEW ARTWORK", key="nWork"):
        turnAddPaint(museumId)
        st.experimental_rerun()
    if st.button("Return", key="returnMusFromAdd}"):
        turnMuseumPage(museumId)
        st.experimental_rerun()
    

    col1, col2, col3 = st.columns([1,1,1])

    with col1:
        artRegisterForm = st.form("ArtRegistForm") #, clear_on_submit=True)
        with artRegisterForm:
            st.markdown(f'<div class = "manageTitles">REGISTER A NEW ARTWORK</div>', unsafe_allow_html=True)
            AwTitleReg = st.text_input("", placeholder="TITLE")
            AwArtistReg = st.text_input("", placeholder="ARTIST")
            AwStyleReg = st.text_input("", placeholder="STYLE")
            AwMediumReg = st.text_input("", placeholder="MEDIUM")
            AwDescReg = st.text_input("", placeholder="DESCRIPTION")
            AwImgReg = st.text_input("", placeholder="IMAGE URL")
            AwYearReg = st.text_input("", placeholder="YEAR MADE")
            AwHeiReg = st.text_input("", placeholder="HEIGHT")
            AwWidReg = st.text_input("", placeholder="WIDTH")
            AwWeiReg = st.text_input("", placeholder="WEIGHT")
            AwWorReg = st.text_input("", placeholder="WORTH")
            AwAqDReg = st.text_input("", placeholder="ACQUISITION DATE")
            AwAqPReg = st.text_input("", placeholder="ACQUISITION PRICE")
            AwOwnReg = st.text_input("", placeholder="OWNER")
            AwStaReg = st.text_input("", placeholder="STATUS")
            AwBoardIdReg = st.text_input("", placeholder="BOARD ID")

            if st.form_submit_button("SUBMIT"):

                valid_register = True

                if AwTitleReg == '':
                    st.text("TITLE CAN NOT BE EMPTY")
                    valid_register = False

                if valid_register:
                    if AwArtistReg == '':
                        st.text("ARTIST CAN NOT BE EMPTY")
                        valid_register = False
                if valid_register:
                    if AwStyleReg == '':
                        st.text("STYLE CAN NOT BE EMPTY")
                        valid_register = False
                
                if valid_register:
                    if AwMediumReg == '':
                        st.text("MEDIUM CAN NOT BE EMPTY")
                        valid_register = False

                if valid_register:
                    if AwDescReg == '':
                        st.text("DESCRIPTION CAN NOT BE EMPTY")
                        valid_register = False

                if valid_register:
                    if AwImgReg == '':
                        st.text("IMAGE URL CAN NOT BE EMPTY")
                        valid_register = False

                if valid_register:
                    if AwOwnReg == '':
                        st.text("OWNER CAN NOT BE EMPTY")
                        valid_register = False
                if valid_register:
                    if AwStaReg == '':
                        st.text("STATUS CAN NOT BE EMPTY")
                        valid_register = False
                
                if valid_register:
                    if AwBoardIdReg == '':
                        st.text("INTERNAL ID CAN NOT BE EMPTY")
                        valid_register = False

                if valid_register:
                    AwAqPReg = float(AwAqPReg) if AwAqPReg else None
                    AwAqPReg = float(AwHeiReg) if AwHeiReg else None
                    AwWidReg = float(AwWidReg) if AwWidReg else None
                    AwWeiReg = float(AwWeiReg) if AwWeiReg else None
                    AwWorReg = float(AwWorReg) if AwWorReg else None
                    AwYearReg = int(AwYearReg) if AwYearReg else None
                    AwAqDReg = AwAqDReg if AwAqDReg else None

                    print("bottao")
                    supabase.table('artwork').insert([{'title': AwTitleReg, 'artist': AwArtistReg, 'style': AwStyleReg, 'medium': AwMediumReg, 'description': AwDescReg, 'img_url': AwImgReg, 'year_made': AwYearReg, 'height': AwHeiReg, 'width': AwWidReg, 'weight': AwWeiReg, 'worth': AwWorReg, 'acq_date': AwAqDReg, 'acq_price': AwAqPReg, 'owner': AwOwnReg, 'status': AwStaReg, 'board_id': AwBoardIdReg, 'museum_m_id': museumId}]).execute();
                    response, count = supabase.table('artwork').select('a_id').eq('title', AwTitleReg).execute()
                    artID =response[1][0]['a_id']
                    supabase.table('risk_analysis').insert([{'movrisk': 0, 'vibrisk': 0, 'smkrisk':0, 'riskreps': 0, 'temprisk': 0, 'humrisk': 0, 'artwork_a_id': artID}]).execute()
                    supabase.table('status').insert([{'temperature': 0, 'humidity': 0, 'smoke': 0, 'vibration': 0, 'movement': 0, 'artwork_a_id': artID}]).execute()

    with col2:
            response, count = supabase.table('artwork').select('*').eq('museum_m_id', museumId).execute()
            PicNamesList = ()
            for i in range (0, len(response[1])):
                PicNamesList += ((response[1][i]['title']),)
            print(PicNamesList)
            st.markdown(f'<div class = "manageTitles">EDIT AN ARTWORK</div>', unsafe_allow_html=True)
            selected_pic = st.selectbox("Select Artwork", PicNamesList, label_visibility="collapsed")
            artEditForm = st.form("ArtEditForm")
            with artEditForm:
                AwTitleReg = st.text_input("", placeholder="TITLE")
                AwArtistReg = st.text_input("", placeholder="ARTIST")
                AwStyleReg = st.text_input("", placeholder="STYLE")
                AwMediumReg = st.text_input("", placeholder="MEDIUM")
                AwDescReg = st.text_input("", placeholder="DESCRIPTION")
                AwImgReg = st.text_input("", placeholder="IMAGE URL")
                AwYearReg = st.text_input("", placeholder="YEAR MADE")
                AwHeiReg = st.text_input("", placeholder="HEIGHT")
                AwWidReg = st.text_input("", placeholder="WIDTH")
                AwWeiReg = st.text_input("", placeholder="WEIGHT")
                AwWorReg = st.text_input("", placeholder="WORTH")
                AwAqDReg = st.text_input("", placeholder="ACQUISITION DATE")
                AwAqPReg = st.text_input("", placeholder="ACQUISITION PRICE")
                AwOwnReg = st.text_input("", placeholder="OWNER")
                AwStaReg = st.text_input("", placeholder="STATUS")
                AwBoardIdReg = st.text_input("", placeholder="BOARD ID")

                if st.form_submit_button("SUBMIT"):

                    valid_register = True

                    if AwTitleReg == '':
                        st.text("TITLE CAN NOT BE EMPTY")
                        valid_register = False

                    if valid_register:
                        if AwArtistReg == '':
                            st.text("ARTIST CAN NOT BE EMPTY")
                            valid_register = False
                    if valid_register:
                        if AwStyleReg == '':
                            st.text("STYLE CAN NOT BE EMPTY")
                            valid_register = False
                            
                    if valid_register:
                        if AwDescReg == '':
                            st.text("DESCRIPTION CAN NOT BE EMPTY")
                            valid_register = False

                    if valid_register:
                        if AwImgReg == '':
                            st.text("IMAGE URL CAN NOT BE EMPTY")
                            valid_register = False

                    if valid_register:
                        if AwOwnReg == '':
                            st.text("OWNER CAN NOT BE EMPTY")
                            valid_register = False
                    if valid_register:
                        if AwStaReg == '':
                            st.text("STATUS CAN NOT BE EMPTY")
                            valid_register = False
                    
                    if valid_register:
                        if AwBoardIdReg == '':
                            st.text("INTERNAL ID CAN NOT BE EMPTY")
                            valid_register = False

                    if valid_register:
                        AwAqPReg = float(AwAqPReg) if AwAqPReg else None
                        AwAqPReg = float(AwHeiReg) if AwHeiReg else None
                        AwWidReg = float(AwWidReg) if AwWidReg else None
                        AwWeiReg = float(AwWeiReg) if AwWeiReg else None
                        AwWorReg = float(AwWorReg) if AwWorReg else None
                        AwYearReg = int(AwYearReg) if AwYearReg else None
                       

                        print("bottao")
                        supabase.table('artwork').update([{'title': AwTitleReg, 'artist': AwArtistReg, 'style': AwStyleReg, 'medium': AwMediumReg, 'description': AwDescReg, 'img_url': AwImgReg, 'year_made': AwYearReg, 'height': AwHeiReg, 'width': AwWidReg, 'weight': AwWeiReg, 'worth': AwWorReg, 'acq_date': AwAqDReg, 'acq_price': AwAqPReg, 'owner': AwOwnReg, 'status': AwStaReg, 'board_id': AwBoardIdReg}]).eq('title', selected_pic).execute(); 

    with col3:
            response, count = supabase.table('artwork').select('*').eq('museum_m_id', museumId).execute()
            PicNamesList = ()
            for i in range (0, len(response[1])):
                PicNamesList += ((response[1][i]['title']),)
            print(PicNamesList)
            st.markdown(f'<div class = "manageTitles">DELETE AN ARTWORK</div>', unsafe_allow_html=True)
            delete_choice = st.selectbox("Select Artwork", PicNamesList, label_visibility="collapsed", key="deleteform")
            if st.button("DELETE"):
                st.write(delete_choice)
                response, count = supabase.table('artwork').select('*').eq('title', delete_choice).execute()
                print (response[1][0]['a_id'])
                supabase.table('history').delete().eq('artwork_a_id', response[1][0]['a_id']).execute()
                supabase.table('risk_analysis').delete().eq('artwork_a_id', response[1][0]['a_id']).execute()
                supabase.table('status').delete().eq('artwork_a_id', response[1][0]['a_id']).execute()
                supabase.table('artwork').delete().eq('a_id', response[1][0]['a_id']).execute()


        

        # artRegisterForm = st.form("ArtDeleteForm")
        # with artRegisterForm:
        #     response, count = supabase.table('artwork').select('*').eq('museum_m_id', museumId).execute()
        #     PicNamesTupple = ()
        #     for i in range (0, len(response) + 1):
        #         PicNamesTupple +=  str(response[1][i]['title'])
        #     st.markdown("REGISTER A NEW ARTWORK")
        #     st.selectbox("Select", PicNamesTupple)

    


def riskpage():
    supabase = init_connection()
    museumId = st.session_state.museumId
    artId = st.session_state.artId

    #st.markdown(str(museumId) + "-" + str(artId))

    if st.button("RETURN", key= "returnsmth"):
        turnMuseumPage(museumId)
        st.experimental_rerun()
    
    response, count = supabase.table('images').select('*').eq('id', random.randint(1, 3)).execute()

    response, count = supabase.table('museum').select('*').eq('m_id', museumId).execute()
    image_url = response[1][0]['image_url']
    urlBackground(image_url)
    #urlBackground(response[1][0]['url'])


    response, count = supabase.table('status').select('*').eq('artwork_a_id', artId).order('s_id', desc=True).limit(1).execute()
    
    
        
    hide_sidebar_style = """
    <style>
        #MainMenu { visibility: hidden; }
        .sidebar .sidebar-content { width: 0; }
    </style>
    """
    st.markdown(hide_sidebar_style, unsafe_allow_html=True)

    col1, col2, col3, col4, col5, col6= st.columns([1.5,0.1,1,0.8,1,1])

    with col1:
        get_img, count = supabase.table('artwork').select('img_url').eq('a_id', artId).execute()
        st.image(get_img[1][0]['img_url']) 

    if response[1] != []:
        
        with col3:

            light_value = response[1][0]['vibration'] 
            if light_value > 18000:
                light_level = "HIGH"
            elif light_value < 10000:
                light_level = "LOW"
            else:
                light_level ="NORMAL"

            smoke_value = response[1][0]['smoke'] 
            if smoke_value > 1200:
                smoke_level = "DETECTED"
            else:
                smoke_level ="NOT DETECTED"
                
            mov_value = response[1][0]['movement'] 
            if mov_value > 80:
                mov_level = "NOT DETECTED"
            else:
                mov_level ="DETECTED"

            markdown_text = (f"<strong>TEMPERATURE:</strong> {str(response[1][0]['temperature']) + 'ºC' if response[1][0]['temperature'] else 'No information'}<br>")
            st.markdown(f'<div class="descryptBoxArtwork">{markdown_text}</div>', unsafe_allow_html=True)
            st.markdown("")
            markdown_text = (f"<strong>HUMIDITY:</strong> {str(response[1][0]['humidity']) + '%' if response[1][0]['humidity'] else 'No information'}<br>")
            st.markdown(f'<div class="descryptBoxArtwork">{markdown_text}</div>', unsafe_allow_html=True)
            st.markdown("")
            markdown_text = (f"<strong>SMOKE:</strong> {smoke_level if response[1][0]['smoke'] else 'No information'}<br>")
            st.markdown(f'<div class="descryptBoxArtwork">{markdown_text}</div>', unsafe_allow_html=True)
            st.markdown("")
            markdown_text = (f"<strong>LIGHT:</strong> {light_level if response[1][0]['vibration'] else 'No information'}<br>")
            st.markdown(f'<div class="descryptBoxArtwork">{markdown_text}</div>', unsafe_allow_html=True)
            st.markdown("")
            markdown_text = (f"<strong>MOVEMENT:</strong> {mov_level if response[1][0]['movement'] else 'No information'}<br>")
            st.markdown(f'<div class="descryptBoxArtwork">{markdown_text}</div>', unsafe_allow_html=True)
            st.markdown("")
            if st.button("REFRESH", key="refreshERROR"):
                turnRiskPage(museumId, artId)
                st.experimental_rerun()
            if st.button("HISTORY", key="history"):
                turnHistoryPage(museumId, artId)
                st.experimental_rerun()

    else:
        with col3:
            st.markdown(f'<div class="emptyBoxDescrypt">THERE IS NO DATA AVAILABLE  </div>', unsafe_allow_html=True)
            st.markdown("")
            if st.button("REFRESH", key="refreshStatus"):
                turnRiskPage(museumId, artId)
                st.experimental_rerun()
    if response[1] != []:
        response, count = supabase.table('risk_analysis').select('*').eq('artwork_a_id', artId).execute()
        temp_risk = response[1][0]['temprisk']
        globalRisk = response[1][0]['riskreps']

    if response[1] != []:
        if globalRisk > 35 and temp_risk != 20:
            risk_analysis = 2  ## ALTERAR ISTO
            response, count = supabase.table('status').select('*').eq('artwork_a_id', artId).execute()
    
            temperature = response[1][0]['temperature']
            humidity = response[1][0]['humidity']
            light = response[1][0]['vibration']
            movement = response[1][0]['movement']
            smoke = response[1][0]['smoke']
            iso_timestamp = datetime.now().isoformat()
            supabase.table('history').insert([{'ev_date':iso_timestamp ,'temperature': temperature, 'humidity': humidity, 'smoke': smoke, 'light': light, 'movement': movement, 'globalrisk': 0, 'artwork_a_id': artId}]).execute()
    
        elif globalRisk < 25:
            risk_analysis = 0
    
    
        else:
            risk_analysis = 1

    with col5:
        if response[1] == []:
            st.markdown(f'<img src="https://media.tenor.com/cIV_T84be0sAAAAC/garfield-hungry.gif" alt="GIF">', unsafe_allow_html=True)
        else:
            if risk_analysis == 0:
                st.markdown(f'<img src="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExNTRhYzdmbXA0ZmI2ZzczeTlneHMxaDl3eDI1cGZ1dXNocmF6M2JjdSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/piO6cmvxIK0A05MNkY/giphy.gif" alt="GIF">', unsafe_allow_html=True)
            elif risk_analysis == 1:
                st.markdown(f'<img src="https://gifbin.com/bin/082010/1282645029_garfield-dont-deal-with-it.gif" alt="GIF">', unsafe_allow_html=True)
            else:
                st.markdown(f'<img src="https://media.tenor.com/Izi-CzQYQPgAAAAC/yaaahh-jon-arbuckle.gif" alt="GIF">', unsafe_allow_html=True)
        

    if response[1] != []:
    
        if risk_analysis == 0:
            st.markdown(f'<div class="descryptBoxRiskGREEN">RISK ANALYSIS</div>', unsafe_allow_html=True)
        elif risk_analysis == 1:
            st.markdown(f'<div class="descryptBoxRiskYELLOW">RISK ANALYSIS</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="descryptBoxRiskRED">RISK ANALYSIS</div>', unsafe_allow_html=True)
    return


def history():

    supabase = init_connection()
    museumId = st.session_state.museumId
    artId = st.session_state.artId
    if st.button("RETURN", key="returnERROR"):
        turnRiskPage(museumId, artId)
        st.experimental_rerun()
    response, count = supabase.table('museum').select('*').eq('m_id', museumId).execute()
    image_url = response[1][0]['image_url']
    urlBackground(image_url)
    
    #response, count = supabase.table('status').select('*').eq('artwork_a_id', artId).execute()
    

    response, count = supabase.table('history').select('*').eq('artwork_a_id', artId).order('ev_date', desc=True).execute()
    for i in range(0, len(response[1])):

        light_value = response[1][i]['light']
        if light_value > 18000:
            light_level = "HIGH"
        elif light_value < 10000:
            light_level = "LOW"
        else:
            light_level ="NORMAL"
    
        
        smoke_value = response[1][i]['smoke'] 
        if smoke_value > 1200:
            smoke_level = "DETECTED"
        else:
            smoke_level ="NOT DETECTED"
                    
        mov_value = response[1][i]['movement'] 
        if mov_value > 80:
            mov_level = "NOT DETECTED"
        else:
            mov_level ="DETECTED"
            
        timestamp_str = response[1][i]['ev_date']
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%f")
        formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")

       

        markdown_text = (f"<strong>DATE:</strong> {formatted_timestamp  if response[1][i]['ev_date'] else 'No information'} <strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;TEMPERATURE:</strong> {str(response[1][i]['temperature']) + 'ºC' if response[1][i]['temperature'] else 'No information'}<strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;HUMIDITY:</strong> {str(response[1][i]['humidity']) + '%' if response[1][i]['humidity'] else 'No information'}<strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;LIGHT:</strong> {light_level  if response[1][i]['light'] else 'No information'}<strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MOVEMENT:</strong> {mov_level  if response[1][i]['movement'] else 'No information'}<strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;SMOKE:</strong> {smoke_level if response[1][i]['smoke'] else 'No information'}<br>")
        st.markdown(f'<div class="descryptBoxArtwork">{markdown_text}</div>', unsafe_allow_html=True)
      
    return



def pages_setup():
    if 'page' not in st.session_state: 
        st.session_state.page = 0
    page_names_to_funcs = {
        0: landPage,
        1: registerPage,
        2: loginPage,
        3: riskpage,
        4: addPaint,
        5: history
    }

    page_names_to_funcs[st.session_state.page]()
    




def main():

    pages_setup()

    # try:
    #     new_user()
    #     del supabase
    # except Exception as e:
    #     print("An error occurred:", e.error)




if __name__ == "__main__":
    
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    main()

