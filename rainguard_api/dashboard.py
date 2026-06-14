# # dashboard.py
# import streamlit as st
# import pandas as pd
# import folium
# from streamlit_folium import st_folium
# from folium.plugins import MarkerCluster, MiniMap, Fullscreen, HeatMap
# from src.camada1_coleta.collectors import carregar_dados_simulados
# from src.camada2_processamento.preprocessing import limpar_dados, engenharia_atributos
# from src.camada3_ia.kmeans_clustering import agrupar_regioes
# from src.camada4_alertas.alert_system import emitir_alerta, NIVEIS
# import altair as alt
# import json
# from datetime import date, datetime
# from pathlib import Path
# import sys
# import os

# # Adiciona a pasta atual ao caminho de busca do Python
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# # Configurar página
# st.set_page_config(page_title="RainGuard", layout="wide")

# # CSS customizado para a interface
# st.markdown("""
#     <style>
#         @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
#         /* Cores de fundo e texto global */
#         body, .stApp { background-color: #ffffff !important; }
#         .block-container, .main, .css-1outpf7, .css-18e3th9 { background-color: #ffffff !important; }
#         p, div, span, label, li, td, th { color: #000000 !important; }
#         h1, h2, h3, h4, h5, h6, .stHeader, [data-testid="stHeader"] { color: #000000 !important; }
        
#         /* Abas (tabs) */
#         .stTabs [data-baseweb="tab-list"] button, .stTabs [role="tab"] { color: #000000 !important; }
#         [data-testid="stTabs"] { color: #000000 !important; }
        
#         /* Input fields, select, multiselect */
#         input, select, textarea, [data-testid="stTextInput"], [data-testid="stSelectbox"], [data-testid="stMultiSelect"] { color: #000000 !important; }
        
#         /* Checkboxes, radios, sliders */
#         [data-testid="stCheckbox"], [data-testid="stRadio"], [data-testid="stSlider"] { color: #000000 !important; }
#         label { color: #000000 !important; }
        
#         /* Expandable sections */
#         [data-testid="stExpander"] { color: #000000 !important; }
        
#         /* Captions */
#         .caption, [data-testid="stCaption"] { color: #000000 !important; }
        
#         /* Tabelas */
#         table, [data-testid="stDataFrame"] { color: #000000 !important; }
        
#         /* Rainguard custom */
#         .rainguard-title { font-family: 'Inter', sans-serif; font-size: 3.4rem; font-weight: 800; text-align: center; margin: 18px 0 6px; letter-spacing: 1.8px; color: #0d3b66; }
#         .rain-word { color: #ffffff; background: linear-gradient(90deg,#0d3b66 0%, #1f4e7f 100%); padding: 6px 12px; border-radius: 6px; margin-right:6px; }
#         .guard-word { color: #0d3b66; }
#         .title-text { display: block; text-transform: uppercase; font-size: 1.05rem; letter-spacing: 4px; color: #1f4e7f; margin-top: 8px; text-align:center; }
        
#         /* Stats e cards */
#         .stats-container{ display:flex; flex-wrap:wrap; justify-content:space-between; margin:28px 0; gap:18px; }
#         .stat-card{ background: rgba(255,255,255,0.92); color:#000000; padding:22px 20px; border-radius:18px; text-align:center; flex:1 1 220px; min-width:220px; box-shadow:0 18px 34px rgba(15,40,75,0.08); border:1px solid rgba(15,40,75,0.08); }
#         .stat-number{ font-size:2.4em; font-weight:800; margin:10px 0; letter-spacing: -0.02em; color: #000000; }
#         .stat-label{ font-size:1.05em; opacity:0.84; letter-spacing:0.3px; color: #000000; }
        
#         /* Legenda */
#         .legend-box{ background: rgba(255,255,255,0.92); padding:18px; border-radius:16px; margin-top:10px; border:1px solid rgba(15,40,75,0.08); box-shadow:0 14px 26px rgba(15,40,75,0.06); }
#         .legend-item{ margin:12px 0; font-weight:600; font-size:1.05em; color: #000000; }
        
#         /* Créditos */
#         .credit-section { background: rgba(255,255,255,0.92); padding: 26px; border-radius: 18px; box-shadow: 0 16px 34px rgba(15,40,75,0.08); border:1px solid rgba(15,40,75,0.08); }
#         .credit-heading { font-family: 'Inter', sans-serif; font-size: 1.75rem; font-weight: 700; color: #000000; margin-bottom: 14px; }
#         .credit-text { font-family: 'Inter', sans-serif; font-size: 1.03rem; line-height: 1.75; color: #000000; }
#         .credit-text strong { color: #000000; }
#         .credit-list { margin-top: 18px; padding-left: 1.3rem; color: #000000; }
#         .credit-list li { margin-bottom: 12px; color: #000000; }
#         .credit-list li code { font-size: 0.95rem; background: rgba(16,55,92,0.06); padding: 2px 6px; border-radius: 6px; color: #000000; }
        
#         /* Mapa */
#         .leaflet-container, .folium-map, iframe { border-radius:16px; }
        
#         /* Métricos */
#         .stMetric, [data-testid="stMetric"] { border-radius:14px; padding:10px; background: rgba(255,255,255,0.92); box-shadow:0 14px 26px rgba(15,40,75,0.06); color: #000000; }
        
#         /* --- ESTILIZAÇÃO CUSTOMIZADA DO BOTÃO DE ALERTA (ABA 3) --- */
#         div.stButton > button {
#             font-family: 'Inter', sans-serif !important;
#             font-size: 1.15rem !important;
#             font-weight: 700 !important;
#             padding: 14px 28px !important;
#             border-radius: 12px !important;
#             border: none !important;
#             transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
#             box-shadow: 0 4px 12px rgba(13, 59, 102, 0.15) !important;
#             text-transform: uppercase !important;
#             letter-spacing: 1px !important;
#             cursor: pointer !important;
#         }
        
#         /* Efeito Hover Geral */
#         div.stButton > button:hover {
#             transform: translateY(-2px) !important;
#             box-shadow: 0 8px 20px rgba(13, 59, 102, 0.25) !important;
#         }
        
#         /* Efeito Clique */
#         div.stButton > button:active {
#             transform: translateY(1px) !important;
#         }
        
#         /* Forçar largura máxima em blocos verticais */
#         div[data-testid="stVerticalBlockBorderWrapper"] button {
#             width: 100% !important;
#         }
#     </style>
    
#     <div class="rainguard-title"><span class="rain-word">RAIN</span><span class="guard-word">GUARD</span></div>
#     <div class="title-text">SISTEMA INTELIGENTE DE PREVISÃO E ALERTA DE ENCHENTES</div>
# """, unsafe_allow_html=True)

# # Processamento inicial dos dados via Pipeline
# df = agrupar_regioes(engenharia_atributos(limpar_dados(carregar_dados_simulados())))

# # Criar coluna `local` legível a partir da latitude/longitude
# import_types = False
# try:
#     import reverse_geocoder as rg  # offline, sem API key
#     import_types = True
# except Exception:
#     import_types = False

# # converter para float por precaução
# coords = list(zip(df['latitude'].astype(float), df['longitude'].astype(float)))

# if import_types:
#     try:
#         # for cloud environments, force single-threaded reverse lookup to avoid multiprocessing issues
#         rg_results = rg.search(coords, mode=1, verbose=False)
#         df = df.copy()
#         df['local'] = [f"{r.get('name')}, {r.get('admin1')}" for r in rg_results]
#     except Exception:
#         df = df.copy()
#         df['local'] = df.apply(lambda r: f"Região ({r['latitude']:.4f}, {r['longitude']:.4f})", axis=1)
#         st.warning("Não foi possível usar reverse_geocoder no modo offline; exibindo coordenadas brutas.")
# else:
#     df = df.copy()
#     df['local'] = df.apply(lambda r: f"Região ({r['latitude']:.4f}, {r['longitude']:.4f})", axis=1)
#     st.warning("Biblioteca 'reverse_geocoder' não encontrada. 'local' contém coordenadas. Para nomes reais, instale: pip install reverse_geocoder")


# # Calcular estatísticas volumétricas dos Clusters do K-means
# stats_critico = len(df[df["cluster_label"] == "Risco Crítico"])
# stats_alto = len(df[df["cluster_label"] == "Risco Alto"])
# stats_medio = len(df[df["cluster_label"] == "Risco Médio"])
# stats_baixo = len(df[df["cluster_label"] == "Risco Baixo"])

# # Exibir estatísticas nos Cards Superiores
# st.markdown("""
#     <div class="stats-container">
#         <div class="stat-card" style="background: linear-gradient(135deg, #FF4444 0%, #CC0000 100%);">
#             <div class="stat-label" style="color: white !important;">🔴 Risco Crítico</div>
#             <div class="stat-number" style="color: white !important;">""" + str(stats_critico) + """</div>
#         </div>
#         <div class="stat-card" style="background: linear-gradient(135deg, #FF9900 0%, #FF6600 100%);">
#             <div class="stat-label" style="color: white !important;">🟠 Risco Alto</div>
#             <div class="stat-number" style="color: white !important;">""" + str(stats_alto) + """</div>
#         </div>
#         <div class="stat-card" style="background: linear-gradient(135deg, #E6BE00 0%, #D4A300 100%); color: black;">
#             <div class="stat-label">🟡 Risco Médio</div>
#             <div class="stat-number">""" + str(stats_medio) + """</div>
#         </div>
#         <div class="stat-card" style="background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%); color: black;">
#             <div class="stat-label">🟢 Risco Baixo</div>
#             <div class="stat-number">""" + str(stats_baixo) + """</div>
#         </div>
#     </div>
# """, unsafe_allow_html=True)

# cor_map = {"Risco Crítico": "red", "Risco Alto": "orange", "Risco Médio": "yellow", "Risco Baixo": "green"}

# cluster_to_alert_level = {
#     "Risco Crítico": "Vermelho",
#     "Risco Alto": "Laranja",
#     "Risco Médio": "Amarelo",
#     "Risco Baixo": "Verde"
# }

# # Criar abas para organizar o conteúdo
# tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Mapa de Riscos", "📊 Dados Detalhados", "🚨 Disparar Alerta", "🧾 Créditos"])

# with tab1:
#     col1, col2 = st.columns([0.7, 6.5])
    
#     with col1:
#         st.subheader("📍 Legenda de Riscos")
#         st.markdown("""
#             <div class="legend-box">
#                 <div class="legend-item" style="color: red;">🔴 Risco Crítico</div>
#                 <div class="legend-item" style="color: orange;">🟠 Risco Alto</div>
#                 <div class="legend-item" style="color: black;">🟡 Risco Médio</div>
#                 <div class="legend-item" style="color: black;">🟢 Risco Baixo</div>
#             </div>
#         """, unsafe_allow_html=True)
        
#         st.markdown("---")
#         st.subheader("📊 Resumo")
#         st.metric("Total de Regiões", len(df))
#         st.metric("Precipitação Média", f"{df['precipitacao'].mean():.1f}mm")
#         st.metric("Nível Médio do Rio", f"{df['nivel_rio'].mean():.1f}m")

#     with col2:
#         # Criar mapa base vazio
#         mapa = folium.Map(
#             location=[-23.0, -46.8],
#             zoom_start=8,
#             tiles=None,
#             control=False
#         )

#         # Camada Satélite (Esri) e Camada Clara (Positron) como opções
#         folium.TileLayer(
#             tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
#             attr='Tiles © Esri — Source: Esri, Maxar, Earthstar Geographics, and the GIS User Community',
#             name='Satélite (Esri)',
#             overlay=False,
#             control=True,
#             opacity=0.9
#         ).add_to(mapa)

#         folium.TileLayer(
#             tiles='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
#             attr='CartoDB Positron',
#             name='Claro (Positron)',
#             overlay=False,
#             control=True,
#             opacity=0.9
#         ).add_to(mapa)

#         # Controls: fullscreen, minimap e layer control
#         Fullscreen(position='topright').add_to(mapa)
#         minimap = MiniMap(toggle_display=True, position='bottomright')
#         minimap.add_to(mapa)

#         # Cluster de marcadores para melhorar visualização em áreas densas
#         marker_cluster = MarkerCluster(name='Marcadores').add_to(mapa)

#         # Preparar dados para heatmap
#         try:
#             heat_data = [[row['latitude'], row['longitude'], float(row['precipitacao'])] for _, row in df.iterrows()]
#             HeatMap(heat_data, name='Heatmap (Precipitação)', min_opacity=0.2, radius=25, blur=15, max_zoom=10).add_to(mapa)
#         except Exception:
#             pass

#         # Adicionar marcadores com tooltips e popups detalhados
#         max_prec = float(df['precipitacao'].max()) if not df['precipitacao'].empty else 1.0
#         for _, row in df.iterrows():
#             lat = row['latitude']
#             lon = row['longitude']
#             color = cor_map.get(row['cluster_label'], 'blue')
            
#             try:
#                 radius = 6 + (float(row['precipitacao']) / max_prec) * 18
#             except Exception:
#                 radius = 8

#             popup_html = folium.IFrame(f"<b>{row['local']}</b><br><b>{row['cluster_label']}</b><br>🌧️ Precip: {row['precipitacao']:.1f} mm<br>💧 Rio: {row['nivel_rio']:.1f} m<br>💨 Umid: {row['umidade']:.0f}%", width=220, height=110)
#             popup = folium.Popup(popup_html, max_width=260)

#             tooltip = f"{row['local']} — {row['cluster_label']} — {row['precipitacao']:.1f}mm"

#             folium.CircleMarker(
#                 location=[lat, lon],
#                 radius=radius,
#                 color=color,
#                 fill=True,
#                 fillColor=color,
#                 fillOpacity=0.65,
#                 weight=2,
#                 popup=popup,
#                 tooltip=tooltip
#             ).add_to(marker_cluster)

#         folium.LayerControl(collapsed=False).add_to(mapa)

#         # Ajustar bounds para focar nos pontos automaticamente
#         try:
#             sw = [float(df['latitude'].min()), float(df['longitude'].min())]
#             ne = [float(df['latitude'].max()), float(df['longitude'].max())]
#             mapa.fit_bounds([sw, ne], padding=(30, 30))
#         except Exception:
#             pass

#         st_folium(mapa, width=1550, height=850)

# with tab2:
#     st.subheader("📋 Análise Detalhada por Região")
    
#     chart_df = df[["local", "cluster_label", "precipitacao", "nivel_rio", "umidade", "latitude", "longitude"]].copy()
#     chart_df["precipitacao"] = chart_df["precipitacao"].astype(float)
    
#     # Controles de filtro do Dataframe
#     clusters = chart_df['cluster_label'].unique().tolist()
#     selected_clusters = st.multiselect("Filtrar por nível de risco:", clusters, default=clusters)
#     min_p = float(chart_df['precipitacao'].min())
#     max_p = float(chart_df['precipitacao'].max())
#     precip_range = st.slider("Faixa de precipitação (mm):", min_value=min_p, max_value=max_p, value=(min_p, max_p))
#     search_city = st.text_input("Buscar por cidade (nome ou parte):")

#     # Aplicar filtros dinâmicos
#     filtered = chart_df[
#         (chart_df['cluster_label'].isin(selected_clusters)) &
#         (chart_df['precipitacao'] >= precip_range[0]) &
#         (chart_df['precipitacao'] <= precip_range[1])
#     ].copy()
#     if search_city:
#         filtered = filtered[filtered['local'].str.contains(search_city, case=False, na=False)]

#     # Layout de Gráficos Altair
#     overview_col, map_col = st.columns([1.2, 1])

#     with overview_col:
#         left, right = st.columns(2)
#         with left:
#             st.write("**Distribuição de Riscos (filtrada)**")
#             risk_counts = filtered['cluster_label'].value_counts().reset_index()
#             risk_counts.columns = ['cluster_label', 'count']
#             bar = alt.Chart(risk_counts).mark_bar().encode(
#                 x=alt.X('cluster_label:N', sort='-y', title='Nível'),
#                 y=alt.Y('count:Q', title='Quantidade'),
#                 color=alt.Color('cluster_label:N', legend=None)
#             ).properties(height=300).configure_axis(grid=False)
#             st.altair_chart(bar, width='stretch')
#             st.markdown('**Método:** k-means (clustering)')

#         with right:
#             st.write('**Histograma de Precipitação (filtrada)**')
#             hist = alt.Chart(filtered).mark_bar().encode(
#                 alt.X('precipitacao:Q', bin=alt.Bin(maxbins=30), title='Precipitação (mm)'),
#                 y='count()',
#                 color=alt.Color('cluster_label:N', legend=None)
#             ).properties(height=300).configure_axis(grid=False)
#             st.altair_chart(hist, width='stretch')
#             st.markdown('**Método:** Estatística descritiva (dados brutos)')

#     st.write('**Mapa de Precipitação (dispersão)**')
#     scatter = alt.Chart(filtered).mark_circle(opacity=0.75).encode(
#         x='longitude:Q',
#         y='latitude:Q',
#         size=alt.Size('precipitacao:Q', title='Precipitação (mm)', scale=alt.Scale(range=[20, 800])),
#         color=alt.Color('cluster_label:N', legend=alt.Legend(title='Nível de Risco')),
#         tooltip=['local', 'cluster_label', 'precipitacao']
#     ).properties(height=420).configure_axis(grid=False)
#     st.altair_chart(scatter, width='stretch')
#     st.markdown('**Método:** k-means (clusters) — visualização geoespacial')

#     st.markdown('**Estatísticas (filtradas)**')
#     stats_data = {
#         'Métrica': ['Precipitação Mín', 'Precipitação Máx', 'Precipitação Média', 'Rio Mín', 'Rio Máx', 'Regiões Filtradas'],
#         'Valor': [
#             f"{filtered['precipitacao'].min():.1f}mm" if not filtered.empty else '—',
#             f"{filtered['precipitacao'].max():.1f}mm" if not filtered.empty else '—',
#             f"{filtered['precipitacao'].mean():.1f}mm" if not filtered.empty else '—',
#             f"{filtered['nivel_rio'].min():.1f}m" if not filtered.empty else '—',
#             f"{filtered['nivel_rio'].max():.1f}m" if not filtered.empty else '—',
#             f"{len(filtered)}"
#         ]
#     }
#     st.dataframe(pd.DataFrame(stats_data), width='stretch')

#     st.divider()
#     with st.expander('Tabela (dados filtrados) - mostrar/ocultar'):
#         st.dataframe(filtered[['local', 'cluster_label', 'precipitacao', 'nivel_rio', 'umidade', 'latitude', 'longitude']], width='stretch')

# with tab3:
#     st.subheader("🚨 Disparar Alerta via WhatsApp")
#     st.caption("O disparo automático foi desativado. Selecione a região abaixo para efetuar o envio manual imediato.")
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.write("**Selecione a Região Alvo**")
        
#         # Obter regiões mapeadas para alimentar a seleção
#         regioes_unicas = df[["local", "latitude", "longitude"]].drop_duplicates().reset_index(drop=True)
#         opcoes_regiao = [f"{row['local']} ({row['latitude']:.2f}, {row['longitude']:.2f})" for _, row in regioes_unicas.iterrows()]
        
#         indice_regiao = st.selectbox(
#             "Escolha uma região para notificação:",
#             range(len(opcoes_regiao)),
#             format_func=lambda x: opcoes_regiao[x],
#             key="regiao_select"
#         )
        
#         regiao_info = regioes_unicas.iloc[indice_regiao]
        
#         st.write("**Nível de Alerta Mapeado**")
#         st.caption("Definido de forma inteligente com base no agrupamento do algoritmo estatístico K-means.")
    
#     with col2:
#         st.write("**Métricas em Tempo Real**")
        
#         regiao_dados = df[
#             (df["latitude"] == regiao_info["latitude"]) &
#             (df["longitude"] == regiao_info["longitude"])
#         ]
        
#         if not regiao_dados.empty:
#             row = regiao_dados.iloc[0]
#             alert_level = cluster_to_alert_level.get(row['cluster_label'], 'Verde')
#             alert_info = NIVEIS.get(alert_level, NIVEIS['Verde'])
            
#             # Sub-colunas para métricas limpas e alinhadas
#             m1, m2, m3 = st.columns(3)
#             m1.metric("Precipitação", f"{row['precipitacao']:.1f}mm")
#             m2.metric("Nível do Rio", f"{row['nivel_rio']:.1f}m")
#             m3.metric("Umidade", f"{row['umidade']:.0f}%")
            
#             # Painel visual colorido do nível de risco mapeado
#             bg_color = cor_map.get(row['cluster_label'], 'green')
#             text_color = 'black' if bg_color in ('yellow', '#DAA520', '#FFD700', 'lightyellow') else 'white'
#             st.markdown(
#                 f"""
#                 <div style="background: {bg_color}; padding: 16px; border-radius: 12px; color: {text_color}; margin-top: 10px; box-shadow: inset 0 0 10px rgba(0,0,0,0.05);">
#                     <div style="display:flex; align-items:center; gap:14px;">
#                         <div style="font-size:32px; font-weight:700; line-height:1;">{alert_info['cor']}</div>
#                         <div>
#                             <div style="font-size:18px; font-weight:800; letter-spacing:0.5px; color: {text_color} !important;">ALERTA {alert_level.upper()}</div>
#                             <div style="font-size:13px; opacity:0.9; font-weight:500; color: {text_color} !important;">Status: {row['cluster_label']} — {alert_info['acao']}</div>
#                         </div>
#                     </div>
#                 </div>
#                 """,
#                 unsafe_allow_html=True
#             )
            
#     st.markdown("<br>", unsafe_allow_html=True)

#     # --- MAPEAMENTO E INJEÇÃO CORES DINÂMICAS DO BOTÃO ---
#     btn_color_map = {
#         "Vermelho": {"bg": "#DC3545", "hover": "#B52A37", "text": "#FFFFFF"},
#         "Laranja": {"bg": "#FD7E14", "hover": "#E06608", "text": "#FFFFFF"},
#         "Amarelo": {"bg": "#FFC107", "hover": "#E0A800", "text": "#000000"},
#         "Verde": {"bg": "#28A745", "hover": "#218838", "text": "#FFFFFF"}
#     }
    
#     colors = btn_color_map.get(alert_level, {"bg": "#0d3b66", "hover": "#1f4e7f", "text": "#FFFFFF"})

#     st.markdown(f"""
#         <style>
#         div.stButton > button {{
#             background-color: {colors['bg']} !important;
#             color: {colors['text']} !important;
#         }}
#         div.stButton > button:hover {{
#             background-color: {colors['hover']} !important;
#             color: {colors['text']} !important;
#         }}
#         </style>
#     """, unsafe_allow_html=True)

#     # --- EXECUÇÃO DO DISPARO ---
#     if not regiao_dados.empty:
#         botao_texto = f"Disparar Alerta {alert_level.upper()} — Notificar {row['local']}"
        
#         if st.button(f"🚀 {botao_texto}", use_container_width=True):
#             dados_alerta = {
#                 "precipitacao": row["precipitacao"],
#                 "nivel_rio": row["nivel_rio"],
#                 "umidade": row["umidade"]
#             }
#             try:
#                 with st.spinner("📤 Conectando à API do Twilio e transmitindo mensagens de contingência..."):
#                     mensagem = emitir_alerta(
#                         regiao_id=f"{row['local']} ({regiao_info['latitude']:.4f}, {regiao_info['longitude']:.4f})",
#                         nivel=alert_level,
#                         dados=dados_alerta
#                     )
#                 st.success(f"✅ Alerta de nível [{alert_level.upper()}] transmitido com sucesso aos canais de emergência!")
                
#                 with st.expander("📄 Visualizar Relatório de Envio (Log)", expanded=True):
#                     st.code(mensagem, language="text")
                    
#             except Exception as e:
#                 st.error(f"❌ Falha crítica ao executar o disparo: {str(e)}")
#     else:
#         st.warning("⚠️ Selecione uma região válida para habilitar os protocolos de disparo.")

# with tab4:
#     st.title("🧾 Créditos")
#     st.markdown("""
#     <div class="credit-section">
#         <div class="credit-heading">O que foi feito com os dados</div>
#         <div class="credit-text">
#             <ul class="credit-list">
#                 <li><strong>Coleta e limpeza:</strong> os dados simulados foram carregados e limpos para remover valores inválidos ou faltantes.</li>
#                 <li><strong>Engenharia de atributos:</strong> novos atributos foram criados para melhorar a análise de risco.</li>
#                 <li><strong>Clusterização:</strong> <code>k-means</code> foi usado para agrupar as regiões em níveis de risco com base em precipitação, umidade e nível do rio.</li>
#                 <li><strong>Visualização:</strong> foram gerados mapas interativos e gráficos para mostrar a distribuição de risco e os pontos críticos.</li>
#                 <li><strong>Alerta inteligente:</strong> o sistema converte o resultado do clustering em alertas de cor e recomendações de ação.</li>
#             </ul>
#         </div>
#     </div>

#     <div class="credit-section" style="margin-top: 24px;">
#         <div class="credit-heading">Vantagens do sistema</div>
#         <div class="credit-text">
#             <ul class="credit-list">
#                 <li>Identifica com antecedência as regiões mais vulneráveis a enchentes.</li>
#                 <li>Permite análise comparativa entre diferentes áreas e condições climáticas.</li>
#                 <li>Oferece monitoramento de indicadores-chave (precipitação, umidade e nível do rio).</li>
#                 <li>Elimina disparos falsos e automatizados indesejados através de controle por clique manual.</li>
#                 <li>Facilita a tomada de decisão rápida com uma interface clara e interativa.</li>
#             </ul>
#         </div>
#     </div>

#     <div class="credit-section" style="margin-top: 24px;">
#         <div class="credit-heading">Criadores</div>
#         <div class="credit-text">
#             <ul class="credit-list">
#                 <li>Cristiano Alves Barbosa</li>
#                 <li>Joana da Silva Andrade Dias</li>
#                 <li>Vinicius Costa Vieira Hodos</li>
#                 <li>Julia Beatriz Crispim</li>
#             </ul>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)


import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from src.camada1_coleta.collectors import carregar_dados_simulados
from src.camada2_processamento.preprocessing import limpar_dados, engenharia_atributos
from src.camada3_ia.kmeans_clustering import agrupar_regioes
from src.camada4_alertas.alert_system import emitir_alerta, NIVEIS
import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
st.set_page_config(page_title="RainGuard", layout="wide")

# Estado de sessão para dados em tempo real
if 'live_p' not in st.session_state:
    st.session_state.live_p = None
    st.session_state.live_r = None
    st.session_state.live_u = None

# --- CSS INTEGRADO E TÍTULO ORIGINAL ---
st.markdown("""
    <style>
        .rainguard-title { font-family: 'Inter', sans-serif; font-size: 3.4rem; font-weight: 800; text-align: center; margin: 18px 0 6px; letter-spacing: 1.8px; color: #0d3b66; }
        .rain-word { color: #ffffff; background: linear-gradient(90deg,#0d3b66 0%, #1f4e7f 100%); padding: 6px 12px; border-radius: 6px; margin-right:6px; }
        .guard-word { color: #0d3b66; }
        .title-text { display: block; text-transform: uppercase; font-size: 1.05rem; letter-spacing: 4px; color: #1f4e7f; margin-top: 8px; text-align:center; }
        .stats-container{ display:flex; flex-wrap:wrap; justify-content:space-between; margin:28px 0; gap:18px; }
        .stat-card{ background: rgba(255,255,255,0.92); padding:22px 20px; border-radius:18px; text-align:center; flex:1 1 220px; box-shadow:0 18px 34px rgba(15,40,75,0.08); border:1px solid rgba(15,40,75,0.08); }
        .stat-number{ font-size:2.4em; font-weight:800; margin:10px 0; color: #000000; }
        .legend-box{ background: white; padding:18px; border-radius:16px; border:1px solid #ddd; }
    </style>
""", unsafe_allow_html=True)

# Título e Subtítulo restaurados
st.markdown('''
    <div class="rainguard-title"><span class="rain-word">RAIN</span><span class="guard-word">GUARD</span></div>
    <div class="title-text">SISTEMA INTELIGENTE DE PREVISÃO E ALERTA DE ENCHENTES</div>
''', unsafe_allow_html=True)

# Processamento
df = agrupar_regioes(engenharia_atributos(limpar_dados(carregar_dados_simulados())))
df['local'] = df.apply(lambda r: f"Região ({r['latitude']:.4f}, {r['longitude']:.4f})", axis=1)

# --- CARDS DE ESTATÍSTICAS ---
if st.session_state.live_p is not None:
    st.markdown(f"""
    <div class="stats-container">
        <div class="stat-card" style="background:#0d3b66; color:white;"><div class="stat-number" style="color:white;">{st.session_state.live_p:.1f}mm</div><div>Precipitação Atual</div></div>
        <div class="stat-card" style="background:#1f4e7f; color:white;"><div class="stat-number" style="color:white;">{st.session_state.live_r:.1f}m</div><div>Nível do Rio</div></div>
        <div class="stat-card"><div class="stat-number">{st.session_state.live_u:.0f}%</div><div>Umidade</div></div>
        <div class="stat-card"><div class="stat-number">✅</div><div>Status: Online</div></div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="stats-container">
        <div class="stat-card" style="background: linear-gradient(135deg, #FF4444 0%, #CC0000 100%); color:white;">
            <div class="stat-number" style="color:white;">""" + str(len(df[df["cluster_label"] == "Risco Crítico"])) + """</div><div>🔴 Risco Crítico</div>
        </div>
        <div class="stat-card" style="background: linear-gradient(135deg, #FF9900 0%, #FF6600 100%); color:white;">
            <div class="stat-number" style="color:white;">""" + str(len(df[df["cluster_label"] == "Risco Alto"])) + """</div><div>🟠 Risco Alto</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">""" + str(len(df[df["cluster_label"] == "Risco Médio"])) + """</div><div>🟡 Risco Médio</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">""" + str(len(df[df["cluster_label"] == "Risco Baixo"])) + """</div><div>🟢 Risco Baixo</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- ABAS ---
tab1, tab2, tab3, tab5, tab4 = st.tabs(["🗺️ Mapa de Riscos", "📊 Dados Detalhados", "🚨 Disparar Alerta", "🌤️ Clima em Tempo Real", "🧾 Créditos"])

with tab1:
    col_leg, col_map = st.columns([1, 4])
    with col_leg:
        st.markdown('<div class="legend-box"><b>Legenda:</b><br><br>🔴 Crítico<br>🟠 Alto<br>🟡 Médio<br>🟢 Baixo</div>', unsafe_allow_html=True)
    with col_map:
        mapa = folium.Map(location=[-23.0, -46.8], zoom_start=8)
        st_folium(mapa, width=1200, height=600)

with tab5:
    st.subheader("Telemetria em Tempo Real")
    regioes = df[["local", "latitude", "longitude"]].drop_duplicates()
    idx = st.selectbox("Selecione a Região:", range(len(regioes)), format_func=lambda x: regioes.iloc[x]['local'])
    if st.button("🛰️ ATUALIZAR DADOS REAIS"):
        r = regioes.iloc[idx]
        url = f"https://api.open-meteo.com/v1/forecast?latitude={r['latitude']}&longitude={r['longitude']}&current=precipitation,relative_humidity_2m"
        data = requests.get(url, timeout=5).json()['current']
        st.session_state.live_p = float(data['precipitation'])
        st.session_state.live_u = float(data['relative_humidity_2m'])
        st.session_state.live_r = 1.2 + (st.session_state.live_p * 0.08)
        st.rerun()
