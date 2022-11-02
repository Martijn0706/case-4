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

# Zoek op welke data beschikbaar is
metadata = pd.DataFrame(cbsodata.get_meta('83765NED', 'DataProperties'))


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


df.head()


# In[12]:


df2.head()


# In[13]:


# Maak een thematische kaart
p = df.plot(column='GemiddeldElektriciteitsverbruikTotaal_47', 
                         figsize = (10,8),
                        legend=True)
p.axis('off')
p.set_title('Gemiddeld Elektriciteitsverbruik')


# In[14]:


# Maak een thematische kaart
p1 = df2.plot(column='GemiddeldAardgasverbruikTotaal_55', 
                         figsize = (10,8),
                        legend=True)
p1.axis('off')
p1.set_title('Gemiddeld Aardgasverbruik')


# In[29]:


fig = px.histogram(df,x =['Appartement', 'Tussenwoning', 'Hoekwoning', 'TweeOnderEenKapWoning', 'VrijstaandeWoning'],
             title='Energieverbruik',
             labels = {'count':'Aantal huishoudens',
                       'value': 'kWh'},
            marginal="box",
                    width=1200, height=700)
                       
fig.show()


# In[16]:


fig = px.histogram(df, x =['Huurwoning', 'Koopwoning'],
             title='Energieverbruik',
             labels = {'variable': 'Soort',
                       'value': 'kWh'},
             marginal="box",
                   width=1200, height=700)

fig.show()


# In[17]:


fig = px.histogram(df2, x =['Huurwoning', 'Koopwoning'],
             title='Gasverbruik',
             labels = {'variable': 'Soort',
                       'value': 'm³'},
             marginal="box",
                   width=1200, height=700)

fig.show()


# In[18]:


fig = px.scatter(df2, x =['Huurwoning', 'Koopwoning'],
             title='Gasverbruik',
             labels = {'variable': 'Soort',
                       'index': 'Aantal',
                       'value': 'm³'},
             width=1200, height=700)

fig.show()


# In[19]:


fig = px.scatter(df, x =['Huurwoning', 'Koopwoning'],
             title='Energieverbruik',
             labels = {'variable': 'Soort',
                       'value': 'kWh',
                       'index': 'Aantal'},
                 width=1200, height=700)

fig.show()


# In[20]:


fig = px.scatter(df, x =['Appartement', 'Tussenwoning', 'Hoekwoning', 'TweeOnderEenKapWoning', 'VrijstaandeWoning'],
             title='Energieverbruik',
            labels = {'variable': 'Soort',
                       'value': 'kWh',
                       'index': 'Aantal'},
                 width=1200, height=700)
                       
fig.show()


# In[21]:


fig = px.scatter(df2, x =['Appartement', 'Tussenwoning', 'Hoekwoning', 'TweeOnderEenKapWoning', 'VrijstaandeWoning'],
             title='Gasverbruik',
            labels = {'variable': 'Soort',
                       'value': 'm³',
                       'index': 'Aantal'},
                 width=1200, height=700)
                       
fig.show()

