# 🧜 Siren Tracker

> Tecnologia de ponta para um problema que a ciência ainda não reconhece.

**[Acesse o Siren Tracker](https://siren-tracker.streamlit.app/)** Não entre no mar sem ele. Na verdade, talvez não entre no mar.

Plataforma de inteligência naval para monitoramento de entidades aquáticas não-catalogadas. Interface rápida, mapas interativos, central de alertas e enciclopédia completa com fichas por espécie.

---

## 🚀 Setup rápido

```bash
# 1. Clone
git clone https://github.com/RegiMaria/Siren-Tracker.git
cd Siren-Tracker

# 2. Ambiente virtual
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows (PowerShell)

# 3. Dependências
pip install -r requirements.txt

# 4. Rode a aplicação
streamlit run app.py
```

---

## 🗂️ Estrutura do projeto

```
Siren-Tracker/
├── app.py               # Entrypoint Streamlit + navegação
├── style.py             # Estilos globais, topbar e helpers de UI
├── requirements.txt
├── data/
│   ├── sereias.json     # Fichas técnicas das 7 espécies catalogadas
│   └── avistamentos.json  # 42 avistamentos georeferenciados globais
└── pages/
    ├── dashboard.py     # Visão geral e métricas operacionais
    ├── encyclopedia.py  # Fichas completas por espécie
    ├── intel.py         # Central de inteligência e alertas
    ├── mapa.py          # Mapa de atividade + análise de rota
    ├── reports.py       # Relatórios e histórico de incidentes
    └── routes.py        # Análise de segmentos de rota
```

---

## 📄 Páginas

- **Dashboard:** métricas globais de operação, mapa de sereias mapeadas no mundo e análise de rota marítima — selecione porto de origem e destino por lista suspensa para traçar a rota no mapa interativo, detectar avistamentos reais no corredor de navegação e visualizar gauge de risco com inteligência oceânica. Tabela de espécies com indicadores de ameaça.
- **Inteligência:** alertas ativos por nível de criticidade, radar oceânico com sonar animado, zonas de caça ativas e densidade de naufrágios por oceano.
- **Enciclopédia:** fichas técnicas completas — habitat, comportamento, fraquezas, lore e avaliação de risco por espécie.
- **Mapa de atividade:** mapa-múndi com heatmap das 7 espécies filtrado por nível de risco; clique num ponto para abrir a ficha da espécie.
- **Mapa de probabilidade:** selecione origem e destino por lista suspensa para traçar a rota, detectar sereias no corredor de navegação e ver o índice de risco calculado com avistamentos georeferenciados reais.
- **Rotas:** selecione porto de origem e destino por lista suspensa para gerar análise completa — linha do tempo de risco segmento a segmento, espécies encontradas por trecho, risco percentual por zona e rotas alternativas sugeridas.
- **Relatórios:** métricas mensais de operação, incidentes por espécie com barras de risco e histórico de incidentes notáveis com classificação de criticidade.

---

## 🌊 Espécies catalogadas

| Espécie | Risco | Habitat |
|---|---|---|
| Merrow | 🔴 Alto | Atlântico Norte, Mar Céltico |
| Selkie | 🔴 Alto | Costas escocesas, Mar do Norte |
| Siren | 🔴 Alto | Mediterrâneo, Açores, Caribe |
| Rusalka | 🟡 Médio | Mar Negro, Mar Báltico |
| Handwerkskunst | 🟡 Médio | Dorsal Mesoatlântica (abissal) |
| Zorah | 🟢 Baixo | Caribe, Índico tropical, Pacífico |
| Locathah | 🟢 Baixo | Atlântico equatorial, costas africanas |

---

## 🛠️ Stack

- **Streamlit** — interface web
- **Folium + streamlit-folium** — mapas interativos com heatmap
- **OpenSeaMap** — overlay de rotas náuticas reais
- **Anthropic Claude API** — análise de canto e laudos científicos

---

## 🧪 Testes

Dois conjuntos de testes verificam a lógica central:

**`tests/test_mapa.py`**

Testa a função `avistamentos_na_rota()`, responsável por detectar sereias dentro de um corredor ao longo de uma rota marítima:
- Rota Santos → Lisboa encontra avistamentos reais no Atlântico
- Rota remota no Pacífico Sul retorna lista vazia
- Corredor mais largo retorna ao menos tantos resultados quanto o estreito

**`tests/test_dados.py`** 

Lê `data/sereias.json` e garante a integridade dos dados:
- Todos os campos obrigatórios estão presentes em cada espécie
- Valores de risco são válidos (`alto`, `medio`, `baixo`)
- Coordenadas estão dentro dos limites geográficos reais
- Não há `key` duplicada

### Como rodar

```bash
source venv/bin/activate
pip install pytest
pytest tests/ -v
```

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
  - **R:** Entre 4°C e "temperatura ambiente do fundo do mar" — mantenha longe de luz direta.

- **P: Existe um endpoint da API para pedir desculpas ao mar?**
  - **R:** Ainda não existe, mas um webhook simbólico é uma ideia curiosa para futuras versões.

- **P: Se eu plantar um coqueiro em alto-mar, ele aparece no mapa?**
  - **R:** Só se o coqueiro enviar coordenadas GPS; plantas sem GPS não são georreferenciadas.

---

## 🚀 Codecon Universe 26

Este projeto foi construído durante o **Codecon Universe 26** — um hackathon de ideias inúteis e absurdas, realizado de 29 a 31 de maio de 2026.

O tema foi inspirado nos livros do Guia do Mochileiro das Galáxias. A instrução era **não entrar em pânico.**

Construímos um rastreador de sereias.

Há quem diga que entramos em pânico.

---

## 🐬 Adeus, e obrigada pelos peixes

O oceano sempre foi vasto, perigoso e cheio de coisas que a ciência oficial prefere não comentar.

Durante um fim de semana, a tripulação do Siren Tracker catalogou 7 espécies, georeferenciou 42 avistamentos, calibrou o sonar manualmente, devolveu a Merrow ao Mar Céltico e jogou o `appy.py` ao mar com honras!

891 vidas salvas. A Merrow continua sendo o problema. O Locathah estava só passando, respeito.

Não entre no mar sem o Siren Tracker.

Na verdade, talvez não entre no mar.

*— A Tripulação e as sereias que colaboraram com a catalogação*
