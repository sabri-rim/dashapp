# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 15:55:59 2021

@author: Rim Sabri
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from datetime import datetime
import plotly.express as px
import requests

import dash_bootstrap_components as dbc


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG])


# Loading data ############################################

## Données monde général
covid_monde_url = ("https://covid19.who.int/WHO-COVID-19-global-data.csv")
df_monde = pd.read_csv(covid_monde_url, sep=",")
df_monde['Date_reported'] = pd.to_datetime(df_monde['Date_reported'], format='%Y-%m-%d')

## Données vaccination dans le monde
covid_monde_vaccination_url = ("https://covid19.who.int/who-data/vaccination-data.csv")
df_monde_vacc = pd.read_csv(covid_monde_vaccination_url, sep=",")
df_monde_vacc['DATE_UPDATED'] = pd.to_datetime(df_monde_vacc['DATE_UPDATED'],format='%Y-%m-%d')

covid_url = ("https://www.data.gouv.fr/fr/datasets/r/900da9b0-8987-4ba7-b117-7aea0e53f530")
df = pd.read_csv(covid_url, sep=";")

## Données hospitalières françaises
covid_france_hosp_url = ("https://www.data.gouv.fr/fr/datasets/r/6fadff46-9efd-4c53-942a-54aca783c30c")
covid_france_hosp = pd.read_csv(covid_france_hosp_url, sep=";")
covid_france_hosp['date_hosp'] = pd.to_datetime(covid_france_hosp['jour'])

## Données générales françaises
covid_france_general_url = ("https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7")
covid_france_general = pd.read_csv(covid_france_general_url, sep=";")
covid_france_general['date_fr'] = pd.to_datetime(covid_france_general['jour'])
covid_france_general_tot = covid_france_general[covid_france_general.sexe == 0]

## Données de vaccination en France 
vaccination_fr_url =("https://www.data.gouv.fr/fr/datasets/r/b8d4eb4c-d0ae-4af6-bb23-0e39f70262bd")
vaccination_fr = pd.read_csv(vaccination_fr_url, sep=";")
vaccination_fr['date_vacc'] = pd.to_datetime(vaccination_fr['jour'])

## Données des graphiques de réanimation
# Graphique en fonction du temps, du sexe et du département

covid_france_rea_tps_sexe_url = (
        "https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7"
        )
covid_france_rea_tps_sexe = pd.read_csv(covid_france_rea_tps_sexe_url, sep=";")
covid_france_rea_tps_sexe['date']=pd.to_datetime(covid_france_rea_tps_sexe['jour'])

# Graphique en fonction de l'âge et de la région

covid_france_rea_age_url = (
        "https://www.data.gouv.fr/fr/datasets/r/08c18e08-6780-452d-9b8c-ae244ad529b3"
        )
covid_france_rea_age = pd.read_csv(covid_france_rea_age_url, sep=";")
covid_france_rea_age['date']=pd.to_datetime(covid_france_rea_age['jour'])

## Données des graphiques de vaccination 
#Graph en fonction du temps
covid_france_vaccination_url = (
        "https://www.data.gouv.fr/fr/datasets/r/900da9b0-8987-4ba7-b117-7aea0e53f530"
        )
covid_france_vaccination = pd.read_csv(covid_france_vaccination_url, sep=";")
covid_france_vaccination['date'] = pd.to_datetime(covid_france_vaccination['jour'])

##Données des graphiques des décès  
# Graphique en fonction du temps, du sexe et du département 
covid_france_dc_tps_sexe_url = (    
        "https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7"   
        )   
covid_france_dc_tps_sexe = pd.read_csv(covid_france_dc_tps_sexe_url, sep=";")   
covid_france_dc_tps_sexe['date']=pd.to_datetime(covid_france_dc_tps_sexe['jour'])   

# Graphique en fonction de la classe d'âge et de la région  
covid_france_dc_age_url = ( 
        "https://www.data.gouv.fr/fr/datasets/r/08c18e08-6780-452d-9b8c-ae244ad529b3"   
        )   
covid_france_dc_age = pd.read_csv(covid_france_dc_age_url, sep=";") 
covid_france_dc_age['date']=pd.to_datetime(covid_france_dc_age['jour'])

#Graph en fonction de la classe d'âge
covid_france_vacc_age_url = (
        "https://www.data.gouv.fr/fr/datasets/r/54dd5f8d-1e2e-4ccb-8fb8-eac68245befd"
        )
covid_france_vacc_age = pd.read_csv(covid_france_vacc_age_url, sep=";")
covid_france_vacc_age['clage_vacsi'] = covid_france_vacc_age['clage_vacsi'].astype(str)

#Graph en fonction de la région
covid_france_vacc_reg_url = (
        "https://www.data.gouv.fr/fr/datasets/r/735b0df8-51b4-4dd2-8a2d-8e46d77d60d8"
        )
covid_france_vacc_reg = pd.read_csv(covid_france_vacc_reg_url, sep=";")
covid_france_vacc_reg['reg'] = covid_france_vacc_reg['reg'].astype(str)

#données france: vaccins

sum_vaccination = df_monde_vacc['TOTAL_VACCINATIONS'].sum()

#df_fr= pd.DataFrame(data_fr, columns =data_fr_columns)


# styling the tabs

# styling the tabs
tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #a7b9cf',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #a7b9cf',
    'borderBottom': '1px solid #a7b9cf',
    'backgroundColor': '#2b4f80',
    'color': 'white',
    'padding': '6px'
}

# Creating the Cards
def create_card(title, content, date):
    card=[
        dbc.CardHeader([html.H6(title)]),
        dbc.CardBody(
            [   
                html.H4(content, className="card-title"),
                html.H6(date, className="card-text"),
            ]
        ),
        ]
    return(card)

#Données monde 
sum_cases_monde = df_monde['New_cases'].sum() 
sum_deaths = df_monde['New_deaths'].sum()
sum_vaccination = df_monde_vacc['TOTAL_VACCINATIONS'].sum()
date_recente = max(df_monde['Date_reported'])
covid_monde_last_day = df_monde[df_monde.Date_reported == date_recente]
sum_cases_last_day = covid_monde_last_day['New_cases'].sum()
sum_deaths_last_day = covid_monde_last_day['New_deaths'].sum()

date_recente_str = date_recente.strftime('%Y-%m-%d')
#Indicateurs du monde
card1=create_card("Nombre accumulé de cas      ", sum_cases_monde, date_recente_str)
card2=create_card("Nombre accumulé de décès    ", sum_deaths, date_recente_str)
card3=create_card("Nombre total de vaccinations", sum_vaccination,date_recente_str)
card4=create_card("Nombre total de nouveaux cas", sum_cases_last_day,date_recente_str)
card5=create_card("Nombre total de nouveaux décès", sum_deaths_last_day,date_recente_str)

cards = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(dbc.Card(card1, color="#85C1E9", inverse=True)),
                dbc.Col(dbc.Card(card2, color="#85C1E9", inverse=True)),
                dbc.Col(dbc.Card(card3, color="#85C1E9", inverse=True)),
                dbc.Col(dbc.Card(card4, color="#85C1E9", inverse=True)),
                dbc.Col(dbc.Card(card5, color="#85C1E9", inverse=True)),
            ],
            className="mb-2",
        ),
    ]
)

# Données France 

total_deces_hosp = covid_france_hosp['incid_dc'].sum()###
covid_france_general_total = covid_france_general[covid_france_general.jour == max(covid_france_general['jour'])]
total_deces_general = covid_france_general_total['dc'].sum()###
total_rea = covid_france_hosp['incid_rea'].sum()###
total_hosp = covid_france_hosp['incid_hosp'].sum()### 
dernier_jour_hosp = max(covid_france_hosp['date_hosp'])
dernier_jour_gen = max(covid_france_general['date_fr'])
covid_france_dernier_jour_hosp = covid_france_hosp[covid_france_hosp.date_hosp == dernier_jour_hosp]
nombre_deces_jour = covid_france_dernier_jour_hosp['incid_dc'].sum()
nombre_rea_jour = covid_france_dernier_jour_hosp['incid_rea'].sum()
nombre_hosp_jour = covid_france_dernier_jour_hosp['incid_hosp'].sum()

dernier_jour_hosp_str = dernier_jour_hosp.strftime('%Y-%m-%d')
dernier_jour_gen_str = dernier_jour_gen.strftime('%Y-%m-%d')

# Données réanimations 

bbd_homme = covid_france_general_total[covid_france_general_total.sexe == 1]
bbd_femme = covid_france_general_total[covid_france_general_total.sexe == 2]

rea_homme = bbd_homme['rea'].sum()
rea_femme = bbd_femme['rea'].sum()

# Données décès 

deces_homme = bbd_homme['dc'].sum()
deces_femme = bbd_femme['dc'].sum()

# Données vaccination 
tout_vaccin = vaccination_fr[vaccination_fr.vaccin == 0]
total_vaccination_fr = tout_vaccin['n_tot_dose2'].sum()

pfizer = vaccination_fr[vaccination_fr.vaccin == 1]
moderna = vaccination_fr[vaccination_fr.vaccin == 2]
astra = vaccination_fr[vaccination_fr.vaccin == 3]
janssen = vaccination_fr[vaccination_fr.vaccin == 4]

dose1_pfizer = pfizer['n_tot_dose1'].sum()
dose1_moderna = moderna['n_tot_dose1'].sum()
dose1_astra = astra['n_tot_dose1'].sum()
dose1_Janssen = janssen['n_tot_dose1'].sum()

dose2_pfizer = pfizer['n_tot_dose2'].sum()
dose2_moderna = moderna['n_tot_dose2'].sum()
dose2_astra = astra['n_tot_dose2'].sum()
dose2_Janssen = janssen['n_tot_dose2'].sum()

date_vacc = max(vaccination_fr['date_vacc'])
mise_a_jour_vacc = date_vacc.strftime('%Y-%m-%d')

# Indicateurs France

card_fr1=create_card("Nombre total de décès           ", total_deces_general,dernier_jour_hosp_str)
card_fr2=create_card("Nombre de réanimations          ", total_rea,dernier_jour_hosp_str)
card_fr3=create_card("Nombre des hospitalisations     ", total_hosp,dernier_jour_hosp_str)
card_fr4=create_card("Vaccinations complètes          ",total_vaccination_fr, mise_a_jour_vacc)

cards_fr = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(dbc.Card(card_fr1, color="#7D3C98", inverse=True)),
                dbc.Col(dbc.Card(card_fr2, color="#7D3C98", inverse=True)),
                dbc.Col(dbc.Card(card_fr3, color="#7D3C98", inverse=True)),
                dbc.Col(dbc.Card(card_fr4, color="#7D3C98", inverse=True))
            ],
            className="mb-2",
        ),
    ]
)


# Indicateurs réanimations

card_rea1=create_card("Nombre de réanimations au total", total_rea, dernier_jour_hosp_str)
card_rea2=create_card("Nombre de réanimations actuelles chez les hommes", rea_homme,dernier_jour_gen_str)
card_rea3=create_card("Nombre de réanimations actuelles chez les femmes", rea_femme,dernier_jour_gen_str)
card_rea4=create_card("Nombre de nouvelles réanimations", nombre_rea_jour,dernier_jour_hosp_str)

cards_rea = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(dbc.Card(card_rea1, color="#ffae19", inverse=True)),
                dbc.Col(dbc.Card(card_rea2, color="#ffae19", inverse=True)),
                dbc.Col(dbc.Card(card_rea3, color="#ffae19", inverse=True)),
                dbc.Col(dbc.Card(card_rea4, color="#ffae19", inverse=True)),

            ],
            className="mb-6",
        ),
    ]
)
# Indicateurs décès

card_dc1=create_card("Nombre de décès", total_deces_general,dernier_jour_hosp_str)
card_dc2=create_card("Nombre de décès chez les hommes en milieu hospitalier", deces_homme,dernier_jour_gen_str)
card_dc3=create_card("Nombre de décès chez les femmes en milieu hospitalier", deces_femme,dernier_jour_gen_str)
card_dc4=create_card("Nombre de décès du jour", nombre_deces_jour,dernier_jour_hosp_str)

cards_dc = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(dbc.Card(card_dc1, color="#B03A2E", inverse=True)),
                dbc.Col(dbc.Card(card_dc2, color="#B03A2E", inverse=True)),
                dbc.Col(dbc.Card(card_dc3, color="#B03A2E", inverse=True)),
                dbc.Col(dbc.Card(card_dc4, color="#B03A2E", inverse=True)),
            ],
            className="mb-2",
        ),
    ]
)

  
#Indicateurs vaccination

card_vacc1=create_card("Nombre de premières doses du vaccin pfizer", dose1_pfizer, mise_a_jour_vacc)
card_vacc2=create_card("Nombre de premières doses du vaccin moderna", dose1_moderna,mise_a_jour_vacc)
card_vacc3=create_card("Nombre de premières doses du vaccin AstraZeneca", dose1_astra,mise_a_jour_vacc)
card_vacc4=create_card("Nombre de premières doses du vaccin Janssen", dose1_Janssen,mise_a_jour_vacc)
card_vacc5=create_card("Nombre de secondes doses du vaccin pfizer", dose2_pfizer, mise_a_jour_vacc)
card_vacc6=create_card("Nombre de secondes doses du vaccin moderna", dose2_moderna,mise_a_jour_vacc)
card_vacc7=create_card("Nombre de secondes doses du vaccin AstraZeneca", dose2_astra,mise_a_jour_vacc)
card_vacc8=create_card("Nombre de secondes doses du vaccin Janssen", dose2_Janssen,mise_a_jour_vacc)

cards_vacc = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(dbc.Card(card_vacc1, color="#58D68D", inverse=True)),
                dbc.Col(dbc.Card(card_vacc2, color="#58D68D", inverse=True)),
                dbc.Col(dbc.Card(card_vacc3, color="#58D68D", inverse=True)),
                dbc.Col(dbc.Card(card_vacc4, color="#58D68D", inverse=True)),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Card(card_vacc5, color="#ABEBC6", inverse=True)),
                dbc.Col(dbc.Card(card_vacc6, color="#ABEBC6", inverse=True)),
                dbc.Col(dbc.Card(card_vacc7, color="#ABEBC6", inverse=True)),
                dbc.Col(dbc.Card(card_vacc8, color="#ABEBC6", inverse=True)),
            ],
            className="mb-2",
        ),
    ]
)

# Monde visualisations:

## New cases graphique:
monde_cases_time = df_monde[['Date_reported','New_cases']].groupby('Date_reported', as_index=False).sum()
def update_graph_monde(title):
    fig_time = px.line(monde_cases_time, x=monde_cases_time['Date_reported'], y=monde_cases_time['New_cases'], labels={"Date_reported":"Date","New_cases":"Nombre de nouveaux cas"}, title=title)
    fig_time.update_xaxes(rangeslider_visible=True)
    return fig_time
    
card_graph_world_time = dbc.Card(
    dcc.Graph(id='my-graph-world_time', figure=update_graph_monde("Evolution du nombre de nouvaux cas dans le monde")), body=True, color ='#000000',
    )
card_graph_world1 = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(card_graph_world_time),
            ],
            className='mb-6',
        ),
    ]
)

monde_cases = df_monde[['New_cases','WHO_region']].groupby('WHO_region', as_index=False).sum()
def update_graph_monde3(title):
    fig_time = px.bar(monde_cases, x=monde_cases['WHO_region'], y=monde_cases['New_cases'], color=monde_cases['WHO_region'],  labels={"WHO_region":"Region du monde","New_cases":"Nombre de nouveaux cas"},title=title)
    return fig_time
    
card_graph_world_time3 = dbc.Card(
    dcc.Graph(id='my-graph-world_time3', figure=update_graph_monde3("Nombre total de cas par région dans le monde")), body=True, color ='#f2ffff',
    )
card_graph_world3 = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(card_graph_world_time3),
            ],
            className='mb-6',
        ),
    ]
)

## New deaths graphics:
      
monde_deaths_time = df_monde[['Date_reported','New_deaths']].groupby('Date_reported', as_index=False).sum()
def update_graph_monde2(title):
    fig_time = px.line(monde_deaths_time, x=monde_deaths_time['Date_reported'], y=monde_deaths_time['New_deaths'],  labels={"Date_reported":"Date","New_Deaths":"Nombre de nouveaux décès"},title=title)
    fig_time.update_xaxes(rangeslider_visible=True)
    return fig_time
    
card_graph_world_time2 = dbc.Card(
    dcc.Graph(id='my-graph-world_time2', figure=update_graph_monde2("Evolution du nombre de décès dans le monde")), body=True, color ='#f2ffff',
    )
card_graph_world2 = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(card_graph_world_time2),
            ],
            className='mb-6',
        ),
    ]
)

monde_deaths = df_monde[['New_deaths','WHO_region']].groupby('WHO_region', as_index=False).sum()
def update_graph_monde5(title):
    fig_time = px.bar(monde_deaths, x=monde_deaths['WHO_region'], y=monde_deaths['New_deaths'], color=monde_deaths['WHO_region'],  labels={"WHO_region":"region du monde","New_deaths":"Nombre de nouveaux décès"}, title=title)
    return fig_time
    
card_graph_world_time5 = dbc.Card(
    dcc.Graph(id='my-graph-world_time5', figure=update_graph_monde5("Nombre total de décès par région dans le monde")), body=True, color ='#f2ffff',
    )
card_graph_world5 = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(card_graph_world_time5),
            ],
            className='mb-6',
        ),
    ]
)
  
# vaccination dans le monde:
# vaccination dans le monde:
        
def update_graph_monde4(title):
    fig_time = px.bar(df_monde_vacc, x='COUNTRY', y='TOTAL_VACCINATIONS', color='WHO_REGION',  labels={"COUNTRY":"Pays","TOTAL_VACCINATIONS":"Nombre total de personnes vaccinées"}, title=title)
    return fig_time
    
card_graph_world_time4 = dbc.Card(
    dcc.Graph(id='my-graph-world_time4', figure=update_graph_monde4("Population vaccinée dans le monde")), body=True, color ='#f2ffff',
    )

card_graph_world4 = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(card_graph_world_time4),
            ],
            className='mb-6',
        ),
    ]
)           

## Graphiques réanimations

# Graphique réanimation en fonction du temps
covid_france_dc_tot = covid_france_rea_tps_sexe[covid_france_rea_tps_sexe.sexe == 0]    
dernier_jour_rea_age = max(covid_france_rea_tps_sexe["date"])   
covid_france_dernier_jour_rea = covid_france_rea_tps_sexe[covid_france_rea_tps_sexe.date == dernier_jour_rea_age]
evol_rea = covid_france_rea_tps_sexe[['date','rea']].groupby('date', as_index=False).sum()

def update_graph_rea_tps(title):
    fig_tps = px.line(evol_rea, x=evol_rea['date'], y=evol_rea['rea'], title=title, labels={"date":"Date","rea":"Nombre de réanimations"})

    return fig_tps

card_graph_rea_tps = dbc.Card(
    dcc.Graph(id='my-graph-rea-tps', figure=update_graph_rea_tps("Evolution du nombre total de réanimations")), body=True, color ='#FDEBD0',
    )
card_graph_rea_tps1 = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(card_graph_rea_tps),
            ],
            className='mb-6',
        ),
    ]
)

####here
# Graphique réanimation en fonction du sexe
dernier_jour_rea = max(covid_france_rea_age["date"])
covid_france_dernier_jour_age_rea = covid_france_rea_age[covid_france_rea_age.date == dernier_jour_rea] 

age_rea = covid_france_dernier_jour_age_rea[['cl_age90','rea']].groupby('cl_age90', as_index=False).sum()
sexe_rea = covid_france_rea_tps_sexe[['sexe','rea']].groupby('sexe', as_index=False).sum()
sexe_rea['sexe_str'] = ["Les deux","Hommes","Femmes"]

def update_graph_rea_sexe(title):
    fig_sexe = px.bar(sexe_rea, x=sexe_rea['sexe_str'], y=sexe_rea['rea'], title=title, text=sexe_rea['rea'],labels={"sexe_str":"Sexe","rea":"Nombre de réanimations"})
    fig_sexe.update_traces(textposition='outside')
    return fig_sexe

card_graph_rea_sexe = dbc.Card(
    dcc.Graph(id='my-graph-rea-sexe', figure=update_graph_rea_sexe("Nombre total de réanimation en fonction du sexe")), body=True, color ='#FAD7A0',
    )
card_graph_rea_sexe1 = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(card_graph_rea_sexe)
            ],
            className='mb-6',
        ),
    ]
)

# Graphique réanimation en fonction de la région



## Graphique des décès  
# Graphique des décès en fonction du temps  
covid_france_dc_tot = covid_france_dc_tps_sexe[covid_france_dc_tps_sexe.sexe == 0]  
dernier_jour_dc1 = max(covid_france_dc_tps_sexe["date"])    
covid_france_dernier_jour_dc1 = covid_france_dc_tps_sexe[covid_france_dc_tps_sexe.date == dernier_jour_dc1] 

evol_dc = covid_france_dc_tot[['date','dc']].groupby('date', as_index=False).sum()  
def update_graph_dc_tps(title): 
    fig_tps_dc = px.line(evol_dc, x=evol_dc['date'], y=evol_dc['dc'], title=title, labels={"date":"Date","dc":"Nombre de décès"})   

    return fig_tps_dc   

card_graph_dc_tps = dbc.Card(   
    dcc.Graph(id='my-graph-dc-tps', figure=update_graph_dc_tps("Evolution du nombre total de décès")), body=True, color ='#EC7063', 
    )   
card_graph_dc_tps1 = html.Div(  
    [   
        dbc.Row(    
            [   
                dbc.Col(card_graph_dc_tps), 
            ],  
            className='mb-6',   
        ),  
    ]   
)   

# Graphique des décès en fonction du sexe   
sexe_dc = covid_france_dernier_jour_dc1[['sexe','dc']].groupby('sexe', as_index=False).sum()    
sexe_dc['sexe_str'] = ["Les deux","Hommes","Femmes"]    

def update_graph_dc_sexe(title):    
    fig_dc_sexe = px.bar(sexe_dc, x=sexe_dc['sexe_str'], y=sexe_dc['dc'], title=title, text=sexe_dc['dc'], labels={"sexe_str":"Sexe","dc":"Nombre de décès"})   
    fig_dc_sexe.update_traces(textposition='outside')   
    return fig_dc_sexe  

card_graph_dc_sexe = dbc.Card(  
    dcc.Graph(id='my-graph-dc-sexe', figure=update_graph_dc_sexe("Nombre total de décès en fonction du sexe")), body=True, color ='#E74C3C',
    )
card_graph_dc_sexe1 = html.Div( 
    [   
        dbc.Row(    
            [   
                dbc.Col(card_graph_dc_sexe) 
            ],  
            className='mb-6',   
        ),  
    ]   
)   

# Graphique des décès en fonction de la région  
dernier_jour_dc = max(covid_france_dc_age["date"])  
covid_france_dernier_jour_dc = covid_france_dc_age[covid_france_dc_age.date == dernier_jour_dc] 



#Graphiques vaccinations dose
evol = covid_france_vaccination[['date','n_dose1']].groupby('date', as_index=False).sum()

def update_graph_dose1(title):
    fig1 = px.line(evol, x=evol['date'], y=evol['n_dose1'], title=title,labels={"date":"Date","n_dose1":"Nombre de vaccinations Dose1"})

    return fig1

card_graph_dose = dbc.Card(
    dcc.Graph(id='my-graph-dose', figure=update_graph_dose1("Nombre quotidien de vaccinations par la 1ère dose")), body=True, color="#ABEBC6",
    )

evol2 = covid_france_vaccination[['date','n_dose2']].groupby('date', as_index=False).sum()

def update_graph_dose2(title):
    fig2 = px.line(evol2, x=evol2['date'], y=evol2['n_dose2'],title=title,labels={"date":"Date","n_dose2":"Nombre de vaccinations 2ème dose"})

    return fig2

card_graph_dose2 = dbc.Card(
    dcc.Graph(id='my-graph-dose2', figure=update_graph_dose2("Nombre quotidien de vaccinations par la 2ème dose")), body=True, color="#58D68D",
    )

card_graph_dose1 = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(card_graph_dose),
                dbc.Col(card_graph_dose2),
            ],
            className='mb-6',
        ),
    ]
)

#Graphique vaccinations doses cumulées

evol_cum = covid_france_vaccination[['date','n_cum_dose1']].groupby('date', as_index=False).sum()

def update_graph_dose_cum1(title):
    fig3 = px.line(evol_cum, x=evol_cum['date'], y=evol_cum['n_cum_dose1'], title=title, labels={"date":"Date","n_cum_dose1":"Nombre de vaccinations Dose1"})

    return fig3

card_graph_dose_cum1 = dbc.Card(
    dcc.Graph(id='my-graph-dose-cum-1', figure=update_graph_dose_cum1("Evolution du nombre de vaccinations par la dose 1")), body=True, color="#ABEBC6")

evol_cum2 = covid_france_vaccination[['date','n_cum_dose2']].groupby('date', as_index=False).sum()

def update_graph_dose_cum1(title):
    fig4 = px.line(evol_cum2, x=evol_cum2['date'], y=evol_cum2['n_cum_dose2'], title=title,labels={"date":"Date","n_cum_dose2":"Nombre de vaccinations Dose 2"})

    return fig4

card_graph_dose_cum2 = dbc.Card(
    dcc.Graph(id='my-graph-dose-cum-2', figure=update_graph_dose_cum1("Evolution du nombre de vaccinations par la 2ème dose")), body=True, color="#58D68D")    

card_graph_dose_cum = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(card_graph_dose_cum1),
                dbc.Col(card_graph_dose_cum2),
            ],
            className='mb-6',
        ),
    ]
)



all_dep = covid_france_general.dep.unique()
all_sexe = covid_france_general.sexe.unique()
all_reg = covid_france_dc_age.reg.unique()
all_pays = df_monde.Country.unique()



# Application Layout:
        
app.layout = html.Div([
    html.H1(children='Dashboard of Covid-19 data',
        style={
            'textAlign': 'center',
            'color': '#FFFFFF'
            }
        ),
    dcc.Tabs(id='tabs-world', value='world-data', children=[ 
        dcc.Tab(label='Monde', value='world-data', style=tab_style, selected_style=tab_selected_style,children=[
           
            dbc.Row([
                dbc.Col(html.Div([
                html.Br(),
                cards,
                html.Br(),
                html.Br()])),
                ],style={"margin":"auto"}),

            html.Div(id='tabs-content-inline'),
            
            html.H5(children='The WHO regions: AMRO: The Americas, EMRO: Eastern Mediterrane, EURO: Europe, AFRO: Africa, SEARO: South-East Asia',
        style={
            'textAlign': 'left',
            'color': '#FFFFFF'
            }
        ),   dbc.Row(dbc.Card(html.Div([
                dcc.Dropdown(
                    id="dropdown5",
                    options=[{"label": x, "value": x} for x in all_pays],
                    value=all_pays[0],
                    clearable=False,
             ),
                dcc.Graph(id="line-chart8"),
        ]), body=True, color="#AED6F1")),

            dbc.Row(dbc.Card(html.Div([
                dcc.Dropdown(
                    id="dropdown7",
                    options=[{"label": x, "value": x} for x in all_pays],
                    value=all_pays[0],
                    clearable=False,
             ),
                dcc.Graph(id="line-chart10"),
        ]), body=True, color="#AED6F1")),
            dbc.Row([
                dbc.Col(html.Div([
                html.Br(),
                card_graph_world1,
                html.Br(),
                html.Br()])),
                ],style={"margin":"auto"}),
            dbc.Row([
                dbc.Col(html.Div([
                html.Br(),
                card_graph_world3,
                html.Br(),
                html.Br()])),
                ],style={"margin":"auto"}),
            dbc.Row([
                dbc.Col(html.Div([
                html.Br(),
                card_graph_world2,
                html.Br(),
                html.Br()])),
                ],style={"margin":"auto"}),
            dbc.Row([
                dbc.Col(html.Div([
                html.Br(),
                card_graph_world5,
                html.Br(),
                html.Br()])),
                ],style={"margin":"auto"}),
            dbc.Row([
                dbc.Col(html.Div([
                html.Br(),
                card_graph_world4,
                html.Br(),
                html.Br()])),
                ],style={"margin":"auto"}),  
        ]),
        dcc.Tab(label='Données de la France', value='France-data', style=tab_style, selected_style=tab_selected_style,children=[
             dbc.Row([
                dbc.Col(html.Div([
                html.Br(),
                cards_fr,
                html.Br(),
                html.Br()])),
                ],style={"margin":"auto"}),
             dbc.Row(dbc.Card(html.Div([    
                dcc.Checklist(  
                    id="checklist4", 
                    value=all_dep[3:],  
                    labelStyle={"margin":"auto"}  
                ),  
                dcc.Graph(id="line-chart4"), 
            ]), body=True, color="#C39BD3")),
             dbc.Row(dbc.Card(html.Div([    
                dcc.Checklist(  
                    id="checklist", 
                    value=all_dep[3:],  
                    labelStyle={"margin":"auto"}  
                ),  
                dcc.Graph(id="line-chart"), 
            ]), body=True, color="#C39BD3")),   

             dbc.Row(dbc.Card(html.Div([    
                dcc.Checklist(  
                    id="checklist1",    
                    value=all_dep[3:],  
                    labelStyle={"margin":"auto"}  
                ),  
                dcc.Graph(id="line-chart1"),    
            ]),body=True, color="#AF7AC5")),    

             dbc.Row(dbc.Card(html.Div([    
                dcc.Dropdown(   
                    id="dropdown",  
                    options=[{"label":"Les deux","value":0}, {"label":"Hommes","value":1}, {"label":"Femmes","value":2}],   
                    value=0,    
                    clearable=False,    
             ), 
                dcc.Graph(id="line-chart2"),    
                dcc.Graph(id="line-chart3"),    
        ]), body=True, color="#9B59B6")),   

            dbc.Row(dbc.Card(html.Div([ 
        ]), body=True, color="#7D3C98")),
            ]),
        dcc.Tab(label='France: Réanimation', value='tab-1', style=tab_style, selected_style=tab_selected_style, children=[
             dbc.Row([
                dbc.Col(html.Div([
                html.Br(),
                cards_rea,
                html.Br(),
                html.Br()])),
                ],style={"margin":"auto"}),

             dbc.Row([
                dbc.Col(html.Div([
                html.Br(),
                card_graph_rea_tps1,
                html.Br(),
                html.Br()])),
                ],style={"margin":"auto"}),

             dbc.Row([
                dbc.Col(html.Div([
                html.Br(),
                card_graph_rea_sexe1,
                html.Br(),
                html.Br()])),
                ],style={"margin":"auto"}),
            ]),
        dcc.Tab(label='France: Décès', value='tab-2', style=tab_style, selected_style=tab_selected_style,children=[
             dbc.Row([
                dbc.Col(html.Div([
                html.Br(),
                cards_dc,
                html.Br(),
                html.Br()])),
                ],style={"margin":"auto"}),
            dbc.Row([   
                dbc.Col(html.Div([  
                html.Br(),  
                card_graph_dc_tps1, 
                html.Br(),  
                html.Br()])),   
                ],style={"margin":"auto"}), 

             dbc.Row([  
                dbc.Col(html.Div([  
                html.Br(),  
                card_graph_dc_sexe1,    
                html.Br(),  
                html.Br()])),   
                ],style={"margin":"auto"}),
            ]),
        dcc.Tab(label='France: Vaccination', value='tab-3', style=tab_style, selected_style=tab_selected_style,children=[
            dbc.Row([
                dbc.Col(html.Div([
                html.Br(),
                cards_vacc,
                html.Br(),
                html.Br()])),
                ],style={"margin":"auto"}),

            dbc.Row([
                dbc.Col(html.Div([
                html.Br(),
                card_graph_dose1,
                html.Br(),
                html.Br()])),
                ],style={"margin":"auto"}),  

             dbc.Row([
                dbc.Col(html.Div([
                html.Br(),
                card_graph_dose_cum,
                html.Br(),
                html.Br()])),
                ],style={"margin":"auto"}),

                    ]),
        ], style=tabs_styles),
    

])

###############################################Callbacks#####################################################################"

@app.callback(  
    Output("line-chart4", "figure"),     
    [Input("checklist4", "value")])  

def update_line_chart(continents):  
    mask = covid_france_general.dep.isin(continents)    
    fig = px.line(covid_france_general[mask],   
        x="jour", y="hosp", color='dep',title="Nombre d'hospitalisations en fonction du temps suivant les départements choisis",    
        labels={"jour":"Date", "hosp": "Nombre d'hospitalisations"})    
    return fig  
    
@app.callback(  
    Output("line-chart", "figure"),     
    [Input("checklist", "value")])  

def update_line_chart(continents):  
    mask = covid_france_general.dep.isin(continents)    
    fig = px.line(covid_france_general[mask],   
        x="jour", y="rea", color='dep',title="Nombre de réanimations en fonction du temps suivant les départements choisis",    
        labels={"jour":"Date", "rea": "Nombre de réanimations"})    
    return fig  

@app.callback(  
    Output("line-chart1", "figure"),    
    [Input("checklist1", "value")]) 

def update_line_chart(departements):    
    mask = covid_france_general.dep.isin(departements)  
    fig = px.line(covid_france_general[mask],   
        x="jour", y="dc", color='dep',title='Nombre de décès en fonction du temps suivant les départements choisis',    
        labels={"jour":"Date","dc":"Nombre de décès"})  
    return fig  

@app.callback(  
    Output("line-chart2", "figure"),    
    [Input("dropdown","value")])    
    
def update_bar_chart(sex):  
    mask = covid_france_general["sexe"] == sex  
    fig = px.line(covid_france_general[mask], x="jour", y="rea", title="Nombre de réanimations en fonction du temps suivant le sexe sélectionné",   
        labels={"jour":"Date", "rea":"Nombre de réanimations"}) 
    return fig  

@app.callback(  
    Output("line-chart3", "figure"),    
    [Input("dropdown","value")])    

def update_bar_chart2(sex): 
    mask = covid_france_general["sexe"] == sex  
    fig = px.line(covid_france_general[mask], x="jour", y="dc", title="Nombre de décès en fonction du temps suivant le sexe sélectionné",   
        labels={"jour":"Date","dc":"Nombre de décès"})  
    return fig  





@app.callback(  
    Output("line-chart8", "figure"),    
    [Input("dropdown5","value")])   
def update_bar_chart(pays): 
    mask = df_monde["Country"] == pays  
    fig = px.line(df_monde[mask], x="Date_reported", y="New_cases", title="Nombre de nouveaux cas au cours du temps dans le pays sélectionné",  
        labels={"Date_reported":"Date","New_cases":"Nombre de nouveaux cas"})    
    return fig  


@app.callback(  
    Output("line-chart10", "figure"),   
    [Input("dropdown7","value")])   
def update_bar_chart(pays): 
    mask = df_monde["Country"] == pays  
    fig = px.line(df_monde[mask], x="Date_reported", y="New_deaths", title="Nombre de nouveaux décès au cours du temps dans le pays sélectionné",   
        labels={"Date_reported":"Date","New_deaths":"Nombre de nouveaux décès"}) 
    return fig  




if __name__ == '__main__':
    app.run_server(debug=True,host='localhost',port=8080)