import streamlit as st
import folium
from streamlit_folium import st_folium
import json, os, sys, random
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style import STYLE, topbar, gauge_html, PORTOS, CORES, LABELS, buscar_porto

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sereias.json")
with open(DATA_PATH, encoding="utf-8") as f:
    sereias = json.load(f)

WORLD_MAP_SVG = """
<div style="position:relative;height:340px;overflow:hidden;background:#0d3352;border-radius:0">
  <svg width="100%" height="100%" viewBox="0 0 600 340" style="position:absolute;inset:0">
    <rect width="600" height="340" fill="#0d3352"/>
    <line x1="0" y1="170" x2="600" y2="170" stroke="rgba(255,255,255,.04)" stroke-width=".5"/>
    <line x1="300" y1="0" x2="300" y2="340" stroke="rgba(255,255,255,.04)" stroke-width=".5"/>
    <path d="M60 40 L140 40 L160 60 L170 100 L150 140 L130 170 L110 180 L90 160 L70 140 L50 120 L45 90 L55 60 Z" fill="#2d5a3d" opacity=".85"/>
    <path d="M120 185 L155 180 L170 200 L175 240 L165 280 L145 300 L125 295 L108 270 L100 240 L105 210 Z" fill="#2d5a3d" opacity=".85"/>
    <path d="M240 30 L290 30 L310 50 L305 80 L285 90 L260 85 L240 70 L235 50 Z" fill="#3a6b47" opacity=".85"/>
    <path d="M250 95 L300 90 L320 110 L325 160 L315 210 L295 240 L270 250 L245 240 L230 210 L225 165 L228 120 Z" fill="#2d5a3d" opacity=".85"/>
    <path d="M310 25 L430 25 L460 45 L470 80 L450 120 L410 140 L370 130 L330 110 L305 85 L300 55 Z" fill="#2d5a3d" opacity=".85"/>
    <path d="M420 200 L475 195 L495 215 L490 255 L465 270 L435 265 L415 245 L410 220 Z" fill="#2d5a3d" opacity=".85"/>
    <path d="M140 145 Q200 130 260 140 Q310 148 340 145" stroke="#0B3954" stroke-width="4" fill="none" stroke-linecap="round"/>
    <path d="M140 145 Q200 130 260 140 Q310 148 340 145" stroke="#4379EE" stroke-width="1.5" fill="none" stroke-dasharray="6 4">
      <animate attributeName="stroke-dashoffset" from="0" to="-24" dur="1.5s" repeatCount="indefinite"/>
    </path>
    <polygon points="270,120 276,132 264,132" fill="#A43955" opacity=".9"/>
    <polygon points="298,118 304,130 292,130" fill="#A43955" opacity=".9"/>
    <rect x="134" y="141" width="12" height="6" rx="2" fill="#0B3954" stroke="#2EB8AC" stroke-width="1"/>
    <circle cx="342" cy="145" r="5" fill="#2EB8AC" opacity=".9"/>
    <circle cx="342" cy="145" r="2" fill="#fff"/>
    <circle cx="200" cy="150" r="30" fill="#A43955" opacity=".06"/>
    <circle cx="320" cy="130" r="25" fill="#F39237" opacity=".06"/>
  </svg>
  <div id="pin1" style="position:absolute;left:30%;top:58%;transform:translate(-50%,-50%);transition:all 3s ease-in-out;cursor:pointer;z-index:10">
    <div style="width:26px;height:26px;border-radius:50%;border:2.5px solid rgba(255,255,255,.3);display:flex;align-items:center;justify-content:center;font-size:12px;background:#A43955;position:relative">🧜
      <div style="position:absolute;inset:-4px;border-radius:50%;border:2px solid #A43955;animation:rp 2s ease-out infinite"></div>
    </div>
    <div style="display:none;position:absolute;bottom:calc(100% + 8px);left:50%;transform:translateX(-50%);background:#0B3954;color:#fff;border-radius:8px;padding:6px 10px;font-size:11px;white-space:nowrap">Merrow · Alto Risco</div>
  </div>
  <div style="position:absolute;left:40%;top:47%;transform:translate(-50%,-50%);transition:all 3s ease-in-out 0.4s;cursor:pointer;z-index:10">
    <div style="width:26px;height:26px;border-radius:50%;border:2.5px solid rgba(255,255,255,.3);display:flex;align-items:center;justify-content:center;font-size:12px;background:#F39237;position:relative">🧜
      <div style="position:absolute;inset:-4px;border-radius:50%;border:2px solid #F39237;animation:rp 2s ease-out .3s infinite"></div>
    </div>
  </div>
  <div style="position:absolute;left:48%;top:50%;transform:translate(-50%,-50%);transition:all 3s ease-in-out 0.8s;cursor:pointer;z-index:10">
    <div style="width:26px;height:26px;border-radius:50%;border:2.5px solid rgba(255,255,255,.3);display:flex;align-items:center;justify-content:center;font-size:12px;background:#2EB8AC;position:relative">🧜
      <div style="position:absolute;inset:-4px;border-radius:50%;border:2px solid #2EB8AC;animation:rp 2s ease-out .6s infinite"></div>
    </div>
  </div>
  <div style="position:absolute;left:22%;top:72%;transform:translate(-50%,-50%);transition:all 3s ease-in-out 1.2s;cursor:pointer;z-index:10">
    <div style="width:26px;height:26px;border-radius:50%;border:2.5px solid rgba(255,255,255,.3);display:flex;align-items:center;justify-content:center;font-size:12px;background:#A43955;position:relative">🧜
      <div style="position:absolute;inset:-4px;border-radius:50%;border:2px solid #A43955;animation:rp 2s ease-out .9s infinite"></div>
    </div>
  </div>
  <div style="position:absolute;left:35%;top:65%;transform:translate(-50%,-50%);transition:all 3s ease-in-out 1.6s;cursor:pointer;z-index:10">
    <div style="width:26px;height:26px;border-radius:50%;border:2.5px solid rgba(255,255,255,.3);display:flex;align-items:center;justify-content:center;font-size:12px;background:#F39237;position:relative">🧜
      <div style="position:absolute;inset:-4px;border-radius:50%;border:2px solid #F39237;animation:rp 2s ease-out 1.2s infinite"></div>
    </div>
  </div>
  <div style="position:absolute;left:55%;top:70%;transform:translate(-50%,-50%);transition:all 3s ease-in-out 2s;cursor:pointer;z-index:10">
    <div style="width:26px;height:26px;border-radius:50%;border:2.5px solid rgba(255,255,255,.3);display:flex;align-items:center;justify-content:center;font-size:12px;background:#2EB8AC;position:relative">🧜
      <div style="position:absolute;inset:-4px;border-radius:50%;border:2px solid #2EB8AC;animation:rp 2s ease-out 1.5s infinite"></div>
    </div>
  </div>
  <div style="position:absolute;left:18%;top:82%;transform:translate(-50%,-50%);transition:all 3s ease-in-out 2.4s;cursor:pointer;z-index:10">
    <div style="width:26px;height:26px;border-radius:50%;border:2.5px solid rgba(255,255,255,.3);display:flex;align-items:center;justify-content:center;font-size:12px;background:#A43955;position:relative">🧜
      <div style="position:absolute;inset:-4px;border-radius:50%;border:2px solid #A43955;animation:rp 2s ease-out 1.8s infinite"></div>
    </div>
  </div>
  <div style="position:absolute;left:60%;top:55%;transform:translate(-50%,-50%);transition:all 3s ease-in-out 2.8s;cursor:pointer;z-index:10">
    <div style="width:26px;height:26px;border-radius:50%;border:2.5px solid rgba(255,255,255,.3);display:flex;align-items:center;justify-content:center;font-size:12px;background:#F39237;position:relative">🧜
      <div style="position:absolute;inset:-4px;border-radius:50%;border:2px solid #F39237;animation:rp 2s ease-out 2.1s infinite"></div>
    </div>
  </div>
  <style>@keyframes rp{0%{transform:scale(1);opacity:.6}100%{transform:scale(1.8);opacity:0}}</style>
</div>
<div style="display:flex;gap:18px;padding:10px 18px;border-top:1px solid var(--border)">
  <div style="display:flex;align-items:center;gap:6px;font-size:12px;color:var(--text-muted)"><div style="width:10px;height:10px;border-radius:50%;background:#A43955"></div>Alto Risco</div>
  <div style="display:flex;align-items:center;gap:6px;font-size:12px;color:var(--text-muted)"><div style="width:10px;height:10px;border-radius:50%;background:#F39237"></div>Risco Médio</div>
  <div style="display:flex;align-items:center;gap:6px;font-size:12px;color:var(--text-muted)"><div style="width:10px;height:10px;border-radius:50%;background:#2EB8AC"></div>Baixo Risco</div>
</div>"""

def sereias_proximas(lat_o, lon_o, lat_d, lon_d, margem=4.0):
    resultado = []
    for s in sereias:
        lat_s, lon_s = s["latitude"], s["longitude"]
        if (min(lat_o,lat_d)-margem <= lat_s <= max(lat_o,lat_d)+margem and
            min(lon_o,lon_d)-margem <= lon_s <= max(lon_o,lon_d)+margem):
            resultado.append(s)
    return resultado

def run():
    st.markdown(STYLE, unsafe_allow_html=True)
    st.markdown(topbar("dashboard"), unsafe_allow_html=True)
    st.markdown('<div class="content">', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Dashboard</div>', unsafe_allow_html=True)

    # ── stat cards ────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="stats-grid">
      <div class="stat-card"><div><div class="stat-label">Sereias Detectadas</div><div class="stat-value">40,689</div><div class="stat-trend trend-down">▼ 4.3% desde semana passada</div></div><div class="stat-icon" style="background:#E1B7ED33">🧜</div></div>
      <div class="stat-card"><div><div class="stat-label">Pessoas Salvas</div><div class="stat-value">10,293</div><div class="stat-trend trend-up">▲ 1.3% da semana passada</div></div><div class="stat-icon" style="background:#8280FF22">🛟</div></div>
      <div class="stat-card"><div><div class="stat-label">Regiões Monitoradas</div><div class="stat-value">156</div><div class="stat-trend trend-up">▲ 8.9% mais regiões</div></div><div class="stat-icon" style="background:#2EB8AC22">🌊</div></div>
      <div class="stat-card"><div><div class="stat-label">Precisão da Solução</div><div class="stat-value">99.984%</div><div class="stat-trend trend-up">▲ 97% de acurácia</div></div><div class="stat-icon" style="background:#4AD99122">📡</div></div>
    </div>""", unsafe_allow_html=True)

    # ── dois mapas lado a lado ────────────────────────────────────────────────
    col1, col2 = st.columns(2)

    # MAPA ESQUERDO — SVG original da Ana Luisa com pins de sereias bem animados - vamos deixar esse
    with col1:
        st.markdown(f"""
        <div class="card">
          <div class="card-header"><span class="card-title">Sereias Mapeadas no Mundo</span></div>
          {WORLD_MAP_SVG}
        </div>""", unsafe_allow_html=True)

    # MAPA DIREITO — Folium real com rota pré-calculada (nosso segredinho)
    with col2:
        st.markdown("""
        <div class="card">
          <div class="card-header"><span class="card-title">Análise de Rota Marítima</span></div>
        """, unsafe_allow_html=True)

        # inputs dentro do card
        c_o, c_d, c_b = st.columns([2, 2, 1])
        with c_o:
            origem_txt = st.text_input("Origem", value="Santos, BR",
                                       placeholder="Ex: Santos", key="dash_origem",
                                       label_visibility="collapsed")
        with c_d:
            destino_txt = st.text_input("Destino", value="Lisboa, PT",
                                        placeholder="Ex: Lisboa", key="dash_destino",
                                        label_visibility="collapsed")
        with c_b:
            calcular = st.button("Analisar 🧭", use_container_width=True, key="dash_calc")

        na_rota = []
        porto_o = buscar_porto(origem_txt) if origem_txt else None
        porto_d = buscar_porto(destino_txt) if destino_txt else None

        # mapa Folium compacto
        mapa = folium.Map(
            location=[-5.0, -25.0],
            zoom_start=3,
            tiles="CartoDB dark_matter",
        )

        if calcular and porto_o and porto_d:
            lat_o, lon_o = porto_o["lat"], porto_o["lon"]
            lat_d, lon_d = porto_d["lat"], porto_d["lon"]

            # rota com curva oceânica
            mid_lat = (lat_o + lat_d) / 2
            mid_lon = (lon_o + lon_d) / 2 - 10
            pontos = [[lat_o,lon_o],[( lat_o+mid_lat)/2,(lon_o+mid_lon)/2],[mid_lat,mid_lon],[(mid_lat+lat_d)/2,(mid_lon+lon_d)/2],[lat_d,lon_d]]

            folium.PolyLine(pontos, color="#2EB8AC", weight=2.5,
                            dash_array="8 5", opacity=0.9,
                            tooltip=f"{porto_o['nome']} → {porto_d['nome']}").add_to(mapa)

            folium.Marker([lat_o,lon_o], tooltip=f"🚢 {porto_o['nome']}",
                          icon=folium.Icon(color="blue", icon="home", prefix="fa")).add_to(mapa)
            folium.Marker([lat_d,lon_d], tooltip=f"🏁 {porto_d['nome']}",
                          icon=folium.Icon(color="red", icon="flag", prefix="fa")).add_to(mapa)

            na_rota = sereias_proximas(lat_o, lon_o, lat_d, lon_d)
            mapa.fit_bounds([[lat_o,lon_o],[lat_d,lon_d]])

        elif not calcular and porto_o and porto_d:
            # mostra rota padrão Santos→Lisboa ao carregar
            lat_o, lon_o = porto_o["lat"], porto_o["lon"]
            lat_d, lon_d = porto_d["lat"], porto_d["lon"]
            mid_lat = (lat_o+lat_d)/2
            mid_lon = (lon_o+lon_d)/2 - 10
            pontos = [[lat_o,lon_o],[(lat_o+mid_lat)/2,(lon_o+mid_lon)/2],[mid_lat,mid_lon],[(mid_lat+lat_d)/2,(mid_lon+lon_d)/2],[lat_d,lon_d]]
            folium.PolyLine(pontos, color="#2EB8AC", weight=2.5, dash_array="8 5", opacity=0.7).add_to(mapa)
            folium.Marker([lat_o,lon_o], tooltip=f"🚢 {porto_o['nome']}",
                          icon=folium.Icon(color="blue", icon="home", prefix="fa")).add_to(mapa)
            folium.Marker([lat_d,lon_d], tooltip=f"🏁 {porto_d['nome']}",
                          icon=folium.Icon(color="red", icon="flag", prefix="fa")).add_to(mapa)
            na_rota = sereias_proximas(lat_o, lon_o, lat_d, lon_d)
            mapa.fit_bounds([[lat_o,lon_o],[lat_d,lon_d]])

        # pinta sereias
        for s in sereias:
            na = s in na_rota
            folium.CircleMarker(
                location=[s["latitude"], s["longitude"]],
                radius=11 if na else 6,
                color="white" if na else CORES[s["risco"]],
                weight=2 if na else 1,
                fill=True,
                fill_color=CORES[s["risco"]],
                fill_opacity=0.95 if na else 0.2,
                tooltip=f"{'⚠️ ' if na else ''}{s['nome']} ({s['especie']})",
            ).add_to(mapa)
            if na:
                folium.CircleMarker(
                    location=[s["latitude"], s["longitude"]],
                    radius=18, color=CORES[s["risco"]],
                    weight=1.5, fill=False, opacity=0.35,
                ).add_to(mapa)

        st_folium(mapa, width="100%", height=340, returned_objects=[])

        if calcular:
            if not porto_o:
                st.error(f"'{origem_txt}' não reconhecido pelo sistema de inteligência naval. Tente: Santos, Recife, Lisboa, Miami, Rotterdam, Luanda...")
            elif not porto_d:
                st.error(f"'{destino_txt}' não reconhecido. Tente: Santos, Recife, Lisboa, Miami, Rotterdam, Luanda...")

        # resumo de risco abaixo do mapa
        if na_rota:
            alto  = sum(1 for s in na_rota if s["risco"]=="alto")
            medio = sum(1 for s in na_rota if s["risco"]=="medio")
            risco_pct = min(int((alto*70+medio*40)/max(len(na_rota),1)),95)
            cor_g = "#A43955" if risco_pct>60 else "#F39237"
            nome_rota = f"{porto_o['nome'].split(',')[0]} → {porto_d['nome'].split(',')[0]}" if porto_o and porto_d else ""

            st.markdown(f"""
            <div style="padding:14px 16px;border-top:1px solid var(--border)">
              <div style="font-size:12px;font-weight:500;color:var(--text-muted);margin-bottom:10px">
                Probabilidade de risco: <strong style="color:var(--text-primary)">{nome_rota}</strong>
              </div>
              <div style="display:flex;gap:18px;align-items:flex-start;">
                {gauge_html(risco_pct, cor_g, 'Risco Merrow')}
                {gauge_html(min(risco_pct+random.randint(10,25),95), '#2EB8AC', 'Risco Geral Oceânico')}
                <div style="flex:1;font-size:11px;color:var(--text-muted);line-height:1.7;border-left:1px solid var(--border);padding-left:14px">
                  <strong style="color:var(--text-primary);display:block;margin-bottom:5px;font-size:12px">⚠ Inteligência Oceânica</strong>
                  <div class="risk-factor"><span class="rfd" style="background:#A43955"></span>Lua cheia — atividade Siren +18%</div>
                  <div class="risk-factor"><span class="rfd" style="background:#A43955"></span>Temperatura: 24°C (ideal p/ Merrow)</div>
                  <div class="risk-factor"><span class="rfd" style="background:#F39237"></span>{random.randint(2,5)} naufrágios históricos na rota</div>
                  <div class="risk-factor"><span class="rfd" style="background:#2EB8AC"></span>Ressonância mágica: moderada</div>
                  <div class="alt-route">
                    <div class="alt-label">🧭 Rota alternativa sugerida</div>
                    Rota via sul tem {random.randint(32,45)}% menos risco de encontro hostil.
                  </div>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── tabela de espécies ────────────────────────────────────────────────────
    st.markdown("""
    <div class="card" style="margin-top:4px">
      <div class="card-header"><span class="card-title">Categorização das Sereias</span></div>
      <table class="species-table" style="margin-top:6px">
        <thead><tr><th>Raça</th><th>Risco</th><th>Tipo de Ataque</th><th>Ponto de Atenção</th></tr></thead>
        <tbody>""", unsafe_allow_html=True)

    for s in sereias:
        st.markdown(f"""
        <tr>
          <td><b>{s['emoji']} {s['especie']}</b></td>
          <td><span class="risk-badge {s['risco_class']}">{s['risco_label']}</span></td>
          <td>{s['agressividade']}</td>
          <td><span class="note-btn {s['nota_class']}">{s['nota']}</span></td>
        </tr>""", unsafe_allow_html=True)

    st.markdown("</tbody></table></div></div>", unsafe_allow_html=True)
