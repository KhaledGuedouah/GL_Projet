import mysql.connector
import pandas as pd

# Database connection parameters
db_config = {
    'user': 'yono',
    'password': 'Demo@4300',
    'host': 'localhost',
    'database': 'apprentissage'
}

# Connect to the MySQL database
mydb = mysql.connector.connect(
    host=db_config['host'],
    user=db_config['user'],
    passwd=db_config['password'],
    database=db_config['database'],
    auth_plugin="mysql_native_password"
)

# Create a cursor object
cursor = mydb.cursor()



# Read the CSV file
file_path = 'apprentissage_-_effectifs_detailles_2010-2011.csv'
df = pd.read_csv(file_path, encoding='ISO-8859-1', delimiter=';')

# Transform and map the data for the 'Etudiant' table
df_etudiant = df[['age_jeune_decembre', 'sexe', 'libelle_nationalite', 'Type_contrat', 'code_postal_jeune', 'libelle_ville_jeune']]
df_etudiant.columns = ['Age', 'Sexe', 'libelle_nationalite', 'Type_contrat', 'Code_P', 'Ville']
df_etudiant = df_etudiant.drop_duplicates().dropna()

columns = df.columns.tolist()
print(columns)

# Insert data into 'Etudiant' table
for index, row in df_etudiant.iterrows():
    sql_query = """
    INSERT INTO Etudiant (Age, Sexe, libelle_nationalite, Type_contrat, Code_P, Ville) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql_query, tuple(row))
    mydb.commit()

df_etablissement = df[['id_siteformation', 'code_uai_site', 'adresse1_site', 'code_postal_site']].drop_duplicates(subset=['id_siteformation']).dropna()
for index, row in df_etablissement.iterrows():
    sql_query = "INSERT INTO Etablissement (id_siteformation, code_uai_site, adresse_site, code_postal_site) VALUES (%s, %s, %s, %s)"
    try:
        cursor.execute(sql_query, tuple(row))
        mydb.commit()
    except mysql.connector.errors.IntegrityError:
        print(f"Record with id_siteformation {row['id_siteformation']} already exists. Skipping insertion.")

# Mapping data for 'Entreprise' table
# Adjust column names based on your CSV structure and table schema
df_entreprise = df[['code_insee_entreprise', 'depart_entreprise', 'code_naf_entreprise']].drop_duplicates(subset=['code_insee_entreprise']).dropna()
df_entreprise.columns = ['code_insee_entreprise', 'Departement', 'code_naf_entreprise']

# Insert data into 'Entreprise' table
for index, row in df_entreprise.iterrows():
    sql_query = "INSERT INTO Entreprise (code_insee_entreprise, Departement, code_naf_entreprise) VALUES (%s, %s, %s)"
    try:
        cursor.execute(sql_query, tuple(row))
        mydb.commit()
    except mysql.connector.errors.IntegrityError:
        print(f"Record with id_siteformation {row['code_insee_entreprise']} already exists. Skipping insertion.")


# Mapping data for 'Diplome' table
# Adjust the column names based on your CSV structure and table schema
df_diplome = df[['diplome', 'libelle_diplome', 'type_diplome', 'code_niveau', 'code_groupe_specialite', 'libelle_specialite']].drop_duplicates().dropna()

# Insert data into 'Diplome' table
for index, row in df_diplome.iterrows():
    sql_query = "INSERT INTO Diplome (ID_D, libelle_diplome, type_diplome, code_niveau, code_groupe_specialite, libelle_specialite) VALUES (%s, %s, %s, %s, %s, %s)"
    try:
        cursor.execute(sql_query, tuple(row))
        mydb.commit()
    except mysql.connector.errors.IntegrityError:
        print(f"Record with id_siteformation {row['diplome']} already exists. Skipping insertion.")


def add_autoincrement_column_to_csv(input_file_path, output_file_path, delimiter=';',col_name ='AutoIncrement' ):
    # Read the CSV file with the specified delimiter
    df = pd.read_csv(input_file_path, sep=delimiter,  quotechar='"', escapechar='\\')
    #error_bad_lines=False,
    # Add an autoincrement column
    df[col_name] = range(1, len(df) + 1)

    # Save the updated DataFrame back to a CSV file with the same delimiter
    df.to_csv(output_file_path, index=False, sep=delimiter)


add_autoincrement_column_to_csv(file_path,"Test_updated.csv",col_name ='id_etudiant')

# Read the CSV file
file_path2 = 'Test_updated.csv'
df = pd.read_csv(file_path2, encoding='ISO-8859-1', delimiter=';')

df_cerfa = df[['id_etudiant', 'diplome', 'code_insee_entreprise', 'id_siteformation', 'annee_scolaire', 'duree_formation_mois']].drop_duplicates().dropna()

# Insert data into 'Cerfa' table
for index, row in df_cerfa.iterrows():
    print(row)
    try : 
        sql_query = "INSERT INTO Cerfa (ID_E, ID_D, code_insee_entreprise, id_siteformation, Anne_scolaire, Duree_formation_mois) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql_query, tuple(row))
        mydb.commit()
    except : 
        print("foreign key constraint fails")
    

# Close the database connection
cursor.close()
mydb.close()