import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import json, os, sys, random

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style import STYLE, topbar, gauge_html, PORTOS, CORES, LABELS, buscar_porto

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sereias.json")
with open(DATA_PATH, encoding="utf-8") as f:
    sereias = json.load(f)

AVIST_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "avistamentos.json")
with open(AVIST_PATH, encoding="utf-8") as f:
    avistamentos = json.load(f)

# índice rápido espécie por key (para abrir ficha completa a partir do avistamento)
SEREIA_POR_KEY = {s["key"]: s for s in sereias}

def _dist_ponto_segmento(px, py, ax, ay, bx, by):
    """Distância (graus) de um ponto P ao segmento de rota A→B."""
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return ((px - ax) ** 2 + (py - ay) ** 2) ** 0.5
    t = ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)
    t = max(0.0, min(1.0, t))
    cx, cy = ax + t * dx, ay + t * dy
    return ((px - cx) ** 2 + (py - cy) ** 2) ** 0.5

def avistamentos_na_rota(lat_o, lon_o, lat_d, lon_d, corredor=6.0):
    """Avistamentos dentro do corredor de largura `corredor` ao longo da rota."""
    resultado = []
    for a in avistamentos:
        d = _dist_ponto_segmento(a["lat"], a["lon"], lat_o, lon_o, lat_d, lon_d)
        if d <= corredor:
            resultado.append(a)
    return resultado

def run():
    st.markdown(STYLE, unsafe_allow_html=True)
    st.markdown(topbar("mapa"), unsafe_allow_html=True)
    st.markdown('<div class="content">', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Mapa de Atividade Sereia</div>', unsafe_allow_html=True)

    aba1, aba2 = st.tabs(["🗺️ Mapa de atividade", "🧭 Mapa de probabilidade"])

    with aba1:
        col_f, col_i = st.columns([3, 1])
        with col_f:
            filtro = st.multiselect(
                "Filtrar por risco",
                options=["alto", "medio", "baixo"],
                default=["alto", "medio", "baixo"],
                format_func=lambda x: LABELS[x],
                key="filtro_risco",
            )
        visiveis = [a for a in avistamentos if a["risco"] in filtro]
        with col_i:
            st.metric("Avistamentos no mundo", len(visiveis))

        # ── mapa-múndi ───────────────────────────────────────────────────────
        mapa = folium.Map(location=[20.0, 0.0], zoom_start=2, tiles="CartoDB positron",
                          min_zoom=2, max_bounds=True, world_copy_jump=True)
        folium.TileLayer(
            tiles="https://tiles.openseamap.org/seamark/{z}/{x}/{y}.png",
            name="Rotas náuticas", attr="© OpenSeaMap",
            overlay=True, control=True, opacity=0.7,
        ).add_to(mapa)
        folium.LayerControl(position="topright").add_to(mapa)

        heat_data = [[a["lat"], a["lon"], a["intensidade"]] for a in visiveis]
        if heat_data:
            HeatMap(heat_data, radius=28, blur=18, min_opacity=0.25).add_to(mapa)

        for a in visiveis:
            folium.CircleMarker(
                location=[a["lat"], a["lon"]],
                radius=9, color="white", weight=2,
                fill=True, fill_color=CORES[a["risco"]], fill_opacity=0.95,
                tooltip=f"{a['especie']} — {a['local']} · {LABELS[a['risco']]}",
            ).add_to(mapa)

        saida = st_folium(mapa, width="100%", height=480,
                          returned_objects=["last_object_clicked_tooltip"])

        if saida and saida.get("last_object_clicked_tooltip"):
            especie_clic = saida["last_object_clicked_tooltip"].split(" — ")[0]
            s = next((x for x in sereias if x["especie"] == especie_clic), None)
            if s:
                cor = CORES[s["risco"]]
                st.markdown(f"""
                <div class="ficha-sereia" style="border-color:{cor};background:{cor}11;">
                  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;">
                    <div style="display:flex;align-items:center;gap:10px;">
                      <span style="font-size:22px">{s['emoji']}</span>
                      <div>
                        <b style="font-size:15px">{s['nome']}</b>
                        <span style="font-size:12px;color:#888;margin-left:8px">{s['especie']}</span>
                      </div>
                    </div>
                    <span class="risk-badge {s['risco_class']}">{LABELS[s['risco']]}</span>
                  </div>
                  <div class="ficha-grid">
                    <div><div class="ficha-item-label">Categoria</div><div class="ficha-item-value">{s['categoria']}</div></div>
                    <div><div class="ficha-item-label">Carnívora</div><div class="ficha-item-value">{'Sim ⚠️' if s['carnivora'] else 'Não'}</div></div>
                    <div><div class="ficha-item-label">Profundidade</div><div class="ficha-item-value">{s['profundidade']}</div></div>
                    <div><div class="ficha-item-label">Avistamentos</div><div class="ficha-item-value">{s['avistamentos']} reg.</div></div>
                  </div>
                  <div style="font-size:12px;color:#888;border-top:0.5px solid #eee;padding-top:7px">{s['lore'][:200]}...</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.caption("Mapa-múndi de avistamentos das 7 espécies catalogadas. Clique num ponto para ver a ficha completa da espécie. Dê zoom no litoral para ver as rotas náuticas.")

    with aba2:
        st.markdown("##### Planeje sua rota e veja as sereias no caminho")

        portos_disponiveis = ", ".join(sorted(set(
            v["nome"].split(",")[0] for v in PORTOS.values()
        ))[:20]) + "..."
        st.caption(f"Portos disponíveis: {portos_disponiveis}")

        col_o, col_d, col_b = st.columns([2, 2, 1])
        with col_o:
            origem_txt = st.text_input("Origem", placeholder="Ex: Recife", key="rota_origem")
        with col_d:
            destino_txt = st.text_input("Destino", placeholder="Ex: Luanda", key="rota_destino")
        with col_b:
            st.write("")
            calcular = st.button("Ver rota 🧭", use_container_width=True)

        mapa_rota = folium.Map(location=[20.0, 0.0], zoom_start=2, tiles="CartoDB positron",
                               min_zoom=2, max_bounds=True, world_copy_jump=True)
        folium.TileLayer(
            tiles="https://tiles.openseamap.org/seamark/{z}/{x}/{y}.png",
            name="Rotas náuticas", attr="© OpenSeaMap",
            overlay=True, control=True, opacity=0.7,
        ).add_to(mapa_rota)
        folium.LayerControl(position="topright").add_to(mapa_rota)

        na_rota = []

        if calcular and origem_txt and destino_txt:
            porto_o = buscar_porto(origem_txt)
            porto_d = buscar_porto(destino_txt)

            if not porto_o:
                st.error(f"Porto '{origem_txt}' não encontrado. Tente: Recife, Santos, Lisboa, Luanda, Miami...")
            elif not porto_d:
                st.error(f"Porto '{destino_txt}' não encontrado. Tente: Recife, Santos, Lisboa, Luanda, Miami...")
            else:
                lat_o, lon_o = porto_o["lat"], porto_o["lon"]
                lat_d, lon_d = porto_d["lat"], porto_d["lon"]

                mid_lat = (lat_o + lat_d) / 2
                mid_lon = (lon_o + lon_d) / 2 - 8

                pontos_rota = [
                    [lat_o, lon_o],
                    [(lat_o + mid_lat) / 2, (lon_o + mid_lon) / 2],
                    [mid_lat, mid_lon],
                    [(mid_lat + lat_d) / 2, (mid_lon + lon_d) / 2],
                    [lat_d, lon_d],
                ]

                folium.PolyLine(
                    locations=pontos_rota,
                    color="#2EB8AC", weight=3,
                    dash_array="8 5", opacity=0.9,
                    tooltip=f"Rota: {porto_o['nome']} → {porto_d['nome']}",
                ).add_to(mapa_rota)

                folium.Marker(
                    [lat_o, lon_o], popup=porto_o["nome"],
                    tooltip=f"🚢 Origem: {porto_o['nome']}",
                    icon=folium.Icon(color="blue", icon="home", prefix="fa"),
                ).add_to(mapa_rota)

                folium.Marker(
                    [lat_d, lon_d], popup=porto_d["nome"],
                    tooltip=f"🏁 Destino: {porto_d['nome']}",
                    icon=folium.Icon(color="red", icon="flag", prefix="fa"),
                ).add_to(mapa_rota)

                mapa_rota.fit_bounds([[lat_o, lon_o], [lat_d, lon_d]], padding=(40, 40))
                na_rota = avistamentos_na_rota(lat_o, lon_o, lat_d, lon_d)

        na_rota_ids = {id(a) for a in na_rota}
        for a in avistamentos:
            na = id(a) in na_rota_ids
            folium.CircleMarker(
                location=[a["lat"], a["lon"]],
                radius=12 if na else 6,
                color="white" if na else CORES[a["risco"]],
                weight=3 if na else 1,
                fill=True, fill_color=CORES[a["risco"]],
                fill_opacity=0.95 if na else 0.18,
                tooltip=f"{'⚠️ ' if na else ''}{a['especie']} — {a['local']}",
            ).add_to(mapa_rota)
            if na:
                folium.CircleMarker(
                    location=[a["lat"], a["lon"]],
                    radius=18, color=CORES[a["risco"]],
                    weight=1.5, fill=False, opacity=0.4,
                ).add_to(mapa_rota)

        st_folium(mapa_rota, width="100%", height=460, returned_objects=[])

        if calcular and na_rota and origem_txt and destino_txt:
            porto_o = buscar_porto(origem_txt)
            porto_d = buscar_porto(destino_txt)
            if porto_o and porto_d:
                alto  = sum(1 for s in na_rota if s["risco"] == "alto")
                medio = sum(1 for s in na_rota if s["risco"] == "medio")
                baixo = sum(1 for s in na_rota if s["risco"] == "baixo")
                risco_pct = min(int((alto * 70 + medio * 40 + baixo * 10) / max(len(na_rota), 1)), 95)
                cor_g = "#A43955" if risco_pct > 60 else "#F39237" if risco_pct > 35 else "#2EB8AC"

                especies_rota = list(dict.fromkeys(a["key"] for a in na_rota))

                st.divider()
                st.markdown(f"**Rota: {porto_o['nome']} → {porto_d['nome']}** — "
                            f"{len(na_rota)} avistamentos · {len(especies_rota)} espécies no caminho")

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Avistamentos na rota", len(na_rota))
                c2.metric("🔴 Alto risco", alto)
                c3.metric("🟡 Médio risco", medio)
                c4.metric("🟢 Baixo risco", baixo)

                st.markdown(f"""
                <div style="background:#F8F9FF;border-radius:12px;padding:16px;margin-top:10px">
                  <div style="display:flex;gap:20px;align-items:flex-start;">
                    {gauge_html(risco_pct, cor_g, 'Risco geral na rota')}
                    <div style="flex:1;font-size:12px;color:var(--text-muted);line-height:1.7;border-left:1px solid var(--border);padding-left:16px">
                      <strong style="color:var(--text-primary);display:block;margin-bottom:6px">⚠ Análise de Inteligência Oceânica</strong>
                      <div class="risk-factor"><span class="rfd" style="background:#A43955"></span>{alto} sereia(s) de alto risco detectada(s) na rota</div>
                      <div class="risk-factor"><span class="rfd" style="background:#F39237"></span>Temperatura estimada: {18 + random.random()*8:.1f}°C</div>
                      <div class="risk-factor"><span class="rfd" style="background:#F39237"></span>{random.randint(1,5)} naufrágios históricos registrados na área</div>
                      <div class="risk-factor"><span class="rfd" style="background:#2EB8AC"></span>Ressonância mágica: {'elevada' if alto > 0 else 'moderada'}</div>
                      <div class="alt-route">
                        <div class="alt-label">🧭 Rota alternativa sugerida</div>
                        Rota via {'norte' if random.random() > 0.5 else 'sul'} apresenta {random.randint(20, 42)}% menos risco de encontro hostil.
                      </div>
                    </div>
                  </div>
                </div>""", unsafe_allow_html=True)

                st.divider()
                cols = st.columns(min(len(especies_rota), 4))
                for i, key in enumerate(especies_rota):
                    s = SEREIA_POR_KEY[key]
                    locais = [a["local"] for a in na_rota if a["key"] == key]
                    with cols[i % 4]:
                        cor = CORES[s["risco"]]
                        st.markdown(f"""
                        <div style="border:1px solid {cor};border-radius:10px;padding:11px;margin-bottom:8px">
                          <div style="font-size:20px;margin-bottom:3px">{s['emoji']}</div>
                          <b style="font-size:13px">{s['nome']}</b><br>
                          <span class="risk-badge {s['risco_class']}" style="margin-top:5px;display:inline-flex;font-size:11px">{LABELS[s['risco']]}</span><br>
                          <span style="font-size:11px;color:#888;margin-top:3px;display:block">{s['especie']} · {len(locais)} ponto(s)</span>
                          <span style="font-size:10px;color:#aaa;margin-top:2px;display:block">{', '.join(locais)}</span>
                        </div>""", unsafe_allow_html=True)

        elif calcular and not na_rota and origem_txt and destino_txt:
            porto_o = buscar_porto(origem_txt)
            porto_d = buscar_porto(destino_txt)
            if porto_o and porto_d:
                st.success(f"✅ Rota {porto_o['nome']} → {porto_d['nome']} segura! Nenhuma sereia detectada no trajeto. Boa viagem. 🧜")

    st.markdown("</div>", unsafe_allow_html=True)
