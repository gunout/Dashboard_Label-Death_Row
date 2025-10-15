# dashboard_death_row_records.py
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import re
from datetime import datetime
import warnings
import base64
import io
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="ANALYSE COMPLÈTE - DEATH ROW RECORDS",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé avec thème hip-hop
st.markdown("""
<style>
    .main {
        color: #ffffff !important;
        background-color: #0a0a0a !important;
    }
    
    .stApp {
        background-color: #0a0a0a !important;
        color: #ffffff !important;
    }
    
    .main-header {
        font-size: 3rem;
        color: #ffffff !important;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
        border-bottom: 3px solid #ff0000;
        padding-bottom: 1rem;
        text-shadow: 0 0 20px rgba(255, 0, 0, 0.5);
    }
    
    .academic-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        border: 1px solid #444444;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        color: #ffffff !important;
        transition: all 0.3s ease;
    }
    
    .academic-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255, 0, 0, 0.3);
        border-color: #ff0000;
    }
    
    .dre-card { 
        border-left: 5px solid #ff0000; 
        background: linear-gradient(135deg, #1a0a0a 0%, #2d1a1a 100%);
    }
    .snoop-card { 
        border-left: 5px solid #4169e1; 
        background: linear-gradient(135deg, #0a0a1a 0%, #1a1a2d 100%);
    }
    .tupac-card { 
        border-left: 5px solid #ffd700; 
        background: linear-gradient(135deg, #1a1a0a 0%, #2d2d1a 100%);
    }
    .daz-card { 
        border-left: 5px solid #ff69b4; 
        background: linear-gradient(135deg, #1a0a1a 0%, #2d1a2d 100%);
    }
    .nate-card { 
        border-left: 5px solid #ff8c00; 
        background: linear-gradient(135deg, #1a1a0a 0%, #2d2d1a 100%);
    }
    .warren-card { 
        border-left: 5px solid #9370db; 
        background: linear-gradient(135deg, #0a1a1a 0%, #1a2d2d 100%);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #ff0000 !important;
        margin: 0.5rem 0;
        text-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
    }
    
    .section-title {
        color: #ffffff !important;
        border-bottom: 2px solid #ff0000;
        padding-bottom: 0.5rem;
        margin: 2rem 0 1rem 0;
        font-size: 1.6rem;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(255, 0, 0, 0.3);
    }
    
    .subsection-title {
        color: #ffffff !important;
        border-left: 4px solid #ff0000;
        padding-left: 1rem;
        margin: 1.5rem 0 1rem 0;
        font-size: 1.3rem;
        font-weight: 600;
    }
    
    .stMarkdown {
        color: #ffffff !important;
    }
    
    p, div, span, h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    .secondary-text {
        color: #cccccc !important;
    }
    
    .light-text {
        color: #999999 !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #1a1a1a;
        border-radius: 8px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #2d2d2d;
        border-radius: 5px;
        color: #ffffff !important;
        font-weight: 500;
        border: 1px solid #444444;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #3d3d3d;
        border-color: #ff0000;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #ff0000 !important;
        color: #000000 !important;
        font-weight: 600;
        border-color: #ff0000;
    }
    
    .card-content {
        color: #ffffff !important;
    }
    
    .card-secondary {
        color: #cccccc !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #ff0000 0%, #cc0000 100%);
        color: #ffffff;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 0, 0, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #ff3333 0%, #ff0000 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 0, 0, 0.5);
    }
    
    .stDataFrame {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    .stSelectbox > div > div {
        background-color: #2d2d2d;
        color: #ffffff;
    }
    
    .stSlider > div > div > div {
        background-color: #ff0000;
    }
    
    /* Style pour les graphiques Plotly */
    .js-plotly-plot .plotly .modebar {
        background-color: rgba(26, 26, 26, 0.8) !important;
    }
    
    .js-plotly-plot .plotly .modebar-btn {
        background-color: transparent !important;
        color: #ffffff !important;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #444444;
        border-radius: 6px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #555555;
    }
</style>
""", unsafe_allow_html=True)

class DeathRowAnalyzer:
    def __init__(self):
        # Définition de la palette de couleurs pour Death Row Records
        self.color_palette = {
            'DR. DRE': '#ff0000',        # Rouge
            'SNOOP DOGG': '#4169e1',     # Bleu
            'TUPAC SHAKUR': '#ffd700',   # Or
            'DAZ DILLINGER': '#ff69b4',  # Rose
            'NATE DOGG': '#ff8c00',      # Orange foncé
            'WARREN G': '#9370db',      # Violet
            'THE LADY OF RAGE': '#ff1493',  # Rose profond
            'Période Indépendante': '#ff0000',
            'Période Suge': '#4169e1'
        }
        
        # Couleurs pour les types de données adaptées au thème hip-hop
        self.data_colors = {
            'Ventes': '#ff0000',
            'Albums': '#4169e1',
            'Artistes': '#ffd700',
            'Revenus': '#ff69b4',
            'Croissance': '#ff8c00'
        }
        
        self.initialize_data()
        
    def initialize_data(self):
        """Initialise les données complètes sur Death Row Records"""
        
        # Données principales sur le label
        self.label_data = {
            'fondation': 1991,
            'fondateur': 'Suge Knight, Dr. Dre, The D.O.C.',
            'statut': 'Label indépendant (racheté par WIDEawake Entertainment en 2019)',
            'siege': 'Los Angeles, Californie, USA',
            'specialisation': 'Hip-hop de la West Coast, G-funk',
            'philosophie': 'Révolutionner le son hip-hop',
            'distribution': 'Interscope Records (1992-1996), Priority Records (1996-2001)'
        }

        # Données des artistes principaux
        self.artists_data = {
            'DR. DRE': {
                'debut': 1992,
                'genre': 'G-funk, hip-hop',
                'albums_deathrow': 2,
                'ventes_totales': 7000000,
                'succes_principal': 'The Chronic (1992)',
                'statut': 'Fondateur et producteur',
                'impact': 'Pionnier du G-funk',
                'annees_activite': '1992-1996',
                'albums_principaux': ['The Chronic', '2001'],
                'chiffre_affaires_estime': 45000000,
                'public_cible': 'Fans de hip-hop, urbain',
                'tournees': 'Mondiales'
            },
            'SNOOP DOGG': {
                'debut': 1993,
                'genre': 'G-funk, hip-hop',
                'albums_deathrow': 2,
                'ventes_totales': 10000000,
                'succes_principal': 'Doggystyle (1993)',
                'statut': 'Artiste phare',
                'impact': 'Icône culturelle',
                'annees_activite': '1993-1998',
                'albums_principaux': ['Doggystyle', 'Tha Doggfather'],
                'chiffre_affaires_estime': 60000000,
                'public_cible': 'Jeunes urbains, culture pop',
                'tournees': 'Mondiales'
            },
            'TUPAC SHAKUR': {
                'debut': 1995,
                'genre': 'Hip-hop, rap conscient',
                'albums_deathrow': 2,
                'ventes_totales': 12000000,
                'succes_principal': 'All Eyez on Me (1996)',
                'statut': 'Légende du hip-hop',
                'impact': 'Culturel mondial',
                'annees_activite': '1995-1996',
                'albums_principaux': ['All Eyez on Me', 'The Don Killuminati'],
                'chiffre_affaires_estime': 80000000,
                'public_cible': 'Tous publics, international',
                'tournees': 'Mondiales'
            },
            'DAZ DILLINGER': {
                'debut': 1996,
                'genre': 'G-funk, hip-hop',
                'albums_deathrow': 2,
                'ventes_totales': 1500000,
                'succes_principal': 'Retaliation, Revenge and Get Back (1998)',
                'statut': 'Artiste secondaire',
                'impact': 'West Coast',
                'annees_activite': '1996-2000',
                'albums_principaux': ['Retaliation, Revenge and Get Back', 'R.A.W.'],
                'chiffre_affaires_estime': 8000000,
                'public_cible': 'Fans de hip-hop West Coast',
                'tournees': 'Nationales'
            },
            'NATE DOGG': {
                'debut': 1994,
                'genre': 'G-funk, hip-hop',
                'albums_deathrow': 1,
                'ventes_totales': 800000,
                'succes_principal': 'G-Funk Classics Vol. 1 & 2 (1998)',
                'statut': 'Artiste collaborateur',
                'impact': 'Voix distinctive',
                'annees_activite': '1994-1998',
                'albums_principaux': ['G-Funk Classics Vol. 1 & 2'],
                'chiffre_affaires_estime': 4000000,
                'public_cible': 'Fans de G-funk',
                'tournees': 'Collaborations'
            },
            'WARREN G': {
                'debut': 1994,
                'genre': 'G-funk, hip-hop',
                'albums_deathrow': 1,
                'ventes_totales': 3000000,
                'succes_principal': 'Regulate...G Funk Era (1994)',
                'statut': 'Artiste à succès',
                'impact': 'Hit-maker',
                'annees_activite': '1994-1997',
                'albums_principaux': ['Regulate...G Funk Era'],
                'chiffre_affaires_estime': 15000000,
                'public_cible': 'Fans de hip-hop, grand public',
                'tournees': 'Nationales'
            }
        }

        # Données chronologiques détaillées
        self.timeline_data = [
            {'annee': 1991, 'evenement': 'Fondation par Suge Knight et Dr. Dre', 'type': 'Structure', 'importance': 10},
            {'annee': 1992, 'evenement': 'Sortie de The Chronic (Dr. Dre)', 'type': 'Album', 'importance': 10},
            {'annee': 1993, 'evenement': 'Sortie de Doggystyle (Snoop Dogg)', 'type': 'Album', 'importance': 10},
            {'annee': 1994, 'evenement': 'Sortie de Regulate...G Funk Era (Warren G)', 'type': 'Album', 'importance': 8},
            {'annee': 1995, 'evenement': 'Signature de Tupac Shakur', 'type': 'Artiste', 'importance': 10},
            {'annee': 1996, 'evenement': 'Sortie de All Eyez on Me (Tupac)', 'type': 'Album', 'importance': 10},
            {'annee': 1996, 'evenement': 'Décès de Tupac Shakur', 'type': 'Événement', 'importance': 10},
            {'annee': 1996, 'evenement': 'Départ de Dr. Dre', 'type': 'Structure', 'importance': 9},
            {'annee': 1997, 'evenement': 'Départ de Snoop Dogg', 'type': 'Structure', 'importance': 8},
            {'annee': 2006, 'evenement': 'Faillite du label', 'type': 'Structure', 'importance': 9},
            {'annee': 2019, 'evenement': 'Rachat par WIDEawake Entertainment', 'type': 'Structure', 'importance': 7}
        ]

        # Données financières et commerciales
        self.financial_data = {
            'DR. DRE': {
                'ventes_albums': 7000000,
                'chiffre_affaires': 45000000,
                'rentabilite': 90,
                'cout_production_moyen': 500000,
                'budget_marketing_moyen': 2000000,
                'roi': 800
            },
            'SNOOP DOGG': {
                'ventes_albums': 10000000,
                'chiffre_affaires': 60000000,
                'rentabilite': 85,
                'cout_production_moyen': 600000,
                'budget_marketing_moyen': 3000000,
                'roi': 900
            },
            'TUPAC SHAKUR': {
                'ventes_albums': 12000000,
                'chiffre_affaires': 80000000,
                'rentabilite': 95,
                'cout_production_moyen': 700000,
                'budget_marketing_moyen': 4000000,
                'roi': 1100
            },
            'DAZ DILLINGER': {
                'ventes_albums': 1500000,
                'chiffre_affaires': 8000000,
                'rentabilite': 70,
                'cout_production_moyen': 200000,
                'budget_marketing_moyen': 500000,
                'roi': 300
            },
            'NATE DOGG': {
                'ventes_albums': 800000,
                'chiffre_affaires': 4000000,
                'rentabilite': 65,
                'cout_production_moyen': 150000,
                'budget_marketing_moyen': 300000,
                'roi': 250
            },
            'WARREN G': {
                'ventes_albums': 3000000,
                'chiffre_affaires': 15000000,
                'rentabilite': 75,
                'cout_production_moyen': 300000,
                'budget_marketing_moyen': 1000000,
                'roi': 400
            }
        }

        # Données de stratégie marketing
        self.marketing_data = {
            'DR. DRE': {
                'strategie': 'Innovation sonore, image de producteur de génie',
                'cibles': 'Puristes du hip-hop, critiques musicaux',
                'canaux': ['Radio urbaine', 'Clubs', 'Presse spécialisée', 'Vidéos musicales'],
                'budget_ratio': 20,
                'succes': 'Légendaire',
                'innovations': 'Création du G-funk'
            },
            'SNOOP DOGG': {
                'strategie': 'Personnalité charismatique, style unique',
                'cibles': 'Jeunes urbains, culture pop',
                'canaux': ['Radio grand public', 'MTV', 'Films', 'Apparences publiques'],
                'budget_ratio': 25,
                'succes': 'Exceptionnel',
                'innovations': 'Marketing de personnalité'
            },
            'TUPAC SHAKUR': {
                'strategie': 'Controverses, engagement social, image de martyr',
                'cibles': 'Public engagé, international',
                'canaux': ['Médias grand public', 'Presse people', 'Films', 'Poésie'],
                'budget_ratio': 30,
                'succes': 'Mythique',
                'innovations': 'Marketing post-mortem'
            },
            'DAZ DILLINGER': {
                'strategie': 'Authenticité West Coast',
                'cibles': 'Fans de hip-hop West Coast',
                'canaux': ['Radio locale', 'Mixtapes', 'Concerts locaux'],
                'budget_ratio': 15,
                'succes': 'Modéré',
                'innovations': 'Marketing de rue'
            },
            'NATE DOGG': {
                'strategie': 'Collaborations, hooks mémorables',
                'cibles': 'Fans de G-funk',
                'canaux': ['Collaborations', 'Radio urbaine', 'Mixtapes'],
                'budget_ratio': 12,
                'succes': 'Correct',
                'innovations': 'Marketing de collaboration'
            },
            'WARREN G': {
                'strategie': 'Singles à succès, accessibilité',
                'cibles': 'Grand public, fans de hip-hop',
                'canaux': ['Radio grand public', 'MTV', 'Clips vidéo'],
                'budget_ratio': 18,
                'succes': 'Bon',
                'innovations': 'Marketing de single'
            }
        }

        # Données de production
        self.production_data = {
            'DR. DRE': {
                'albums_produits': 2,
                'duree_contrat': 4,
                'rythme_sorties': '2 ans',
                'qualite_production': 10,
                'autonomie_artistique': 9,
                'support_label': 9
            },
            'SNOOP DOGG': {
                'albums_produits': 2,
                'duree_contrat': 5,
                'rythme_sorties': '2.5 ans',
                'qualite_production': 9,
                'autonomie_artistique': 7,
                'support_label': 9
            },
            'TUPAC SHAKUR': {
                'albums_produits': 2,
                'duree_contrat': 1,
                'rythme_sorties': '6 mois',
                'qualite_production': 9,
                'autonomie_artistique': 8,
                'support_label': 8
            },
            'DAZ DILLINGER': {
                'albums_produits': 2,
                'duree_contrat': 4,
                'rythme_sorties': '2 ans',
                'qualite_production': 7,
                'autonomie_artistique': 6,
                'support_label': 7
            },
            'NATE DOGG': {
                'albums_produits': 1,
                'duree_contrat': 4,
                'rythme_sorties': '4 ans',
                'qualite_production': 7,
                'autonomie_artistique': 6,
                'support_label': 6
            },
            'WARREN G': {
                'albums_produits': 1,
                'duree_contrat': 3,
                'rythme_sorties': '3 ans',
                'qualite_production': 8,
                'autonomie_artistique': 7,
                'support_label': 7
            }
        }

        # Données de gestion et management
        self.management_data = {
            'structure': {
                'type': 'Label indépendant avec distribution majeure',
                'effectif': 25,
                'departements': ['A&R', 'Production', 'Marketing', 'Commercial', 'Legal'],
                'processus_decision': 'Centralisé (Suge Knight)',
                'culture_entreprise': 'Agressive, controversée, loyauté'
            },
            'ressources_humaines': {
                'turnover': 'Élevé',
                'expertise': 'Production hip-hop',
                'reseautage': 'Industrie musicale',
                'formation': 'Apprentissage'
            },
            'finances': {
                'model_economique': 'Avances sur royalties, droits de publication',
                'marge_nette': '20-25%',
                'investissement_artistes': 'Court terme',
                'risque': 'Élevé'
            },
            'relations_artistes': {
                'approche': 'Contrôlante, protectionniste',
                'contrats': 'Controversés',
                'communication': 'Directe, parfois conflictuelle',
                'loyaute': 'Variable'
            }
        }

    def display_header(self):
        """Affiche l'en-tête du dashboard"""
        st.markdown('<h1 class="main-header">🎤 DEATH ROW RECORDS - DASHBOARD STRATÉGIQUE</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #cccccc; font-size: 1.2rem; margin-bottom: 2rem;">Label de hip-hop américain - Analyse complète 1991-2024</p>', unsafe_allow_html=True)
        
        # Métriques principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_ventes = sum(self.financial_data[artist]['ventes_albums'] for artist in self.financial_data)
            st.markdown(f"""
            <div class="academic-card dre-card">
                <div style="color: {self.color_palette['DR. DRE']}; font-size: 1rem; font-weight: 600; text-align: center;">📀 VENTES TOTALES</div>
                <div class="metric-value" style="color: {self.color_palette['DR. DRE']}; text-align: center;">{total_ventes:,}</div>
                <div style="color: #cccccc; text-align: center;">Albums vendus</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_artistes = len(self.artists_data)
            st.markdown(f"""
            <div class="academic-card snoop-card">
                <div style="color: {self.color_palette['SNOOP DOGG']}; font-size: 1rem; font-weight: 600; text-align: center;">🎤 ARTISTES</div>
                <div class="metric-value" style="color: {self.color_palette['SNOOP DOGG']}; text-align: center;">{total_artistes}</div>
                <div style="color: #cccccc; text-align: center;">Artistes principaux</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            total_albums = sum(self.artists_data[artist]['albums_deathrow'] for artist in self.artists_data)
            st.markdown(f"""
            <div class="academic-card tupac-card">
                <div style="color: {self.color_palette['TUPAC SHAKUR']}; font-size: 1rem; font-weight: 600; text-align: center;">💿 ALBUMS</div>
                <div class="metric-value" style="color: {self.color_palette['TUPAC SHAKUR']}; text-align: center;">{total_albums}</div>
                <div style="color: #cccccc; text-align: center;">Produits par le label</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            chiffre_affaires_total = sum(self.financial_data[artist]['chiffre_affaires'] for artist in self.financial_data)
            st.markdown(f"""
            <div class="academic-card daz-card">
                <div style="color: {self.color_palette['DAZ DILLINGER']}; font-size: 1rem; font-weight: 600; text-align: center;">💰 CHIFFRE D'AFFAIRES</div>
                <div class="metric-value" style="color: {self.color_palette['DAZ DILLINGER']}; text-align: center;">{chiffre_affaires_total/1000000:.1f}M$</div>
                <div style="color: #cccccc; text-align: center;">Estimé sur la période</div>
            </div>
            """, unsafe_allow_html=True)

    def create_artist_analysis(self):
        """Analyse complète des artistes"""
        st.markdown('<h3 class="section-title">🎤 ANALYSE DU PORTFOLIO ARTISTES</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="subsection-title">📊 Performance Commerciale</div>', unsafe_allow_html=True)
            self.create_sales_comparison_chart()
        
        with col2:
            st.markdown('<div class="subsection-title">📈 Rentabilité par Artiste</div>', unsafe_allow_html=True)
            self.create_roi_chart()
        
        # Analyse détaillée par artiste
        st.markdown('<div class="subsection-title">🔍 Analyse Détailée par Artiste</div>', unsafe_allow_html=True)
        self.create_detailed_artist_analysis()

    def create_sales_comparison_chart(self):
        """Graphique de comparaison des ventes"""
        artists = list(self.artists_data.keys())
        ventes = [self.financial_data[artist]['ventes_albums'] for artist in artists]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=artists,
            y=ventes,
            marker_color=[self.color_palette[artist] for artist in artists],
            text=[f"{v/1000000:.1f}M" for v in ventes],
            textposition='auto',
            textfont=dict(color='white', size=14, weight='bold')
        ))
        
        fig.update_layout(
            title='Ventes Totalisées par Artiste',
            xaxis_title='Artistes',
            yaxis_title="Nombre d'albums vendus",
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            showlegend=False,
            xaxis=dict(tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_roi_chart(self):
        """Graphique du retour sur investissement"""
        artists = list(self.financial_data.keys())
        roi = [self.financial_data[artist]['roi'] for artist in artists]
        rentabilite = [self.financial_data[artist]['rentabilite'] for artist in artists]
        
        fig = go.Figure()
        
        for i, artist in enumerate(artists):
            fig.add_trace(go.Scatter(
                x=[roi[i]],
                y=[rentabilite[i]],
                mode='markers+text',
                marker=dict(
                    size=80, 
                    color=self.color_palette[artist], 
                    opacity=0.9,
                    line=dict(width=3, color='#ffffff')
                ),
                text=[artist],
                textposition="middle center",
                textfont=dict(color='white', size=12, weight='bold'),
                name=artist,
                showlegend=True
            ))
        
        fig.update_layout(
            title='ROI vs Rentabilité',
            xaxis_title='Retour sur Investissement (%)',
            yaxis_title='Taux de Rentabilité (%)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#ff0000',
                borderwidth=1,
                font=dict(color='white', size=10)
            ),
            xaxis=dict(range=[200, 1200], tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(range=[60, 100], tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_detailed_artist_analysis(self):
        """Analyse détaillée par artiste"""
        artists = list(self.artists_data.keys())
        tabs = st.tabs(artists)
        
        for i, artist in enumerate(artists):
            with tabs[i]:
                couleur = self.color_palette[artist]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Informations générales
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, {couleur}20 0%, {couleur}05 100%); padding: 1rem; border-radius: 8px; border-left: 5px solid {couleur}; margin-bottom: 1rem;">
                        <div style="color: {couleur}; font-weight: bold; font-size: 1.5rem; margin-bottom: 0.5rem;">{artist}</div>
                        <div style="color: #cccccc; font-size: 1.1rem; font-weight: 500;">{self.artists_data[artist]['genre']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Métriques clés
                    st.metric("Albums chez Death Row", self.artists_data[artist]['albums_deathrow'])
                    st.metric("Ventes totales", f"{self.financial_data[artist]['ventes_albums']:,}")
                    st.metric("Chiffre d'affaires", f"{self.financial_data[artist]['chiffre_affaires']/1000000:.2f}M$")
                    
                    # Succès principal
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; margin-top: 1rem; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Succès Principal:</div>
                        <div style="color: #ffffff; font-style: italic; font-size: 1.1rem;">{self.artists_data[artist]['succes_principal']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Caractéristiques commerciales
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Performance Commerciale:</div>
                        <ul style="color: #ffffff; font-weight: 500;">
                            <li>Rentabilité: {self.financial_data[artist]['rentabilite']}%</li>
                            <li>ROI: {self.financial_data[artist]['roi']}%</li>
                            <li>Coût production moyen: {self.financial_data[artist]['cout_production_moyen']/1000:.0f}k$</li>
                            <li>Budget marketing moyen: {self.financial_data[artist]['budget_marketing_moyen']/1000:.0f}k$</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Graphique radar des caractéristiques
                    categories = ['Ventes', 'Rentabilité', 'ROI', 'Impact']
                    valeurs = [
                        min(100, self.financial_data[artist]['ventes_albums'] / 120000),  # Normalisé
                        self.financial_data[artist]['rentabilite'],
                        min(100, self.financial_data[artist]['roi'] / 12),  # Normalisé
                        100 if self.artists_data[artist]['impact'] in ['Pionnier du G-funk', 'Icône culturelle', 'Légende du hip-hop', 'Culturel mondial'] else 
                        80 if self.artists_data[artist]['impact'] in ['West Coast', 'Hit-maker', 'Voix distinctive'] else
                        60
                    ]
                    
                    fig = go.Figure()
                    
                    fig.add_trace(go.Scatterpolar(
                        r=valeurs + [valeurs[0]],
                        theta=categories + [categories[0]],
                        fill='toself',
                        line=dict(color=couleur, width=3),
                        marker=dict(size=8, color=couleur),
                        name=artist
                    ))
                    
                    fig.update_layout(
                        polar=dict(
                            bgcolor='#1a1a1a',
                            radialaxis=dict(
                                visible=True, 
                                range=[0, 100],
                                gridcolor='#333333',
                                tickfont=dict(color='#ffffff', size=12),
                                linecolor='#444444'
                            ),
                            angularaxis=dict(
                                gridcolor='#333333',
                                tickfont=dict(color='#ffffff', size=12),
                                linecolor='#444444'
                            )
                        ),
                        paper_bgcolor='#0a0a0a',
                        font=dict(color='#ffffff', size=14),
                        showlegend=False,
                        height=300,
                        title=f"Profil de Performance - {artist}"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)

    def create_production_analysis(self):
        """Analyse de la production"""
        st.markdown('<h3 class="section-title">🏭 ANALYSE DE LA PRODUCTION</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="subsection-title">📅 Cycles de Production</div>', unsafe_allow_html=True)
            self.create_production_timeline()
        
        with col2:
            st.markdown('<div class="subsection-title">⚙️ Qualité et Support</div>', unsafe_allow_html=True)
            self.create_quality_support_chart()
        
        # Analyse des coûts
        st.markdown('<div class="subsection-title">💰 Analyse des Coûts de Production</div>', unsafe_allow_html=True)
        self.create_cost_analysis()

    def create_production_timeline(self):
        """Timeline de la production"""
        artists = list(self.production_data.keys())
        durees = [self.production_data[artist]['duree_contrat'] for artist in artists]
        albums = [self.production_data[artist]['albums_produits'] for artist in artists]
        
        fig = go.Figure()
        
        for i, artist in enumerate(artists):
            fig.add_trace(go.Scatter(
                x=[durees[i]],
                y=[albums[i]],
                mode='markers+text',
                marker=dict(
                    size=60, 
                    color=self.color_palette[artist], 
                    opacity=0.9,
                    line=dict(width=2, color='#ffffff')
                ),
                text=[artist],
                textposition="middle center",
                textfont=dict(color='white', size=10, weight='bold'),
                name=artist
            ))
        
        fig.update_layout(
            title='Durée des Contrats vs Nombre d\'Albums',
            xaxis_title='Durée du contrat (années)',
            yaxis_title="Nombre d'albums produits",
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            showlegend=False,
            xaxis=dict(tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_quality_support_chart(self):
        """Graphique qualité vs support"""
        artists = list(self.production_data.keys())
        qualite = [self.production_data[artist]['qualite_production'] for artist in artists]
        support = [self.production_data[artist]['support_label'] for artist in artists]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=qualite,
            y=support,
            mode='markers+text',
            marker=dict(
                size=60,
                color=[self.color_palette[artist] for artist in artists],
                opacity=0.9
            ),
            text=artists,
            textposition="top center",
            textfont=dict(color='white', size=10, weight='bold')
        ))
        
        fig.update_layout(
            title='Qualité de Production vs Support du Label',
            xaxis_title='Qualité de Production (1-10)',
            yaxis_title='Support du Label (1-10)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            showlegend=False,
            xaxis=dict(range=[6, 10.5], tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(range=[5, 9.5], tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_cost_analysis(self):
        """Analyse des coûts de production"""
        artists = list(self.financial_data.keys())
        couts_production = [self.financial_data[artist]['cout_production_moyen'] for artist in artists]
        budgets_marketing = [self.financial_data[artist]['budget_marketing_moyen'] for artist in artists]
        ventes = [self.financial_data[artist]['ventes_albums'] for artist in artists]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Coût Production',
            x=artists,
            y=couts_production,
            marker_color='#ff0000',
            text=[f"{v/1000:.0f}k$" for v in couts_production],
            textposition='auto',
            textfont=dict(color='white', size=10, weight='bold')
        ))
        
        fig.add_trace(go.Bar(
            name='Budget Marketing',
            x=artists,
            y=budgets_marketing,
            marker_color='#4169e1',
            text=[f"{v/1000:.0f}k$" for v in budgets_marketing],
            textposition='auto',
            textfont=dict(color='white', size=10, weight='bold')
        ))
        
        fig.update_layout(
            barmode='group',
            title='Répartition des Coûts par Artiste',
            xaxis_title='Artistes',
            yaxis_title='Montant ($)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#ff0000',
                borderwidth=1,
                font=dict(color='white', size=12)
            ),
            xaxis=dict(tickfont=dict(size=10), gridcolor='#333333'),
            yaxis=dict(tickfont=dict(size=10), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_marketing_analysis(self):
        """Analyse des stratégies marketing"""
        st.markdown('<h3 class="section-title">🎯 ANALYSE DES STRATÉGIES MARKETING</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="subsection-title">📢 Budgets Marketing</div>', unsafe_allow_html=True)
            self.create_marketing_budget_chart()
        
        with col2:
            st.markdown('<div class="subsection-title">🎪 Canaux de Distribution</div>', unsafe_allow_html=True)
            self.create_marketing_channels_analysis()
        
        # Analyse détaillée par stratégie
        st.markdown('<div class="subsection-title">🔍 Analyse par Stratégie Marketing</div>', unsafe_allow_html=True)
        self.create_detailed_marketing_analysis()

    def create_marketing_budget_chart(self):
        """Graphique des budgets marketing"""
        artists = list(self.marketing_data.keys())
        budget_ratios = [self.marketing_data[artist]['budget_ratio'] for artist in artists]
        succes = [10 if self.marketing_data[artist]['succes'] == 'Légendaire' else 
                 9 if self.marketing_data[artist]['succes'] == 'Exceptionnel' else
                 8 if self.marketing_data[artist]['succes'] == 'Mythique' else
                 7 if self.marketing_data[artist]['succes'] == 'Bon' else
                 6 if self.marketing_data[artist]['succes'] == 'Modéré' else
                 5 for artist in artists]
        
        fig = go.Figure()
        
        for i, artist in enumerate(artists):
            fig.add_trace(go.Scatter(
                x=[budget_ratios[i]],
                y=[succes[i]],
                mode='markers+text',
                marker=dict(
                    size=80, 
                    color=self.color_palette[artist], 
                    opacity=0.9,
                    line=dict(width=3, color='#ffffff')
                ),
                text=[artist],
                textposition="middle center",
                textfont=dict(color='white', size=10, weight='bold'),
                name=artist
            ))
        
        fig.update_layout(
            title='Budget Marketing vs Succès Commercial',
            xaxis_title='Ratio Budget Marketing (%)',
            yaxis_title='Niveau de Succès (1-10)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            showlegend=False,
            xaxis=dict(range=[10, 35], tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(range=[4, 11], tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_marketing_channels_analysis(self):
        """Analyse des canaux marketing"""
        # Compter les canaux les plus utilisés
        canaux_count = {}
        for artist_data in self.marketing_data.values():
            for canal in artist_data['canaux']:
                canaux_count[canal] = canaux_count.get(canal, 0) + 1
        
        canaux = list(canaux_count.keys())
        counts = list(canaux_count.values())
        
        fig = go.Figure(go.Bar(
            x=counts,
            y=canaux,
            orientation='h',
            marker_color='#ff69b4',
            text=counts,
            textposition='auto',
            textfont=dict(color='white', size=12, weight='bold')
        ))
        
        fig.update_layout(
            title='Canaux Marketing les Plus Utilisés',
            xaxis_title="Nombre d'artistes utilisant le canal",
            yaxis_title='Canaux Marketing',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_detailed_marketing_analysis(self):
        """Analyse marketing détaillée"""
        artists = list(self.marketing_data.keys())
        tabs = st.tabs(artists)
        
        for i, artist in enumerate(artists):
            with tabs[i]:
                couleur = self.color_palette[artist]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Stratégie marketing
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, {couleur}20 0%, {couleur}05 100%); padding: 1rem; border-radius: 8px; border-left: 5px solid {couleur}; margin-bottom: 1rem;">
                        <div style="color: {couleur}; font-weight: bold; font-size: 1.5rem; margin-bottom: 0.5rem;">{artist}</div>
                        <div style="color: #cccccc; font-size: 1.1rem; font-weight: 500;">Stratégie Marketing</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.metric("Stratégie", self.marketing_data[artist]['strategie'])
                    st.metric("Budget Ratio", f"{self.marketing_data[artist]['budget_ratio']}%")
                    st.metric("Succès", self.marketing_data[artist]['succes'])
                    
                    # Cibles
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; margin-top: 1rem; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Public Cible:</div>
                        <div style="color: #ffffff; font-weight: 500;">{self.marketing_data[artist]['cibles']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Canaux utilisés
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Canaux Principaux:</div>
                        <ul style="color: #ffffff; font-weight: 500;">
                    """, unsafe_allow_html=True)
                    
                    for canal in self.marketing_data[artist]['canaux']:
                        st.markdown(f"<li>{canal}</li>", unsafe_allow_html=True)
                    
                    st.markdown("</ul></div>", unsafe_allow_html=True)
                    
                    # Innovations
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; margin-top: 1rem; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Innovations:</div>
                        <div style="color: #ffffff; font-weight: 500;">{self.marketing_data[artist]['innovations']}</div>
                    </div>
                    """, unsafe_allow_html=True)

    def create_management_analysis(self):
        """Analyse de la gestion et management"""
        st.markdown('<h3 class="section-title">🏢 ANALYSE DE LA GESTION</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="subsection-title">📊 Structure Organisationnelle</div>', unsafe_allow_html=True)
            self.create_org_structure()
        
        with col2:
            st.markdown('<div class="subsection-title">💼 Modèle Économique</div>', unsafe_allow_html=True)
            self.create_economic_model()
        
        # Analyse SWOT
        st.markdown('<div class="subsection-title">🔍 Analyse SWOT du Label</div>', unsafe_allow_html=True)
        self.create_swot_analysis()

    def create_org_structure(self):
        """Structure organisationnelle"""
        # Créer un graphique pour la structure organisationnelle
        fig = go.Figure()
        
        # Ajouter les données pour l'organigramme
        fig.add_trace(go.Scatter(
            x=[1, 2, 3, 4],
            y=[1, 1, 1, 1],
            mode='markers+text',
            marker=dict(
                size=[40, 30, 30, 30],
                color=['#ff0000', '#4169e1', '#ffd700', '#ff69b4'],
                opacity=0.9,
                line=dict(width=2, color='#ffffff')
            ),
            text=['Direction', 'A&R', 'Production', 'Marketing'],
            textposition="middle center",
            textfont=dict(color='white', size=12, weight='bold'),
            showlegend=False
        ))
        
        # Ajouter les lignes de connexion
        fig.add_shape(type="line", x0=1, y0=1, x1=4, y1=1, line=dict(color="#ffffff", width=2))
        
        fig.update_layout(
            title='Structure Organisationnelle',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=300,
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Construire la liste des départements en HTML
        departments_html = "".join([f"<li>{dept}</li>" for dept in self.management_data['structure']['departements']])
        
        # Construire le HTML final en une seule chaîne propre
        html_card = f"""
        <div class="academic-card">
            <h4 style="color: #ffffff; text-align: center; font-weight: bold;">🏗️ STRUCTURE ORGANISATIONNELLE</h4>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                <div style="font-weight: 500;">
                    <strong style="color: #ff0000;">Type:</strong> {self.management_data['structure']['type']}
                </div>
                <div style="font-weight: 500;">
                    <strong style="color: #ff0000;">Effectif:</strong> {self.management_data['structure']['effectif']} personnes
                </div>
            </div>
            
            <div style="margin-top: 1rem;">
                <strong style="color: #ff0000;">Départements:</strong>
                <ul style="color: #ffffff; font-weight: 500;">
                    {departments_html}
                </ul>
            </div>
            
            <div style="margin-top: 1rem;">
                <strong style="color: #ff0000;">Culture d'entreprise:</strong>
                <div style="color: #ffffff; font-weight: 500;">{self.management_data['structure']['culture_entreprise']}</div>
            </div>
        </div>
        """
        
        # Afficher le HTML avec le composant dédié
        components.html(html_card, height=250)

    def create_economic_model(self):
        """Modèle économique"""
        # Créer un graphique pour le modèle économique
        categories = ['Revenus', 'Coûts', 'Marge', 'Réinvestissement']
        valeurs = [100, 75, 25, 20]  # Valeurs en pourcentage
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=categories,
            y=valeurs,
            marker_color=['#ff0000', '#4169e1', '#ffd700', '#ff69b4'],
            text=[f"{v}%" for v in valeurs],
            textposition='auto',
            textfont=dict(color='white', size=12, weight='bold')
        ))
        
        fig.update_layout(
            title='Répartition Économique',
            xaxis_title='Catégories',
            yaxis_title='Pourcentage (%)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=300,
            showlegend=False,
            xaxis=dict(tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Construire le HTML final en une seule chaîne propre
        html_card = f"""
        <div class="academic-card">
            <h4 style="color: #ffffff; text-align: center; font-weight: bold;">💼 MODÈLE ÉCONOMIQUE</h4>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                <div style="font-weight: 500;">
                    <strong style="color: #4169e1;">Modèle:</strong> {self.management_data['finances']['model_economique']}
                </div>
                <div style="font-weight: 500;">
                    <strong style="color: #4169e1;">Marge nette:</strong> {self.management_data['finances']['marge_nette']}
                </div>
            </div>
            
            <div style="margin-top: 1rem;">
                <strong style="color: #4169e1;">Investissement:</strong>
                <div style="color: #ffffff; font-weight: 500;">{self.management_data['finances']['investissement_artistes']}</div>
            </div>
            
            <div style="margin-top: 1rem;">
                <strong style="color: #4169e1;">Gestion du risque:</strong>
                <div style="color: #ffffff; font-weight: 500;">{self.management_data['finances']['risque']}</div>
            </div>
        </div>
        """
        
        # Afficher le HTML avec le composant dédié
        components.html(html_card, height=250)

    def create_swot_analysis(self):
        """Analyse SWOT"""
        # Créer un graphique radar pour l'analyse SWOT
        categories = ['Forces', 'Faiblesses', 'Opportunités', 'Menaces']
        valeurs = [9, 6, 7, 8]  # Scores sur 10
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=valeurs + [valeurs[0]],
            theta=categories + [categories[0]],
            fill='toself',
            line=dict(color='#ff0000', width=3),
            marker=dict(size=8, color='#ff0000'),
            name='Analyse SWOT'
        ))
        
        fig.update_layout(
            polar=dict(
                bgcolor='#1a1a1a',
                radialaxis=dict(
                    visible=True, 
                    range=[0, 10],
                    gridcolor='#333333',
                    tickfont=dict(color='#ffffff', size=12),
                    linecolor='#444444'
                ),
                angularaxis=dict(
                    gridcolor='#333333',
                    tickfont=dict(color='#ffffff', size=12),
                    linecolor='#444444'
                )
            ),
            paper_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            showlegend=False,
            height=400,
            title="Analyse SWOT du Label"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Afficher les détails de l'analyse SWOT
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="academic-card dre-card">
                <h4 style="color: #ff0000; text-align: center; font-weight: bold;">FORCES</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>Talents légendaires</li>
                    <li>Innovation sonore (G-funk)</li>
                    <li>Impact culturel majeur</li>
                    <li>Reconnaissance mondiale</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="academic-card snoop-card">
                <h4 style="color: #4169e1; text-align: center; font-weight: bold;">FAIBLESSES</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>Gestion controversée</li>
                    <li>Instabilité structurelle</li>
                    <li>Conflits internes</li>
                    <li>Problèmes légaux</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="academic-card tupac-card">
                <h4 style="color: #ffd700; text-align: center; font-weight: bold;">OPPORTUNITÉS</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>Rééditions et compilations</li>
                    <li>Documentaires et biopics</li>
                    <li>Marché de la nostalgie</li>
                    <li>Partenariats stratégiques</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="academic-card daz-card">
                <h4 style="color: #ff69b4; text-align: center; font-weight: bold;">MENACES</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>Concurrence moderne</li>
                    <li>Évolution du hip-hop</li>
                    <li>Changements de consommation</li>
                    <li>Perte de pertinence</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    def create_timeline_analysis(self):
        """Analyse chronologique"""
        st.markdown('<h3 class="section-title">📅 ANALYSE CHRONOLOGIQUE</h3>', unsafe_allow_html=True)
        
        # Créer un DataFrame pour la timeline
        df_timeline = pd.DataFrame(self.timeline_data)
        
        fig = go.Figure()
        
        # Ajouter les événements par type
        for event_type in df_timeline['type'].unique():
            df_type = df_timeline[df_timeline['type'] == event_type]
            fig.add_trace(go.Scatter(
                x=df_type['annee'],
                y=df_type['importance'],
                mode='markers+text',
                marker=dict(
                    size=df_type['importance'] * 8,
                    color=self.data_colors.get(event_type, '#ffffff'),
                    opacity=0.8,
                    line=dict(width=2, color='#ffffff')
                ),
                text=df_type['evenement'],
                textposition="top center",
                textfont=dict(color='white', size=10),
                name=event_type,
                showlegend=True
            ))
        
        fig.update_layout(
            title='Timeline Événements Clés du Label',
            xaxis_title='Année',
            yaxis_title='Importance (1-10)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=500,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#ff0000',
                borderwidth=1,
                font=dict(color='white', size=12)
            ),
            xaxis=dict(range=[1990, 2020], tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(range=[0, 11], tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Tableau détaillé des événements
        st.markdown('<div class="subsection-title">📋 Détail des Événements</div>', unsafe_allow_html=True)
        
        # Formatage du tableau avec style
        st.markdown("""
        <style>
            .event-table {
                background-color: #1a1a1a;
                border-radius: 8px;
                padding: 1rem;
                margin-top: 1rem;
            }
            .event-row {
                display: grid;
                grid-template-columns: 80px 150px 1fr 100px;
                gap: 1rem;
                padding: 0.5rem 0;
                border-bottom: 1px solid #333333;
                color: #ffffff;
            }
            .event-header {
                font-weight: bold;
                color: #ff0000;
                border-bottom: 2px solid #ff0000;
                padding-bottom: 0.5rem;
            }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="event-table">', unsafe_allow_html=True)
        st.markdown('<div class="event-row event-header"><div>Année</div><div>Type</div><div>Événement</div><div>Importance</div></div>', unsafe_allow_html=True)
        
        for event in self.timeline_data:
            color = self.data_colors.get(event['type'], '#ffffff')
            st.markdown(f"""
            <div class="event-row">
                <div style="color: {color}; font-weight: bold;">{event['annee']}</div>
                <div style="color: {color};">{event['type']}</div>
                <div>{event['evenement']}</div>
                <div style="color: {color};">{'⭐' * event['importance']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    def create_conclusions(self):
        """Conclusions et recommandations"""
        st.markdown('<h3 class="section-title">📝 CONCLUSIONS ET RECOMMANDATIONS</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="academic-card dre-card">
                <h4 style="color: #ff0000; text-align: center; font-weight: bold;">🎯 POINTS CLÉS</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>Death Row a révolutionné le hip-hop des années 90</li>
                    <li>Le G-funk a défini une ère musicale</li>
                    <li>Talents exceptionnels malgré une gestion chaotique</li>
                    <li>L'héritage culturel dépasse les problèmes commerciaux</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="academic-card snoop-card">
                <h4 style="color: #4169e1; text-align: center; font-weight: bold;">💡 LEÇONS APPRISES</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>L'importance d'une gestion stable</li>
                    <li>Les relations artistes-labels sont cruciales</li>
                    <li>L'innovation sonore peut créer un héritage durable</li>
                    <li>Les controverses peuvent nuire à la pérennité</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="academic-card tupac-card">
                <h4 style="color: #ffd700; text-align: center; font-weight: bold;">🚀 RECOMMANDATIONS STRATÉGIQUES</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>Valoriser le catalogue historique</li>
                    <li>Créer des éditions deluxe et inédits</li>
                    <li>Développer des partenariats avec les artistes</li>
                    <li>Explorer les opportunités de streaming</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="academic-card daz-card">
                <h4 style="color: #ff69b4; text-align: center; font-weight: bold;">🔮 PERSPECTIVES D'AVENIR</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>Repositionnement comme label de catalogue</li>
                    <li>Opportunités de documentaires et films</li>
                    <li>Collaborations avec artistes contemporains</li>
                    <li>Exploitation de la nostalgie des années 90</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    def run(self):
        """Fonction principale pour exécuter le dashboard"""
        self.display_header()
        
        # Créer les onglets principaux
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🎤 Artistes", 
            "🏭 Production", 
            "🎯 Marketing", 
            "🏢 Gestion", 
            "📅 Timeline", 
            "📝 Conclusions"
        ])
        
        with tab1:
            self.create_artist_analysis()
        
        with tab2:
            self.create_production_analysis()
        
        with tab3:
            self.create_marketing_analysis()
        
        with tab4:
            self.create_management_analysis()
        
        with tab5:
            self.create_timeline_analysis()
        
        with tab6:
            self.create_conclusions()
        
        # Footer
        st.markdown("""
        <div style="text-align: center; margin-top: 3rem; padding: 2rem; background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); border-radius: 10px; border: 1px solid #444444;">
            <p style="color: #ff0000; font-weight: bold; font-size: 1.2rem;">DEATH ROW RECORDS - Dashboard Stratégique</p>
            <p style="color: #cccccc; margin-top: 0.5rem;">Analyse complète 1991-2024 | Label de hip-hop américain</p>
            <p style="color: #999999; margin-top: 1rem; font-size: 0.9rem;">© 2024 - Tous droits réservés</p>
        </div>
        """, unsafe_allow_html=True)

# Point d'entrée principal
if __name__ == "__main__":
    analyzer = DeathRowAnalyzer()
    analyzer.run()