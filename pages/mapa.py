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

def sereias_proximas(lat_o, lon_o, lat_d, lon_d, margem=4.0):
    resultado = []
    for s in sereias:
        lat_s, lon_s = s["latitude"], s["longitude"]
        lat_min = min(lat_o, lat_d) - margem
        lat_max = max(lat_o, lat_d) + margem
        lon_min = min(lon_o, lon_d) - margem
        lon_max = max(lon_o, lon_d) + margem
        if lat_min <= lat_s <= lat_max and lon_min <= lon_s <= lon_max:
            resultado.append(s)
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
            if "filtro_risco" not in st.session_state:
                st.session_state.filtro_risco = ["alto", "medio", "baixo"]
            filtro = st.multiselect(
                "Filtrar por risco",
                options=["alto", "medio", "baixo"],
                default=st.session_state.filtro_risco,
                format_func=lambda x: LABELS[x],
                key="filtro_risco",
            )
        filtradas = [s for s in sereias if s["risco"] in filtro]
        with col_i:
            st.metric("Sereias visíveis", len(filtradas))

        mapa = folium.Map(location=[-15.0, -35.0], zoom_start=4, tiles="CartoDB positron")
        folium.TileLayer(
            tiles="https://tiles.openseamap.org/seamark/{z}/{x}/{y}.png",
            name="Rotas náuticas", attr="© OpenSeaMap",
            overlay=True, control=True, opacity=0.7,
        ).add_to(mapa)
        folium.LayerControl(position="topright").add_to(mapa)

        heat_data = [[s["latitude"], s["longitude"], s["avistamentos"]] for s in filtradas]
        if heat_data:
            HeatMap(heat_data, radius=40, blur=25, min_opacity=0.3).add_to(mapa)

        for s in filtradas:
            folium.CircleMarker(
                location=[s["latitude"], s["longitude"]],
                radius=10, color="white", weight=2,
                fill=True, fill_color=CORES[s["risco"]], fill_opacity=0.9,
                tooltip=f"{s['nome']} ({s['especie']}) — clique para ver ficha",
            ).add_to(mapa)

        saida = st_folium(mapa, width="100%", height=460,
                          returned_objects=["last_object_clicked_tooltip"])

        if saida and saida.get("last_object_clicked_tooltip"):
            nome = saida["last_object_clicked_tooltip"].split(" (")[0]
            s = next((x for x in sereias if x["nome"] == nome), None)
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
            st.caption("Clique num ponto do mapa para ver a ficha da sereia. Dê zoom no litoral para ver as rotas náuticas.")

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

        mapa_rota = folium.Map(location=[-10.0, -20.0], zoom_start=3, tiles="CartoDB positron")
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

                mapa_rota.fit_bounds([[lat_o, lon_o], [lat_d, lon_d]])
                na_rota = sereias_proximas(lat_o, lon_o, lat_d, lon_d)

        for s in sereias:
            na = s in na_rota
            folium.CircleMarker(
                location=[s["latitude"], s["longitude"]],
                radius=13 if na else 7,
                color="white" if na else CORES[s["risco"]],
                weight=3 if na else 1,
                fill=True, fill_color=CORES[s["risco"]],
                fill_opacity=0.95 if na else 0.2,
                tooltip=f"{'⚠️ ' if na else ''}{s['nome']} — {s['especie']}",
            ).add_to(mapa_rota)
            if na:
                folium.CircleMarker(
                    location=[s["latitude"], s["longitude"]],
                    radius=20, color=CORES[s["risco"]],
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

                st.divider()
                st.markdown(f"**Rota: {porto_o['nome']} → {porto_d['nome']}** — {len(na_rota)} sereias detectadas")

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Sereias na rota", len(na_rota))
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
                cols = st.columns(min(len(na_rota), 4))
                for i, s in enumerate(na_rota):
                    with cols[i % 4]:
                        cor = CORES[s["risco"]]
                        st.markdown(f"""
                        <div style="border:1px solid {cor};border-radius:10px;padding:11px;margin-bottom:8px">
                          <div style="font-size:20px;margin-bottom:3px">{s['emoji']}</div>
                          <b style="font-size:13px">{s['nome']}</b><br>
                          <span class="risk-badge {s['risco_class']}" style="margin-top:5px;display:inline-flex;font-size:11px">{LABELS[s['risco']]}</span><br>
                          <span style="font-size:11px;color:#888;margin-top:3px;display:block">{s['especie']} · {s['regiao']}</span>
                        </div>""", unsafe_allow_html=True)

        elif calcular and not na_rota and origem_txt and destino_txt:
            porto_o = buscar_porto(origem_txt)
            porto_d = buscar_porto(destino_txt)
            if porto_o and porto_d:
                st.success(f"✅ Rota {porto_o['nome']} → {porto_d['nome']} segura! Nenhuma sereia detectada no trajeto. Boa viagem. 🧜")

    st.markdown("</div>", unsafe_allow_html=True)
