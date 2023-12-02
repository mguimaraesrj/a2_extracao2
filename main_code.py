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
st.write("###### Faça a sua consulta para otimizar seu tempo e aprimorar seu processo de análise. Selecione o ticker do seu ativo de interesse e veja as informações relacionadas a companhia.")

st.sidebar.markdown("# Start Investor 📈")  # Adiciona título à barra lateral

dados = [{'Código': 'MGLU3', 'Nome': 'Magazine Luiza'}, {'Código': 'HAPV3', 'Nome': 'Hapvida'}, {'Código': 'CIEL3', 'Nome': 'Cielo'}, {'Código': 'BBDC4', 'Nome': 'Banco Bradesco'}, {'Código': 'PETR4', 'Nome': 'Petrobras'}, {'Código': 'ITUB4', 'Nome': 'Itaú Unibanco'}, {'Código': 'ABEV3', 'Nome': 'Ambev'}, {'Código': 'LREN3', 'Nome': 'Lojas Renner'}, {'Código': 'COGN3', 'Nome': 'Cogna'}, {'Código': 'B3SA3', 'Nome': 'B3'}, {'Código': 'CVCB3', 'Nome': 'CVC'}, {'Código': 'ITSA4', 'Nome': 'Itaúsa'}, {'Código': 'VALE3', 'Nome': 'Vale'}, {'Código': 'SOMA3', 'Nome': 'Grupo Soma'}, {'Código': 'USIM5', 'Nome': 'Usiminas'}, {'Código': 'ASAI3', 'Nome': 'Assaí'}, {'Código': 'BRKM5', 'Nome': 'Braskem'}, {'Código': 'RAIZ4', 'Nome': 'Raízen'}, {'Código': 'MRVE3', 'Nome': 'MRV'}, {'Código': 'SUZB3', 'Nome': 'Suzano'}, {'Código': 'CPLE6', 'Nome': 'Copel'}, {'Código': 'VBBR3', 'Nome': 'Vibra Energia'}, {'Código': 'ANIM3', 'Nome': 'Ânima Educação'}, {'Código': 'ENEV3', 'Nome': 'Eneva'}, {'Código': 'EMBR3', 'Nome': 'Embraer'}, {'Código': 'RAIL3', 'Nome': 'Rumo'}, {'Código': 'MRFG3', 'Nome': 'Marfrig'}, {'Código': 'CMIG4', 'Nome': 'CEMIG'}, {'Código': 'BEEF3', 'Nome': 'Minerva'}, {'Código': 'PRIO3', 'Nome': 'PetroRio'}, {'Código': 'POMO4', 'Nome': 'Marcopolo'}, {'Código': 'BBSE3', 'Nome': 'BB Seguridade'}, {'Código': 'AMER3', 'Nome': 'Americanas'}, {'Código': 'GGBR4', 'Nome': 'Gerdau'}, {'Código': 'KLBN4', 'Nome': 'Klabin'}, {'Código': 'RENT3', 'Nome': 'Localiza'}, {'Código': 'CSNA3', 'Nome': 'Siderúrgica Nacional'}, {'Código': 'AZUL4', 'Nome': 'Azul'}, {'Código': 'GOAU4', 'Nome': 'Metalúrgica Gerdau'}, {'Código': 'RDOR3', 'Nome': "Rede D'Or"}, {'Código': 'BBAS3', 'Nome': 'Banco do Brasil'}, {'Código': 'HBSA3', 'Nome': 'Hidrovias do Brasil'}, {'Código': 'PETZ3', 'Nome': 'Petz'}, {'Código': 'NTCO3', 'Nome': 'Natura'}, {'Código': 'QUAL3', 'Nome': 'Qualicorp'}, {'Código': 'CMIN3', 'Nome': 'CSN Mineração'}, {'Código': 'GMAT3', 'Nome': 'Grupo Mateus'}, {'Código': 'CCRO3', 'Nome': 'Grupo CCR'}, {'Código': 'CYRE3', 'Nome': 'Cyrela'}, {'Código': 'BRFS3', 'Nome': 'BRF'}, {'Código': 'EQTL3', 'Nome': 'Equatorial Energia'}, {'Código': 'AERI3', 'Nome': 'Aeris Energy'}, {'Código': 'PETR3', 'Nome': 'Petrobras'}, {'Código': 'CEAB3', 'Nome': 'C&A'}, {'Código': 'JBSS3', 'Nome': 'JBS'}, {'Código': 'AURE3', 'Nome': 'VTRM ENERGIA PARTICIPAÃiES S.A.'}, {'Código': 'RRRP3', 'Nome': '3R Petroleum'}, {'Código': 'TIMS3', 'Nome': 'TIM'}, {'Código': 'ELET3', 'Nome': 'Eletrobras'}, {'Código': 'BBDC3', 'Nome': 'Banco Bradesco'}, {'Código': 'CRFB3', 'Nome': 'Carrefour Brasil'}, {'Código': 'PCAR3', 'Nome': 'Grupo Pão de Açúcar'}, {'Código': 'ALPA4', 'Nome': 'Alpargatas'}, {'Código': 'CSMG3', 'Nome': 'COPASA'}, {'Código': 'LWSA3', 'Nome': 'Locaweb'}, {'Código': 'MULT3', 'Nome': 'Multiplan'}, {'Código': 'JHSF3', 'Nome': 'JHSF'}, {'Código': 'RADL3', 'Nome': 'RaiaDrogasil'}, {'Código': 'IFCM3', 'Nome': 'Infracommerce'}, {'Código': 'WEGE3', 'Nome': 'WEG'}, {'Código': 'GOLL4', 'Nome': 'GOL'}, {'Código': 'RECV3', 'Nome': 'PetroRecôncavo'}, {'Código': 'SEQL3', 'Nome': 'Sequoia Logística'}, {'Código': 'MLAS3', 'Nome': 'Multilaser'}, {'Código': 'MOVI3', 'Nome': 'Movida'}, {'Código': 'CSAN3', 'Nome': 'Cosan'}, {'Código': 'VAMO3', 'Nome': 'Grupo Vamos'}, {'Código': 'TEND3', 'Nome': 'Construtora Tenda'}, {'Código': 'SMFT3', 'Nome': 'Smart Fit'}, {'Código': 'ECOR3', 'Nome': 'EcoRodovias'}, {'Código': 'TOTS3', 'Nome': 'Totvs'}, {'Código': 'CBAV3', 'Nome': 'CBA'}, {'Código': 'UGPA3', 'Nome': 'Ultrapar'}, {'Código': 'GFSA3', 'Nome': 'Gafisa'}, {'Código': 'IRBR3', 'Nome': 'IRB Brasil RE'}, {'Código': 'FLRY3', 'Nome': 'Fleury'}, {'Código': 'CXSE3', 'Nome': 'Caixa Seguridade'}, {'Código': 'ONCO3', 'Nome': 'Oncoclínicas'}, {'Código': 'BRAP4', 'Nome': 'Bradespar'}, {'Código': 'SBFG3', 'Nome': 'Grupo SBF'}, {'Código': 'OIBR3', 'Nome': 'Oi'}, {'Código': 'RAPT4', 'Nome': 'Randon'}, {'Código': 'SIMH3', 'Nome': 'Simpar'}, {'Código': 'CPFE3', 'Nome': 'CPFL Energia'}, {'Código': 'YDUQ3', 'Nome': 'YDUQS'}, {'Código': 'CURY3', 'Nome': 'Cury'}, {'Código': 'TRPL4', 'Nome': 'Transmissão Paulista'}, {'Código': 'CPLE3', 'Nome': 'Copel'}, {'Código': 'KEPL3', 'Nome': 'Kepler Weber'}, {'Código': 'LJQQ3', 'Nome': 'Lojas Quero-Quero'}, {'Código': 'SBSP3', 'Nome': 'Sabesp'}, {'Código': 'DXCO3', 'Nome': 'Dexco'}, {'Código': 'ESPA3', 'Nome': 'Espaçolaser'}, {'Código': 'EZTC3', 'Nome': 'EZTEC'}, {'Código': 'SAPR4', 'Nome': 'Sanepar'}, {'Código': 'DIRR3', 'Nome': 'Direcional'}, {'Código': 'BRSR6', 'Nome': 'Banrisul'}, {'Código': 'KLBN3', 'Nome': 'Klabin'}, {'Código': 'AZEV4', 'Nome': 'Azevedo & Travassos'}, {'Código': 'STBP3', 'Nome': 'Santos Brasil'}, {'Código': 'GUAR3', 'Nome': 'Guararapes'}, {'Código': 'ARZZ3', 'Nome': 'Arezzo'}, {'Código': 'SGPS3', 'Nome': 'Springs'}, {'Código': 'MEGA3', 'Nome': 'OMEGA ENERGIA S.A.'}, {'Código': 'SLCE3', 'Nome': 'SLC Agrícola'}, {'Código': 'HYPE3', 'Nome': 'Hypera'}, {'Código': 'EGIE3', 'Nome': 'Engie'}, {'Código': 'NEOE3', 'Nome': 'Neoenergia'}, {'Código': 'GGPS3', 'Nome': 'GPS'}, {'Código': 'VIVA3', 'Nome': 'Vivara'}, {'Código': 'TTEN3', 'Nome': '3tentos'}, {'Código': 'RANI3', 'Nome': 'Irani'}, {'Código': 'PSSA3', 'Nome': 'Porto Seguro'}, {'Código': 'INTB3', 'Nome': 'Intelbras'}, {'Código': 'VIVT3', 'Nome': 'Vivo'}, {'Código': 'AMAR3', 'Nome': 'Lojas Marisa'}, {'Código': 'PDGR3', 'Nome': 'PDG Realty'}, {'Código': 'SMTO3', 'Nome': 'São Martinho'}, {'Código': 'ENAT3', 'Nome': 'Enauta'}, {'Código': 'AMBP3', 'Nome': 'Ambipar'}, {'Código': 'MEAL3', 'Nome': 'IMC Alimentação'}, {'Código': 'CLSA3', 'Nome': 'ClearSale'}, {'Código': 'GRND3', 'Nome': 'Grendene'}, {'Código': 'POSI3', 'Nome': 'Positivo'}, {'Código': 'AESB3', 'Nome': 'AES Brasil'}, {'Código': 'CASH3', 'Nome': 'Méliuz'}, {'Código': 'MDIA3', 'Nome': 'M. Dias Branco'}, {'Código': 'DESK3', 'Nome': 'Desktop'}, {'Código': 'MTRE3', 'Nome': 'Mitre Realty'}, {'Código': 'VVEO3', 'Nome': 'Viveo'}, {'Código': 'MBLY3', 'Nome': 'Mobly'}, {'Código': 'RCSL4', 'Nome': 'Recrusul'}, {'Código': 'PLPL3', 'Nome': 'Plano&Plano'}, {'Código': 'PGMN3', 'Nome': 'Pague Menos'}, {'Código': 'WIZC3', 'Nome': 'Wiz Soluções'}, {'Código': 'SHUL4', 'Nome': 'Schulz'}, {'Código': 'BPAN4', 'Nome': 'Banco Pan'}, {'Código': 'SEER3', 'Nome': 'Ser Educacional'}, {'Código': 'CAML3', 'Nome': 'Camil Alimentos'}, {'Código': 'ARML3', 'Nome': 'Armac'}, {'Código': 'ODPV3', 'Nome': 'Odontoprev'}, {'Código': 'MATD3', 'Nome': 'Mater Dei'}, {'Código': 'LEVE3', 'Nome': 'Mahle Metal Leve'}, {'Código': 'ZAMP3', 'Nome': 'Zamp'}, {'Código': 'CSED3', 'Nome': 'Cruzeiro do Sul Educacional'}, {'Código': 'TRAD3', 'Nome': 'Traders Club'}, {'Código': 'AGRO3', 'Nome': 'BrasilAgro'}, {'Código': 'LIGT3', 'Nome': 'Light'}, {'Código': 'ELET6', 'Nome': 'Eletrobras'}, {'Código': 'VULC3', 'Nome': 'Vulcabras'}, {'Código': 'DASA3', 'Nome': 'Dasa'}, {'Código': 'MYPK3', 'Nome': 'Iochpe-Maxion'}, {'Código': 'TRIS3', 'Nome': 'Trisul'}, {'Código': 'OPCT3', 'Nome': 'OceanPact'}, {'Código': 'AZEV3', 'Nome': 'Azevedo & Travassos'}, {'Código': 'ABCB4', 'Nome': 'Banco ABC Brasil'}, {'Código': 'ORVR3', 'Nome': 'Orizon'}, {'Código': 'RCSL3', 'Nome': 'Recrusul'}, {'Código': 'PFRM3', 'Nome': 'Profarma'}, {'Código': 'CMIG3', 'Nome': 'CEMIG'}, {'Código': 'LAVV3', 'Nome': 'Lavvi Incorporadora'}, {'Código': 'JALL3', 'Nome': 'Jalles Machado'}, {'Código': 'MDNE3', 'Nome': 'Moura Dubeux'}, {'Código': 'LOGG3', 'Nome': 'LOG CP'}, {'Código': 'BMGB4', 'Nome': 'Banco BMG'}, {'Código': 'PNVL3', 'Nome': 'Dimed'}, {'Código': 'PTBL3', 'Nome': 'Portobello'}, {'Código': 'MILS3', 'Nome': 'Mills'}, {'Código': 'FIQE3', 'Nome': 'Unifique'}, {'Código': 'LUPA3', 'Nome': 'Lupatech'}, {'Código': 'BRIT3', 'Nome': 'Brisanet'}, {'Código': 'BLAU3', 'Nome': 'Blau Farmacêutica'}, {'Código': 'PRNR3', 'Nome': 'Priner'}, {'Código': 'EVEN3', 'Nome': 'Even'}, {'Código': 'CTNM4', 'Nome': 'Coteminas'}, {'Código': 'VLID3', 'Nome': 'Valid'}, {'Código': 'TASA4', 'Nome': 'Taurus'}, {'Código': 'HBOR3', 'Nome': 'Helbor'}, {'Código': 'FRAS3', 'Nome': 'Fras-le'}, {'Código': 'SHOW3', 'Nome': 'Time For Fun'}, {'Código': 'HBRE3', 'Nome': 'HBR Realty'}, {'Código': 'ENJU3', 'Nome': 'Enjoei'}, {'Código': 'NGRD3', 'Nome': 'Neogrid'}, {'Código': 'FESA4', 'Nome': 'Ferbasa'}, {'Código': 'ITUB3', 'Nome': 'Itaú Unibanco'}, {'Código': 'PINE4', 'Nome': 'PINE'}, {'Código': 'VIVR3', 'Nome': 'Viver'}, {'Código': 'CTSA4', 'Nome': 'Santanense'}, {'Código': 'JSLG3', 'Nome': 'JSL'}, {'Código': 'CTSA3', 'Nome': 'Santanense'}, {'Código': 'RNEW4', 'Nome': 'Renova Energia'}, {'Código': 'SAPR3', 'Nome': 'Sanepar'}, {'Código': 'VITT3', 'Nome': 'Vittia'}, {'Código': 'TUPY3', 'Nome': 'Tupy'}, {'Código': 'USIM3', 'Nome': 'Usiminas'}, {'Código': 'ROMI3', 'Nome': 'Indústrias ROMI'}, {'Código': 'KRSA3', 'Nome': 'Kora Saúde'}, {'Código': 'ALPK3', 'Nome': 'Estapar'}, {'Código': 'SYNE3', 'Nome': 'SYN'}, {'Código': 'WEST3', 'Nome': 'Westwing'}, {'Código': 'PDTC3', 'Nome': 'Padtec'}, {'Código': 'BMOB3', 'Nome': 'Bemobi'}, {'Código': 'TGMA3', 'Nome': 'Tegma'}, {'Código': 'BRKM3', 'Nome': 'Braskem'}, {'Código': 'UNIP6', 'Nome': 'Unipar'}, {'Código': 'PORT3', 'Nome': 'Wilson Sons'}, {'Código': 'AALR3', 'Nome': 'Alliança'}, {'Código': 'TECN3', 'Nome': 'Technos'}, {'Código': 'TAEE4', 'Nome': 'Taesa'}, {'Código': 'ETER3', 'Nome': 'Eternit'}, {'Código': 'UCAS3', 'Nome': 'Unicasa'}, {'Código': 'TFCO4', 'Nome': 'Track & Field'}, {'Código': 'LPSB3', 'Nome': 'Lopes'}, {'Código': 'ITSA3', 'Nome': 'Itaúsa'}, {'Código': 'MTSA4', 'Nome': 'METISA'}, {'Código': 'SOJA3', 'Nome': 'Boa Safra Sementes'}, {'Código': 'BRAP3', 'Nome': 'Bradespar'}, {'Código': 'POMO3', 'Nome': 'Marcopolo'}, {'Código': 'TCSA3', 'Nome': 'Tecnisa'}, {'Código': 'NINJ3', 'Nome': 'GetNinjas'}, {'Código': 'IGTI3', 'Nome': 'Jereissati Participações'}, {'Código': 'IGTI3', 'Nome': 'Iguatemi'}, {'Código': 'DEXP3', 'Nome': 'Dexxos'}, {'Código': 'SANB4', 'Nome': 'Banco Santander'}, {'Código': 'MELK3', 'Nome': 'Melnick'}, {'Código': 'LAND3', 'Nome': 'Terra Santa'}, {'Código': 'ALLD3', 'Nome': 'Allied'}, {'Código': 'SANB3', 'Nome': 'Banco Santander'}, {'Código': 'TAEE3', 'Nome': 'Taesa'}, {'Código': 'CAMB3', 'Nome': 'Cambuci'}, {'Código': 'RSID3', 'Nome': 'Rossi Residencial'}, {'Código': 'RNEW3', 'Nome': 'Renova Energia'}, {'Código': 'DMVF3', 'Nome': 'D1000 Varejo Farma'}, {'Código': 'CSUD3', 'Nome': 'CSU Cardsystem'}, {'Código': 'ELMD3', 'Nome': 'Eletromidia'}, {'Código': 'DOTZ3', 'Nome': 'Dotz'}, {'Código': 'GGBR3', 'Nome': 'Gerdau'}, {'Código': 'GOAU3', 'Nome': 'Metalúrgica Gerdau'}, {'Código': 'LOGN3', 'Nome': 'Log-In'}, {'Código': 'APER3', 'Nome': 'Alper'}, {'Código': 'TPIS3', 'Nome': 'Triunfo'}, {'Código': 'AGXY3', 'Nome': 'AgroGalaxy'}, {'Código': 'PMAM3', 'Nome': 'Paranapanema'}, {'Código': 'EUCA4', 'Nome': 'Eucatex'}, {'Código': 'BPAC5', 'Nome': 'Banco BTG Pactual'}, {'Código': 'SCAR3', 'Nome': 'São Carlos'}, {'Código': 'OIBR4', 'Nome': 'Oi'}, {'Código': 'BOBR4', 'Nome': 'Bombril'}, {'Código': 'JFEN3', 'Nome': 'João Fortes'}, {'Código': 'INEP4', 'Nome': 'Inepar'}, {'Código': 'TASA3', 'Nome': 'Taurus'}, {'Código': 'ALUP4', 'Nome': 'Alupar'}, {'Código': 'INEP3', 'Nome': 'Inepar'}, {'Código': 'ATMP3', 'Nome': 'Atma'}, {'Código': 'BMEB4', 'Nome': 'Banco Mercantil do Brasil'}, {'Código': 'RPMG3', 'Nome': 'Refinaria de Manguinhos'}, {'Código': 'ALUP3', 'Nome': 'Alupar'}, {'Código': 'CEBR6', 'Nome': 'CEB'}, {'Código': 'ATOM3', 'Nome': 'ATOM'}, {'Código': 'LVTC3', 'Nome': 'WDC Networks'}, {'Código': 'SNSY5', 'Nome': 'Sansuy'}, {'Código': 'EPAR3', 'Nome': 'EPAR3'}, {'Código': 'RAPT3', 'Nome': 'Randon'}, {'Código': 'PTNT4', 'Nome': 'Pettenati'}, {'Código': 'COCE5', 'Nome': 'Coelce'}, {'Código': 'UNIP3', 'Nome': 'Unipar'}, {'Código': 'BEES3', 'Nome': 'Banestes'}, {'Código': 'NUTR3', 'Nome': 'Nutriplant'}, {'Código': 'TELB4', 'Nome': 'Telebras'}, {'Código': 'CEBR3', 'Nome': 'CEB'}, {'Código': 'CGRA4', 'Nome': 'Grazziotin'}, {'Código': 'MNPR3', 'Nome': 'Minupar'}, {'Código': 'ENGI4', 'Nome': 'Energisa'}, {'Código': 'BIOM3', 'Nome': 'Biomm'}, {'Código': 'VSTE3', 'Nome': 'LE LIS BLANC'}, {'Código': 'BPAC3', 'Nome': 'Banco BTG Pactual'}, {'Código': 'BRSR3', 'Nome': 'Banrisul'}, {'Código': 'REDE3', 'Nome': 'Rede Energia'}, {'Código': 'DEXP4', 'Nome': 'Dexxos'}, {'Código': 'FHER3', 'Nome': 'Fertilizantes Heringer'}, {'Código': 'CGRA3', 'Nome': 'Grazziotin'}, {'Código': 'ENGI3', 'Nome': 'Energisa'}, {'Código': 'BEES4', 'Nome': 'Banestes'}, {'Código': 'BRIV4', 'Nome': 'Alfa Investimento'}, {'Código': 'ESTR4', 'Nome': 'Estrela'}, {'Código': 'WHRL3', 'Nome': 'Whirlpool'}, {'Código': 'HAGA3', 'Nome': 'Haga'}, {'Código': 'BAHI3', 'Nome': 'Bahema'}, {'Código': 'MWET4', 'Nome': 'Wetzel'}, {'Código': 'EMAE4', 'Nome': 'EMAE'}, {'Código': 'ALPA3', 'Nome': 'Alpargatas'}, {'Código': 'OSXB3', 'Nome': 'OSX Brasil'}, {'Código': 'EALT4', 'Nome': 'Electro Aço Altona'}, {'Código': 'CRIV3', 'Nome': 'Alfa Financeira'}, {'Código': 'CRIV4', 'Nome': 'Alfa Financeira'}, {'Código': 'EUCA3', 'Nome': 'Eucatex'}, {'Código': 'HOOT4', 'Nome': 'Hotéis Othon'}, {'Código': 'CRPG6', 'Nome': 'Tronox Pigmentos'}, {'Código': 'OFSA3', 'Nome': 'Ourofino Saúde Animal'}, {'Código': 'RDNI3', 'Nome': 'RNI'}, {'Código': 'RSUL4', 'Nome': 'Metalúrgica Riosulense'}, {'Código': 'EQPA3', 'Nome': 'Equatorial Energia Pará'}, {'Código': 'BGIP4', 'Nome': 'Banese'}, {'Código': 'CEBR5', 'Nome': 'CEB'}, {'Código': 'FRTA3', 'Nome': 'Pomi Frutas'}, {'Código': 'TRPL3', 'Nome': 'Transmissão Paulista'}, {'Código': 'CTKA4', 'Nome': 'Karsten'}, {'Código': 'HETA4', 'Nome': 'Hercules'}, {'Código': 'CLSC4', 'Nome': 'Celesc'}, {'Código': 'CEEB3', 'Nome': 'COELBA'}, {'Código': 'CRPG5', 'Nome': 'Tronox Pigmentos'}, {'Código': 'BRKM6', 'Nome': 'Braskem'}, {'Código': 'NEXP3', 'Nome': 'Brasil Brokers'}, {'Código': 'HAGA4', 'Nome': 'Haga'}, {'Código': 'FRIO3', 'Nome': 'Metalfrio'}, {'Código': 'WHRL4', 'Nome': 'Whirlpool'}, {'Código': 'MGEL4', 'Nome': 'Mangels'}, {'Código': 'EQPA5', 'Nome': 'Equatorial Energia Pará'}, {'Código': 'AVLL3', 'Nome': 'Alphaville'}, {'Código': 'WLMM3', 'Nome': 'WLM'}, {'Código': 'BAZA3', 'Nome': 'Banco da Amazônia'}, {'Código': 'TEKA4', 'Nome': 'Teka'}, {'Código': 'BDLL4', 'Nome': 'Bardella'}, {'Código': 'EKTR4', 'Nome': 'Elektro'}, {'Código': 'GEPA4', 'Nome': 'Rio Paranapanema Energia'}, {'Código': 'CPLE5', 'Nome': 'Copel'}, {'Código': 'CTNM3', 'Nome': 'Coteminas'}, {'Código': 'AFLT3', 'Nome': 'Afluente T'}, {'Código': 'TELB3', 'Nome': 'Telebras'}, {'Código': 'MNDL3', 'Nome': 'Mundial'}, {'Código': 'CSRN3', 'Nome': 'COSERN'}, {'Código': 'CEDO4', 'Nome': 'Cedro Têxtil'}, {'Código': 'BMEB3', 'Nome': 'Banco Mercantil do Brasil'}, {'Código': 'BMIN4', 'Nome': 'Banco Mercantil de Investimentos'}, {'Código': 'IGTI4', 'Nome': 'Jereissati Participações'}, {'Código': 'IGTI4', 'Nome': 'Iguatemi'}, {'Código': 'PLAS3', 'Nome': 'Plascar'}, {'Código': 'CGAS5', 'Nome': 'Comgás'}, {'Código': 'EQPA7', 'Nome': 'Equatorial Energia Pará'}, {'Código': 'ENMT3', 'Nome': 'Energisa MT'}, {'Código': 'BALM4', 'Nome': 'Baumer'}, {'Código': 'BAUH4', 'Nome': 'Excelsior'}, {'Código': 'HBTS5', 'Nome': 'Habitasul'}, {'Código': 'WLMM4', 'Nome': 'WLM'}, {'Código': 'PTNT3', 'Nome': 'Pettenati'}, {'Código': 'BNBR3', 'Nome': 'Banco do Nordeste'}, {'Código': 'BGIP3', 'Nome': 'Banese'}, {'Código': 'JOPA3', 'Nome': 'Josapar'}, {'Código': 'CALI3', 'Nome': 'Adolpho Lindenberg'}, {'Código': 'DOHL4', 'Nome': 'Döhler'}, {'Código': 'DTCY3', 'Nome': 'Dtcom'}, {'Código': 'NORD3', 'Nome': 'Nordon'}, {'Código': 'BMKS3', 'Nome': 'Monark'}, {'Código': 'BSLI4', 'Nome': 'Banco de Brasília'}, {'Código': 'FESA3', 'Nome': 'Ferbasa'}, {'Código': 'LUXM4', 'Nome': 'Trevisa'}, {'Código': 'BALM3', 'Nome': 'Baumer'}, {'Código': 'BMIN3', 'Nome': 'Banco Mercantil de Investimentos'}, {'Código': 'PATI3', 'Nome': 'Panatlântica'}, {'Código': 'BRIV3', 'Nome': 'Alfa Investimento'}, {'Código': 'CSAB3', 'Nome': 'Cia. de Seg. Aliança da Bahia'}, {'Código': 'EQMA3B', 'Nome': 'Equatorial Maranhão'}, {'Código': 'CSAB4', 'Nome': 'Cia. de Seg. Aliança da Bahia'}, {'Código': 'CEDO3', 'Nome': 'Cedro Têxtil'}, {'Código': 'BRSR5', 'Nome': 'Banrisul'}, {'Código': 'MERC4', 'Nome': 'Mercantil do Brasil Financeira'}, {'Código': 'DMFN3', 'Nome': 'DMFN3'}, {'Código': 'CEED3', 'Nome': 'CEEE D'}, {'Código': 'BSLI3', 'Nome': 'Banco de Brasília'}, {'Código': 'CGAS3', 'Nome': 'Comgás'}, {'Código': 'UNIP5', 'Nome': 'Unipar'}, {'Código': 'FIEI3', 'Nome': 'FIEI3'}, {'Código': 'RPAD3', 'Nome': 'Alfa Holdings'}, {'Código': 'EALT3', 'Nome': 'Electro Aço Altona'}, {'Código': 'ENMT4', 'Nome': 'Energisa MT'}, {'Código': 'CEED4', 'Nome': 'CEEE D'}, {'Código': 'DOHL3', 'Nome': 'Döhler'}, {'Código': 'CEEB5', 'Nome': 'COELBA'}, {'Código': 'PEAB3', 'Nome': 'Participações Aliança da Bahia'}, {'Código': 'MRSA3B', 'Nome': 'MRS Logística'}, {'Código': 'BRGE12', 'Nome': 'Consórcio Alfa'}, {'Código': 'CLSC3', 'Nome': 'Celesc'}, {'Código': 'RPAD6', 'Nome': 'Alfa Holdings'}, {'Código': 'BRGE6', 'Nome': 'Consórcio Alfa'}, {'Código': 'CRPG3', 'Nome': 'Tronox Pigmentos'}, {'Código': 'SNSY3', 'Nome': 'Sansuy'}, {'Código': 'MRSA5B', 'Nome': 'MRS Logística'}, {'Código': 'MAPT4', 'Nome': 'Cemepe'}, {'Código': 'CTKA3', 'Nome': 'Karsten'}, {'Código': 'CSRN5', 'Nome': 'COSERN'}, {'Código': 'GEPA3', 'Nome': 'Rio Paranapanema Energia'}, {'Código': 'GSHP3', 'Nome': 'General Shopping & Outlets'}, {'Código': 'RPAD5', 'Nome': 'Alfa Holdings'}, {'Código': 'AHEB3', 'Nome': 'São Paulo Turismo'}, {'Código': 'BRGE3', 'Nome': 'Consórcio Alfa'}, {'Código': 'MOAR3', 'Nome': 'Monteiro Aranha'}, {'Código': 'BRGE5', 'Nome': 'Consórcio Alfa'}, {'Código': 'CSRN6', 'Nome': 'COSERN'}, {'Código': 'TKNO4', 'Nome': 'Tekno'}, {'Código': 'BDLL3', 'Nome': 'Bardella'}, {'Código': 'ELET5', 'Nome': 'Eletrobras'}, {'Código': 'SOND6', 'Nome': 'Sondotécnica'}, {'Código': 'CBEE3', 'Nome': 'Ampla Energia'}, {'Código': 'SOND5', 'Nome': 'Sondotécnica'}, {'Código': 'GPAR3', 'Nome': 'CELGPAR'}, {'Código': 'SQIA3', 'Nome': 'Sinqia'}, {'Código': 'ESTR3', 'Nome': 'Estrela'}, {'Código': 'BRGE11', 'Nome': 'Consórcio Alfa'}, {'Código': 'BRGE8', 'Nome': 'Consórcio Alfa'}, {'Código': 'BRGE7', 'Nome': 'Consórcio Alfa'}, {'Código': 'MRSA6B', 'Nome': 'MRS Logística'}, {'Código': 'ALSO3', 'Nome': 'Aliansce Sonae'}, {'Código': 'BRPR3', 'Nome': 'BR Properties'}, {'Código': 'LIPR3', 'Nome': 'Eletropar'}, {'Código': 'PATI4', 'Nome': 'Panatlântica'}, {'Código': 'MTSA3', 'Nome': 'METISA'}, {'Código': 'SLED4', 'Nome': 'Saraiva'}, {'Código': 'SLED3', 'Nome': 'Saraiva'}, {'Código': 'EQPA6', 'Nome': 'Equatorial Energia Pará'}, {'Código': 'AHEB6', 'Nome': 'São Paulo Turismo'}, {'Código': 'PINE3', 'Nome': 'PINE'}, {'Código': 'VIIA3', 'Nome': 'VIIA3'}, {'Código': 'EKTR3', 'Nome': 'Elektro'}, {'Código': 'MWET3', 'Nome': 'Wetzel'}, {'Código': 'USIM6', 'Nome': 'Usiminas'}, {'Código': 'AHEB5', 'Nome': 'São Paulo Turismo'}, {'Código': 'ENBR3', 'Nome': 'EDP Brasil'}, {'Código': 'BOAS3', 'Nome': 'Boa Vista'}, {'Código': 'PEAB4', 'Nome': 'Participações Aliança da Bahia'}, {'Código': 'COCE3', 'Nome': 'Coelce'}, {'Código': 'JOPA4', 'Nome': 'Josapar'}, {'Código': 'MODL3', 'Nome': 'Banco Modal'}, {'Código': 'MERC3', 'Nome': 'Mercantil do Brasil Financeira'}, {'Código': 'CEGR3', 'Nome': 'Naturgy (CEG)'}, {'Código': 'MAPT3', 'Nome': 'Cemepe'}, {'Código': 'CRDE3', 'Nome': 'CR2'}, {'Código': 'IGBR3', 'Nome': 'IGB Eletrônica'}, {'Código': 'MSPA4', 'Nome': 'Melhoramentos'}, {'Código': 'ODER4', 'Nome': 'Conservas Oderich'}, {'Código': 'PARD3', 'Nome': 'Hermes Pardini'}, {'Código': 'CASN3', 'Nome': 'CASAN'}, {'Código': 'WIZS3', 'Nome': 'WIZS3'}, {'Código': 'LLIS3', 'Nome': 'LLIS3'}, {'Código': 'MSPA3', 'Nome': 'Melhoramentos'}, {'Código': 'BRML3', 'Nome': 'BRMalls'}, {'Código': 'DMMO3', 'Nome': 'Dommo Energia'}, {'Código': 'GETT3', 'Nome': 'Getnet'}, {'Código': 'GETT4', 'Nome': 'Getnet'}, {'Código': 'SULA4', 'Nome': 'SulAmérica'}, {'Código': 'SULA3', 'Nome': 'SulAmérica'}, {'Código': 'CEPE5', 'Nome': 'CELPE'}, {'Código': 'TCNO4', 'Nome': 'Tecnosolo'}, {'Código': 'TCNO3', 'Nome': 'Tecnosolo'}, {'Código': 'CEPE6', 'Nome': 'CELPE'}, {'Código': 'BKBR3', 'Nome': 'BKBR3'}, {'Código': 'MTIG4', 'Nome': 'Metalgráfica Iguaçu'}, {'Código': 'BLUT4', 'Nome': 'Blue Tech Solutions'}, {'Código': 'BLUT3', 'Nome': 'Blue Tech Solutions'}, {'Código': 'MODL4', 'Nome': 'Banco Modal'}, {'Código': 'CARD3', 'Nome': 'CARD3'}, {'Código': 'SHUL3', 'Nome': 'Schulz'}, {'Código': 'FIGE3', 'Nome': 'Investimentos Bemge'}, {'Código': 'FNCN3', 'Nome': 'Finansinos'}, {'Código': 'TEKA3', 'Nome': 'Teka'}, {'Código': 'HETA3', 'Nome': 'Hercules'}, {'Código': 'LCAM3', 'Nome': 'Locamerica'}, {'Código': 'BIDI4', 'Nome': 'Banco Inter'}, {'Código': 'BIDI3', 'Nome': 'Banco Inter'}, {'Código': 'EEEL4', 'Nome': 'CEEE GT'}, {'Código': 'EEEL3', 'Nome': 'CEEE GT'}, {'Código': 'BBRK3', 'Nome': 'BBRK3'}, {'Código': 'SOND3', 'Nome': 'Sondotécnica'}, {'Código': 'CESP6', 'Nome': 'CESP'}, {'Código': 'CESP3', 'Nome': 'CESP'}, {'Código': 'CESP5', 'Nome': 'CESP'}, {'Código': 'ECPR4', 'Nome': 'Encorpar'}, {'Código': 'MOSI3', 'Nome': 'Mosaico'}, {'Código': 'POWE3', 'Nome': 'Focus Energia'}, {'Código': 'ECPR3', 'Nome': 'Encorpar'}, {'Código': 'GNDI3', 'Nome': 'NotreDame Intermédica'}, {'Código': 'LAME4', 'Nome': 'Lojas Americanas'}, {'Código': 'LAME3', 'Nome': 'Lojas Americanas'}, {'Código': 'OMGE3', 'Nome': 'Omega Geração'}, {'Código': 'IGTA3', 'Nome': 'IGTA3'}, {'Código': 'JPSA3', 'Nome': 'JPSA3'}, {'Código': 'BRDT3', 'Nome': 'BRDT3'}, {'Código': 'JBDU4', 'Nome': 'JBDU4'}, {'Código': 'JBDU3', 'Nome': 'JBDU3'}, {'Código': 'HGTX3', 'Nome': 'Hering'}, {'Código': 'CCPR3', 'Nome': 'CCPR3'}, {'Código': 'DTEX3', 'Nome': 'DTEX3'}, {'Código': 'VVAR3', 'Nome': 'VVAR3'}, {'Código': 'PNVL4', 'Nome': 'Dimed'}, {'Código': 'TESA3', 'Nome': 'Terra Santa'}, {'Código': 'BTOW3', 'Nome': 'BTOW3'}, {'Código': 'LINX3', 'Nome': 'Linx'}, {'Código': 'BTTL3', 'Nome': 'Embpar'}, {'Código': 'GPCP3', 'Nome': 'GPCP3'}, {'Código': 'GPCP4', 'Nome': 'GPCP4'}, {'Código': 'SMLS3', 'Nome': 'Smiles'}, {'Código': 'MMXM3', 'Nome': 'MMX Mineração'}, {'Código': 'BSEV3', 'Nome': 'Biosev'}, {'Código': 'CNTO3', 'Nome': 'CNTO3'}, {'Código': 'TIET4', 'Nome': 'AES Tietê Energia'}, {'Código': 'TIET3', 'Nome': 'AES Tietê Energia'}, {'Código': 'CORR4', 'Nome': 'Corrêa Ribeiro'}, {'Código': 'CEPE3', 'Nome': 'CELPE'}, {'Código': 'CALI4', 'Nome': 'Adolpho Lindenberg'}, {'Código': 'SNSY6', 'Nome': 'Sansuy'}, {'Código': 'CASN4', 'Nome': 'CASAN'}, {'Código': 'EMAE3', 'Nome': 'EMAE'}, {'Código': 'BPAR3', 'Nome': 'Banpará'}, {'Código': 'APTI4', 'Nome': 'Aliperti'}, {'Código': 'VSPT3', 'Nome': 'FCA'}, {'Código': 'MTIG3', 'Nome': 'Metalgráfica Iguaçu'}, {'Código': 'FIGE4', 'Nome': 'Investimentos Bemge'}, {'Código': 'LUXM3', 'Nome': 'Trevisa'}, {'Código': 'TKNO3', 'Nome': 'Tekno'}, {'Código': 'COCE6', 'Nome': 'Coelce'}, {'Código': 'MGEL3', 'Nome': 'Mangels'}, {'Código': 'CTSA8', 'Nome': 'Santanense'}, {'Código': 'MMAQ4', 'Nome': 'Minasmáquinas'}]

# Transforma a lista de dicionários em um DataFrame
df = pd.DataFrame(dados)

# Adiciona uma barra lateral para filtrar os dados
filtro_codigo = st.sidebar.text_input("Filtrar a tabela por Ticker:", "")
filtro_nome = st.sidebar.text_input("Filtrar a tabela por Empresa:", "")

# Aplica os filtros
df_filtrado = df[df["Código"].str.contains(filtro_codigo) & df["Nome"].str.contains(filtro_nome, case=False)]

# Exibe o DataFrame filtrado no Streamlit

st.write("Não sabe o ticker da companhia que está analisando? Basta filtrar a tabela.")
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
periodo_interesse = st.sidebar.text_input("Insira o período desejado para o histórico de preços (ex: 3mo):")

if st.sidebar.button("Analisar"):
    # Criar instância do AnalisadorDadosMercado
    analisador = AnalisadorDadosMercado()

    # Obter dados
    precos, noticias = analisador.baixar_dados(ticker_interesse, periodo_interesse)

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

    # Exibir probabilidade na barra lateral
    st.sidebar.markdown(f"\nProbabilidade de Retorno ser maior ou igual a {analisador.retorno_esperado*100}%: {prob_retorno*100:.2f}%, segundo o Movimento Browniano Geométrico.")

    # Exibir títulos e links das notícias
    st.markdown(f"\nÚltimas Notícias para {ticker_interesse}")
    if noticias:
        # Criar lista para exibir títulos e links
        for noticia in noticias:
            link_parts = noticia['link'].split('/~/+/')
            link = link_parts[1] if len(link_parts) > 1 else noticia['link']  # Se o padrão não estiver presente, use o link original
            st.markdown(f"- [{noticia['title']}]({link})", unsafe_allow_html=True)
