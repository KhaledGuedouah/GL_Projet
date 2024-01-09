import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

# Creating a cursor object using the cursor() method
cursor = mydb.cursor()

# Query to find the number of students per location (first two digits of the postal code)
query_students_per_location = """
SELECT LEFT(Etablissement.code_postal_site, 2) AS postal_code_prefix, COUNT(Cerfa.ID_E) AS student_count
FROM Cerfa 
JOIN Etablissement ON Cerfa.id_siteformation = Etablissement.id_siteformation
GROUP BY postal_code_prefix
"""
cursor.execute(query_students_per_location)
result_students_per_location = cursor.fetchall()
df_students_per_location = pd.DataFrame(result_students_per_location, columns=['Postal Code Prefix', 'Student Count'])

# Plotting the number of students per location (first two digits of the postal code)
plt.figure(figsize=(10, 10))
plt.pie(df_students_per_location['Student Count'], labels=df_students_per_location['Postal Code Prefix'], autopct='%1.1f%%')
plt.title('Nombres d\'apprenties par Departement')
plt.show()

query_students_per_age = """
SELECT Age, COUNT(*) as student_count
FROM etudiant
GROUP BY Age
ORDER BY Age;
"""

cursor.execute(query_students_per_age)
result_students_per_age = cursor.fetchall()
df_students_per_age = pd.DataFrame(result_students_per_age, columns=['Age', 'student_count'])

# Plotting the number of students per age
plt.figure(figsize=(15, 11))
plt.bar(df_students_per_age['Age'], df_students_per_age['student_count'], color='skyblue')
plt.xlabel('Age')
plt.ylabel('Number of Students')
plt.title('Number of Students per Age')
plt.xticks(df_students_per_age['Age'])
plt.show()

query_students_per_Sexe = """
SELECT Sexe, COUNT(*) as student_count
FROM etudiant
GROUP BY Sexe;
"""

cursor.execute(query_students_per_Sexe)
result_students_per_Sexe = cursor.fetchall()
df_students_per_Sexe = pd.DataFrame(result_students_per_Sexe, columns=['Sexe', 'student_count'])

# Plotting the number of students per Sexe
plt.figure(figsize=(3, 8))

# Creating a bar plot for student count grouped by Sexe
plt.bar(df_students_per_Sexe['Sexe'], df_students_per_Sexe['student_count'], color=['pink', 'blue'])
plt.xlabel('Sexe')
plt.ylabel('Number of Students')
plt.title('Number of Students per Sexe')
plt.tight_layout()
plt.show()

query_students_per_nationalite = """
SELECT libelle_nationalite, COUNT(*) as student_count
FROM etudiant
GROUP BY libelle_nationalite;
"""

cursor.execute(query_students_per_nationalite)
result_students_per_nationalite = cursor.fetchall()
df_students_per_nationalite = pd.DataFrame(result_students_per_nationalite, columns=['libelle_nationalite', 'student_count'])

# Plotting the number of students per libelle_nationalite
plt.figure(figsize=(10, 6))

# Creating a bar plot for student count grouped by Sexe
plt.bar(df_students_per_nationalite['libelle_nationalite'], df_students_per_nationalite['student_count'])
plt.xlabel('Nationality')
plt.ylabel('Number of Students')
plt.tight_layout()
plt.show()

# Query to find the number of apprentices per company (limited to 10 companies)
query_apprentices_per_sector = """
SELECT e.code_naf_entreprise, COUNT(c.ID_E) as apprentice_count
FROM Cerfa c
INNER JOIN entreprise e ON c.code_insee_entreprise = e.code_insee_entreprise
GROUP BY e.code_naf_entreprise
ORDER BY apprentice_count DESC
LIMIT 10;
"""
cursor.execute(query_apprentices_per_sector)
result_apprentices_per_company = cursor.fetchall()
df_apprentices_per_company = pd.DataFrame(result_apprentices_per_company, columns=['Company Code', 'Apprentice Count'])

# Plotting the number of apprentices per company
sns.barplot(x='Company Code', y='Apprentice Count', data=df_apprentices_per_company)
plt.title('Number of Apprentices per Company (Top 10 Companies)')
plt.xticks(rotation=45)
plt.show()


# Query to find the number of students per establishment (limited to 10 establishments)
query_students_per_establishment = """
SELECT Etablissement.id_siteformation, COUNT(Cerfa.ID_E) as student_count 
FROM Cerfa 
JOIN Etablissement ON Cerfa.id_siteformation = Etablissement.id_siteformation
GROUP BY Etablissement.id_siteformation
ORDER BY student_count DESC
LIMIT 10
"""
cursor.execute(query_students_per_establishment)
result_students_per_establishment = cursor.fetchall()
df_students_per_establishment = pd.DataFrame(result_students_per_establishment, columns=['Establishment ID', 'Student Count'])

# Plotting the number of students per establishment
sns.barplot(x='Establishment ID', y='Student Count', data=df_students_per_establishment)
plt.title('Number of Students per Establishment (Top 10 Establishments)')
plt.xticks(rotation=45)
plt.show()

# Close the connection
cursor.close()
mydb.close()


