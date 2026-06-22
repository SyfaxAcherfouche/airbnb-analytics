import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

# ============================================================
# CONFIG PAGE
# ============================================================
st.set_page_config(
    page_title="Airbnb Analytics",
    page_icon="🏠",
    layout="wide"
)

# ============================================================
# CONNEXION DUCKDB
# ============================================================
@st.cache_resource
def get_conn():
    return duckdb.connect("airbnb.duckdb")

conn = get_conn()

# ============================================================
# FONCTION UTILITAIRE
# ============================================================
@st.cache_data
def load(query):
    return conn.execute(query).df()

# ============================================================
# SIDEBAR – Filtres
# ============================================================
st.sidebar.title("🔎 Filtres")

room_types = load("""
    SELECT DISTINCT room_type 
    FROM silver_listings 
    ORDER BY 1
""")["room_type"].tolist()

selected_room_type = st.sidebar.multiselect(
    "Type de logement",
    room_types,
    default=room_types
)

sentiments = ["positive", "neutral", "negative", "unknown"]
selected_sentiment = st.sidebar.multiselect(
    "Sentiment des avis",
    sentiments,
    default=sentiments
)

# ============================================================
# TITRE
# ============================================================
st.title("🏠 Airbnb Analytics Platform")
st.markdown("Plateforme d'analyse basée sur **DuckDB + dbt + Streamlit**")
st.divider()

# ============================================================
# MÉTRIQUES CLÉS
# ============================================================
st.subheader("📊 Indicateurs clés")

# ── Ligne 1 ─────────────────────────────────────────────────
kpi1 = load("""
    SELECT
        COUNT(*)                        AS nb_logements,
        ROUND(AVG(price), 2)            AS prix_moyen,
        ROUND(MEDIAN(price), 2)         AS prix_median,
        COUNT(DISTINCT host_id)         AS nb_hotes
    FROM silver_listings
""")

kpi2 = load("""
    SELECT
        COUNT(*)                        AS total_avis,
        ROUND(COUNT(*) * 100.0 / (
            SELECT COUNT(*) FROM silver_reviews
        ), 1)                           AS pct_avis_positifs
    FROM silver_reviews
    WHERE sentiment = 'positive'
""")

kpi3 = load("""
    SELECT
        ROUND(COUNT(*) * 100.0 / (
            SELECT COUNT(*) FROM silver_hosts
        ), 1)                           AS pct_superhosts
    FROM silver_hosts
    WHERE is_superhost = TRUE
""")

kpi4 = load("""
    SELECT
        ROUND(COUNT(*) * 100.0 / (
            SELECT COUNT(*) FROM silver_reviews
        ), 1)                           AS pct_pleine_lune
    FROM silver_reviews
    WHERE is_full_moon_review = TRUE
""")

kpi5 = load("""
    SELECT
        ROUND(AVG(price), 2)            AS prix_moyen_superhost
    FROM silver_listings l
    JOIN silver_hosts h ON l.host_id = h.host_id
    WHERE h.is_superhost = TRUE
""")

kpi6 = load("""
    SELECT
        ROUND(COUNT(*) * 100.0 / (
            SELECT COUNT(*) FROM silver_reviews
        ), 1)                           AS pct_negatifs
    FROM silver_reviews
    WHERE sentiment = 'negative'
""")

# ── Affichage Ligne 1 ────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("🏘️ Logements",      int(kpi1["nb_logements"][0]))
col2.metric("💶 Prix moyen",      f"{kpi1['prix_moyen'][0]} €")
col3.metric("💰 Prix médian",     f"{kpi1['prix_median'][0]} €")
col4.metric("👤 Hôtes",           int(kpi1["nb_hotes"][0]))

# ── Affichage Ligne 2 ────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("🏅 Superhosts",      f"{kpi3['pct_superhosts'][0]} %")
col2.metric("😊 Avis positifs",   f"{kpi2['pct_avis_positifs'][0]} %")
col3.metric("😠 Avis négatifs",   f"{kpi6['pct_negatifs'][0]} %")
col4.metric("🌕 Avis pleine lune", f"{kpi4['pct_pleine_lune'][0]} %")

# ── Affichage Ligne 3 ────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("⭐ Total avis",       int(kpi2["total_avis"][0]))
col2.metric("💎 Prix moyen Superhost", f"{kpi5['prix_moyen_superhost'][0]} €")
col3.metric("🌙 Total pleine lune", load("""
    SELECT COUNT(*) AS total 
    FROM silver_reviews 
    WHERE is_full_moon_review = TRUE
""")["total"][0])
col4.metric("🏠 Prix max",         f"{load('SELECT MAX(price) AS max_price FROM silver_listings')['max_price'][0]} €")

# ============================================================
# VIZ 1 – Analyse des logements
# ============================================================
st.subheader("🏘️ Analyse des logements par type")

room_filter = str(selected_room_type)[1:-1]
df_listings = load(f"""
    SELECT
        room_type,
        nb_logements,
        prix_moyen,
        prix_min,
        prix_max
    FROM gold_listings_analysis
    WHERE room_type IN ({room_filter})
""")

col1, col2 = st.columns(2)

fig1a = px.bar(
    df_listings,
    x="room_type", y="prix_moyen",
    color="room_type",
    title="Prix moyen par type de logement",
    labels={"room_type": "Type", "prix_moyen": "Prix moyen (€)"}
)
col1.plotly_chart(fig1a, use_container_width=True)

fig1b = px.bar(
    df_listings,
    x="room_type", y="nb_logements",
    color="room_type",
    title="Nombre de logements par type",
    labels={"room_type": "Type", "nb_logements": "Nombre"}
)
col2.plotly_chart(fig1b, use_container_width=True)

st.divider()

# ============================================================
# VIZ 2 – Analyse des hôtes
# ============================================================
st.subheader("🏅 Superhosts vs Hôtes classiques")

df_hosts = load("""
    SELECT
        CASE WHEN is_superhost THEN 'Superhost' 
             ELSE 'Hôte classique' END  AS type_hote,
        nb_hotes,
        nb_logements,
        prix_moyen,
        prix_min,
        prix_max
    FROM gold_hosts_analysis
""")

col1, col2, col3 = st.columns(3)

fig2a = px.pie(
    df_hosts,
    names="type_hote", values="nb_hotes",
    title="Répartition des hôtes"
)
col1.plotly_chart(fig2a, use_container_width=True)

fig2b = px.bar(
    df_hosts,
    x="type_hote", y="prix_moyen",
    color="type_hote",
    title="Prix moyen par type d'hôte",
    labels={"type_hote": "Type", "prix_moyen": "Prix moyen (€)"}
)
col2.plotly_chart(fig2b, use_container_width=True)

fig2c = px.bar(
    df_hosts,
    x="type_hote", y="nb_logements",
    color="type_hote",
    title="Nombre de logements par type d'hôte",
    labels={"type_hote": "Type", "nb_logements": "Nombre"}
)
col3.plotly_chart(fig2c, use_container_width=True)

st.divider()

# ============================================================
# VIZ 3 – Évolution des avis
# ============================================================
st.subheader("📅 Évolution des avis clients")

sentiment_filter = str(selected_sentiment)[1:-1]
df_reviews = load(f"""
    SELECT
        mois,
        sentiment,
        nb_avis,
        nb_avis_pleine_lune
    FROM gold_reviews_analysis
    WHERE sentiment IN ({sentiment_filter})
    ORDER BY mois
""")

fig3 = px.line(
    df_reviews,
    x="mois", y="nb_avis",
    color="sentiment",
    title="Évolution mensuelle des avis par sentiment",
    markers=True,
    labels={"mois": "Mois", "nb_avis": "Nombre d'avis", "sentiment": "Sentiment"}
)
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ============================================================
# VIZ 4 – Impact pleine lune
# ============================================================
st.subheader("🌕 Impact des nuits de pleine lune sur les avis")

df_moon = load("""
    SELECT
        CASE WHEN is_full_moon_review 
             THEN 'Pleine lune' 
             ELSE 'Nuit normale' END    AS type_nuit,
        sentiment,
        nb_avis,
        pct_sentiment
    FROM gold_full_moon_impact
    ORDER BY type_nuit, sentiment
""")

col1, col2 = st.columns(2)

fig4a = px.bar(
    df_moon,
    x="sentiment", y="nb_avis",
    color="type_nuit",
    barmode="group",
    title="Avis par sentiment : pleine lune vs nuit normale",
    labels={
        "sentiment": "Sentiment",
        "nb_avis": "Nombre d'avis",
        "type_nuit": "Type de nuit"
    }
)
col1.plotly_chart(fig4a, use_container_width=True)

fig4b = px.bar(
    df_moon,
    x="sentiment", y="pct_sentiment",
    color="type_nuit",
    barmode="group",
    title="Répartition (%) des sentiments par type de nuit",
    labels={
        "sentiment": "Sentiment",
        "pct_sentiment": "Pourcentage (%)",
        "type_nuit": "Type de nuit"
    }
)
col2.plotly_chart(fig4b, use_container_width=True)