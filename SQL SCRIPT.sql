#------------------------------------------------------------
# Table: Etudiant
#------------------------------------------------------------

create Database apprentissage; 
use apprentissage;
CREATE TABLE Etudiant(
        ID_E                Int NOT NULL AUTO_INCREMENT,
        Age                 Int NOT NULL ,
        Sexe                Char (15) NOT NULL ,
        libelle_nationalite Varchar (50) NOT NULL ,
        Type_contrat        Varchar (100) NOT NULL ,
        Code_P              Int NOT NULL ,
        Ville               Varchar (50) NOT NULL
	,CONSTRAINT Etudiant_PK PRIMARY KEY (ID_E)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Etablissement 
#------------------------------------------------------------

CREATE TABLE Etablissement(
        id_siteformation Int NOT NULL ,
        code_uai_site    Varchar (25) NOT NULL ,
        adresse_site     Varchar (100) NOT NULL ,
        code_postal_site Int NOT NULL
	,CONSTRAINT Etablissement_PK PRIMARY KEY (id_siteformation)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Diplome
#------------------------------------------------------------

CREATE TABLE Diplome(
        ID_D                   Int NOT NULL ,
        libelle_diplome        Varchar (500) NOT NULL ,
        type_diplome           Varchar (15) NOT NULL ,
        code_niveau            Int NOT NULL ,
        code_groupe_specialite Int NOT NULL ,
        libelle_specialite     Varchar (200) NOT NULL
	,CONSTRAINT Diplome_PK PRIMARY KEY (ID_D)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Entreprise
#------------------------------------------------------------

CREATE TABLE Entreprise(
        code_insee_entreprise Int NOT NULL ,
        Departement           Int NOT NULL ,
        code_naf_entreprise   Varchar (15) NOT NULL
	,CONSTRAINT Entreprise_PK PRIMARY KEY (code_insee_entreprise)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Cerfa
#------------------------------------------------------------

CREATE TABLE Cerfa(
        ID_E                  Int NOT NULL ,
        ID_D                  Int NOT NULL ,
        code_insee_entreprise Int NOT NULL ,
        id_siteformation      Int NOT NULL ,
        Anne_scolaire         Int NOT NULL ,
        ID_Cerfa              Int NOT NULL AUTO_INCREMENT ,
        Duree_formation_mois  Int NOT NULL
	,CONSTRAINT Cerfa_PK PRIMARY KEY (ID_Cerfa)

	,CONSTRAINT Cerfa_Etudiant_FK FOREIGN KEY (ID_E) REFERENCES Etudiant(ID_E)
	,CONSTRAINT Cerfa_Diplome0_FK FOREIGN KEY (ID_D) REFERENCES Diplome(ID_D)
	,CONSTRAINT Cerfa_Entreprise1_FK FOREIGN KEY (code_insee_entreprise) REFERENCES Entreprise(code_insee_entreprise)
	,CONSTRAINT Cerfa_Etablissement2_FK FOREIGN KEY (id_siteformation) REFERENCES Etablissement(id_siteformation)
)ENGINE=InnoDB;

