#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!pip install geopandas


# In[2]:


#!pip install cbsodata


# In[3]:


import pandas as pd
import geopandas as gpd
import cbsodata
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
from PIL import Image

# Zoek op welke data beschikbaar is
metadata = pd.DataFrame(cbsodata.get_meta('83765NED', 'DataProperties'))
image = Image.open('streamlit elek.jfif')
image2 = Image.open('streamlit gas.jfif')
image3 = Image.open('HVA-logo.jpg')
image4 = Image.open('gasverbruik_streamlit.jpg')

# In[4]:


# Download geboortecijfers en verwijder spaties uit regiocodes
data = pd.DataFrame(cbsodata.get_data('83765NED', select = ['WijkenEnBuurten', 
                                                            'Codering_3', 
                                                            'GemiddeldElektriciteitsverbruikTotaal_47', 
                                                            'Appartement_48', 
                                                            'Tussenwoning_49', 
                                                            'Hoekwoning_50', 
                                                            'TweeOnderEenKapWoning_51',
                                                            'VrijstaandeWoning_52',
                                                            'Huurwoning_53',
                                                            'EigenWoning_54',
                                                            'GemiddeldAardgasverbruikTotaal_55',
                                                            'Huurwoning_61',
                                                            'EigenWoning_62']))
data['Codering_3'] = data['Codering_3'].str.strip()


# In[5]:


data2 = pd.DataFrame(cbsodata.get_data('83765NED', select = ['WijkenEnBuurten', 
                                                            'Codering_3', 
                                                            'GemiddeldAardgasverbruikTotaal_55',
                                                            'Appartement_56',
                                                            'Tussenwoning_57',
                                                            'Hoekwoning_58',
                                                            'TweeOnderEenKapWoning_59',
                                                            'VrijstaandeWoning_60',
                                                            'Huurwoning_61',
                                                            'EigenWoning_62']))
data2['Codering_3'] = data2['Codering_3'].str.strip()


# In[6]:


# Haal de kaart met gemeentegrenzen op van PDOK
geodata_url = 'https://geodata.nationaalgeoregister.nl/cbsgebiedsindelingen/wfs?request=GetFeature&service=WFS&version=2.0.0&typeName=cbs_gemeente_2017_gegeneraliseerd&outputFormat=json'
df = gpd.read_file(geodata_url)
df2 = gpd.read_file(geodata_url)


# In[7]:


# Koppel CBS-data aan geodata met regiocodes
df = pd.merge(df, data,
                           left_on = "statcode", 
                           right_on = "Codering_3")


# In[8]:


df2 = pd.merge(df2, data2,
                           left_on = "statcode", 
                           right_on = "Codering_3")


# In[9]:


df.rename(columns = {"Appartement_48": "Appartement",
                    "Tussenwoning_49": "Tussenwoning",
                    'Hoekwoning_50': 'Hoekwoning',
                    'TweeOnderEenKapWoning_51': 'TweeOnderEenKapWoning',
                    'VrijstaandeWoning_52': 'VrijstaandeWoning',
                    'Huurwoning_53': 'Huurwoning',
                    'EigenWoning_54': 'Koopwoning'}, inplace = True)


# In[10]:


df2.rename(columns = {'Huurwoning_61': 'Huurwoning',
                      'EigenWoning_62': 'Koopwoning',
                      "Appartement_56": "Appartement",
                      "Tussenwoning_57": "Tussenwoning",
                      'Hoekwoning_58': 'Hoekwoning',
                      'TweeOnderEenKapWoning_59': 'TweeOnderEenKapWoning',
                      'VrijstaandeWoning_60': 'VrijstaandeWoning',}, inplace = True)
           
# In[11]:

fig1 = px.histogram(df, x =['Appartement', 'Tussenwoning', 'Hoekwoning', 'TweeOnderEenKapWoning', 'VrijstaandeWoning'],
             title='Energieverbruik',
             labels = {'count':'Aantal huishoudens',
                       'value': 'kWh'},
            marginal="box",
                   width=800, height=700)




# In[12]:

fig2 = px.histogram(df, x =['Huurwoning', 'Koopwoning'],
             title='Energieverbruik',
             labels = {'variable': 'Soort',
                       'value': 'kWh'},
             marginal="box",
                   width=800, height=700)


# In[13]:


fig3 = px.histogram(df2, x =['Huurwoning', 'Koopwoning'],
             marginal="box",
                   width=800, height=700)
fig3.update_layout(yaxis_title="Aantal Huishoudens",
                  xaxis_title="m³",
                  title='Gasverbruik')

# In[18]:
fig4 = px.histogram(df2, x =['Appartement', 'Tussenwoning', 'Hoekwoning', 'TweeOnderEenKapWoning', 'VrijstaandeWoning'],
             title='Gasverbruik',
             labels = {'variable': 'Soort',
                       'value': 'm³'},
             marginal="box",
                   width=800, height=700)

# In[19]:


fig5 = px.scatter(df2, x =['Huurwoning', 'Koopwoning'],
             width=800, height=700)
fig5.update_layout(yaxis_title="Aantal Huishoudens",
                  xaxis_title="m³",
                  title='Gasverbruik')



# In[20]:


fig6 = px.scatter(df, x =['Huurwoning', 'Koopwoning'],
                 width=800, height=700)
fig6.update_layout(yaxis_title="Aantal Huishoudens",
                  xaxis_title="kWh",
                  title='Energieverbruik')



# In[21]:


fig7 = px.scatter(df, x =['Appartement', 'Tussenwoning', 'Hoekwoning', 'TweeOnderEenKapWoning', 'VrijstaandeWoning'],
             title='Energieverbruik',
            labels = {'variable': 'Soort',
                       'value': 'kWh',
                       'index': 'Aantal'},
                 width=800, height=700)
                       


# In[22]:


fig8 = px.scatter(df2, x =['Appartement', 'Tussenwoning', 'Hoekwoning', 'TweeOnderEenKapWoning', 'VrijstaandeWoning'],
             title='Gasverbruik',
            labels = {'variable': 'Soort',
                       'value': 'm³',
                       'index': 'Aantal'},
                 width=800, height=700)
                       


# In[23]:
#Radioknoppen in de sidebar die navigatie over de pagina mogelijk maken. 
pages = st.sidebar.radio('paginas', options=['Home','Kaart elektriciteit en gas', 'Energieverbruik', 'Gasverbruik', 'Scatterplots', 'Einde'], label_visibility='hidden')

if pages == 'Home':
    st.title("Welkom op het dashboard van Thomas Basioni en Martijn de Rooij")
    st.image(image3)
    st.write('Onderwerp: gas- en energieverbruik bij koop- en huurwoningen en bij verschillende soorten woningen.')
elif pages == 'Kaart elektriciteit en gas':
    tab1, tab2 = st.tabs(["Elektriciteit", "Gas"])
    with tab1:
        st.image(image)
    with tab2:
        st.image(image2)
elif pages == 'Energieverbruik':
    tab3, tab4 = st.tabs(["Soort woning", "Huur of Koop"])
    with tab3:
        st.plotly_chart(fig1)
    with tab4:
        st.plotly_chart(fig2)
elif pages == 'Gasverbruik':
    tab5, tab6 = st.tabs(["Soort woning", "Huur of Koop"])
    with tab5:
        st.plotly_chart(fig4)
    with tab6:
        st.plotly_chart(fig3)
elif pages == 'Scatterplots':
    tab7, tab8, tab9, tab10 = st.tabs(["Gas soort woning", "Gas koop/huur", 'Energie soort woning', 'Energie koop/huur'])
    with tab7:
        st.plotly_chart(fig8)
    with tab8:
        st.plotly_chart(fig5)
    with tab9:
        st.plotly_chart(fig7)
    with tab10:
        st.plotly_chart(fig6)
elif pages == 'Einde':
    st.title('Bedankt voor het bekijken')
    st.image(image4)
    st.write('Conclusie: Appartementen zijn het meest energiezuinig, meestal zijn dit ook huurwoningen. Vrijstaande woning vraagt het meeste energie.')
    st.text('bron:https://opendata.cbs.nl/#/CBS/nl/') 

# In[21]:



# In[21]:



# In[21]:


# In[21]:


# In[21]:



# In[21]:

# In[21]:
