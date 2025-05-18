import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

# Charger le modèle
model = joblib.load("random_forest_model.pkl")

# Configuration de la page
st.set_page_config(page_title="Simulation Crédit", layout="wide", page_icon="💳")

# Titre
st.markdown("""
    <h2 style="color:#2E86C1;text-align:center;">💳 Simulateur de Crédit - Prédiction de Défaut</h2>
    <p style="text-align:center;">Entrez les informations du client pour estimer le risque de défaut.</p>
    <hr>
""", unsafe_allow_html=True)

# Sidebar pour les inputs
with st.sidebar:
    st.header("🔧 Paramètres du client")
    limit_bal = st.slider("Limite de crédit (LIMIT_BAL)", 0, 1000000, 200000)
    sex = st.radio("Sexe", [1, 2], format_func=lambda x: "Homme" if x == 1 else "Femme")
    education = st.selectbox("Niveau d'éducation", [1, 2, 3, 4], 
                             format_func=lambda x: ["Graduate School", "University", "High School", "Autre"][x - 1])
    marriage = st.selectbox("Statut marital", [1, 2, 3], 
                            format_func=lambda x: ["Marié(e)", "Célibataire", "Autre"][x - 1])
    age = st.slider("Âge", 18, 100, 30)

    st.subheader("📆 Historique de paiement")
    pay_0 = st.slider("Retard (mois -1)", -2, 8, 0)
    pay_2 = st.slider("Retard (mois -2)", -2, 8, 0)
    pay_3 = st.slider("Retard (mois -3)", -2, 8, 0)
    pay_4 = st.slider("Retard (mois -4)", -2, 8, 0)
    pay_5 = st.slider("Retard (mois -5)", -2, 8, 0)
    pay_6 = st.slider("Retard (mois -6)", -2, 8, 0)

    st.subheader("💰 Factures & Paiements")
    bill_amt1 = st.number_input("Facture (mois -1)", 0)
    bill_amt2 = st.number_input("Facture (mois -2)", 0)
    bill_amt3 = st.number_input("Facture (mois -3)", 0)
    bill_amt4 = st.number_input("Facture (mois -4)", 0)
    bill_amt5 = st.number_input("Facture (mois -5)", 0)
    bill_amt6 = st.number_input("Facture (mois -6)", 0)

    pay_amt1 = st.number_input("Paiement (mois -1)", 0)
    pay_amt2 = st.number_input("Paiement (mois -2)", 0)
    pay_amt3 = st.number_input("Paiement (mois -3)", 0)
    pay_amt4 = st.number_input("Paiement (mois -4)", 0)
    pay_amt5 = st.number_input("Paiement (mois -5)", 0)
    pay_amt6 = st.number_input("Paiement (mois -6)", 0)

# Construire le DataFrame utilisateur
user_data = pd.DataFrame({
    'LIMIT_BAL': [limit_bal],
    'SEX': [sex],
    'EDUCATION': [education],
    'MARRIAGE': [marriage],
    'AGE': [age],
    'PAY_0': [pay_0],
    'PAY_2': [pay_2],
    'PAY_3': [pay_3],
    'PAY_4': [pay_4],
    'PAY_5': [pay_5],
    'PAY_6': [pay_6],
    'BILL_AMT1': [bill_amt1],
    'BILL_AMT2': [bill_amt2],
    'BILL_AMT3': [bill_amt3],
    'BILL_AMT4': [bill_amt4],
    'BILL_AMT5': [bill_amt5],
    'BILL_AMT6': [bill_amt6],
    'PAY_AMT1': [pay_amt1],
    'PAY_AMT2': [pay_amt2],
    'PAY_AMT3': [pay_amt3],
    'PAY_AMT4': [pay_amt4],
    'PAY_AMT5': [pay_amt5],
    'PAY_AMT6': [pay_amt6]
})

# Prédiction
if st.button("🚀 Lancer la prédiction"):
    prediction = model.predict(user_data)
    probability = model.predict_proba(user_data)[0][1]

    st.markdown("### 🔎 Résultat de la prédiction")
    if prediction[0] == 1:
        st.error(f"❌ Risque de défaut élevé ({round(probability*100, 2)} %)")
    else:
        st.success(f"✅ Client fiable ({round((1 - probability)*100, 2)} %)")

    # Graphique circulaire
    fig = go.Figure(go.Pie(labels=["Défaut", "Pas de défaut"], values=[probability, 1 - probability],
                           hole=0.5, marker=dict(colors=["#E74C3C", "#2ECC71"])))
    fig.update_layout(width=400, height=400)
    st.plotly_chart(fig)
