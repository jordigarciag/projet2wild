# bibliothèques
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# configuration de la page
st.set_page_config(
    page_title="Los Sanchos - Data Analyst",
    page_icon="📊",
    layout="wide"  # utilise toute la largeur de l'écran
)

# titre principal
st.title("Dashboard pour le directeur de cinéma")

# menu horizontal en haut
selected_tab = option_menu(
    menu_title=None,
    options=["Accueil", "Indicateurs", "Films français", "Films étrangers"],
    icons=["house", "graph-up", "flag", "globe"],
    orientation="horizontal"
)

# Création du layout avec colonnes
col1, col2 = st.columns([1, 4])  # Ratio 1:4 pour le menu latéral et le contenu principal

# menu latéral dans la première colonne
with col1:
    st.sidebar.title("Menu latéral")
    sidebar_choice = st.sidebar.radio(
        "Sélectionnez une option:",
        ["Option 1", "Option 2", "Option 3"]
    )

# contenu principal dans la deuxième colonne
with col2:
    if selected_tab == "Accueil":
        st.header("Bienvenue")
        st.write("Veuillez trouver dans cette application le résultat de nos recherches pour la création d'un cinéma dans la Creuse. Les indicateurs présentés vous aideront à prendre les meilleures décisions.")
        
    elif selected_tab == "Indicateurs":
        st.header("Vue d'ensemble des indicateurs")
        # Ici les graphiques
        






    elif selected_tab == "Films français":
        st.header("Films français les mieux notés par décennie")
        
        # Chargement des données
        link = "tmdb_full.csv"
        df = pd.read_csv(link, low_memory=False)
        
        # Filtrer les films français avec un minimum de votes
        df_fr = df[(df['original_language'] == 'fr') & (df['vote_count'] >= 1000)]
        
        # Ajouter la décennie
        df_fr['decade'] = (pd.to_datetime(df_fr['release_date']).dt.year // 10) * 10
        df_fr = df_fr[df_fr['decade'] >= 1960]
        
        # Création de la figure
        fig, ax = plt.subplots(figsize=(15, 8))
        
        # Recherche du meilleur film de chaque décennie
        top_by_decade = df_fr.groupby('decade').apply(
            lambda x: x.nlargest(1, 'vote_average')).reset_index(drop=True)
        
        # Création du graphique à barres horizontales
        bars = ax.barh(
            top_by_decade['decade'].astype(str) + 's',
            top_by_decade['vote_average']
        )
        
        # Titre et étiquettes
        ax.set_title('Films français les mieux notés par décennie')
        ax.set_xlabel('Note moyenne')
        
        # Ajout des titres et notes
        for bar, original_title, note, vote_count in zip(bars,
            top_by_decade['original_title'],
            top_by_decade['vote_average'],
            top_by_decade['vote_count']):
            width = bar.get_width()
            
            # Titre original du film dans la barre avec nombre de votes
            ax.text(
                width/2,
                bar.get_y() + bar.get_height()/2,
                f'{original_title} ({vote_count} votes)',
                va='center', ha='center',
                color='white',
                fontsize=12,
                weight='bold'
            )
            # Note après la barre
            ax.text(
                width + 0.1,
                bar.get_y() + bar.get_height()/2,
                f'{note:.1f}',
                va='center',
                fontsize=12
            )
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Afficher les détails
        st.subheader("Détails")
        for _, film in top_by_decade.iterrows():
            st.write(f"\nDécennie: {film['decade']}s")
            st.write(f"Titre original: {film['original_title']} ({film['vote_count']} votes)")
            st.write(f"Note: {film['vote_average']:.1f}/10")
            st.write("---")





        

    elif selected_tab == "Films étrangers":
        st.header("Répartition des films par pays et par nombre de votes")
        
        # Chargement des données
        link = "tmdb_full.csv"
        df = pd.read_csv(link, low_memory=False)
        
        # Préparation des données
        df['decade'] = (pd.to_datetime(df['release_date']).dt.year // 10) * 10
        
        # Créer deux DataFrames selon le nombre de votes
        df_1000_10000 = df[(df['vote_count'] >= 1000) & (df['vote_count'] < 10000)]
        df_10000plus = df[df['vote_count'] >= 10000]
        
        # On ne garde que les films à partir de 1960 pour les deux groupes
        df_1000_10000 = df_1000_10000[df_1000_10000['decade'] >= 1960]
        df_10000plus = df_10000plus[df_10000plus['decade'] >= 1960]
        
        # Pour chaque décennie et groupe, trouver le film le mieux noté
        top_by_decade_1000 = df_1000_10000.groupby('decade').apply(
            lambda x: x.nlargest(1, 'vote_average')).reset_index(drop=True).sort_values('decade')
        
        top_by_decade_10000 = df_10000plus.groupby('decade').apply(
            lambda x: x.nlargest(1, 'vote_average')).reset_index(drop=True).sort_values('decade')
        
        # Création de la visualisation
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Premier camembert (à gauche) - Films avec 1000-10000 votes
        countries_1000 = top_by_decade_1000['production_countries'].value_counts()
        ax1.pie(countries_1000.values, labels=countries_1000.index, autopct='%1.1f%%')
        ax1.set_title('Répartition par pays (1000-10000 votes)')
        
        # Deuxième camembert (à droite) - Films avec plus de 10000 votes
        countries_10000 = top_by_decade_10000['production_countries'].value_counts()
        ax2.pie(countries_10000.values, labels=countries_10000.index, autopct='%1.1f%%')
        ax2.set_title('Répartition par pays (>10000 votes)')
        
        plt.tight_layout()
        st.pyplot(fig)
        
        
        
        
        
        
        st.subheader("Meilleurs films par décennie selon le nombre de votes")
        
        # Importation des bibliothèques nécessaires
        import matplotlib.pyplot as plt  # Pour créer des graphiques
        import pandas as pd  # Pour manipuler les données

        # Définition d'une fonction qui catégorise les films selon leur nombre de votes
        def get_vote_group(votes):
            if votes < 10000:
                return "Moyennement votés (1000-10000)"  # Films entre 1000 et 10000 votes
            else:
                return "Très votés (>10000)"  # Films avec plus de 10000 votes

        # Préparation des données
        df = df[df['vote_count'] >= 1000]  # On ne garde que les films avec au moins 1000 votes
        df['vote_group'] = df['vote_count'].apply(get_vote_group)  # Ajout de la catégorie de votes
        df['decade'] = (pd.to_datetime(df['release_date']).dt.year // 10) * 10  # Calcul de la décennie

        # On ne garde que les films à partir de 1960
        df = df[df['decade'] >= 1960]

        # Définition des groupes de votes dans l'ordre décroissant
        vote_groups = ["Très votés (>10000)", "Moyennement votés (1000-10000)"]

        # Création de la figure avec 2 sous-graphiques (un pour chaque groupe)
        fig, axes = plt.subplots(len(vote_groups), 1, figsize=(15, 15))

        # Boucle sur chaque groupe de votes
        for idx, group in enumerate(vote_groups):
            # Filtrage des données pour le groupe actuel
            group_data = df[df['vote_group'] == group]
            
            # Recherche du meilleur film de chaque décennie pour ce groupe
            top_by_decade = group_data.groupby('decade').apply(
                lambda x: x.nlargest(1, 'vote_average')).reset_index(drop=True)
            
            # Création du graphique à barres horizontales
            bars = axes[idx].barh(
                top_by_decade['decade'].astype(int).astype(str) + 's',  # Étiquettes des décennies
                top_by_decade['vote_average']  # Valeurs des notes moyennes
            )
            
            # Ajout du titre et de l'étiquette de l'axe x
            axes[idx].set_title(f'Films les mieux notés par décennie - {group}')
            axes[idx].set_xlabel('Note moyenne')
            
            # Ajout des titres des films à l'intérieur des barres et des notes à l'extérieur
            for bar, title, note, vote_count in zip(bars, top_by_decade['title'], 
                                                top_by_decade['vote_average'], 
                                                top_by_decade['vote_count']):
                width = bar.get_width()
                # Titre du film à l'intérieur de la barre
                axes[idx].text(
                    width/2,  # Position x (milieu de la barre)
                    bar.get_y() + bar.get_height()/2,  # Position y (milieu de la barre)
                    f'{title} ({vote_count} votes)',  # Texte à afficher (titre et nombre de votes)
                    va='center', ha='center',  # Alignement vertical et horizontal
                    color='white',  # Couleur du texte en blanc
                    fontsize=12,  # Taille de police plus grande
                    weight='bold'  # Ajout du style gras
                )
                # Note à l'extérieur de la barre
                axes[idx].text(
                    width + 0.1,  # Position x (juste après la barre)
                    bar.get_y() + bar.get_height()/2,  # Position y (milieu de la barre)
                    f'{note:.1f}',  # Note avec une décimale
                    va='center',  # Alignement vertical
                    fontsize=12  # Taille de police plus grande
                )

        plt.tight_layout()
        st.pyplot(fig)

        # Afficher les détails
        st.subheader("Détails")
        for group in vote_groups:
            st.write(f"\n**{group}**")
            group_data = df[df['vote_group'] == group]
            top_by_decade = group_data.groupby('decade').apply(
                lambda x: x.nlargest(1, 'vote_average')).reset_index(drop=True)
            
            for _, film in top_by_decade.iterrows():
                st.write(f"\nDécennie: {film['decade']}s")
                st.write(f"Titre: {film['title']} ({film['vote_count']} votes)")
                st.write(f"Note: {film['vote_average']:.1f}/10")
                st.write("---")
        