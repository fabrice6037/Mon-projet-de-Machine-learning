
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import fanalysis.mca as MCA
import numpy as np 
import streamlit as st
import plotly.express as px
from ast import literal_eval
import os
import warnings
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
import joblib
from sklearn.metrics import r2_score
from warnings import filterwarnings
filterwarnings('ignore')
#from streamlit_extras.metric_cards import style_metric_cards
data_credit=pd.read_csv("C:/Fabrice_LPAS/fichier/S2/FORMATIONS/Video/formations python et django/credit.csv",sep=";")

#discretisation de la variable age
#definition des limites du groupe d'age
#age_bins=["19","29","39","49","59","100"]

#definir les labels
#age_labels=["20-29","30-39","40-49","50-59","60+"]
#creation d'une nouvelle colonne age_groupe en utilisant la foncion cut()
#data_credit["group_age"]=pd.cut(data_credit["Age"],bins=age_bins,labels=age_labels,right=False)

#creation d'un vecteur variables pour contenir le nom des variables
variables=[]
for i in data_credit.head(0):
    variables.append(i)

#suppression de la variable age
for i in variables:
    if i=="Age":
        variables.remove(i)
#variables.remove("Age")

    #acm
selection=['Marche','Impaye','Assurance','Endettement','Profession','Intitule']
x=data_credit[selection].values
my_mca=MCA.MCA(row_labels=data_credit.index.values,var_labels=selection)
variable_categoriel=data_credit.select_dtypes(include="object").columns.to_list()
variable_numerique=data_credit.select_dtypes(exclude="object").columns.to_list()



#my_mca.mapping(1,2, figsize=(10, 8))

#st.dataframe(data_credit.head())
st.sidebar.title("sommaire")
###st.sidebar.radio("aller sur la page")
pages=["contexte du projet","analyse des données","faire l'acm","modelisation"]
page=st.sidebar.radio("aller vers la page", pages)

if page==pages[0]:
    st.title("Contenu du projet")
    st.write("Ce projet nous permet de faire du machine learning")
    st.write("Il fournit des information sur l'analyse exploratoire")
    st.write("Analyse descriptive")
    st.write("Analyse de correspondance multiple")
    st.date_input(label="Date du jour",value="today")
    st.image("C:/Users/ISSP/Pictures/Nouveau dossier/télécharger.jpg")

elif page==pages[1]:
    if st.checkbox("analyse exploratoire des données"):
        st.dataframe(data_credit.head())
    elif st.checkbox("Dimmension du dataframe"):
        st.write(data_credit.shape)
    elif st.checkbox("Les données manquantes"):
       st.dataframe(data_credit.isnull().sum())
       
    elif st.checkbox("analyse descriptives"):
        st.dataframe(data_credit[variable_numerique].describe(include="all"))
elif page==pages[2]:
    if st.checkbox("afficher les valeurs normalisée"):
        st.write(my_mca.fit(x))
    elif st.checkbox("afficher les coordonnées"):
        st.write(my_mca.row_topandas())
elif page==pages[3]:
    if st.checkbox("diagramme en bar niveau1") :
        nbins=st.number_input("saisir l'amplitude des bars de l'histogramme: ",max_value=8,min_value=2)
        var_choix_cat=st.selectbox("choisir la variable categoriel",variable_categoriel)
        var_choix_num=st.selectbox("choisir la variable numerique",variable_numerique)
        fig=sns.displot(data_credit[var_choix_num],kde=True,bins=nbins)
        fig2=sns.countplot(x = var_choix_num, hue = var_choix_cat, data = data_credit)
        graph_titre=st.text_input(label="Donner un titre a votre graphique")
        plt.title(graph_titre)
        st.pyplot(fig)
        st.pyplot(fig2)
    elif st.checkbox("diagramme en bar niveau2"):
        if st.checkbox("diagramme en bar"):
            for col in variable_categoriel:
                proportions=data_credit[col].value_counts(normalize=True)*100
                st.plotly_chart(px.bar(data_frame=data_credit,x=proportions.index,y=proportions.values,title=f"Diagrammes en bar pour la variable {col} (proportions)"))
        if st.checkbox("diagramme circulaire"):
            for col in variables:
                 proportions=data_credit[col].value_counts()
                 st.plotly_chart(px.pie(data_frame=data_credit,values=proportions,title=f"Diagrammes camembert pour la variable {col} (proportions)")) 
    with st.sidebar:
        selected_marche = st.multiselect(label = "trier par Marche",options = data_credit["Marche"].unique().tolist(),default = data_credit["Marche"].unique())
        selected_appart = st.multiselect(label = "trier par Apport",options = data_credit["Apport"].unique().tolist(),default = data_credit["Apport"].unique())
        selected_impaye = st.multiselect(label ="trier par Impaye",options = data_credit["Impaye"].unique().tolist(),default = data_credit["Impaye"].unique())
        selected_assurance = st.multiselect(label = "trier par Assurance",options = data_credit["Assurance"].unique().tolist(),default = data_credit["Assurance"].unique())
    
    # Filtrage des données
        filtered_data = data_credit.copy()

        if selected_marche:
            filtered_data = filtered_data[filtered_data["Marche"].isin(selected_marche)]

        if selected_appart:
            filtered_data = filtered_data[filtered_data['Apport'].isin(selected_appart)]

        if selected_impaye:
            filtered_data = filtered_data[filtered_data['Impaye'].isin(selected_impaye)]

        if selected_assurance and "Tous" not in selected_assurance:
            filtered_data = filtered_data[filtered_data['Assurance'].isin(selected_assurance)]


        