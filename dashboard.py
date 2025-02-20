import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Titre et description de l'application
st.title("Tableau de Bord d'Entretien Courant de l'Autoroute")
st.markdown("""
Ce tableau de bord vous permet de visualiser les données relatives aux interventions d'entretien courant de l'autoroute.  
Les données doivent inclure les champs suivants :
- **date**
- **type d’intervention**
- **localisation**
- **équipe**
- **durée**
- **coût**
- **observations**

Vous pouvez importer vos données via un fichier CSV ou Excel.
""")

# Upload de fichier : CSV ou Excel
uploaded_file = st.file_uploader("Téléchargez votre fichier CSV ou Excel", type=['csv', 'xlsx'])

if uploaded_file is not None:
    try:
        # Lecture du fichier en fonction de son extension
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, parse_dates=['date'])
        else:
            df = pd.read_excel(uploaded_file, parse_dates=['date'])
        st.success("Fichier chargé avec succès!")

        # On exécute le reste du code seulement si df est bien défini
        if 'df' in locals():
            # Affichage d'un aperçu des données
            st.subheader("Aperçu des données")
            st.dataframe(df.head())

            # ---------------- Indicateurs Clés ----------------
            st.header("Indicateurs Clés")
            total_interventions = len(df)
            avg_duration = df['durée'].mean() if 'durée' in df.columns else 0
            total_cost = df['coût'].sum() if 'coût' in df.columns else 0

            col1, col2, col3 = st.columns(3)
            col1.metric("Nombre total d'interventions", total_interventions)
            col2.metric("Durée moyenne", f"{avg_duration:.2f} (unité de temps)")
            col3.metric("Coût total", f"{total_cost:.2f} €")

            # ---------------- Histogramme : Interventions par type ----------------
            st.header("Histogramme : Interventions par type")
            fig1, ax1 = plt.subplots(figsize=(10, 6))
            sns.countplot(x='type d’intervention', data=df, ax=ax1, palette="viridis")
            ax1.set_title("Nombre d'interventions par type")
            ax1.set_xlabel("Type d'intervention")
            ax1.set_ylabel("Nombre d'interventions")
            plt.xticks(rotation=45)
            st.pyplot(fig1)

            # ---------------- Courbe temporelle : Interventions quotidiennes ----------------
            st.header("Courbe : Interventions dans le temps")
            df_time = df.groupby('date').size().reset_index(name='nombre')
            fig2 = px.line(df_time, x='date', y='nombre', title='Évolution quotidienne des interventions', markers=True)
            st.plotly_chart(fig2)

            # ---------------- Camembert : Répartition par équipe ----------------
            st.header("Camembert : Répartition des interventions par équipe")
            df_team = df['équipe'].value_counts().reset_index()
            df_team.columns = ['équipe', 'nombre']
            fig3 = px.pie(df_team, values='nombre', names='équipe', title='Répartition des interventions par équipe')
            st.plotly_chart(fig3)

            # ---------------- Coût total par jour ----------------
            st.header("Courbe : Coût total par jour")
            df_cost = df.groupby('date')['coût'].sum().reset_index()
            fig4 = px.bar(df_cost, x='date', y='coût', title='Coût total des interventions par jour')
            st.plotly_chart(fig4)

            # Optionnel : Affichage complet des données avec possibilité de filtrer
            st.header("Données détaillées")
            st.dataframe(df)
    except Exception as e:
        st.error("Erreur lors du chargement ou du traitement du fichier : " + str(e))
else:
    st.info("Veuillez télécharger un fichier CSV ou Excel pour afficher le tableau de bord.")

