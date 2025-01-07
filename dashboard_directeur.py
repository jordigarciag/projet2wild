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
    layout="wide")

# titre principal
st.title("📊 Tableau de bord analytique - Indicateurs clés de performance pour la direction du cinéma 🎥")

# menu horizontal en haut
selected_tab = option_menu(
    menu_title=None,
    options=["Accueil", "Quantité", "Budget", "Durée", "Acteurs", "Votes"],
    icons=["house", "bar-chart", "graph-up", "clock", "people", "graph-up-arrow"],
    orientation="horizontal")

# Création du layout avec colonnes
col1, col2 = st.columns([1, 4])  # Ratio 1:4 pour le menu latéral et le contenu principal

# menu latéral dans la première colonne
with col1:
    st.sidebar.title("Filtrer par décennie")
    decades = ["Toutes les décennies"] + [f"{d}s" for d in range(1960, 2030, 10)]
    selected_decade = st.sidebar.radio(
        "Sélectionnez une décennie:",
        decades
    )

# Fonction pour filtrer les données par décennie
def filter_by_decade(df, selected_decade):
    if selected_decade == "Toutes les décennies":
        return df
    else:
        decade = int(selected_decade[:-1])  # Enlève le 's' et convertit en int
        return df[df['decade'] == decade]

# contenu principal dans la deuxième colonne
with col2:
    if selected_tab == "Accueil":
        st.header("Chère équipe de direction")
        st.write("🎬 Bienvenue dans notre tableau de bord analytique dédié à l'analyse des tendances cinématographiques pour votre nouveau cinéma dans la Creuse. ")
        st.write("📈 Notre équipe a minutieusement analysé les données des films des dernières décennies pour vous aider à sélectionner une programmation attractive et pertinente pour votre public.")
        
    elif selected_tab == "Quantité":
        st.header("Nombre de films par décennie")
        
        # Chargement des données
        url = "https://raw.githubusercontent.com/florianhoarau/streamlit_imdb/main/tconst.tsv.gz"
        df = pd.read_csv(url, sep='\t')
        
        # Préparation des données
        df['decade'] = (pd.to_datetime(df['year'].astype(str), format='%Y').dt.year // 10) * 10
        df_actor_decade = df.groupby('decade').size().reset_index(name='nb_films')
        df_actor_decade = df_actor_decade.set_index('decade')
        
        # Filtrer les données selon la décennie sélectionnée
        if selected_decade != "Toutes les décennies":
            decade = int(selected_decade[:-1])
            df_actor_decade = df_actor_decade[df_actor_decade.index == decade]
        
        # Création du graphique
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x=df_actor_decade.index.astype(str), y=df_actor_decade['nb_films'], palette="crest", ax=ax)
        
        # Ajouter les valeurs sur les barres
        for p in ax.patches:
            ax.annotate(
                format(p.get_height(), '.0f'),
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center',
                xytext=(0, 8),
                textcoords='offset points',
                fontsize=10
            )
        
        # Personnalisation du graphique
        plt.title("Nombre de films par décennie", fontsize=16)
        plt.xlabel("Année", fontsize=14)
        plt.ylabel("Nombre de films", fontsize=14)
        
        # Ajuster les marges
        plt.tight_layout()
        
        # Afficher le graphique dans Streamlit
        st.pyplot(fig)

    elif selected_tab == "Budget":
        st.header("Répartition des budgets de 1950 à 2024")
        
        # Message de construction avec animation
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("![Construction](https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif)")
        with col2:
            st.markdown("### Section en construction 🏗️ ")
            st.write("Cette section est en cours de développement. Revenez bientôt !")

    elif selected_tab == "Durée":
        st.header("Répartition de la durée des films 1950 à 2024")
        
        # Message de construction avec animation
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("![Construction](https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif)")
        with col2:
            st.markdown("### Section en construction 🏗️ ")
            st.write("Cette section est en cours de développement. Revenez bientôt !")

    elif selected_tab == "Acteurs":
        # Sous-menu pour les acteurs
        acteurs_submenu = st.radio(
            "Sélectionnez une catégorie",
            ["Âge moyen des acteurs", "Acteurs les plus présents"]
        )
        
        if acteurs_submenu == "Âge moyen des acteurs":
            st.header("Âge moyen des acteurs par décennie")
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown("![Construction](https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif)")
            with col2:
                st.markdown("### Section en construction 🏗️ ")
                st.write("Cette section est en cours de développement. Revenez bientôt !")
        
# ------

        elif acteurs_submenu == "Acteurs les plus présents":
            st.header("Top 10 des acteurs les plus présents")
            
            # Chargement des données
            url = "https://raw.githubusercontent.com/florianhoarau/streamlit_imdb/main/nconst.tsv.gz"
            df = pd.read_csv(url, sep='\t', low_memory=False, na_values=['\\N'])
            
            url2 = "https://raw.githubusercontent.com/florianhoarau/streamlit_imdb/main/tconst.tsv.gz"
            df2 = pd.read_csv(url2, sep='\t', low_memory=False, na_values=['\\N'])
            
            # Préparation des données
            df2['decade'] = df2['year'].apply(lambda x: int((x // 10) * 10))
            
            # Traitement des acteurs
            acteur = df2['actor'].dropna().apply(lambda x: x.replace("'","").replace("[","").replace("]","").split(",")).apply(lambda x: list(filter(None, [ele.strip() for ele in x])))
            
            # Créer un DataFrame avec les acteurs et leurs décennies
            actor_decades = []
            for idx, row in df2.iterrows():
                if pd.notna(row['actor']):
                    actors = row['actor'].replace("'","").replace("[","").replace("]","").split(",")
                    actors = [a.strip() for a in actors if a.strip()]
                    for actor in actors:
                        actor_decades.append({'actor': actor, 'decade': row['decade']})
            
            actor_decades_df = pd.DataFrame(actor_decades)
            
            # Filtrer par décennie si nécessaire
            if selected_decade != "Toutes les décennies":
                decade = int(selected_decade[:-1])
                actor_decades_df = actor_decades_df[actor_decades_df['decade'] == decade]
            
            # Compter les apparitions des acteurs pour la décennie sélectionnée
            df_top_actor = pd.DataFrame(actor_decades_df['actor'].value_counts().head(10))
            df_top_actor.reset_index(inplace=True)
            df_top_actor.columns = ['nconst', 'nb_films']
            
            # Joindre avec les informations des acteurs
            df_actor_film = pd.merge(
                left=df,
                right=df_top_actor,
                how='inner',
                left_on='nconst',
                right_on='nconst'
            )
            
            # Trier les données par nombre de films (décroissant)
            df_actor_film = df_actor_film.sort_values(by='nb_films', ascending=False)
            
            # Création du graphique
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Créer un graphique à barres horizontales avec les données triées
            sns.barplot(
                y=df_actor_film['primaryName'],
                x=df_actor_film['nb_films'],
                palette="viridis",
                ax=ax,
                order=df_actor_film['primaryName']  # Utiliser l'ordre trié
            )
            
            # Ajouter les valeurs sur les barres
            for p in ax.patches:
                ax.annotate(
                    format(p.get_width(), '.0f'),
                    (p.get_width(), p.get_y() + p.get_height() / 2),
                    ha='left', va='center',
                    xytext=(5, 0),
                    textcoords='offset points',
                    fontsize=10
                )
            
            # Personnalisation du graphique
            decade_text = "toutes décennies confondues" if selected_decade == "Toutes les décennies" else f"dans les années {selected_decade}"
            plt.title(f"Top 10 des acteurs les plus présents {decade_text}", fontsize=16)
            plt.xlabel("Nombre de films", fontsize=14)
            plt.ylabel("Acteurs", fontsize=14)
            
            # Ajuster les marges
            plt.tight_layout()
            
            # Afficher le graphique
            st.pyplot(fig)
            
            # Afficher les détails (triés par nombre de films décroissant)
            st.subheader(f"Détails des acteurs {decade_text}")
            for _, acteur in df_actor_film.iterrows():
                st.write(f"**{acteur['primaryName']}** : {int(acteur['nb_films'])} films")
                st.write("---")

# -----        

    elif selected_tab == "Votes":
        # Sous-menu pour l'origine
        origine_submenu = st.radio(
            "Sélectionnez une catégorie",
            ["Films français", "Films étrangers"]
        )
        
        if origine_submenu == "Films français":
            st.header("Films français les mieux notés par décennie")
            
            # Chargement des données
            url = "https://raw.githubusercontent.com/florianhoarau/streamlit_imdb/main/tconst.tsv.gz"
            df = pd.read_csv(url, sep='\t')
            
            # Filtrer les films français
            df_fr = df[df['original_language'] == 'fr']
            
            # Convertir l'année en format datetime et filtrer depuis 1960
            df_fr['decade'] = (pd.to_datetime(df_fr['year'].astype(str), format='%Y').dt.year // 10) * 10
            df_fr = df_fr[df_fr['decade'] >= 1960]
            
            # Filtrer les films avec au moins 1000 votes
            df_fr = df_fr[df_fr['vote'] >= 1000]
            
            # Appliquer le filtre de décennie
            df_fr = filter_by_decade(df_fr, selected_decade)
            
            if len(df_fr) > 0:
                # Création de la figure
                fig, ax = plt.subplots(figsize=(15, 10))
                
                # Recherche du meilleur film de chaque décennie
                if selected_decade == "Toutes les décennies":
                    top_by_decade = df_fr.groupby('decade').apply(
                        lambda x: x.nlargest(1, 'rate')).reset_index(drop=True)
                else:
                    top_by_decade = df_fr.nlargest(5, 'rate')
                
                # Création du graphique à barres horizontales
                if selected_decade == "Toutes les décennies":
                    x_labels = top_by_decade['decade'].astype(str) + 's'
                else:
                    x_labels = top_by_decade['title']
                
                bars = ax.barh(x_labels, top_by_decade['rate'])
                
                # Ajout du titre et de l'étiquette
                ax.set_title('Films français les mieux notés' +
                            (' par décennie' if selected_decade == "Toutes les décennies" else f" des années {selected_decade}"))
                ax.set_xlabel('Note moyenne')
                
                # Ajout des titres et notes
                for bar, title, note, vote_count in zip(bars,
                    top_by_decade['title'],
                    top_by_decade['rate'],
                    top_by_decade['vote']):
                    width = bar.get_width()
                    
                    # Titre du film dans la barre
                    ax.text(
                        width/2,
                        bar.get_y() + bar.get_height()/2,
                        f'{title} ({int(vote_count)} votes)',
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
                st.subheader("Détails des films")
                for _, film in top_by_decade.iterrows():
                    if selected_decade == "Toutes les décennies":
                        st.write(f"\nDécennie: {film['decade']}s")
                    st.write(f"Titre: {film['title']} ({int(film['vote'])} votes)")
                    st.write(f"Note: {film['rate']:.1f}/10")
                    st.write("---")
            else:
                st.write("Aucun film français disponible pour cette période.")
        
        elif origine_submenu == "Films étrangers":
            st.header("Films étrangers les mieux notés par décennie")
            
            # Chargement des données
            url = "https://raw.githubusercontent.com/florianhoarau/streamlit_imdb/main/tconst.tsv.gz"
            df = pd.read_csv(url, sep='\t')
            
            # Préparation des données
            df['decade'] = (pd.to_datetime(df['year'].astype(str), format='%Y').dt.year // 10) * 10
            
            # Filtrer les films non français
            df = df[df['original_language'] != 'fr']
            
            # Créer deux DataFrames selon le nombre de votes
            df_1000_10000 = df[(df['vote'] >= 1000) & (df['vote'] < 10000)]
            df_10000plus = df[df['vote'] >= 10000]
            
            # On ne garde que les films à partir de 1960 pour les deux groupes
            df_1000_10000 = df_1000_10000[df_1000_10000['decade'] >= 1960]
            df_10000plus = df_10000plus[df_10000plus['decade'] >= 1960]
            
            # Appliquer le filtre de décennie
            df_1000_10000 = filter_by_decade(df_1000_10000, selected_decade)
            df_10000plus = filter_by_decade(df_10000plus, selected_decade)
            
            if len(df_1000_10000) > 0 or len(df_10000plus) > 0:
                st.subheader("Répartition des films par langue selon le nombre de votes")
                
                # Création de la visualisation
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
                
                # Premier camembert (à gauche) - Films avec 1000-10000 votes
                if len(df_1000_10000) > 0:
                    countries_1000 = df_1000_10000['original_language'].value_counts().head(5)
                    ax1.pie(countries_1000.values, labels=countries_1000.index, autopct='%1.1f%%')
                    ax1.set_title('Répartition par langue (1000-10000 votes)')
                else:
                    ax1.text(0.5, 0.5, 'Pas de données disponibles', ha='center')
                
                # Deuxième camembert (à droite) - Films avec plus de 10000 votes
                if len(df_10000plus) > 0:
                    countries_10000 = df_10000plus['original_language'].value_counts().head(5)
                    ax2.pie(countries_10000.values, labels=countries_10000.index, autopct='%1.1f%%')
                    ax2.set_title('Répartition par langue (>10000 votes)')
                else:
                    ax2.text(0.5, 0.5, 'Pas de données disponibles', ha='center')
                
                plt.tight_layout()
                st.pyplot(fig)
                
                st.subheader("Meilleurs films par décennie selon le nombre de votes")
                
                # Définition des groupes de votes dans l'ordre décroissant
                vote_groups = ["Très votés (>10000)", "Moyennement votés (1000-10000)"]
                
                # Création de la figure avec 2 sous-graphiques
                fig, axes = plt.subplots(len(vote_groups), 1, figsize=(15, 15))
                
                # Boucle sur chaque groupe de votes
                for idx, group in enumerate(vote_groups):
                    # Sélection des données selon le groupe
                    if group == "Très votés (>10000)":
                        group_data = df_10000plus
                    else:
                        group_data = df_1000_10000
                    
                    if len(group_data) > 0:
                        # Recherche des meilleurs films
                        if selected_decade == "Toutes les décennies":
                            top_films = group_data.groupby('decade').apply(
                                lambda x: x.nlargest(1, 'rate')).reset_index(drop=True)
                        else:
                            top_films = group_data.nlargest(5, 'rate')
                        
                        # Création du graphique à barres horizontales
                        if selected_decade == "Toutes les décennies":
                            x_labels = top_films['decade'].astype(str) + 's'
                        else:
                            x_labels = top_films['title']
                        
                        bars = axes[idx].barh(x_labels, top_films['rate'])
                        
                        # Ajout du titre et de l'étiquette
                        axes[idx].set_title(f'Films les mieux notés - {group}')
                        axes[idx].set_xlabel('Note moyenne')
                        
                        # Ajout des titres et notes
                        for bar, title, note, vote_count in zip(bars,
                            top_films['title'],
                            top_films['rate'],
                            top_films['vote']):
                            width = bar.get_width()
                            
                            # Titre du film dans la barre
                            axes[idx].text(
                                width/2,
                                bar.get_y() + bar.get_height()/2,
                                f'{title} ({int(vote_count)} votes)',
                                va='center', ha='center',
                                color='white',
                                fontsize=12,
                                weight='bold'
                            )
                            # Note après la barre
                            axes[idx].text(
                                width + 0.1,
                                bar.get_y() + bar.get_height()/2,
                                f'{note:.1f}',
                                va='center',
                                fontsize=12
                            )
                    else:
                        axes[idx].text(0.5, 0.5, 'Pas de données disponibles pour cette période',
                                     ha='center', va='center')
                
                plt.tight_layout()
                st.pyplot(fig)
                
                # Afficher les détails
                st.subheader("Détails")
                for group in vote_groups:
                    st.write(f"\n**{group}**")
                    if group == "Très votés (>10000)":
                        group_data = df_10000plus
                    else:
                        group_data = df_1000_10000
                    
                    if len(group_data) > 0:
                        if selected_decade == "Toutes les décennies":
                            top_films = group_data.groupby('decade').apply(
                                lambda x: x.nlargest(1, 'rate')).reset_index(drop=True)
                        else:
                            top_films = group_data.nlargest(5, 'rate')
                        
                        for _, film in top_films.iterrows():
                            if selected_decade == "Toutes les décennies":
                                st.write(f"\nDécennie: {film['decade']}s")
                            st.write(f"Titre: {film['title']} ({int(film['vote'])} votes)")
                            st.write(f"Note: {film['rate']:.1f}/10")
                            st.write("---")
                    else:
                        st.write("Pas de données disponibles pour cette période")