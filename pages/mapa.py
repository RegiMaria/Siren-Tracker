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

def _na_rota_pontos(waypoints, corredor=6.0):
    """Avistamentos no corredor de uma rota definida por múltiplos waypoints."""
    resultado = []
    for a in avistamentos:
        for i in range(len(waypoints) - 1):
            d = _dist_ponto_segmento(
                a["lat"], a["lon"],
                waypoints[i][0], waypoints[i][1],
                waypoints[i+1][0], waypoints[i+1][1],
            )
            if d <= corredor:
                resultado.append(a)
                break
    return resultado

def run():
    st.markdown(STYLE, unsafe_allow_html=True)
    st.markdown(topbar("mapa"), unsafe_allow_html=True)
    st.markdown('<div class="content">', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Mapa de Atividade Sereia</div>', unsafe_allow_html=True)

    # ── Mapa de atividade ────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:#FEFEFE;border:1px solid #DAE3F8;border-radius:12px;padding:16px 20px;margin-bottom:14px">
      <div style="font-size:20px;font-weight:600;color:#0B1C33;margin-bottom:4px">Mapa de atividade global</div>
      <div style="font-size:13px;color:#606060">Heatmap das 7 espécies catalogadas — filtre por nível de risco e clique para ver a ficha</div>
    </div>""", unsafe_allow_html=True)

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

    saida = st_folium(mapa, use_container_width=True, height=460,
                      returned_objects=["last_object_clicked_tooltip"])

    if saida and saida.get("last_object_clicked_tooltip"):
        tooltip_txt = saida["last_object_clicked_tooltip"]
        especie_clic = tooltip_txt.split(" — ")[0] if " — " in tooltip_txt else tooltip_txt
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
        st.caption("Clique num ponto para ver a ficha da espécie. Dê zoom no litoral para ver as rotas náuticas.")

    st.divider()

    # ── Mapa de probabilidade ────────────────────────────────────────────────
    st.markdown("""
    <div style="background:#FEFEFE;border:1px solid #DAE3F8;border-radius:12px;padding:16px 20px;margin-bottom:14px">
      <div style="font-size:20px;font-weight:600;color:#0B1C33;margin-bottom:4px">Mapa de probabilidade por rota</div>
      <div style="font-size:13px;color:#606060">Planeje sua rota e veja as sereias no caminho</div>
    </div>""", unsafe_allow_html=True)

    opcoes_portos = sorted(PORTOS.keys(), key=lambda k: PORTOS[k]["nome"])
    labels_portos = {k: PORTOS[k]["nome"] for k in opcoes_portos}

    col_o, col_d, col_b = st.columns([2, 2, 1])
    with col_o:
        origem_key = st.selectbox(
            "Origem", options=opcoes_portos,
            format_func=lambda k: labels_portos[k],
            index=opcoes_portos.index("lisboa") if "lisboa" in opcoes_portos else 0,
            key="rota_origem",
        )
        origem_txt = origem_key
    with col_d:
        destino_key = st.selectbox(
            "Destino", options=opcoes_portos,
            format_func=lambda k: labels_portos[k],
            index=opcoes_portos.index("miami") if "miami" in opcoes_portos else 1,
            key="rota_destino",
        )
        destino_txt = destino_key
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
    na_rota_alt = []
    porto_o = porto_d = None
    dir_alt = "sul"

    if calcular and origem_txt and destino_txt:
        porto_o = buscar_porto(origem_txt)
        porto_d = buscar_porto(destino_txt)

        if not porto_o:
            st.error(f"Porto '{origem_txt}' não encontrado.")
            porto_o = porto_d = None
        elif not porto_d:
            st.error(f"Porto '{destino_txt}' não encontrado.")
            porto_o = porto_d = None
        else:
            lat_o, lon_o = porto_o["lat"], porto_o["lon"]
            lat_d, lon_d = porto_d["lat"], porto_d["lon"]

            mid_lat = (lat_o + lat_d) / 2
            mid_lon = (lon_o + lon_d) / 2 - 8

            # rota principal (teal)
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
                tooltip=f"🗺️ Rota principal: {porto_o['nome']} → {porto_d['nome']}",
            ).add_to(mapa_rota)

            # rota alternativa (laranja) — desvia pelo sul no hemisfério norte, pelo norte no sul
            offset = -11 if mid_lat > 0 else 11
            dir_alt = "sul" if offset < 0 else "norte"
            mid_lat_alt = mid_lat + offset
            pontos_alt = [
                [lat_o, lon_o],
                [(lat_o + mid_lat_alt) / 2, (lon_o + mid_lon) / 2 + 4],
                [mid_lat_alt, mid_lon - 6],
                [(mid_lat_alt + lat_d) / 2, (mid_lon + lon_d) / 2 + 4],
                [lat_d, lon_d],
            ]
            folium.PolyLine(
                locations=pontos_alt,
                color="#F39237", weight=2,
                dash_array="4 8", opacity=0.65,
                tooltip=f"🧭 Rota alternativa via {dir_alt}",
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
            na_rota = _na_rota_pontos(pontos_rota)
            na_rota_alt = _na_rota_pontos(pontos_alt)

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

    st_folium(mapa_rota, use_container_width=True, height=460, returned_objects=[])

    if calcular and porto_o and porto_d:
        alto  = sum(1 for a in na_rota if a["risco"] == "alto")
        medio = sum(1 for a in na_rota if a["risco"] == "medio")
        baixo = sum(1 for a in na_rota if a["risco"] == "baixo")
        risco_pct = min(int((alto * 70 + medio * 40 + baixo * 10) / max(len(na_rota), 1)), 95) if na_rota else 5
        cor_g   = "#A43955" if risco_pct > 60 else "#F39237" if risco_pct > 35 else "#2EB8AC"
        badge_g = "risk-high" if risco_pct > 60 else "risk-med" if risco_pct > 35 else "risk-low"
        label_g = "ALTO" if risco_pct > 60 else "MODERADO" if risco_pct > 35 else "LEVE"

        alto_alt  = sum(1 for a in na_rota_alt if a["risco"] == "alto")
        medio_alt = sum(1 for a in na_rota_alt if a["risco"] == "medio")
        risco_alt = min(int((alto_alt * 70 + medio_alt * 40 + sum(1 for a in na_rota_alt if a["risco"] == "baixo") * 10) / max(len(na_rota_alt), 1)), 95) if na_rota_alt else 5

        especies_rota = list(dict.fromkeys(a["key"] for a in na_rota))
        cidade_o = porto_o["nome"].split(",")[0]
        cidade_d = porto_d["nome"].split(",")[0]

        st.divider()
        col_a, col_b = st.columns([1, 2])

        with col_a:
            especies_html = "".join(
                f'<div style="display:flex;align-items:center;gap:8px;padding:7px 9px;background:#F8F9FF;border-radius:8px;font-size:12px;margin-bottom:5px">'
                f'<span style="font-size:17px">{SEREIA_POR_KEY[k]["emoji"]}</span>'
                f'<span style="flex:1;font-weight:500">{SEREIA_POR_KEY[k]["especie"]}</span>'
                f'<span class="risk-badge {SEREIA_POR_KEY[k]["risco_class"]}" style="font-size:10px;padding:2px 7px">{LABELS[SEREIA_POR_KEY[k]["risco"]]}</span>'
                f'</div>'
                for k in especies_rota
            ) if especies_rota else '<div style="font-size:12px;color:#888;padding:8px">Nenhuma sereia na rota</div>'

            st.markdown(f"""
            <div style="text-align:center;padding:22px;background:#F8F9FF;border-radius:12px;margin-bottom:14px">
              <div style="font-size:48px;font-weight:700;color:{cor_g}">{risco_pct}%</div>
              <div style="font-size:13px;color:var(--text-muted);margin-bottom:6px">Risco médio da rota</div>
              <span class="risk-badge {badge_g}">{label_g}</span>
            </div>
            <span class="section-label">Espécies na rota principal</span>
            {especies_html}""", unsafe_allow_html=True)

        with col_b:
            # segmentos da rota — 4 quartis entre origem e destino
            lat_o_v, lon_o_v = porto_o["lat"], porto_o["lon"]
            lat_d_v, lon_d_v = porto_d["lat"], porto_d["lon"]
            quartis = [
                (lat_o_v, lon_o_v),
                (lat_o_v + (lat_d_v - lat_o_v) * 0.25, lon_o_v + (lon_d_v - lon_o_v) * 0.25),
                (lat_o_v + (lat_d_v - lat_o_v) * 0.50, lon_o_v + (lon_d_v - lon_o_v) * 0.50),
                (lat_o_v + (lat_d_v - lat_o_v) * 0.75, lon_o_v + (lon_d_v - lon_o_v) * 0.75),
                (lat_d_v, lon_d_v),
            ]
            seg_nomes = [f"Saída — {cidade_o}", "Trecho central", "Oceano aberto", f"Chegada — {cidade_d}"]
            seg_km    = ["0–25%", "25–50%", "50–75%", "75–100%"]

            zonas_html = ""
            for i in range(4):
                ax, ay = quartis[i]
                bx, by = quartis[i + 1]
                seg_a = [a for a in na_rota
                         if _dist_ponto_segmento(a["lat"], a["lon"], ax, ay, bx, by) <= 8.0]
                sp_names = ", ".join(dict.fromkeys(a["especie"] for a in seg_a)) or "Nenhuma"
                r_seg = min(int(sum(70 if a["risco"]=="alto" else 40 if a["risco"]=="medio" else 10 for a in seg_a) / max(len(seg_a), 1)), 95) if seg_a else 5
                cor_seg = "#A43955" if r_seg > 60 else "#F39237" if r_seg > 35 else "#2EB8AC"
                nota_seg = f"{len(seg_a)} avistamento(s) detectado(s)" if seg_a else "Corredor seguro"
                zonas_html += (
                    f'<div class="rt-row">'
                    f'<div class="rt-dot" style="background:{cor_seg}"></div>'
                    f'<div>'
                    f'<div style="font-weight:500;color:var(--text-primary);font-size:12px">{seg_nomes[i]} <span style="color:var(--text-muted)">({seg_km[i]})</span></div>'
                    f'<div style="color:var(--text-muted);font-size:11px;margin-top:2px">Espécie: <strong>{sp_names}</strong> · Risco: <strong style="color:{cor_seg}">{r_seg}%</strong></div>'
                    f'<div style="color:var(--text-muted);font-size:11px;margin-top:1px">{nota_seg}</div>'
                    f'</div></div>'
                )

            reducao = max(risco_pct - risco_alt, 0)
            aumento = max(risco_alt - risco_pct, 0)
            alt_msg = (f"Via {dir_alt} — {len(na_rota_alt)} sereias (tracejado laranja). "
                       + (f"Reduz risco em ~{reducao}%." if reducao > 0 else f"Aumenta risco em ~{aumento}%."))

            st.markdown(f"""
            <span class="section-label">Linha do Tempo — {porto_o['nome']} → {porto_d['nome']}</span>
            <div class="route-timeline">
              <div class="rt-header">ANÁLISE SEGMENTO POR SEGMENTO — {porto_o['nome']} → {porto_d['nome']}</div>
              {zonas_html}
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px">
              <div style="padding:11px;background:var(--teal-light);border:1px solid var(--teal-border);border-radius:8px">
                <div style="font-size:11px;font-weight:700;color:#27A468;margin-bottom:3px">🗺️ ROTA PRINCIPAL — {label_g}</div>
                <div style="font-size:12px">{len(na_rota)} sereia(s) no corredor principal (tracejado verde). Risco calculado: {risco_pct}%.</div>
              </div>
              <div style="padding:11px;background:var(--amber-light);border:1px solid var(--amber-border);border-radius:8px">
                <div style="font-size:11px;font-weight:700;color:#c07a0a;margin-bottom:3px">🧭 ROTA ALTERNATIVA VIA {dir_alt.upper()}</div>
                <div style="font-size:12px">{alt_msg}</div>
              </div>
            </div>""", unsafe_allow_html=True)

    elif calcular and porto_o and porto_d and not na_rota:
        st.success(f"✅ Rota {porto_o['nome']} → {porto_d['nome']} segura! Nenhuma sereia detectada no trajeto. Boa viagem. 🧜")

    st.markdown("</div>", unsafe_allow_html=True)
