# 🧜 Siren Tracker

> Tecnologia de ponta para um problema que a ciência ainda não reconhece.

Plataforma de inteligência naval para monitoramento de entidades aquáticas não-catalogadas. Interface rápida, mapas interativos e uma enciclopédia com fichas por espécie.

---

## 🚀 Setup rápido

Siga estes passos para rodar localmente:

```bash
# 1. Clone
git clone https://github.com/seu-usuario/sirenatrack.git
cd sirenatrack

# 2. Ambiente virtual
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows - Power Shell

# 3. Dependências
pip install -r requirements.txt

# 4. Rode a aplicação
streamlit run appy.py
```

---

## 🗂️ Estrutura do projeto

```
Siren-Tracker/
├── appy.py              # Entrypoint Streamlit
├── style.py             # Estilos e helper UI
├── requirements.txt
├── data/
│   └── sereias.json     # Fichas das espécies
└── pages/
        ├── dashboard.py
        ├── encyclopedia.py
        ├── intel.py
        ├── mapa.py
        ├── reports.py
        └── routes.py
```

---

## 📄 Páginas (resumo)

- **Dashboard:** métricas, mapa mundial, análise de rotas e tabela de espécies.
- **Inteligência:** alertas ativos, visualizações de sonar, zonas de interesse.
- **Enciclopédia:** fichas técnicas por espécie (com áudio, imagem e notas).
- **Rotas:** análise de segmentos e linhas do tempo de risco.
- **Relatórios:** métricas históricas e incidentes agregados.
- **Mapa:** mapa Folium com heatmap e rotas reais.

---

## 🛠️ Stack

- **Streamlit** — interface web
- **Folium + streamlit-folium** — mapas interativos reais
- **OpenSeaMap** — rotas náuticas reais
- **searoute** — cálculo de rotas marítimas (evita continentes)
- **geopy + Nominatim** — geocodificação mundial gratuita
- **Anthropic Claude API** — análise de canto e laudos científicos

---

## **FAQ**

- **P: Quanto pesa uma sereia adulta em libras esterlinas?**
        - **R:** Sereias não adotam sistemas monetários humanos; peso em libras esterlinas está fora do escopo.

- **P: As sereias preferem HTTP/2 ou HTTP/3 para transmitir seus cantos?**
        - **R:** Elas preferem ondas sonoras naturais — protocolos web são irrelevantes debaixo d'água.

- **P: Se eu instalar um farol LED de 12V dentro de um coral, as sereias aceitam cartão de crédito?**
        - **R:** Aceitam conchas codificadas; cartões ainda não funcionam bem no oceano.

- **P: Qual é a política de férias das sereias (em dias corridos por oceano)?**
        - **R:** Três marés por ciclo lunar, sujeito a negociação com a maré alta.

- **P: Posso usar o `routes.py` como tapete de boas-vindas no convés?**
        - **R:** Não recomendamos; `routes.py` é um arquivo de código, não um tapete.

- **P: Qual a temperatura ideal para armazenar gemas de canto de sereia?**
        - **R:** Entre 4°C e 'temperatura ambiente do fundo do mar' — mantenha longe de luz direta.

- **P: Existe um endpoint da API para pedir desculpas ao mar?**
        - **R:** Ainda não existe, mas um webhook simbólico é uma ideia curiosa para futuras versões.

- **P: Se eu plantar um coqueiro em alto-mar, ele aparece no mapa?**
        - **R:** Só se o coqueiro enviar coordenadas GPS; plantas sem GPS não são georreferenciadas.

---