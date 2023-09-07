import pandas as pd

# Liste de mots clés liés à chaque problématique
problematiques = {
    'Retard navire': ['retard', 'heure', 'arrivée','départ','late','ora'],
    'Garage': ['garage', 'Place','parking','circuler'],
    'Personnel': ['personnel', 'amabilité','aimable','désagréable','courtois','éducation','educato'],
    'Bruit moteur': ['moteur', 'vibration','bruit','vibrazioni'],
    'Wifi': ['connexion', 'wifi'],
    'Communication': ['langue', 'parle','français','language','speak'],
    'Locaux fermés': ['ouvert', 'fermé','bar','restaurant','chiuso','chiusi'],
    'Distributeurs': ['distributeurs', 'distributori','HS','cassé','vide','empty','vuoto','broken'],
    'Cabine': ['cabine', 'libéré','liberare'],
    'Propreté cabine': ['propreté', 'hygiène','sale','saleté','poussière','pulizia','clean','dirty','gross','filthy'],
    'Matelas': ['literie', 'matelas','letti','materassi'],
    'Climatisation': ['clim', 'ac','température','chaud','froid','condizionata','conditioner'],
    'Eau chaude': ['eau', 'acqua'],
    'Toilettes': ['toilette', 'toilettes','wc','bagni','otturati'],
    'Odeurs': ['odeur', 'odore','égoûts','fogna','ombrinale','ombrinali','scarico','odour','smell'],
}

# Lire le fichier CSV
df = pd.read_csv('Test_juillet_aout.csv', dtype='string', sep=';',encoding='latin_1')  # Remplacez 'your_file.csv' par le nom de votre fichier

# Convertir la colonne des notes en numérique
df['Traversée dans son ensemble - 25515'] = pd.to_numeric(df['Traversée dans son ensemble - 25515'], errors='coerce')

# Calculer le total des commentaires par Site Code
total_commentaires_par_site = df['Site Code'].value_counts()

# Filtrer les données pour ne conserver que les lignes avec des notes entre 0 et 6
df_filtered = df[df['Traversée dans son ensemble - 25515'].between(0, 6)]

# Initialiser un dictionnaire pour stocker les comptes
compte_par_site = {}

# Parcourir chaque ligne du DataFrame
for index, row in df_filtered.iterrows():
    site_code = row['Site Code']
    
    # Vérifier si le commentaire est une valeur manquante
    if pd.isna(row['Commentaire global - 25666']):
        continue  # Ignore cette ligne et passe à la suivante
    
    commentaire = row['Commentaire global - 25666'].lower()  # Convertir le commentaire en minuscules pour une comparaison insensible à la casse
    
    if site_code not in compte_par_site:
        compte_par_site[site_code] = {problematique: 0 for problematique in problematiques.keys()}
    

    # Compter les occurrences de chaque mot clé dans le commentaire
    for probleme, mots_cles in problematiques.items():
      if any(mot in commentaire for mot in mots_cles):
        compte_par_site[site_code][probleme] += 1

# Convertir les comptes en DataFrame pour un affichage plus facile
df_compte = pd.DataFrame.from_dict(compte_par_site, orient='index')


# Calculer les pourcentages
df_compte['Total'] = df_compte.sum(axis=1)
for probleme in problematiques.keys():
    df_compte[f'{probleme} (%)'] = (df_compte[probleme] / df_compte['Total']) * 100

df_compte['Total Commentaires'] = df_compte.index.map(total_commentaires_par_site)


# Transposer le DataFrame
df_compte_transpose = df_compte.transpose()

# Afficher les DataFrames
print("DataFrame original:")
print(df_compte)
print("DataFrame transposé:")
print(df_compte_transpose)

df_compte_transpose.to_excel('resultats_problematiques_par_navire.xlsx')
