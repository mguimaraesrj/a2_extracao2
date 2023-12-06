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

dados = [{'Ticker': 'MGLU3', 'Empresa': 'Magazine Luiza'}, {'Ticker': 'HAPV3', 'Empresa': 'Hapvida'}, {'Ticker': 'CIEL3', 'Empresa': 'Cielo'}, {'Ticker': 'BBDC4', 'Empresa': 'Banco Bradesco'}, {'Ticker': 'PETR4', 'Empresa': 'Petrobras'}, {'Ticker': 'ITUB4', 'Empresa': 'Itaú Unibanco'}, {'Ticker': 'ABEV3', 'Empresa': 'Ambev'}, {'Ticker': 'LREN3', 'Empresa': 'Lojas Renner'}, {'Ticker': 'COGN3', 'Empresa': 'Cogna'}, {'Ticker': 'B3SA3', 'Empresa': 'B3'}, {'Ticker': 'CVCB3', 'Empresa': 'CVC'}, {'Ticker': 'ITSA4', 'Empresa': 'Itaúsa'}, {'Ticker': 'VALE3', 'Empresa': 'Vale'}, {'Ticker': 'SOMA3', 'Empresa': 'Grupo Soma'}, {'Ticker': 'USIM5', 'Empresa': 'Usiminas'}, {'Ticker': 'ASAI3', 'Empresa': 'Assaí'}, {'Ticker': 'BRKM5', 'Empresa': 'Braskem'}, {'Ticker': 'RAIZ4', 'Empresa': 'Raízen'}, {'Ticker': 'MRVE3', 'Empresa': 'MRV'}, {'Ticker': 'SUZB3', 'Empresa': 'Suzano'}, {'Ticker': 'CPLE6', 'Empresa': 'Copel'}, {'Ticker': 'VBBR3', 'Empresa': 'Vibra Energia'}, {'Ticker': 'ANIM3', 'Empresa': 'Ânima Educação'}, {'Ticker': 'ENEV3', 'Empresa': 'Eneva'}, {'Ticker': 'EMBR3', 'Empresa': 'Embraer'}, {'Ticker': 'RAIL3', 'Empresa': 'Rumo'}, {'Ticker': 'MRFG3', 'Empresa': 'Marfrig'}, {'Ticker': 'CMIG4', 'Empresa': 'CEMIG'}, {'Ticker': 'BEEF3', 'Empresa': 'Minerva'}, {'Ticker': 'PRIO3', 'Empresa': 'PetroRio'}, {'Ticker': 'POMO4', 'Empresa': 'Marcopolo'}, {'Ticker': 'BBSE3', 'Empresa': 'BB Seguridade'}, {'Ticker': 'AMER3', 'Empresa': 'Americanas'}, {'Ticker': 'GGBR4', 'Empresa': 'Gerdau'}, {'Ticker': 'KLBN4', 'Empresa': 'Klabin'}, {'Ticker': 'RENT3', 'Empresa': 'Localiza'}, {'Ticker': 'CSNA3', 'Empresa': 'Siderúrgica Nacional'}, {'Ticker': 'AZUL4', 'Empresa': 'Azul'}, {'Ticker': 'GOAU4', 'Empresa': 'Metalúrgica Gerdau'}, {'Ticker': 'RDOR3', 'Empresa': "Rede D'Or"}, {'Ticker': 'BBAS3', 'Empresa': 'Banco do Brasil'}, {'Ticker': 'HBSA3', 'Empresa': 'Hidrovias do Brasil'}, {'Ticker': 'PETZ3', 'Empresa': 'Petz'}, {'Ticker': 'NTCO3', 'Empresa': 'Natura'}, {'Ticker': 'QUAL3', 'Empresa': 'Qualicorp'}, {'Ticker': 'CMIN3', 'Empresa': 'CSN Mineração'}, {'Ticker': 'GMAT3', 'Empresa': 'Grupo Mateus'}, {'Ticker': 'CCRO3', 'Empresa': 'Grupo CCR'}, {'Ticker': 'CYRE3', 'Empresa': 'Cyrela'}, {'Ticker': 'BRFS3', 'Empresa': 'BRF'}, {'Ticker': 'EQTL3', 'Empresa': 'Equatorial Energia'}, {'Ticker': 'AERI3', 'Empresa': 'Aeris Energy'}, {'Ticker': 'PETR3', 'Empresa': 'Petrobras'}, {'Ticker': 'CEAB3', 'Empresa': 'C&A'}, {'Ticker': 'JBSS3', 'Empresa': 'JBS'}, {'Ticker': 'AURE3', 'Empresa': 'VTRM ENERGIA PARTICIPAÃiES S.A.'}, {'Ticker': 'RRRP3', 'Empresa': '3R Petroleum'}, {'Ticker': 'TIMS3', 'Empresa': 'TIM'}, {'Ticker': 'ELET3', 'Empresa': 'Eletrobras'}, {'Ticker': 'BBDC3', 'Empresa': 'Banco Bradesco'}, {'Ticker': 'CRFB3', 'Empresa': 'Carrefour Brasil'}, {'Ticker': 'PCAR3', 'Empresa': 'Grupo Pão de Açúcar'}, {'Ticker': 'ALPA4', 'Empresa': 'Alpargatas'}, {'Ticker': 'CSMG3', 'Empresa': 'COPASA'}, {'Ticker': 'LWSA3', 'Empresa': 'Locaweb'}, {'Ticker': 'MULT3', 'Empresa': 'Multiplan'}, {'Ticker': 'JHSF3', 'Empresa': 'JHSF'}, {'Ticker': 'RADL3', 'Empresa': 'RaiaDrogasil'}, {'Ticker': 'IFCM3', 'Empresa': 'Infracommerce'}, {'Ticker': 'WEGE3', 'Empresa': 'WEG'}, {'Ticker': 'GOLL4', 'Empresa': 'GOL'}, {'Ticker': 'RECV3', 'Empresa': 'PetroRecôncavo'}, {'Ticker': 'SEQL3', 'Empresa': 'Sequoia Logística'}, {'Ticker': 'MLAS3', 'Empresa': 'Multilaser'}, {'Ticker': 'MOVI3', 'Empresa': 'Movida'}, {'Ticker': 'CSAN3', 'Empresa': 'Cosan'}, {'Ticker': 'VAMO3', 'Empresa': 'Grupo Vamos'}, {'Ticker': 'TEND3', 'Empresa': 'Construtora Tenda'}, {'Ticker': 'SMFT3', 'Empresa': 'Smart Fit'}, {'Ticker': 'ECOR3', 'Empresa': 'EcoRodovias'}, {'Ticker': 'TOTS3', 'Empresa': 'Totvs'}, {'Ticker': 'CBAV3', 'Empresa': 'CBA'}, {'Ticker': 'UGPA3', 'Empresa': 'Ultrapar'}, {'Ticker': 'GFSA3', 'Empresa': 'Gafisa'}, {'Ticker': 'IRBR3', 'Empresa': 'IRB Brasil RE'}, {'Ticker': 'FLRY3', 'Empresa': 'Fleury'}, {'Ticker': 'CXSE3', 'Empresa': 'Caixa Seguridade'}, {'Ticker': 'ONCO3', 'Empresa': 'Oncoclínicas'}, {'Ticker': 'BRAP4', 'Empresa': 'Bradespar'}, {'Ticker': 'SBFG3', 'Empresa': 'Grupo SBF'}, {'Ticker': 'OIBR3', 'Empresa': 'Oi'}, {'Ticker': 'RAPT4', 'Empresa': 'Randon'}, {'Ticker': 'SIMH3', 'Empresa': 'Simpar'}, {'Ticker': 'CPFE3', 'Empresa': 'CPFL Energia'}, {'Ticker': 'YDUQ3', 'Empresa': 'YDUQS'}, {'Ticker': 'CURY3', 'Empresa': 'Cury'}, {'Ticker': 'TRPL4', 'Empresa': 'Transmissão Paulista'}, {'Ticker': 'CPLE3', 'Empresa': 'Copel'}, {'Ticker': 'KEPL3', 'Empresa': 'Kepler Weber'}, {'Ticker': 'LJQQ3', 'Empresa': 'Lojas Quero-Quero'}, {'Ticker': 'SBSP3', 'Empresa': 'Sabesp'}, {'Ticker': 'DXCO3', 'Empresa': 'Dexco'}, {'Ticker': 'ESPA3', 'Empresa': 'Espaçolaser'}, {'Ticker': 'EZTC3', 'Empresa': 'EZTEC'}, {'Ticker': 'SAPR4', 'Empresa': 'Sanepar'}, {'Ticker': 'DIRR3', 'Empresa': 'Direcional'}, {'Ticker': 'BRSR6', 'Empresa': 'Banrisul'}, {'Ticker': 'KLBN3', 'Empresa': 'Klabin'}, {'Ticker': 'AZEV4', 'Empresa': 'Azevedo & Travassos'}, {'Ticker': 'STBP3', 'Empresa': 'Santos Brasil'}, {'Ticker': 'GUAR3', 'Empresa': 'Guararapes'}, {'Ticker': 'ARZZ3', 'Empresa': 'Arezzo'}, {'Ticker': 'SGPS3', 'Empresa': 'Springs'}, {'Ticker': 'MEGA3', 'Empresa': 'OMEGA ENERGIA S.A.'}, {'Ticker': 'SLCE3', 'Empresa': 'SLC Agrícola'}, {'Ticker': 'HYPE3', 'Empresa': 'Hypera'}, {'Ticker': 'EGIE3', 'Empresa': 'Engie'}, {'Ticker': 'NEOE3', 'Empresa': 'Neoenergia'}, {'Ticker': 'GGPS3', 'Empresa': 'GPS'}, {'Ticker': 'VIVA3', 'Empresa': 'Vivara'}, {'Ticker': 'TTEN3', 'Empresa': '3tentos'}, {'Ticker': 'RANI3', 'Empresa': 'Irani'}, {'Ticker': 'PSSA3', 'Empresa': 'Porto Seguro'}, {'Ticker': 'INTB3', 'Empresa': 'Intelbras'}, {'Ticker': 'VIVT3', 'Empresa': 'Vivo'}, {'Ticker': 'AMAR3', 'Empresa': 'Lojas Marisa'}, {'Ticker': 'PDGR3', 'Empresa': 'PDG Realty'}, {'Ticker': 'SMTO3', 'Empresa': 'São Martinho'}, {'Ticker': 'ENAT3', 'Empresa': 'Enauta'}, {'Ticker': 'AMBP3', 'Empresa': 'Ambipar'}, {'Ticker': 'MEAL3', 'Empresa': 'IMC Alimentação'}, {'Ticker': 'CLSA3', 'Empresa': 'ClearSale'}, {'Ticker': 'GRND3', 'Empresa': 'Grendene'}, {'Ticker': 'POSI3', 'Empresa': 'Positivo'}, {'Ticker': 'AESB3', 'Empresa': 'AES Brasil'}, {'Ticker': 'CASH3', 'Empresa': 'Méliuz'}, {'Ticker': 'MDIA3', 'Empresa': 'M. Dias Branco'}, {'Ticker': 'DESK3', 'Empresa': 'Desktop'}, {'Ticker': 'MTRE3', 'Empresa': 'Mitre Realty'}, {'Ticker': 'VVEO3', 'Empresa': 'Viveo'}, {'Ticker': 'MBLY3', 'Empresa': 'Mobly'}, {'Ticker': 'RCSL4', 'Empresa': 'Recrusul'}, {'Ticker': 'PLPL3', 'Empresa': 'Plano&Plano'}, {'Ticker': 'PGMN3', 'Empresa': 'Pague Menos'}, {'Ticker': 'WIZC3', 'Empresa': 'Wiz Soluções'}, {'Ticker': 'SHUL4', 'Empresa': 'Schulz'}, {'Ticker': 'BPAN4', 'Empresa': 'Banco Pan'}, {'Ticker': 'SEER3', 'Empresa': 'Ser Educacional'}, {'Ticker': 'CAML3', 'Empresa': 'Camil Alimentos'}, {'Ticker': 'ARML3', 'Empresa': 'Armac'}, {'Ticker': 'ODPV3', 'Empresa': 'Odontoprev'}, {'Ticker': 'MATD3', 'Empresa': 'Mater Dei'}, {'Ticker': 'LEVE3', 'Empresa': 'Mahle Metal Leve'}, {'Ticker': 'ZAMP3', 'Empresa': 'Zamp'}, {'Ticker': 'CSED3', 'Empresa': 'Cruzeiro do Sul Educacional'}, {'Ticker': 'TRAD3', 'Empresa': 'Traders Club'}, {'Ticker': 'AGRO3', 'Empresa': 'BrasilAgro'}, {'Ticker': 'LIGT3', 'Empresa': 'Light'}, {'Ticker': 'ELET6', 'Empresa': 'Eletrobras'}, {'Ticker': 'VULC3', 'Empresa': 'Vulcabras'}, {'Ticker': 'DASA3', 'Empresa': 'Dasa'}, {'Ticker': 'MYPK3', 'Empresa': 'Iochpe-Maxion'}, {'Ticker': 'TRIS3', 'Empresa': 'Trisul'}, {'Ticker': 'OPCT3', 'Empresa': 'OceanPact'}, {'Ticker': 'AZEV3', 'Empresa': 'Azevedo & Travassos'}, {'Ticker': 'ABCB4', 'Empresa': 'Banco ABC Brasil'}, {'Ticker': 'ORVR3', 'Empresa': 'Orizon'}, {'Ticker': 'RCSL3', 'Empresa': 'Recrusul'}, {'Ticker': 'PFRM3', 'Empresa': 'Profarma'}, {'Ticker': 'CMIG3', 'Empresa': 'CEMIG'}, {'Ticker': 'LAVV3', 'Empresa': 'Lavvi Incorporadora'}, {'Ticker': 'JALL3', 'Empresa': 'Jalles Machado'}, {'Ticker': 'MDNE3', 'Empresa': 'Moura Dubeux'}, {'Ticker': 'LOGG3', 'Empresa': 'LOG CP'}, {'Ticker': 'BMGB4', 'Empresa': 'Banco BMG'}, {'Ticker': 'PNVL3', 'Empresa': 'Dimed'}, {'Ticker': 'PTBL3', 'Empresa': 'Portobello'}, {'Ticker': 'MILS3', 'Empresa': 'Mills'}, {'Ticker': 'FIQE3', 'Empresa': 'Unifique'}, {'Ticker': 'LUPA3', 'Empresa': 'Lupatech'}, {'Ticker': 'BRIT3', 'Empresa': 'Brisanet'}, {'Ticker': 'BLAU3', 'Empresa': 'Blau Farmacêutica'}, {'Ticker': 'PRNR3', 'Empresa': 'Priner'}, {'Ticker': 'EVEN3', 'Empresa': 'Even'}, {'Ticker': 'CTNM4', 'Empresa': 'Coteminas'}, {'Ticker': 'VLID3', 'Empresa': 'Valid'}, {'Ticker': 'TASA4', 'Empresa': 'Taurus'}, {'Ticker': 'HBOR3', 'Empresa': 'Helbor'}, {'Ticker': 'FRAS3', 'Empresa': 'Fras-le'}, {'Ticker': 'SHOW3', 'Empresa': 'Time For Fun'}, {'Ticker': 'HBRE3', 'Empresa': 'HBR Realty'}, {'Ticker': 'ENJU3', 'Empresa': 'Enjoei'}, {'Ticker': 'NGRD3', 'Empresa': 'Neogrid'}, {'Ticker': 'FESA4', 'Empresa': 'Ferbasa'}, {'Ticker': 'ITUB3', 'Empresa': 'Itaú Unibanco'}, {'Ticker': 'PINE4', 'Empresa': 'PINE'}, {'Ticker': 'VIVR3', 'Empresa': 'Viver'}, {'Ticker': 'CTSA4', 'Empresa': 'Santanense'}, {'Ticker': 'JSLG3', 'Empresa': 'JSL'}, {'Ticker': 'CTSA3', 'Empresa': 'Santanense'}, {'Ticker': 'RNEW4', 'Empresa': 'Renova Energia'}, {'Ticker': 'SAPR3', 'Empresa': 'Sanepar'}, {'Ticker': 'VITT3', 'Empresa': 'Vittia'}, {'Ticker': 'TUPY3', 'Empresa': 'Tupy'}, {'Ticker': 'USIM3', 'Empresa': 'Usiminas'}, {'Ticker': 'ROMI3', 'Empresa': 'Indústrias ROMI'}, {'Ticker': 'KRSA3', 'Empresa': 'Kora Saúde'}, {'Ticker': 'ALPK3', 'Empresa': 'Estapar'}, {'Ticker': 'SYNE3', 'Empresa': 'SYN'}, {'Ticker': 'WEST3', 'Empresa': 'Westwing'}, {'Ticker': 'PDTC3', 'Empresa': 'Padtec'}, {'Ticker': 'BMOB3', 'Empresa': 'Bemobi'}, {'Ticker': 'TGMA3', 'Empresa': 'Tegma'}, {'Ticker': 'BRKM3', 'Empresa': 'Braskem'}, {'Ticker': 'UNIP6', 'Empresa': 'Unipar'}, {'Ticker': 'PORT3', 'Empresa': 'Wilson Sons'}, {'Ticker': 'AALR3', 'Empresa': 'Alliança'}, {'Ticker': 'TECN3', 'Empresa': 'Technos'}, {'Ticker': 'TAEE4', 'Empresa': 'Taesa'}, {'Ticker': 'ETER3', 'Empresa': 'Eternit'}, {'Ticker': 'UCAS3', 'Empresa': 'Unicasa'}, {'Ticker': 'TFCO4', 'Empresa': 'Track & Field'}, {'Ticker': 'LPSB3', 'Empresa': 'Lopes'}, {'Ticker': 'ITSA3', 'Empresa': 'Itaúsa'}, {'Ticker': 'MTSA4', 'Empresa': 'METISA'}, {'Ticker': 'SOJA3', 'Empresa': 'Boa Safra Sementes'}, {'Ticker': 'BRAP3', 'Empresa': 'Bradespar'}, {'Ticker': 'POMO3', 'Empresa': 'Marcopolo'}, {'Ticker': 'TCSA3', 'Empresa': 'Tecnisa'}, {'Ticker': 'NINJ3', 'Empresa': 'GetNinjas'}, {'Ticker': 'IGTI3', 'Empresa': 'Jereissati Participações'}, {'Ticker': 'IGTI3', 'Empresa': 'Iguatemi'}, {'Ticker': 'DEXP3', 'Empresa': 'Dexxos'}, {'Ticker': 'SANB4', 'Empresa': 'Banco Santander'}, {'Ticker': 'MELK3', 'Empresa': 'Melnick'}, {'Ticker': 'LAND3', 'Empresa': 'Terra Santa'}, {'Ticker': 'ALLD3', 'Empresa': 'Allied'}, {'Ticker': 'SANB3', 'Empresa': 'Banco Santander'}, {'Ticker': 'TAEE3', 'Empresa': 'Taesa'}, {'Ticker': 'CAMB3', 'Empresa': 'Cambuci'}, {'Ticker': 'RSID3', 'Empresa': 'Rossi Residencial'}, {'Ticker': 'RNEW3', 'Empresa': 'Renova Energia'}, {'Ticker': 'DMVF3', 'Empresa': 'D1000 Varejo Farma'}, {'Ticker': 'CSUD3', 'Empresa': 'CSU Cardsystem'}, {'Ticker': 'ELMD3', 'Empresa': 'Eletromidia'}, {'Ticker': 'DOTZ3', 'Empresa': 'Dotz'}, {'Ticker': 'GGBR3', 'Empresa': 'Gerdau'}, {'Ticker': 'GOAU3', 'Empresa': 'Metalúrgica Gerdau'}, {'Ticker': 'LOGN3', 'Empresa': 'Log-In'}, {'Ticker': 'APER3', 'Empresa': 'Alper'}, {'Ticker': 'TPIS3', 'Empresa': 'Triunfo'}, {'Ticker': 'AGXY3', 'Empresa': 'AgroGalaxy'}, {'Ticker': 'PMAM3', 'Empresa': 'Paranapanema'}, {'Ticker': 'EUCA4', 'Empresa': 'Eucatex'}, {'Ticker': 'BPAC5', 'Empresa': 'Banco BTG Pactual'}, {'Ticker': 'SCAR3', 'Empresa': 'São Carlos'}, {'Ticker': 'OIBR4', 'Empresa': 'Oi'}, {'Ticker': 'BOBR4', 'Empresa': 'Bombril'}, {'Ticker': 'JFEN3', 'Empresa': 'João Fortes'}, {'Ticker': 'INEP4', 'Empresa': 'Inepar'}, {'Ticker': 'TASA3', 'Empresa': 'Taurus'}, {'Ticker': 'ALUP4', 'Empresa': 'Alupar'}, {'Ticker': 'INEP3', 'Empresa': 'Inepar'}, {'Ticker': 'ATMP3', 'Empresa': 'Atma'}, {'Ticker': 'BMEB4', 'Empresa': 'Banco Mercantil do Brasil'}, {'Ticker': 'RPMG3', 'Empresa': 'Refinaria de Manguinhos'}, {'Ticker': 'ALUP3', 'Empresa': 'Alupar'}, {'Ticker': 'CEBR6', 'Empresa': 'CEB'}, {'Ticker': 'ATOM3', 'Empresa': 'ATOM'}, {'Ticker': 'LVTC3', 'Empresa': 'WDC Networks'}, {'Ticker': 'SNSY5', 'Empresa': 'Sansuy'}, {'Ticker': 'EPAR3', 'Empresa': 'EPAR3'}, {'Ticker': 'RAPT3', 'Empresa': 'Randon'}, {'Ticker': 'PTNT4', 'Empresa': 'Pettenati'}, {'Ticker': 'COCE5', 'Empresa': 'Coelce'}, {'Ticker': 'UNIP3', 'Empresa': 'Unipar'}, {'Ticker': 'BEES3', 'Empresa': 'Banestes'}, {'Ticker': 'NUTR3', 'Empresa': 'Nutriplant'}, {'Ticker': 'TELB4', 'Empresa': 'Telebras'}, {'Ticker': 'CEBR3', 'Empresa': 'CEB'}, {'Ticker': 'CGRA4', 'Empresa': 'Grazziotin'}, {'Ticker': 'MNPR3', 'Empresa': 'Minupar'}, {'Ticker': 'ENGI4', 'Empresa': 'Energisa'}, {'Ticker': 'BIOM3', 'Empresa': 'Biomm'}, {'Ticker': 'VSTE3', 'Empresa': 'LE LIS BLANC'}, {'Ticker': 'BPAC3', 'Empresa': 'Banco BTG Pactual'}, {'Ticker': 'BRSR3', 'Empresa': 'Banrisul'}, {'Ticker': 'REDE3', 'Empresa': 'Rede Energia'}, {'Ticker': 'DEXP4', 'Empresa': 'Dexxos'}, {'Ticker': 'FHER3', 'Empresa': 'Fertilizantes Heringer'}, {'Ticker': 'CGRA3', 'Empresa': 'Grazziotin'}, {'Ticker': 'ENGI3', 'Empresa': 'Energisa'}, {'Ticker': 'BEES4', 'Empresa': 'Banestes'}, {'Ticker': 'BRIV4', 'Empresa': 'Alfa Investimento'}, {'Ticker': 'ESTR4', 'Empresa': 'Estrela'}, {'Ticker': 'WHRL3', 'Empresa': 'Whirlpool'}, {'Ticker': 'HAGA3', 'Empresa': 'Haga'}, {'Ticker': 'BAHI3', 'Empresa': 'Bahema'}, {'Ticker': 'MWET4', 'Empresa': 'Wetzel'}, {'Ticker': 'EMAE4', 'Empresa': 'EMAE'}, {'Ticker': 'ALPA3', 'Empresa': 'Alpargatas'}, {'Ticker': 'OSXB3', 'Empresa': 'OSX Brasil'}, {'Ticker': 'EALT4', 'Empresa': 'Electro Aço Altona'}, {'Ticker': 'CRIV3', 'Empresa': 'Alfa Financeira'}, {'Ticker': 'CRIV4', 'Empresa': 'Alfa Financeira'}, {'Ticker': 'EUCA3', 'Empresa': 'Eucatex'}, {'Ticker': 'HOOT4', 'Empresa': 'Hotéis Othon'}, {'Ticker': 'CRPG6', 'Empresa': 'Tronox Pigmentos'}, {'Ticker': 'OFSA3', 'Empresa': 'Ourofino Saúde Animal'}, {'Ticker': 'RDNI3', 'Empresa': 'RNI'}, {'Ticker': 'RSUL4', 'Empresa': 'Metalúrgica Riosulense'}, {'Ticker': 'EQPA3', 'Empresa': 'Equatorial Energia Pará'}, {'Ticker': 'BGIP4', 'Empresa': 'Banese'}, {'Ticker': 'CEBR5', 'Empresa': 'CEB'}, {'Ticker': 'FRTA3', 'Empresa': 'Pomi Frutas'}, {'Ticker': 'TRPL3', 'Empresa': 'Transmissão Paulista'}, {'Ticker': 'CTKA4', 'Empresa': 'Karsten'}, {'Ticker': 'HETA4', 'Empresa': 'Hercules'}, {'Ticker': 'CLSC4', 'Empresa': 'Celesc'}, {'Ticker': 'CEEB3', 'Empresa': 'COELBA'}, {'Ticker': 'CRPG5', 'Empresa': 'Tronox Pigmentos'}, {'Ticker': 'BRKM6', 'Empresa': 'Braskem'}, {'Ticker': 'NEXP3', 'Empresa': 'Brasil Brokers'}, {'Ticker': 'HAGA4', 'Empresa': 'Haga'}, {'Ticker': 'FRIO3', 'Empresa': 'Metalfrio'}, {'Ticker': 'WHRL4', 'Empresa': 'Whirlpool'}, {'Ticker': 'MGEL4', 'Empresa': 'Mangels'}, {'Ticker': 'EQPA5', 'Empresa': 'Equatorial Energia Pará'}, {'Ticker': 'AVLL3', 'Empresa': 'Alphaville'}, {'Ticker': 'WLMM3', 'Empresa': 'WLM'}, {'Ticker': 'BAZA3', 'Empresa': 'Banco da Amazônia'}, {'Ticker': 'TEKA4', 'Empresa': 'Teka'}, {'Ticker': 'BDLL4', 'Empresa': 'Bardella'}, {'Ticker': 'EKTR4', 'Empresa': 'Elektro'}, {'Ticker': 'GEPA4', 'Empresa': 'Rio Paranapanema Energia'}, {'Ticker': 'CPLE5', 'Empresa': 'Copel'}, {'Ticker': 'CTNM3', 'Empresa': 'Coteminas'}, {'Ticker': 'AFLT3', 'Empresa': 'Afluente T'}, {'Ticker': 'TELB3', 'Empresa': 'Telebras'}, {'Ticker': 'MNDL3', 'Empresa': 'Mundial'}, {'Ticker': 'CSRN3', 'Empresa': 'COSERN'}, {'Ticker': 'CEDO4', 'Empresa': 'Cedro Têxtil'}, {'Ticker': 'BMEB3', 'Empresa': 'Banco Mercantil do Brasil'}, {'Ticker': 'BMIN4', 'Empresa': 'Banco Mercantil de Investimentos'}, {'Ticker': 'IGTI4', 'Empresa': 'Jereissati Participações'}, {'Ticker': 'IGTI4', 'Empresa': 'Iguatemi'}, {'Ticker': 'PLAS3', 'Empresa': 'Plascar'}, {'Ticker': 'CGAS5', 'Empresa': 'Comgás'}, {'Ticker': 'EQPA7', 'Empresa': 'Equatorial Energia Pará'}, {'Ticker': 'ENMT3', 'Empresa': 'Energisa MT'}, {'Ticker': 'BALM4', 'Empresa': 'Baumer'}, {'Ticker': 'BAUH4', 'Empresa': 'Excelsior'}, {'Ticker': 'HBTS5', 'Empresa': 'Habitasul'}, {'Ticker': 'WLMM4', 'Empresa': 'WLM'}, {'Ticker': 'PTNT3', 'Empresa': 'Pettenati'}, {'Ticker': 'BNBR3', 'Empresa': 'Banco do Nordeste'}, {'Ticker': 'BGIP3', 'Empresa': 'Banese'}, {'Ticker': 'JOPA3', 'Empresa': 'Josapar'}, {'Ticker': 'CALI3', 'Empresa': 'Adolpho Lindenberg'}, {'Ticker': 'DOHL4', 'Empresa': 'Döhler'}, {'Ticker': 'DTCY3', 'Empresa': 'Dtcom'}, {'Ticker': 'NORD3', 'Empresa': 'Nordon'}, {'Ticker': 'BMKS3', 'Empresa': 'Monark'}, {'Ticker': 'BSLI4', 'Empresa': 'Banco de Brasília'}, {'Ticker': 'FESA3', 'Empresa': 'Ferbasa'}, {'Ticker': 'LUXM4', 'Empresa': 'Trevisa'}, {'Ticker': 'BALM3', 'Empresa': 'Baumer'}, {'Ticker': 'BMIN3', 'Empresa': 'Banco Mercantil de Investimentos'}, {'Ticker': 'PATI3', 'Empresa': 'Panatlântica'}, {'Ticker': 'BRIV3', 'Empresa': 'Alfa Investimento'}, {'Ticker': 'CSAB3', 'Empresa': 'Cia. de Seg. Aliança da Bahia'}, {'Ticker': 'EQMA3B', 'Empresa': 'Equatorial Maranhão'}, {'Ticker': 'CSAB4', 'Empresa': 'Cia. de Seg. Aliança da Bahia'}, {'Ticker': 'CEDO3', 'Empresa': 'Cedro Têxtil'}, {'Ticker': 'BRSR5', 'Empresa': 'Banrisul'}, {'Ticker': 'MERC4', 'Empresa': 'Mercantil do Brasil Financeira'}, {'Ticker': 'DMFN3', 'Empresa': 'DMFN3'}, {'Ticker': 'CEED3', 'Empresa': 'CEEE D'}, {'Ticker': 'BSLI3', 'Empresa': 'Banco de Brasília'}, {'Ticker': 'CGAS3', 'Empresa': 'Comgás'}, {'Ticker': 'UNIP5', 'Empresa': 'Unipar'}, {'Ticker': 'FIEI3', 'Empresa': 'FIEI3'}, {'Ticker': 'RPAD3', 'Empresa': 'Alfa Holdings'}, {'Ticker': 'EALT3', 'Empresa': 'Electro Aço Altona'}, {'Ticker': 'ENMT4', 'Empresa': 'Energisa MT'}, {'Ticker': 'CEED4', 'Empresa': 'CEEE D'}, {'Ticker': 'DOHL3', 'Empresa': 'Döhler'}, {'Ticker': 'CEEB5', 'Empresa': 'COELBA'}, {'Ticker': 'PEAB3', 'Empresa': 'Participações Aliança da Bahia'}, {'Ticker': 'MRSA3B', 'Empresa': 'MRS Logística'}, {'Ticker': 'BRGE12', 'Empresa': 'Consórcio Alfa'}, {'Ticker': 'CLSC3', 'Empresa': 'Celesc'}, {'Ticker': 'RPAD6', 'Empresa': 'Alfa Holdings'}, {'Ticker': 'BRGE6', 'Empresa': 'Consórcio Alfa'}, {'Ticker': 'CRPG3', 'Empresa': 'Tronox Pigmentos'}, {'Ticker': 'SNSY3', 'Empresa': 'Sansuy'}, {'Ticker': 'MRSA5B', 'Empresa': 'MRS Logística'}, {'Ticker': 'MAPT4', 'Empresa': 'Cemepe'}, {'Ticker': 'CTKA3', 'Empresa': 'Karsten'}, {'Ticker': 'CSRN5', 'Empresa': 'COSERN'}, {'Ticker': 'GEPA3', 'Empresa': 'Rio Paranapanema Energia'}, {'Ticker': 'GSHP3', 'Empresa': 'General Shopping & Outlets'}, {'Ticker': 'RPAD5', 'Empresa': 'Alfa Holdings'}, {'Ticker': 'AHEB3', 'Empresa': 'São Paulo Turismo'}, {'Ticker': 'BRGE3', 'Empresa': 'Consórcio Alfa'}, {'Ticker': 'MOAR3', 'Empresa': 'Monteiro Aranha'}, {'Ticker': 'BRGE5', 'Empresa': 'Consórcio Alfa'}, {'Ticker': 'CSRN6', 'Empresa': 'COSERN'}, {'Ticker': 'TKNO4', 'Empresa': 'Tekno'}, {'Ticker': 'BDLL3', 'Empresa': 'Bardella'}, {'Ticker': 'ELET5', 'Empresa': 'Eletrobras'}, {'Ticker': 'SOND6', 'Empresa': 'Sondotécnica'}, {'Ticker': 'CBEE3', 'Empresa': 'Ampla Energia'}, {'Ticker': 'SOND5', 'Empresa': 'Sondotécnica'}, {'Ticker': 'GPAR3', 'Empresa': 'CELGPAR'}, {'Ticker': 'SQIA3', 'Empresa': 'Sinqia'}, {'Ticker': 'ESTR3', 'Empresa': 'Estrela'}, {'Ticker': 'BRGE11', 'Empresa': 'Consórcio Alfa'}, {'Ticker': 'BRGE8', 'Empresa': 'Consórcio Alfa'}, {'Ticker': 'BRGE7', 'Empresa': 'Consórcio Alfa'}, {'Ticker': 'MRSA6B', 'Empresa': 'MRS Logística'}, {'Ticker': 'ALSO3', 'Empresa': 'Aliansce Sonae'}, {'Ticker': 'BRPR3', 'Empresa': 'BR Properties'}, {'Ticker': 'LIPR3', 'Empresa': 'Eletropar'}, {'Ticker': 'PATI4', 'Empresa': 'Panatlântica'}, {'Ticker': 'MTSA3', 'Empresa': 'METISA'}, {'Ticker': 'SLED4', 'Empresa': 'Saraiva'}, {'Ticker': 'SLED3', 'Empresa': 'Saraiva'}, {'Ticker': 'EQPA6', 'Empresa': 'Equatorial Energia Pará'}, {'Ticker': 'AHEB6', 'Empresa': 'São Paulo Turismo'}, {'Ticker': 'PINE3', 'Empresa': 'PINE'}, {'Ticker': 'VIIA3', 'Empresa': 'VIIA3'}, {'Ticker': 'EKTR3', 'Empresa': 'Elektro'}, {'Ticker': 'MWET3', 'Empresa': 'Wetzel'}, {'Ticker': 'USIM6', 'Empresa': 'Usiminas'}, {'Ticker': 'AHEB5', 'Empresa': 'São Paulo Turismo'}, {'Ticker': 'ENBR3', 'Empresa': 'EDP Brasil'}, {'Ticker': 'BOAS3', 'Empresa': 'Boa Vista'}, {'Ticker': 'PEAB4', 'Empresa': 'Participações Aliança da Bahia'}, {'Ticker': 'COCE3', 'Empresa': 'Coelce'}, {'Ticker': 'JOPA4', 'Empresa': 'Josapar'}, {'Ticker': 'MODL3', 'Empresa': 'Banco Modal'}, {'Ticker': 'MERC3', 'Empresa': 'Mercantil do Brasil Financeira'}, {'Ticker': 'CEGR3', 'Empresa': 'Naturgy (CEG)'}, {'Ticker': 'MAPT3', 'Empresa': 'Cemepe'}, {'Ticker': 'CRDE3', 'Empresa': 'CR2'}, {'Ticker': 'IGBR3', 'Empresa': 'IGB Eletrônica'}, {'Ticker': 'MSPA4', 'Empresa': 'Melhoramentos'}, {'Ticker': 'ODER4', 'Empresa': 'Conservas Oderich'}, {'Ticker': 'PARD3', 'Empresa': 'Hermes Pardini'}, {'Ticker': 'CASN3', 'Empresa': 'CASAN'}, {'Ticker': 'WIZS3', 'Empresa': 'WIZS3'}, {'Ticker': 'LLIS3', 'Empresa': 'LLIS3'}, {'Ticker': 'MSPA3', 'Empresa': 'Melhoramentos'}, {'Ticker': 'BRML3', 'Empresa': 'BRMalls'}, {'Ticker': 'DMMO3', 'Empresa': 'Dommo Energia'}, {'Ticker': 'GETT3', 'Empresa': 'Getnet'}, {'Ticker': 'GETT4', 'Empresa': 'Getnet'}, {'Ticker': 'SULA4', 'Empresa': 'SulAmérica'}, {'Ticker': 'SULA3', 'Empresa': 'SulAmérica'}, {'Ticker': 'CEPE5', 'Empresa': 'CELPE'}, {'Ticker': 'TCNO4', 'Empresa': 'Tecnosolo'}, {'Ticker': 'TCNO3', 'Empresa': 'Tecnosolo'}, {'Ticker': 'CEPE6', 'Empresa': 'CELPE'}, {'Ticker': 'BKBR3', 'Empresa': 'BKBR3'}, {'Ticker': 'MTIG4', 'Empresa': 'Metalgráfica Iguaçu'}, {'Ticker': 'BLUT4', 'Empresa': 'Blue Tech Solutions'}, {'Ticker': 'BLUT3', 'Empresa': 'Blue Tech Solutions'}, {'Ticker': 'MODL4', 'Empresa': 'Banco Modal'}, {'Ticker': 'CARD3', 'Empresa': 'CARD3'}, {'Ticker': 'SHUL3', 'Empresa': 'Schulz'}, {'Ticker': 'FIGE3', 'Empresa': 'Investimentos Bemge'}, {'Ticker': 'FNCN3', 'Empresa': 'Finansinos'}, {'Ticker': 'TEKA3', 'Empresa': 'Teka'}, {'Ticker': 'HETA3', 'Empresa': 'Hercules'}, {'Ticker': 'LCAM3', 'Empresa': 'Locamerica'}, {'Ticker': 'BIDI4', 'Empresa': 'Banco Inter'}, {'Ticker': 'BIDI3', 'Empresa': 'Banco Inter'}, {'Ticker': 'EEEL4', 'Empresa': 'CEEE GT'}, {'Ticker': 'EEEL3', 'Empresa': 'CEEE GT'}, {'Ticker': 'BBRK3', 'Empresa': 'BBRK3'}, {'Ticker': 'SOND3', 'Empresa': 'Sondotécnica'}, {'Ticker': 'CESP6', 'Empresa': 'CESP'}, {'Ticker': 'CESP3', 'Empresa': 'CESP'}, {'Ticker': 'CESP5', 'Empresa': 'CESP'}, {'Ticker': 'ECPR4', 'Empresa': 'Encorpar'}, {'Ticker': 'MOSI3', 'Empresa': 'Mosaico'}, {'Ticker': 'POWE3', 'Empresa': 'Focus Energia'}, {'Ticker': 'ECPR3', 'Empresa': 'Encorpar'}, {'Ticker': 'GNDI3', 'Empresa': 'NotreDame Intermédica'}, {'Ticker': 'LAME4', 'Empresa': 'Lojas Americanas'}, {'Ticker': 'LAME3', 'Empresa': 'Lojas Americanas'}, {'Ticker': 'OMGE3', 'Empresa': 'Omega Geração'}, {'Ticker': 'IGTA3', 'Empresa': 'IGTA3'}, {'Ticker': 'JPSA3', 'Empresa': 'JPSA3'}, {'Ticker': 'BRDT3', 'Empresa': 'BRDT3'}, {'Ticker': 'JBDU4', 'Empresa': 'JBDU4'}, {'Ticker': 'JBDU3', 'Empresa': 'JBDU3'}, {'Ticker': 'HGTX3', 'Empresa': 'Hering'}, {'Ticker': 'CCPR3', 'Empresa': 'CCPR3'}, {'Ticker': 'DTEX3', 'Empresa': 'DTEX3'}, {'Ticker': 'VVAR3', 'Empresa': 'VVAR3'}, {'Ticker': 'PNVL4', 'Empresa': 'Dimed'}, {'Ticker': 'TESA3', 'Empresa': 'Terra Santa'}, {'Ticker': 'BTOW3', 'Empresa': 'BTOW3'}, {'Ticker': 'LINX3', 'Empresa': 'Linx'}, {'Ticker': 'BTTL3', 'Empresa': 'Embpar'}, {'Ticker': 'GPCP3', 'Empresa': 'GPCP3'}, {'Ticker': 'GPCP4', 'Empresa': 'GPCP4'}, {'Ticker': 'SMLS3', 'Empresa': 'Smiles'}, {'Ticker': 'MMXM3', 'Empresa': 'MMX Mineração'}, {'Ticker': 'BSEV3', 'Empresa': 'Biosev'}, {'Ticker': 'CNTO3', 'Empresa': 'CNTO3'}, {'Ticker': 'TIET4', 'Empresa': 'AES Tietê Energia'}, {'Ticker': 'TIET3', 'Empresa': 'AES Tietê Energia'}, {'Ticker': 'CORR4', 'Empresa': 'Corrêa Ribeiro'}, {'Ticker': 'CEPE3', 'Empresa': 'CELPE'}, {'Ticker': 'CALI4', 'Empresa': 'Adolpho Lindenberg'}, {'Ticker': 'SNSY6', 'Empresa': 'Sansuy'}, {'Ticker': 'CASN4', 'Empresa': 'CASAN'}, {'Ticker': 'EMAE3', 'Empresa': 'EMAE'}, {'Ticker': 'BPAR3', 'Empresa': 'Banpará'}, {'Ticker': 'APTI4', 'Empresa': 'Aliperti'}, {'Ticker': 'VSPT3', 'Empresa': 'FCA'}, {'Ticker': 'MTIG3', 'Empresa': 'Metalgráfica Iguaçu'}, {'Ticker': 'FIGE4', 'Empresa': 'Investimentos Bemge'}, {'Ticker': 'LUXM3', 'Empresa': 'Trevisa'}, {'Ticker': 'TKNO3', 'Empresa': 'Tekno'}, {'Ticker': 'COCE6', 'Empresa': 'Coelce'}, {'Ticker': 'MGEL3', 'Empresa': 'Mangels'}, {'Ticker': 'CTSA8', 'Empresa': 'Santanense'}, {'Ticker': 'MMAQ4', 'Empresa': 'Minasmáquinas'}]
# Transforma a lista de dicionários em um DataFrame
df = pd.DataFrame(dados)

# Adiciona uma barra lateral para filtrar os dados
filtro_nome = st.sidebar.text_input("Filtrar a tabela por Empresa:", "")
filtro_codigo = st.sidebar.text_input("Filtrar a tabela por Ticker:", "")


# Aplica os filtros
df_filtrado = df[df["Ticker"].str.contains(filtro_codigo) & df["Empresa"].str.contains(filtro_nome, case=False)]

# Adiciona um botão de alternância para mostrar/ocultar a tabela de tickers
mostrar_tabela = st.sidebar.checkbox("Ver Tabela Tickers x Empresas", True)

# Exibe o DataFrame filtrado no Streamlit apenas se o botão estiver marcado
if mostrar_tabela:
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
ticker_interesse = st.sidebar.text_input("1) Insira o ticker de interesse (ex: MGLU3):").upper()

# Adiciona botões para escolher entre Dias, Meses e Anos
periodo_opcao = st.sidebar.radio("2) Escolha o período do histórico de preços:", ["Dias", "Meses", "Anos"])

# Adiciona um número input entre 1 e 30
if periodo_opcao == "Dias":
    numero_periodo = st.sidebar.number_input("3) Escolha o número de dias (1-30):", min_value=1, max_value=30)
    periodo_interesse = f"{numero_periodo}d"
elif periodo_opcao == "Meses":
    numero_periodo = st.sidebar.number_input("3. Escolha o número de meses (1-12):", min_value=1, max_value=12)
    periodo_interesse = f"{numero_periodo}mo"
else:
    numero_periodo = st.sidebar.number_input("3) Escolha o número de anos:", min_value=1, max_value=1000)
    periodo_interesse = f"{numero_periodo}y"

# Adiciona um novo input para a porcentagem desejada
porcentagem_desejada = st.sidebar.slider("4) Escolha a porcentagem desejada para o MBG:", min_value=0.01, max_value=1.0, value=0.05, step=0.01)

# Restante do código permanece igual
if st.sidebar.button("Analisar"):
    try:
        # Criar instância do AnalisadorDadosMercado com a porcentagem desejada
        analisador = AnalisadorDadosMercado(days_ahead=numero_periodo, return_expected=porcentagem_desejada)

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

            height = min(len(df_precos) * 25, 400)  # Define uma altura máxima de 400 pixels (ou ajuste conforme necessário)
    
            # Exibe a tabela limitando a altura
            st.dataframe(df_precos, height=height)

            st.write(f"**Probabilidade de Retorno ser maior ou igual a {porcentagem_desejada*100}% (MBG): {prob_retorno*100:.2f}%**")

            # Explanação do Movimento Browniano Geométrico
            st.markdown("""
            **Movimento Browniano Geométrico (MBG):**
            
            O MBG simula trajetórias futuras de preços de ações usando retornos log-normais,
            considerando média e volatilidade históricas. Ele é empregado para estimar a probabilidade
            de atingir um determinado retorno, proporcionando insights sobre o risco e a incerteza associados
            aos movimentos de preços no mercado financeiro. Portanto, o resultado obtido reflete a análise do Movimento Browniano Geométrico, considerando as características históricas do ativo
            """)

            # Exibir títulos e links das notícias
            st.markdown(f"**📰 Últimas Notícias para {ticker_interesse}**")
            if noticias:
                # Criar lista para exibir títulos e links
                for noticia in noticias:
                    link_parts = noticia['link'].split('/~/+/')
                    link = link_parts[1] if len(link_parts) > 1 else noticia['link']  # Se o padrão não estiver presente, use o link original
                    st.markdown(f"- [{noticia['title']}]({link})", unsafe_allow_html=True)

    except Exception as e:
        st.sidebar.error("Há dados incompletos. Tente novamente.")
