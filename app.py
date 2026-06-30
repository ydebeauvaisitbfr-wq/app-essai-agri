import streamlit as st
import pandas as pd

# Configuration de la page pour mobile
st.set_page_config(page_title="Saisie Essais", layout="centered")

st.title("🌱 Générateur & Saisie d'Essai")

# 1. PARAMÉTRAGE DE L'ESSAI
with st.expander("⚙️ Configuration de l'essai", expanded=True):
    nom_essai = st.text_input("Nom de l'essai", "Essai Betteraves 2026")
    
    col1, col2 = st.columns(2)
    with col1:
        nb_modalites = st.number_input("Nombre de modalités", min_value=1, value=4, step=1)
    with col2:
        nb_blocs = st.number_input("Nombre de blocs", min_value=1, value=3, step=1)
        
    nb_obs = st.number_input("Observations par modalité (Répétitions)", min_value=1, value=1, step=1)

# Liste des variables demandées
variables = [
    "Pucerons aptères verts / pl", "Pucerons ailés verts / pl",
    "Pucerons aptères noirs", "Pucerons ailés noirs",
    "Sélectivité", "Efficacité", "Type adventice",
    "Gravité Cercosporiose", "Gravité Oïdium", "Gravité Rouille", "Gravité Ramulariose",
    "Nombre de montées", "% Jaunisse", "Gravité Jaunisse"
]

# 2. GÉNÉRATION DU PLAN DE PARCELLES
bouton_generer = st.button("🔄 Générer le plan de parcelles", type="primary", use_container_width=True)

# Initialisation de la session pour stocker les données
if "df_essai" not in st.session_state:
    st.session_state.df_essai = None

if bouton_generer:
    donnees = []
    # Logique de numérotation : Bloc 1 -> 101, Bloc 2 -> 201...
    for b in range(1, nb_blocs + 1):
        for m in range(1, nb_modalites + 1):
            for o in range(1, nb_obs + 1):
                num_parcelle = (b * 100) + m
                # Label unique si plusieurs observations par modalité dans le même bloc
                if nb_obs > 1:
                    label_parcelle = f"{num_parcelle} (Obs {o})"
                else:
                    label_parcelle = str(num_parcelle)
                    
                ligne = {
                    "Essai": nom_essai,
                    "Parcelle": label_parcelle,
                    "Bloc": b,
                    "Modalité": m
                }
                # Ajout des colonnes vides pour les variables
                for var in variables:
                    ligne[var] = ""
                donnees.append(ligne)
                
    st.session_state.df_essai = pd.DataFrame(donnees)
    st.success(f"Plan généré : {len(st.session_state.df_essai)} lignes prêtes !")

# 3. INTERFACE DE SAISIE MOBILE
if st.session_state.df_essai is not None:
    st.write("---")
    st.subheader("📱 Saisie des données au champ")
    
    # Sélection de la parcelle via un gros menu déroulant (idéal sur smartphone)
    liste_parcelles = st.session_state.df_essai["Parcelle"].tolist()
    parcelle_selectionnee = st.selectbox("🎯 Choisir la parcelle à noter :", liste_parcelles)
    
    # Index de la ligne correspondante
    idx = st.session_state.df_essai[st.session_state.df_essai["Parcelle"] == parcelle_selectionnee].index[0]
    
    # Formulaire de saisie pour la parcelle sélectionnée
    with st.form("form_saisie"):
        st.info(f"Saisie pour la Parcelle {parcelle_selectionnee} (Bloc {st.session_state.df_essai.at[idx, 'Bloc']}, Mod {st.session_state.df_essai.at[idx, 'Modalité']})")
        
        # Organisation des inputs en sections pour que ce soit lisible sur écran étroit
        st.markdown("**🪳 Pucerons**")
        p_av = st.number_input("Aptères verts / pl", value=0.0, step=0.1, key="p_av")
        p_aiv = st.number_input("Ailés verts / pl", value=0.0, step=0.1, key="p_aiv")
        p_an = st.number_input("Aptères noirs", value=0.0, step=1.0, key="p_an")
        p_ain = st.number_input("Ailés noirs", value=0.0, step=1.0, key="p_ain")
        
        st.markdown("**🛡️ Efficacité & Adventices**")
        select = st.slider("Sélectivité (0 à 10)", 0, 10, 10)
        effic = st.slider("Efficacité (0 à 100%)", 0, 100, 100)
        adventice = st.text_input("Type adventice (optionnel)", "")
        
        st.markdown("**🍂 Maladies & Jaunisse**")
        cerco = st.slider("Gravité Cercosporiose", 0, 9, 0)
        oidium = st.slider("Gravité Oïdium", 0, 9, 0)
        rouille = st.slider("Gravité Rouille", 0, 9, 0)
        ramu = st.slider("Gravité Ramulariose", 0, 9, 0)
        
        jaunisse_pct = st.slider("% Jaunisse", 0, 100, 0)
        jaunisse_grav = st.slider("Gravité Jaunisse", 0, 9, 0)
        monteees = st.number_input("Nombre de montées", min_value=0, value=0, step=1)
        
        # Bouton de sauvegarde de la parcelle
        sauvegarder = st.form_submit_button("💾 Enregistrer cette parcelle", use_container_width=True)
        
        if sauvegarder:
            st.session_state.df_essai.at[idx, "Pucerons aptères verts / pl"] = p_av
            st.session_state.df_essai.at[idx, "Pucerons ailés verts / pl"] = p_aiv
            st.session_state.df_essai.at[idx, "Pucerons aptères noirs"] = p_an
            st.session_state.df_essai.at[idx, "Pucerons ailés noirs"] = p_ain
            st.session_state.df_essai.at[idx, "Sélectivité"] = select
            st.session_state.df_essai.at[idx, "Efficacité"] = effic
            st.session_state.df_essai.at[idx, "Type adventice"] = adventice
            st.session_state.df_essai.at[idx, "Gravité Cercosporiose"] = cerco
            st.session_state.df_essai.at[idx, "Gravité Oïdium"] = oidium
            st.session_state.df_essai.at[idx, "Gravité Rouille"] = rouille
            st.session_state.df_essai.at[idx, "Gravité Ramulariose"] = ramu
            st.session_state.df_essai.at[idx, "% Jaunisse"] = jaunisse_pct
            st.session_state.df_essai.at[idx, "Gravité Jaunisse"] = jaunisse_grav
            st.session_state.df_essai.at[idx, "Nombre de montées"] = monteees
            st.success(f"Données enregistrées pour la parcelle {parcelle_selectionnee} !")

    # 4. EXPORT DES DONNÉES
    st.write("---")
    st.subheader("📊 Récupérer le fichier")
    csv = st.session_state.df_essai.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Télécharger le fichier CSV",
        data=csv,
        file_name=f"{nom_essai.lower().replace(' ', '_')}_data.csv",
        mime='text/csv',
        use_container_width=True
    )
