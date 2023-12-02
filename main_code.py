# Importações
import yfinance as yf
import pandas as pd
import numpy as np
from scipy.stats import norm
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from dataclasses import dataclass
import altair as alt
import streamlit as st
from GoogleNews import GoogleNews

# Breve descrição sobre o projeto
st.write("## Bem-vindo ao Start Investor")
st.write("Faça a sua consulta para otimizar seu tempo e aprimorar seu processo de análise. Selecione o ticker do seu ativo de interesse e veja as informações relacionadas a companhia.")

st.sidebar.markdown("# Start Investor 📈")  # Adiciona título à barra lateral

dados = [{'Ticker': 'MGLU3', 'Nome': 'Magazine Luiza'}, {'Ticker': 'HAPV3', 'Nome': 'Hapvida'}, {'Ticker': 'CIEL3', 'Nome': 'Cielo'}, {'Ticker': 'BBDC4', 'Nome': 'Banco Bradesco'}, {'Ticker': 'PETR4', 'Nome': 'Petrobras'}, {'Ticker': 'ITUB4', 'Nome': 'Itaú Unibanco'}, {'Ticker': 'ABEV3', 'Nome': 'Ambev'}, {'Ticker': 'LREN3', 'Nome': 'Lojas Renner'}, {'Ticker': 'COGN3', 'Nome': 'Cogna'}, {'Ticker': 'B3SA3', 'Nome': 'B3'}, {'Ticker': 'CVCB3', 'Nome': 'CVC'}, {'Ticker': 'ITSA4', 'Nome': 'Itaúsa'}, {'Ticker': 'VALE3', 'Nome': 'Vale'}, {'Ticker': 'SOMA3', 'Nome': 'Grupo Soma'}, {'Ticker': 'USIM5', 'Nome': 'Usiminas'}, {'Ticker': 'ASAI3', 'Nome': 'Assaí'}, {'Ticker': 'BRKM5', 'Nome': 'Braskem'}, {'Ticker': 'RAIZ4', 'Nome': 'Raízen'}, {'Ticker': 'MRVE3', 'Nome': 'MRV'}, {'Ticker': 'SUZB3', 'Nome': 'Suzano'}, {'Ticker': 'CPLE6', 'Nome': 'Copel'}, {'Ticker': 'VBBR3', 'Nome': 'Vibra Energia'}, {'Ticker': 'ANIM3', 'Nome': 'Ânima Educação'}, {'Ticker': 'ENEV3', 'Nome': 'Eneva'}, {'Ticker': 'EMBR3', 'Nome': 'Embraer'}, {'Ticker': 'RAIL3', 'Nome': 'Rumo'}, {'Ticker': 'MRFG3', 'Nome': 'Marfrig'}, {'Ticker': 'CMIG4', 'Nome': 'CEMIG'}, {'Ticker': 'BEEF3', 'Nome': 'Minerva'}, {'Ticker': 'PRIO3', 'Nome': 'PetroRio'}, {'Ticker': 'POMO4', 'Nome': 'Marcopolo'}, {'Ticker': 'BBSE3', 'Nome': 'BB Seguridade'}, {'Ticker': 'AMER3', 'Nome': 'Americanas'}, {'Ticker': 'GGBR4', 'Nome': 'Gerdau'}, {'Ticker': 'KLBN4', 'Nome': 'Klabin'}, {'Ticker': 'RENT3', 'Nome': 'Localiza'}, {'Ticker': 'CSNA3', 'Nome': 'Siderúrgica Nacional'}, {'Ticker': 'AZUL4', 'Nome': 'Azul'}, {'Ticker': 'GOAU4', 'Nome': 'Metalúrgica Gerdau'}, {'Ticker': 'RDOR3', 'Nome': "Rede D'Or"}, {'Ticker': 'BBAS3', 'Nome': 'Banco do Brasil'}, {'Ticker': 'HBSA3', 'Nome': 'Hidrovias do Brasil'}, {'Ticker': 'PETZ3', 'Nome': 'Petz'}, {'Ticker': 'NTCO3', 'Nome': 'Natura'}, {'Ticker': 'QUAL3', 'Nome': 'Qualicorp'}, {'Ticker': 'CMIN3', 'Nome': 'CSN Mineração'}, {'Ticker': 'GMAT3', 'Nome': 'Grupo Mateus'}, {'Ticker': 'CCRO3', 'Nome': 'Grupo CCR'}, {'Ticker': 'CYRE3', 'Nome': 'Cyrela'}, {'Ticker': 'BRFS3', 'Nome': 'BRF'}, {'Ticker': 'EQTL3', 'Nome': 'Equatorial Energia'}, {'Ticker': 'AERI3', 'Nome': 'Aeris Energy'}, {'Ticker': 'PETR3', 'Nome': 'Petrobras'}, {'Ticker': 'CEAB3', 'Nome': 'C&A'}, {'Ticker': 'JBSS3', 'Nome': 'JBS'}, {'Ticker': 'AURE3', 'Nome': 'VTRM ENERGIA PARTICIPAÃiES S.A.'}, {'Ticker': 'RRRP3', 'Nome': '3R Petroleum'}, {'Ticker': 'TIMS3', 'Nome': 'TIM'}, {'Ticker': 'ELET3', 'Nome': 'Eletrobras'}, {'Ticker': 'BBDC3', 'Nome': 'Banco Bradesco'}, {'Ticker': 'CRFB3', 'Nome': 'Carrefour Brasil'}, {'Ticker': 'PCAR3', 'Nome': 'Grupo Pão de Açúcar'}, {'Ticker': 'ALPA4', 'Nome': 'Alpargatas'}, {'Ticker': 'CSMG3', 'Nome': 'COPASA'}, {'Ticker': 'LWSA3', 'Nome': 'Locaweb'}, {'Ticker': 'MULT3', 'Nome': 'Multiplan'}, {'Ticker': 'JHSF3', 'Nome': 'JHSF'}, {'Ticker': 'RADL3', 'Nome': 'RaiaDrogasil'}, {'Ticker': 'IFCM3', 'Nome': 'Infracommerce'}, {'Ticker': 'WEGE3', 'Nome': 'WEG'}, {'Ticker': 'GOLL4', 'Nome': 'GOL'}, {'Ticker': 'RECV3', 'Nome': 'PetroRecôncavo'}, {'Ticker': 'SEQL3', 'Nome': 'Sequoia Logística'}, {'Ticker': 'MLAS3', 'Nome': 'Multilaser'}, {'Ticker': 'MOVI3', 'Nome': 'Movida'}, {'Ticker': 'CSAN3', 'Nome': 'Cosan'}, {'Ticker': 'VAMO3', 'Nome': 'Grupo Vamos'}, {'Ticker': 'TEND3', 'Nome': 'Construtora Tenda'}, {'Ticker': 'SMFT3', 'Nome': 'Smart Fit'}, {'Ticker': 'ECOR3', 'Nome': 'EcoRodovias'}, {'Ticker': 'TOTS3', 'Nome': 'Totvs'}, {'Ticker': 'CBAV3', 'Nome': 'CBA'}, {'Ticker': 'UGPA3', 'Nome': 'Ultrapar'}, {'Ticker': 'GFSA3', 'Nome': 'Gafisa'}, {'Ticker': 'IRBR3', 'Nome': 'IRB Brasil RE'}, {'Ticker': 'FLRY3', 'Nome': 'Fleury'}, {'Ticker': 'CXSE3', 'Nome': 'Caixa Seguridade'}, {'Ticker': 'ONCO3', 'Nome': 'Oncoclínicas'}, {'Ticker': 'BRAP4', 'Nome': 'Bradespar'}, {'Ticker': 'SBFG3', 'Nome': 'Grupo SBF'}, {'Ticker': 'OIBR3', 'Nome': 'Oi'}, {'Ticker': 'RAPT4', 'Nome': 'Randon'}, {'Ticker': 'SIMH3', 'Nome': 'Simpar'}, {'Ticker': 'CPFE3', 'Nome': 'CPFL Energia'}, {'Ticker': 'YDUQ3', 'Nome': 'YDUQS'}, {'Ticker': 'CURY3', 'Nome': 'Cury'}, {'Ticker': 'TRPL4', 'Nome': 'Transmissão Paulista'}, {'Ticker': 'CPLE3', 'Nome': 'Copel'}, {'Ticker': 'KEPL3', 'Nome': 'Kepler Weber'}, {'Ticker': 'LJQQ3', 'Nome': 'Lojas Quero-Quero'}, {'Ticker': 'SBSP3', 'Nome': 'Sabesp'}, {'Ticker': 'DXCO3', 'Nome': 'Dexco'}, {'Ticker': 'ESPA3', 'Nome': 'Espaçolaser'}, {'Ticker': 'EZTC3', 'Nome': 'EZTEC'}, {'Ticker': 'SAPR4', 'Nome': 'Sanepar'}, {'Ticker': 'DIRR3', 'Nome': 'Direcional'}, {'Ticker': 'BRSR6', 'Nome': 'Banrisul'}, {'Ticker': 'KLBN3', 'Nome': 'Klabin'}, {'Ticker': 'AZEV4', 'Nome': 'Azevedo & Travassos'}, {'Ticker': 'STBP3', 'Nome': 'Santos Brasil'}, {'Ticker': 'GUAR3', 'Nome': 'Guararapes'}, {'Ticker': 'ARZZ3', 'Nome': 'Arezzo'}, {'Ticker': 'SGPS3', 'Nome': 'Springs'}, {'Ticker': 'MEGA3', 'Nome': 'OMEGA ENERGIA S.A.'}, {'Ticker': 'SLCE3', 'Nome': 'SLC Agrícola'}, {'Ticker': 'HYPE3', 'Nome': 'Hypera'}, {'Ticker': 'EGIE3', 'Nome': 'Engie'}, {'Ticker': 'NEOE3', 'Nome': 'Neoenergia'}, {'Ticker': 'GGPS3', 'Nome': 'GPS'}, {'Ticker': 'VIVA3', 'Nome': 'Vivara'}, {'Ticker': 'TTEN3', 'Nome': '3tentos'}, {'Ticker': 'RANI3', 'Nome': 'Irani'}, {'Ticker': 'PSSA3', 'Nome': 'Porto Seguro'}, {'Ticker': 'INTB3', 'Nome': 'Intelbras'}, {'Ticker': 'VIVT3', 'Nome': 'Vivo'}, {'Ticker': 'AMAR3', 'Nome': 'Lojas Marisa'}, {'Ticker': 'PDGR3', 'Nome': 'PDG Realty'}, {'Ticker': 'SMTO3', 'Nome': 'São Martinho'}, {'Ticker': 'ENAT3', 'Nome': 'Enauta'}, {'Ticker': 'AMBP3', 'Nome': 'Ambipar'}, {'Ticker': 'MEAL3', 'Nome': 'IMC Alimentação'}, {'Ticker': 'CLSA3', 'Nome': 'ClearSale'}, {'Ticker': 'GRND3', 'Nome': 'Grendene'}, {'Ticker': 'POSI3', 'Nome': 'Positivo'}, {'Ticker': 'AESB3', 'Nome': 'AES Brasil'}, {'Ticker': 'CASH3', 'Nome': 'Méliuz'}, {'Ticker': 'MDIA3', 'Nome': 'M. Dias Branco'}, {'Ticker': 'DESK3', 'Nome': 'Desktop'}, {'Ticker': 'MTRE3', 'Nome': 'Mitre Realty'}, {'Ticker': 'VVEO3', 'Nome': 'Viveo'}, {'Ticker': 'MBLY3', 'Nome': 'Mobly'}, {'Ticker': 'RCSL4', 'Nome': 'Recrusul'}, {'Ticker': 'PLPL3', 'Nome': 'Plano&Plano'}, {'Ticker': 'PGMN3', 'Nome': 'Pague Menos'}, {'Ticker': 'WIZC3', 'Nome': 'Wiz Soluções'}, {'Ticker': 'SHUL4', 'Nome': 'Schulz'}, {'Ticker': 'BPAN4', 'Nome': 'Banco Pan'}, {'Ticker': 'SEER3', 'Nome': 'Ser Educacional'}, {'Ticker': 'CAML3', 'Nome': 'Camil Alimentos'}, {'Ticker': 'ARML3', 'Nome': 'Armac'}, {'Ticker': 'ODPV3', 'Nome': 'Odontoprev'}, {'Ticker': 'MATD3', 'Nome': 'Mater Dei'}, {'Ticker': 'LEVE3', 'Nome': 'Mahle Metal Leve'}, {'Ticker': 'ZAMP3', 'Nome': 'Zamp'}, {'Ticker': 'CSED3', 'Nome': 'Cruzeiro do Sul Educacional'}, {'Ticker': 'TRAD3', 'Nome': 'Traders Club'}, {'Ticker': 'AGRO3', 'Nome': 'BrasilAgro'}, {'Ticker': 'LIGT3', 'Nome': 'Light'}, {'Ticker': 'ELET6', 'Nome': 'Eletrobras'}, {'Ticker': 'VULC3', 'Nome': 'Vulcabras'}, {'Ticker': 'DASA3', 'Nome': 'Dasa'}, {'Ticker': 'MYPK3', 'Nome': 'Iochpe-Maxion'}, {'Ticker': 'TRIS3', 'Nome': 'Trisul'}, {'Ticker': 'OPCT3', 'Nome': 'OceanPact'}, {'Ticker': 'AZEV3', 'Nome': 'Azevedo & Travassos'}, {'Ticker': 'ABCB4', 'Nome': 'Banco ABC Brasil'}, {'Ticker': 'ORVR3', 'Nome': 'Orizon'}, {'Ticker': 'RCSL3', 'Nome': 'Recrusul'}, {'Ticker': 'PFRM3', 'Nome': 'Profarma'}, {'Ticker': 'CMIG3', 'Nome': 'CEMIG'}, {'Ticker': 'LAVV3', 'Nome': 'Lavvi Incorporadora'}, {'Ticker': 'JALL3', 'Nome': 'Jalles Machado'}, {'Ticker': 'MDNE3', 'Nome': 'Moura Dubeux'}, {'Ticker': 'LOGG3', 'Nome': 'LOG CP'}, {'Ticker': 'BMGB4', 'Nome': 'Banco BMG'}, {'Ticker': 'PNVL3', 'Nome': 'Dimed'}, {'Ticker': 'PTBL3', 'Nome': 'Portobello'}, {'Ticker': 'MILS3', 'Nome': 'Mills'}, {'Ticker': 'FIQE3', 'Nome': 'Unifique'}, {'Ticker': 'LUPA3', 'Nome': 'Lupatech'}, {'Ticker': 'BRIT3', 'Nome': 'Brisanet'}, {'Ticker': 'BLAU3', 'Nome': 'Blau Farmacêutica'}, {'Ticker': 'PRNR3', 'Nome': 'Priner'}, {'Ticker': 'EVEN3', 'Nome': 'Even'}, {'Ticker': 'CTNM4', 'Nome': 'Coteminas'}, {'Ticker': 'VLID3', 'Nome': 'Valid'}, {'Ticker': 'TASA4', 'Nome': 'Taurus'}, {'Ticker': 'HBOR3', 'Nome': 'Helbor'}, {'Ticker': 'FRAS3', 'Nome': 'Fras-le'}, {'Ticker': 'SHOW3', 'Nome': 'Time For Fun'}, {'Ticker': 'HBRE3', 'Nome': 'HBR Realty'}, {'Ticker': 'ENJU3', 'Nome': 'Enjoei'}, {'Ticker': 'NGRD3', 'Nome': 'Neogrid'}, {'Ticker': 'FESA4', 'Nome': 'Ferbasa'}, {'Ticker': 'ITUB3', 'Nome': 'Itaú Unibanco'}, {'Ticker': 'PINE4', 'Nome': 'PINE'}, {'Ticker': 'VIVR3', 'Nome': 'Viver'}, {'Ticker': 'CTSA4', 'Nome': 'Santanense'}, {'Ticker': 'JSLG3', 'Nome': 'JSL'}, {'Ticker': 'CTSA3', 'Nome': 'Santanense'}, {'Ticker': 'RNEW4', 'Nome': 'Renova Energia'}, {'Ticker': 'SAPR3', 'Nome': 'Sanepar'}, {'Ticker': 'VITT3', 'Nome': 'Vittia'}, {'Ticker': 'TUPY3', 'Nome': 'Tupy'}, {'Ticker': 'USIM3', 'Nome': 'Usiminas'}, {'Ticker': 'ROMI3', 'Nome': 'Indústrias ROMI'}, {'Ticker': 'KRSA3', 'Nome': 'Kora Saúde'}, {'Ticker': 'ALPK3', 'Nome': 'Estapar'}, {'Ticker': 'SYNE3', 'Nome': 'SYN'}, {'Ticker': 'WEST3', 'Nome': 'Westwing'}, {'Ticker': 'PDTC3', 'Nome': 'Padtec'}, {'Ticker': 'BMOB3', 'Nome': 'Bemobi'}, {'Ticker': 'TGMA3', 'Nome': 'Tegma'}, {'Ticker': 'BRKM3', 'Nome': 'Braskem'}, {'Ticker': 'UNIP6', 'Nome': 'Unipar'}, {'Ticker': 'PORT3', 'Nome': 'Wilson Sons'}, {'Ticker': 'AALR3', 'Nome': 'Alliança'}, {'Ticker': 'TECN3', 'Nome': 'Technos'}, {'Ticker': 'TAEE4', 'Nome': 'Taesa'}, {'Ticker': 'ETER3', 'Nome': 'Eternit'}, {'Ticker': 'UCAS3', 'Nome': 'Unicasa'}, {'Ticker': 'TFCO4', 'Nome': 'Track & Field'}, {'Ticker': 'LPSB3', 'Nome': 'Lopes'}, {'Ticker': 'ITSA3', 'Nome': 'Itaúsa'}, {'Ticker': 'MTSA4', 'Nome': 'METISA'}, {'Ticker': 'SOJA3', 'Nome': 'Boa Safra Sementes'}, {'Ticker': 'BRAP3', 'Nome': 'Bradespar'}, {'Ticker': 'POMO3', 'Nome': 'Marcopolo'}, {'Ticker': 'TCSA3', 'Nome': 'Tecnisa'}, {'Ticker': 'NINJ3', 'Nome': 'GetNinjas'}, {'Ticker': 'IGTI3', 'Nome': 'Jereissati Participações'}, {'Ticker': 'IGTI3', 'Nome': 'Iguatemi'}, {'Ticker': 'DEXP3', 'Nome': 'Dexxos'}, {'Ticker': 'SANB4', 'Nome': 'Banco Santander'}, {'Ticker': 'MELK3', 'Nome': 'Melnick'}, {'Ticker': 'LAND3', 'Nome': 'Terra Santa'}, {'Ticker': 'ALLD3', 'Nome': 'Allied'}, {'Ticker': 'SANB3', 'Nome': 'Banco Santander'}, {'Ticker': 'TAEE3', 'Nome': 'Taesa'}, {'Ticker': 'CAMB3', 'Nome': 'Cambuci'}, {'Ticker': 'RSID3', 'Nome': 'Rossi Residencial'}, {'Ticker': 'RNEW3', 'Nome': 'Renova Energia'}, {'Ticker': 'DMVF3', 'Nome': 'D1000 Varejo Farma'}, {'Ticker': 'CSUD3', 'Nome': 'CSU Cardsystem'}, {'Ticker': 'ELMD3', 'Nome': 'Eletromidia'}, {'Ticker': 'DOTZ3', 'Nome': 'Dotz'}, {'Ticker': 'GGBR3', 'Nome': 'Gerdau'}, {'Ticker': 'GOAU3', 'Nome': 'Metalúrgica Gerdau'}, {'Ticker': 'LOGN3', 'Nome': 'Log-In'}, {'Ticker': 'APER3', 'Nome': 'Alper'}, {'Ticker': 'TPIS3', 'Nome': 'Triunfo'}, {'Ticker': 'AGXY3', 'Nome': 'AgroGalaxy'}, {'Ticker': 'PMAM3', 'Nome': 'Paranapanema'}, {'Ticker': 'EUCA4', 'Nome': 'Eucatex'}, {'Ticker': 'BPAC5', 'Nome': 'Banco BTG Pactual'}, {'Ticker': 'SCAR3', 'Nome': 'São Carlos'}, {'Ticker': 'OIBR4', 'Nome': 'Oi'}, {'Ticker': 'BOBR4', 'Nome': 'Bombril'}, {'Ticker': 'JFEN3', 'Nome': 'João Fortes'}, {'Ticker': 'INEP4', 'Nome': 'Inepar'}, {'Ticker': 'TASA3', 'Nome': 'Taurus'}, {'Ticker': 'ALUP4', 'Nome': 'Alupar'}, {'Ticker': 'INEP3', 'Nome': 'Inepar'}, {'Ticker': 'ATMP3', 'Nome': 'Atma'}, {'Ticker': 'BMEB4', 'Nome': 'Banco Mercantil do Brasil'}, {'Ticker': 'RPMG3', 'Nome': 'Refinaria de Manguinhos'}, {'Ticker': 'ALUP3', 'Nome': 'Alupar'}, {'Ticker': 'CEBR6', 'Nome': 'CEB'}, {'Ticker': 'ATOM3', 'Nome': 'ATOM'}, {'Ticker': 'LVTC3', 'Nome': 'WDC Networks'}, {'Ticker': 'SNSY5', 'Nome': 'Sansuy'}, {'Ticker': 'EPAR3', 'Nome': 'EPAR3'}, {'Ticker': 'RAPT3', 'Nome': 'Randon'}, {'Ticker': 'PTNT4', 'Nome': 'Pettenati'}, {'Ticker': 'COCE5', 'Nome': 'Coelce'}, {'Ticker': 'UNIP3', 'Nome': 'Unipar'}, {'Ticker': 'BEES3', 'Nome': 'Banestes'}, {'Ticker': 'NUTR3', 'Nome': 'Nutriplant'}, {'Ticker': 'TELB4', 'Nome': 'Telebras'}, {'Ticker': 'CEBR3', 'Nome': 'CEB'}, {'Ticker': 'CGRA4', 'Nome': 'Grazziotin'}, {'Ticker': 'MNPR3', 'Nome': 'Minupar'}, {'Ticker': 'ENGI4', 'Nome': 'Energisa'}, {'Ticker': 'BIOM3', 'Nome': 'Biomm'}, {'Ticker': 'VSTE3', 'Nome': 'LE LIS BLANC'}, {'Ticker': 'BPAC3', 'Nome': 'Banco BTG Pactual'}, {'Ticker': 'BRSR3', 'Nome': 'Banrisul'}, {'Ticker': 'REDE3', 'Nome': 'Rede Energia'}, {'Ticker': 'DEXP4', 'Nome': 'Dexxos'}, {'Ticker': 'FHER3', 'Nome': 'Fertilizantes Heringer'}, {'Ticker': 'CGRA3', 'Nome': 'Grazziotin'}, {'Ticker': 'ENGI3', 'Nome': 'Energisa'}, {'Ticker': 'BEES4', 'Nome': 'Banestes'}, {'Ticker': 'BRIV4', 'Nome': 'Alfa Investimento'}, {'Ticker': 'ESTR4', 'Nome': 'Estrela'}, {'Ticker': 'WHRL3', 'Nome': 'Whirlpool'}, {'Ticker': 'HAGA3', 'Nome': 'Haga'}, {'Ticker': 'BAHI3', 'Nome': 'Bahema'}, {'Ticker': 'MWET4', 'Nome': 'Wetzel'}, {'Ticker': 'EMAE4', 'Nome': 'EMAE'}, {'Ticker': 'ALPA3', 'Nome': 'Alpargatas'}, {'Ticker': 'OSXB3', 'Nome': 'OSX Brasil'}, {'Ticker': 'EALT4', 'Nome': 'Electro Aço Altona'}, {'Ticker': 'CRIV3', 'Nome': 'Alfa Financeira'}, {'Ticker': 'CRIV4', 'Nome': 'Alfa Financeira'}, {'Ticker': 'EUCA3', 'Nome': 'Eucatex'}, {'Ticker': 'HOOT4', 'Nome': 'Hotéis Othon'}, {'Ticker': 'CRPG6', 'Nome': 'Tronox Pigmentos'}, {'Ticker': 'OFSA3', 'Nome': 'Ourofino Saúde Animal'}, {'Ticker': 'RDNI3', 'Nome': 'RNI'}, {'Ticker': 'RSUL4', 'Nome': 'Metalúrgica Riosulense'}, {'Ticker': 'EQPA3', 'Nome': 'Equatorial Energia Pará'}, {'Ticker': 'BGIP4', 'Nome': 'Banese'}, {'Ticker': 'CEBR5', 'Nome': 'CEB'}, {'Ticker': 'FRTA3', 'Nome': 'Pomi Frutas'}, {'Ticker': 'TRPL3', 'Nome': 'Transmissão Paulista'}, {'Ticker': 'CTKA4', 'Nome': 'Karsten'}, {'Ticker': 'HETA4', 'Nome': 'Hercules'}, {'Ticker': 'CLSC4', 'Nome': 'Celesc'}, {'Ticker': 'CEEB3', 'Nome': 'COELBA'}, {'Ticker': 'CRPG5', 'Nome': 'Tronox Pigmentos'}, {'Ticker': 'BRKM6', 'Nome': 'Braskem'}, {'Ticker': 'NEXP3', 'Nome': 'Brasil Brokers'}, {'Ticker': 'HAGA4', 'Nome': 'Haga'}, {'Ticker': 'FRIO3', 'Nome': 'Metalfrio'}, {'Ticker': 'WHRL4', 'Nome': 'Whirlpool'}, {'Ticker': 'MGEL4', 'Nome': 'Mangels'}, {'Ticker': 'EQPA5', 'Nome': 'Equatorial Energia Pará'}, {'Ticker': 'AVLL3', 'Nome': 'Alphaville'}, {'Ticker': 'WLMM3', 'Nome': 'WLM'}, {'Ticker': 'BAZA3', 'Nome': 'Banco da Amazônia'}, {'Ticker': 'TEKA4', 'Nome': 'Teka'}, {'Ticker': 'BDLL4', 'Nome': 'Bardella'}, {'Ticker': 'EKTR4', 'Nome': 'Elektro'}, {'Ticker': 'GEPA4', 'Nome': 'Rio Paranapanema Energia'}, {'Ticker': 'CPLE5', 'Nome': 'Copel'}, {'Ticker': 'CTNM3', 'Nome': 'Coteminas'}, {'Ticker': 'AFLT3', 'Nome': 'Afluente T'}, {'Ticker': 'TELB3', 'Nome': 'Telebras'}, {'Ticker': 'MNDL3', 'Nome': 'Mundial'}, {'Ticker': 'CSRN3', 'Nome': 'COSERN'}, {'Ticker': 'CEDO4', 'Nome': 'Cedro Têxtil'}, {'Ticker': 'BMEB3', 'Nome': 'Banco Mercantil do Brasil'}, {'Ticker': 'BMIN4', 'Nome': 'Banco Mercantil de Investimentos'}, {'Ticker': 'IGTI4', 'Nome': 'Jereissati Participações'}, {'Ticker': 'IGTI4', 'Nome': 'Iguatemi'}, {'Ticker': 'PLAS3', 'Nome': 'Plascar'}, {'Ticker': 'CGAS5', 'Nome': 'Comgás'}, {'Ticker': 'EQPA7', 'Nome': 'Equatorial Energia Pará'}, {'Ticker': 'ENMT3', 'Nome': 'Energisa MT'}, {'Ticker': 'BALM4', 'Nome': 'Baumer'}, {'Ticker': 'BAUH4', 'Nome': 'Excelsior'}, {'Ticker': 'HBTS5', 'Nome': 'Habitasul'}, {'Ticker': 'WLMM4', 'Nome': 'WLM'}, {'Ticker': 'PTNT3', 'Nome': 'Pettenati'}, {'Ticker': 'BNBR3', 'Nome': 'Banco do Nordeste'}, {'Ticker': 'BGIP3', 'Nome': 'Banese'}, {'Ticker': 'JOPA3', 'Nome': 'Josapar'}, {'Ticker': 'CALI3', 'Nome': 'Adolpho Lindenberg'}, {'Ticker': 'DOHL4', 'Nome': 'Döhler'}, {'Ticker': 'DTCY3', 'Nome': 'Dtcom'}, {'Ticker': 'NORD3', 'Nome': 'Nordon'}, {'Ticker': 'BMKS3', 'Nome': 'Monark'}, {'Ticker': 'BSLI4', 'Nome': 'Banco de Brasília'}, {'Ticker': 'FESA3', 'Nome': 'Ferbasa'}, {'Ticker': 'LUXM4', 'Nome': 'Trevisa'}, {'Ticker': 'BALM3', 'Nome': 'Baumer'}, {'Ticker': 'BMIN3', 'Nome': 'Banco Mercantil de Investimentos'}, {'Ticker': 'PATI3', 'Nome': 'Panatlântica'}, {'Ticker': 'BRIV3', 'Nome': 'Alfa Investimento'}, {'Ticker': 'CSAB3', 'Nome': 'Cia. de Seg. Aliança da Bahia'}, {'Ticker': 'EQMA3B', 'Nome': 'Equatorial Maranhão'}, {'Ticker': 'CSAB4', 'Nome': 'Cia. de Seg. Aliança da Bahia'}, {'Ticker': 'CEDO3', 'Nome': 'Cedro Têxtil'}, {'Ticker': 'BRSR5', 'Nome': 'Banrisul'}, {'Ticker': 'MERC4', 'Nome': 'Mercantil do Brasil Financeira'}, {'Ticker': 'DMFN3', 'Nome': 'DMFN3'}, {'Ticker': 'CEED3', 'Nome': 'CEEE D'}, {'Ticker': 'BSLI3', 'Nome': 'Banco de Brasília'}, {'Ticker': 'CGAS3', 'Nome': 'Comgás'}, {'Ticker': 'UNIP5', 'Nome': 'Unipar'}, {'Ticker': 'FIEI3', 'Nome': 'FIEI3'}, {'Ticker': 'RPAD3', 'Nome': 'Alfa Holdings'}, {'Ticker': 'EALT3', 'Nome': 'Electro Aço Altona'}, {'Ticker': 'ENMT4', 'Nome': 'Energisa MT'}, {'Ticker': 'CEED4', 'Nome': 'CEEE D'}, {'Ticker': 'DOHL3', 'Nome': 'Döhler'}, {'Ticker': 'CEEB5', 'Nome': 'COELBA'}, {'Ticker': 'PEAB3', 'Nome': 'Participações Aliança da Bahia'}, {'Ticker': 'MRSA3B', 'Nome': 'MRS Logística'}, {'Ticker': 'BRGE12', 'Nome': 'Consórcio Alfa'}, {'Ticker': 'CLSC3', 'Nome': 'Celesc'}, {'Ticker': 'RPAD6', 'Nome': 'Alfa Holdings'}, {'Ticker': 'BRGE6', 'Nome': 'Consórcio Alfa'}, {'Ticker': 'CRPG3', 'Nome': 'Tronox Pigmentos'}, {'Ticker': 'SNSY3', 'Nome': 'Sansuy'}, {'Ticker': 'MRSA5B', 'Nome': 'MRS Logística'}, {'Ticker': 'MAPT4', 'Nome': 'Cemepe'}, {'Ticker': 'CTKA3', 'Nome': 'Karsten'}, {'Ticker': 'CSRN5', 'Nome': 'COSERN'}, {'Ticker': 'GEPA3', 'Nome': 'Rio Paranapanema Energia'}, {'Ticker': 'GSHP3', 'Nome': 'General Shopping & Outlets'}, {'Ticker': 'RPAD5', 'Nome': 'Alfa Holdings'}, {'Ticker': 'AHEB3', 'Nome': 'São Paulo Turismo'}, {'Ticker': 'BRGE3', 'Nome': 'Consórcio Alfa'}, {'Ticker': 'MOAR3', 'Nome': 'Monteiro Aranha'}, {'Ticker': 'BRGE5', 'Nome': 'Consórcio Alfa'}, {'Ticker': 'CSRN6', 'Nome': 'COSERN'}, {'Ticker': 'TKNO4', 'Nome': 'Tekno'}, {'Ticker': 'BDLL3', 'Nome': 'Bardella'}, {'Ticker': 'ELET5', 'Nome': 'Eletrobras'}, {'Ticker': 'SOND6', 'Nome': 'Sondotécnica'}, {'Ticker': 'CBEE3', 'Nome': 'Ampla Energia'}, {'Ticker': 'SOND5', 'Nome': 'Sondotécnica'}, {'Ticker': 'GPAR3', 'Nome': 'CELGPAR'}, {'Ticker': 'SQIA3', 'Nome': 'Sinqia'}, {'Ticker': 'ESTR3', 'Nome': 'Estrela'}, {'Ticker': 'BRGE11', 'Nome': 'Consórcio Alfa'}, {'Ticker': 'BRGE8', 'Nome': 'Consórcio Alfa'}, {'Ticker': 'BRGE7', 'Nome': 'Consórcio Alfa'}, {'Ticker': 'MRSA6B', 'Nome': 'MRS Logística'}, {'Ticker': 'ALSO3', 'Nome': 'Aliansce Sonae'}, {'Ticker': 'BRPR3', 'Nome': 'BR Properties'}, {'Ticker': 'LIPR3', 'Nome': 'Eletropar'}, {'Ticker': 'PATI4', 'Nome': 'Panatlântica'}, {'Ticker': 'MTSA3', 'Nome': 'METISA'}, {'Ticker': 'SLED4', 'Nome': 'Saraiva'}, {'Ticker': 'SLED3', 'Nome': 'Saraiva'}, {'Ticker': 'EQPA6', 'Nome': 'Equatorial Energia Pará'}, {'Ticker': 'AHEB6', 'Nome': 'São Paulo Turismo'}, {'Ticker': 'PINE3', 'Nome': 'PINE'}, {'Ticker': 'VIIA3', 'Nome': 'VIIA3'}, {'Ticker': 'EKTR3', 'Nome': 'Elektro'}, {'Ticker': 'MWET3', 'Nome': 'Wetzel'}, {'Ticker': 'USIM6', 'Nome': 'Usiminas'}, {'Ticker': 'AHEB5', 'Nome': 'São Paulo Turismo'}, {'Ticker': 'ENBR3', 'Nome': 'EDP Brasil'}, {'Ticker': 'BOAS3', 'Nome': 'Boa Vista'}, {'Ticker': 'PEAB4', 'Nome': 'Participações Aliança da Bahia'}, {'Ticker': 'COCE3', 'Nome': 'Coelce'}, {'Ticker': 'JOPA4', 'Nome': 'Josapar'}, {'Ticker': 'MODL3', 'Nome': 'Banco Modal'}, {'Ticker': 'MERC3', 'Nome': 'Mercantil do Brasil Financeira'}, {'Ticker': 'CEGR3', 'Nome': 'Naturgy (CEG)'}, {'Ticker': 'MAPT3', 'Nome': 'Cemepe'}, {'Ticker': 'CRDE3', 'Nome': 'CR2'}, {'Ticker': 'IGBR3', 'Nome': 'IGB Eletrônica'}, {'Ticker': 'MSPA4', 'Nome': 'Melhoramentos'}, {'Ticker': 'ODER4', 'Nome': 'Conservas Oderich'}, {'Ticker': 'PARD3', 'Nome': 'Hermes Pardini'}, {'Ticker': 'CASN3', 'Nome': 'CASAN'}, {'Ticker': 'WIZS3', 'Nome': 'WIZS3'}, {'Ticker': 'LLIS3', 'Nome': 'LLIS3'}, {'Ticker': 'MSPA3', 'Nome': 'Melhoramentos'}, {'Ticker': 'BRML3', 'Nome': 'BRMalls'}, {'Ticker': 'DMMO3', 'Nome': 'Dommo Energia'}, {'Ticker': 'GETT3', 'Nome': 'Getnet'}, {'Ticker': 'GETT4', 'Nome': 'Getnet'}, {'Ticker': 'SULA4', 'Nome': 'SulAmérica'}, {'Ticker': 'SULA3', 'Nome': 'SulAmérica'}, {'Ticker': 'CEPE5', 'Nome': 'CELPE'}, {'Ticker': 'TCNO4', 'Nome': 'Tecnosolo'}, {'Ticker': 'TCNO3', 'Nome': 'Tecnosolo'}, {'Ticker': 'CEPE6', 'Nome': 'CELPE'}, {'Ticker': 'BKBR3', 'Nome': 'BKBR3'}, {'Ticker': 'MTIG4', 'Nome': 'Metalgráfica Iguaçu'}, {'Ticker': 'BLUT4', 'Nome': 'Blue Tech Solutions'}, {'Ticker': 'BLUT3', 'Nome': 'Blue Tech Solutions'}, {'Ticker': 'MODL4', 'Nome': 'Banco Modal'}, {'Ticker': 'CARD3', 'Nome': 'CARD3'}, {'Ticker': 'SHUL3', 'Nome': 'Schulz'}, {'Ticker': 'FIGE3', 'Nome': 'Investimentos Bemge'}, {'Ticker': 'FNCN3', 'Nome': 'Finansinos'}, {'Ticker': 'TEKA3', 'Nome': 'Teka'}, {'Ticker': 'HETA3', 'Nome': 'Hercules'}, {'Ticker': 'LCAM3', 'Nome': 'Locamerica'}, {'Ticker': 'BIDI4', 'Nome': 'Banco Inter'}, {'Ticker': 'BIDI3', 'Nome': 'Banco Inter'}, {'Ticker': 'EEEL4', 'Nome': 'CEEE GT'}, {'Ticker': 'EEEL3', 'Nome': 'CEEE GT'}, {'Ticker': 'BBRK3', 'Nome': 'BBRK3'}, {'Ticker': 'SOND3', 'Nome': 'Sondotécnica'}, {'Ticker': 'CESP6', 'Nome': 'CESP'}, {'Ticker': 'CESP3', 'Nome': 'CESP'}, {'Ticker': 'CESP5', 'Nome': 'CESP'}, {'Ticker': 'ECPR4', 'Nome': 'Encorpar'}, {'Ticker': 'MOSI3', 'Nome': 'Mosaico'}, {'Ticker': 'POWE3', 'Nome': 'Focus Energia'}, {'Ticker': 'ECPR3', 'Nome': 'Encorpar'}, {'Ticker': 'GNDI3', 'Nome': 'NotreDame Intermédica'}, {'Ticker': 'LAME4', 'Nome': 'Lojas Americanas'}, {'Ticker': 'LAME3', 'Nome': 'Lojas Americanas'}, {'Ticker': 'OMGE3', 'Nome': 'Omega Geração'}, {'Ticker': 'IGTA3', 'Nome': 'IGTA3'}, {'Ticker': 'JPSA3', 'Nome': 'JPSA3'}, {'Ticker': 'BRDT3', 'Nome': 'BRDT3'}, {'Ticker': 'JBDU4', 'Nome': 'JBDU4'}, {'Ticker': 'JBDU3', 'Nome': 'JBDU3'}, {'Ticker': 'HGTX3', 'Nome': 'Hering'}, {'Ticker': 'CCPR3', 'Nome': 'CCPR3'}, {'Ticker': 'DTEX3', 'Nome': 'DTEX3'}, {'Ticker': 'VVAR3', 'Nome': 'VVAR3'}, {'Ticker': 'PNVL4', 'Nome': 'Dimed'}, {'Ticker': 'TESA3', 'Nome': 'Terra Santa'}, {'Ticker': 'BTOW3', 'Nome': 'BTOW3'}, {'Ticker': 'LINX3', 'Nome': 'Linx'}, {'Ticker': 'BTTL3', 'Nome': 'Embpar'}, {'Ticker': 'GPCP3', 'Nome': 'GPCP3'}, {'Ticker': 'GPCP4', 'Nome': 'GPCP4'}, {'Ticker': 'SMLS3', 'Nome': 'Smiles'}, {'Ticker': 'MMXM3', 'Nome': 'MMX Mineração'}, {'Ticker': 'BSEV3', 'Nome': 'Biosev'}, {'Ticker': 'CNTO3', 'Nome': 'CNTO3'}, {'Ticker': 'TIET4', 'Nome': 'AES Tietê Energia'}, {'Ticker': 'TIET3', 'Nome': 'AES Tietê Energia'}, {'Ticker': 'CORR4', 'Nome': 'Corrêa Ribeiro'}, {'Ticker': 'CEPE3', 'Nome': 'CELPE'}, {'Ticker': 'CALI4', 'Nome': 'Adolpho Lindenberg'}, {'Ticker': 'SNSY6', 'Nome': 'Sansuy'}, {'Ticker': 'CASN4', 'Nome': 'CASAN'}, {'Ticker': 'EMAE3', 'Nome': 'EMAE'}, {'Ticker': 'BPAR3', 'Nome': 'Banpará'}, {'Ticker': 'APTI4', 'Nome': 'Aliperti'}, {'Ticker': 'VSPT3', 'Nome': 'FCA'}, {'Ticker': 'MTIG3', 'Nome': 'Metalgráfica Iguaçu'}, {'Ticker': 'FIGE4', 'Nome': 'Investimentos Bemge'}, {'Ticker': 'LUXM3', 'Nome': 'Trevisa'}, {'Ticker': 'TKNO3', 'Nome': 'Tekno'}, {'Ticker': 'COCE6', 'Nome': 'Coelce'}, {'Ticker': 'MGEL3', 'Nome': 'Mangels'}, {'Ticker': 'CTSA8', 'Nome': 'Santanense'}, {'Ticker': 'MMAQ4', 'Nome': 'Minasmáquinas'}]

# Transforma a lista de dicionários em um DataFrame
mostrar_tabela = st.checkbox("Exibir Tabela")

# Exibir a tabela se a opção estiver marcada
if mostrar_tabela:
    st.write('Tickers x Empresas')
    st.write(df)
else:
    st.write("A tabela está oculta. Marque a opção acima para exibi-la.")
df = pd.DataFrame(dados)

# Adiciona uma barra lateral para filtrar os dados
filtro_nome = st.sidebar.text_input("Filtrar a tabela por Empresa:", "")
filtro_codigo = st.sidebar.text_input("Filtrar a tabela por Ticker:", "")


# Aplica os filtros
df_filtrado = df[df["Ticker"].str.contains(filtro_codigo) & df["Nome"].str.contains(filtro_nome, case=False)]

# Exibe o DataFrame filtrado no Streamlit

st.write("###### Não sabe o ticker da companhia que está analisando? Basta filtrar a tabela.")
st.table(df_filtrado)



@dataclass
class Ativo:
    ticker: str
    periodo_anterior: str = '1y'
    dias_a_frente: int = 30
    retorno_esperado: float = 0.05

    @staticmethod
    def obter_precos(ticker, periodo):
        ativo = yf.Ticker(ticker)
        historico_ativo = ativo.history(period=periodo)
        return historico_ativo['Close']

    @staticmethod
    def simular_precos(historico_ativo, dias_a_frente, retorno_esperado):
        retornos_log = np.log(1 + historico_ativo.pct_change())
        media_retornos = retornos_log.mean()
        variancia_retornos = retornos_log.var()
        drift = media_retornos - (0.5 * variancia_retornos)
        desvio_padrao = retornos_log.std()

        retornos_diarios = np.exp(drift + desvio_padrao * norm.ppf(np.random.rand(dias_a_frente, dias_a_frente)))

        caminhos_precos = np.zeros((dias_a_frente, dias_a_frente))
        caminhos_precos[0] = historico_ativo.iloc[-1]

        for t in range(1, dias_a_frente):
            caminhos_precos[t] = caminhos_precos[t - 1] * retornos_diarios[t]

        return caminhos_precos

    @staticmethod
    def calcular_retorno_probabilidade(caminhos_precos, retorno_esperado):
        previsto = caminhos_precos[-1]
        lista_prevista = list(previsto)
        atual = caminhos_precos[0, 0]
        maiores_ou_iguais = [i / atual for i in lista_prevista if 1 - (i / atual) >= retorno_esperado]
        probabilidade = len(maiores_ou_iguais) / len(lista_prevista)
        return probabilidade * 100

    def probabilidade_retorno(self):
        historico_ativo = self.obter_precos(self.ticker, self.periodo_anterior)
        caminhos_precos = self.simular_precos(historico_ativo, self.dias_a_frente, self.retorno_esperado)
        return self.calcular_retorno_probabilidade(caminhos_precos, self.retorno_esperado)


class AnalisadorDadosMercado(Ativo):
    def __init__(self, days_ahead=30, return_expected=0.02):
        super().__init__('')  # Inicializa a classe Ativo com um ticker fictício
        self.dias_a_frente = days_ahead
        self.retorno_esperado = return_expected

    def obter_preco(self, ticker, periodo='2mo'):
        ticker = ticker.upper()
        if not ticker.endswith('.SA'):
            ticker += '.SA'

        ativo = yf.Ticker(ticker)
        precos = ativo.history(period=periodo)
        return precos['Close']

    def obter_noticias(self, ticker, num_noticias=10):
        googlenews = GoogleNews(lang='ptbr', region='BR', period='7d')
        googlenews.get_news(ticker)
        results = googlenews.results()
        return results[:num_noticias]

    def baixar_dados(self, ticker, periodo='2mo'):
        precos = self.obter_preco(ticker, periodo)
        noticias = self.obter_noticias(ticker)
        return precos, noticias

    def simular_precos(self, historico_ativo):
        retornos_log = np.log(1 + historico_ativo.pct_change())
        mu = retornos_log.mean()
        var = retornos_log.var()
        drift = mu - (0.5 * var)
        stdev = retornos_log.std()

        daily_returns = np.exp(drift + stdev * norm.ppf(np.random.rand(self.dias_a_frente, self.dias_a_frente)))

        price_paths = np.zeros((self.dias_a_frente, self.dias_a_frente))
        price_paths[0] = historico_ativo.iloc[-1]

        for t in range(1, self.dias_a_frente):
            price_paths[t] = price_paths[t - 1] * daily_returns[t]

        return price_paths

    def calcular_retorno_probabilidade(self, price_paths):
        actual = price_paths[0, 0]
        over = (price_paths[-1] / actual) >= (1 + self.retorno_esperado)
        prob = np.mean(over)
        return prob


# Exemplo de uso com Streamlit

# Adiciona os inputs na barra lateral
ticker_interesse = st.sidebar.text_input("Insira o ticker de interesse (ex: MGLU3):").upper()

# Adiciona botões para escolher entre Dias, Meses e Anos
periodo_opcao = st.sidebar.radio("Escolha o período do histórico de preços:", ["Dias", "Meses", "Anos"])

# Adiciona um número input entre 1 e 30
if periodo_opcao == "Dias":
    numero_periodo = st.sidebar.number_input("Escolha o número de dias (1-30):", min_value=1, max_value=30)
    periodo_interesse = f"{numero_periodo}d"
elif periodo_opcao == "Meses":
    numero_periodo = st.sidebar.number_input("Escolha o número de meses (1-12):", min_value=1, max_value=12)
    periodo_interesse = f"{numero_periodo}mo"
else:
    numero_periodo = st.sidebar.number_input("Escolha o número de anos:", min_value=1, max_value=1000)
    periodo_interesse = f"{numero_periodo}y"

# Restante do código permanece igual
if st.sidebar.button("Analisar"):
    try:
        # Criar instância do AnalisadorDadosMercado
        analisador = AnalisadorDadosMercado(days_ahead=numero_periodo)

        # Obter dados
        precos, noticias = analisador.baixar_dados(ticker_interesse, periodo_interesse)

        # Verificar se os dados foram obtidos corretamente
        if precos is None or noticias is None:
            st.sidebar.error("Não foi possível obter dados para o ativo selecionado. Tente novamente mais tarde.")
        else:
            # Simular preços futuros e calcular probabilidade de retorno
            caminhos_precos = analisador.simular_precos(precos)
            prob_retorno = analisador.calcular_retorno_probabilidade(caminhos_precos)

            # Plotar gráfico de histórico de preços
            df_precos = pd.DataFrame({'Data': precos.index, 'Preço de Fechamento': precos.values})
            chart_precos = alt.Chart(df_precos).mark_line().encode(
                x='Data:T',
                y='Preço de Fechamento:Q'
            ).properties(
                width=600,
                height=400,
                title=f'Histórico de Preços para {ticker_interesse}'
            )
            st.altair_chart(chart_precos)

            st.write(f"**Probabilidade de Retorno ser maior ou igual a {analisador.retorno_esperado*100}%:{prob_retorno*100:.2f}% (MBG)**")

            # Exibir títulos e links das notícias
            st.markdown(f"**📰 Últimas Notícias para {ticker_interesse}**")
            if noticias:
                # Criar lista para exibir títulos e links
                for noticia in noticias:
                    link_parts = noticia['link'].split('/~/+/')
                    link = link_parts[1] if len(link_parts) > 1 else noticia['link']  # Se o padrão não estiver presente, use o link original
                    st.markdown(f"- [{noticia['title']}]({link})", unsafe_allow_html=True)

    except Exception as e:
        st.sidebar.error("Não foi possível realizar o cálculo para o ativo selecionado no momento. Tente novamente mais tarde.")

