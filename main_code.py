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

# Lista de códigos e nomes das empresas
empresas = [('MGLU3', 'Magazine Luiza'), ('HAPV3', 'Hapvida'), ('CIEL3', 'Cielo'), ('BBDC4', 'Banco Bradesco'), ('PETR4', 'Petrobras'), ('ITUB4', 'Itaú Unibanco'), ('ABEV3', 'Ambev'), ('LREN3', 'Lojas Renner'), ('COGN3', 'Cogna'), ('B3SA3', 'B3'), ('CVCB3', 'CVC'), ('ITSA4', 'Itaúsa'), ('VALE3', 'Vale'), ('SOMA3', 'Grupo Soma'), ('USIM5', 'Usiminas'), ('ASAI3', 'Assaí'), ('BRKM5', 'Braskem'), ('RAIZ4', 'Raízen'), ('MRVE3', 'MRV'), ('SUZB3', 'Suzano'), ('CPLE6', 'Copel'), ('VBBR3', 'Vibra Energia'), ('ANIM3', 'Ânima Educação'), ('ENEV3', 'Eneva'), ('EMBR3', 'Embraer'), ('RAIL3', 'Rumo'), ('MRFG3', 'Marfrig'), ('CMIG4', 'CEMIG'), ('BEEF3', 'Minerva'), ('PRIO3', 'PetroRio'), ('POMO4', 'Marcopolo'), ('BBSE3', 'BB Seguridade'), ('AMER3', 'Americanas'), ('GGBR4', 'Gerdau'), ('KLBN4', 'Klabin'), ('RENT3', 'Localiza'), ('CSNA3', 'Siderúrgica Nacional'), ('AZUL4', 'Azul'), ('GOAU4', 'Metalúrgica Gerdau'), ('RDOR3', "Rede D'Or"), ('BBAS3', 'Banco do Brasil'), ('HBSA3', 'Hidrovias do Brasil'), ('PETZ3', 'Petz'), ('NTCO3', 'Natura'), ('QUAL3', 'Qualicorp'), ('CMIN3', 'CSN Mineração'), ('GMAT3', 'Grupo Mateus'), ('CCRO3', 'Grupo CCR'), ('CYRE3', 'Cyrela'), ('BRFS3', 'BRF'), ('EQTL3', 'Equatorial Energia'), ('AERI3', 'Aeris Energy'), ('PETR3', 'Petrobras'), ('CEAB3', 'C&A'), ('JBSS3', 'JBS'), ('AURE3', 'VTRM ENERGIA PARTICIPAÃiES S.A.'), ('RRRP3', '3R Petroleum'), ('TIMS3', 'TIM'), ('ELET3', 'Eletrobras'), ('BBDC3', 'Banco Bradesco'), ('CRFB3', 'Carrefour Brasil'), ('PCAR3', 'Grupo Pão de Açúcar'), ('ALPA4', 'Alpargatas'), ('CSMG3', 'COPASA'), ('LWSA3', 'Locaweb'), ('MULT3', 'Multiplan'), ('JHSF3', 'JHSF'), ('RADL3', 'RaiaDrogasil'), ('IFCM3', 'Infracommerce'), ('WEGE3', 'WEG'), ('GOLL4', 'GOL'), ('RECV3', 'PetroRecôncavo'), ('SEQL3', 'Sequoia Logística'), ('MLAS3', 'Multilaser'), ('MOVI3', 'Movida'), ('CSAN3', 'Cosan'), ('VAMO3', 'Grupo Vamos'), ('TEND3', 'Construtora Tenda'), ('SMFT3', 'Smart Fit'), ('ECOR3', 'EcoRodovias'), ('TOTS3', 'Totvs'), ('CBAV3', 'CBA'), ('UGPA3', 'Ultrapar'), ('GFSA3', 'Gafisa'), ('IRBR3', 'IRB Brasil RE'), ('FLRY3', 'Fleury'), ('CXSE3', 'Caixa Seguridade'), ('ONCO3', 'Oncoclínicas'), ('BRAP4', 'Bradespar'), ('SBFG3', 'Grupo SBF'), ('OIBR3', 'Oi'), ('RAPT4', 'Randon'), ('SIMH3', 'Simpar'), ('CPFE3', 'CPFL Energia'), ('YDUQ3', 'YDUQS'), ('CURY3', 'Cury'), ('TRPL4', 'Transmissão Paulista'), ('CPLE3', 'Copel'), ('KEPL3', 'Kepler Weber'), ('LJQQ3', 'Lojas Quero-Quero'), ('SBSP3', 'Sabesp'), ('DXCO3', 'Dexco'), ('ESPA3', 'Espaçolaser'), ('EZTC3', 'EZTEC'), ('SAPR4', 'Sanepar'), ('DIRR3', 'Direcional'), ('BRSR6', 'Banrisul'), ('KLBN3', 'Klabin'), ('AZEV4', 'Azevedo & Travassos'), ('STBP3', 'Santos Brasil'), ('GUAR3', 'Guararapes'), ('ARZZ3', 'Arezzo'), ('SGPS3', 'Springs'), ('MEGA3', 'OMEGA ENERGIA S.A.'), ('SLCE3', 'SLC Agrícola'), ('HYPE3', 'Hypera'), ('EGIE3', 'Engie'), ('NEOE3', 'Neoenergia'), ('GGPS3', 'GPS'), ('VIVA3', 'Vivara'), ('TTEN3', '3tentos'), ('RANI3', 'Irani'), ('PSSA3', 'Porto Seguro'), ('INTB3', 'Intelbras'), ('VIVT3', 'Vivo'), ('AMAR3', 'Lojas Marisa'), ('PDGR3', 'PDG Realty'), ('SMTO3', 'São Martinho'), ('ENAT3', 'Enauta'), ('AMBP3', 'Ambipar'), ('MEAL3', 'IMC Alimentação'), ('CLSA3', 'ClearSale'), ('GRND3', 'Grendene'), ('POSI3', 'Positivo'), ('AESB3', 'AES Brasil'), ('CASH3', 'Méliuz'), ('MDIA3', 'M. Dias Branco'), ('DESK3', 'Desktop'), ('MTRE3', 'Mitre Realty'), ('VVEO3', 'Viveo'), ('MBLY3', 'Mobly'), ('RCSL4', 'Recrusul'), ('PLPL3', 'Plano&Plano'), ('PGMN3', 'Pague Menos'), ('WIZC3', 'Wiz Soluções'), ('SHUL4', 'Schulz'), ('BPAN4', 'Banco Pan'), ('SEER3', 'Ser Educacional'), ('CAML3', 'Camil Alimentos'), ('ARML3', 'Armac'), ('ODPV3', 'Odontoprev'), ('MATD3', 'Mater Dei'), ('LEVE3', 'Mahle Metal Leve'), ('ZAMP3', 'Zamp'), ('CSED3', 'Cruzeiro do Sul Educacional'), ('TRAD3', 'Traders Club'), ('AGRO3', 'BrasilAgro'), ('LIGT3', 'Light'), ('ELET6', 'Eletrobras'), ('VULC3', 'Vulcabras'), ('DASA3', 'Dasa'), ('MYPK3', 'Iochpe-Maxion'), ('TRIS3', 'Trisul'), ('OPCT3', 'OceanPact'), ('AZEV3', 'Azevedo & Travassos'), ('ABCB4', 'Banco ABC Brasil'), ('ORVR3', 'Orizon'), ('RCSL3', 'Recrusul'), ('PFRM3', 'Profarma'), ('CMIG3', 'CEMIG'), ('LAVV3', 'Lavvi Incorporadora'), ('JALL3', 'Jalles Machado'), ('MDNE3', 'Moura Dubeux'), ('LOGG3', 'LOG CP'), ('BMGB4', 'Banco BMG'), ('PNVL3', 'Dimed'), ('PTBL3', 'Portobello'), ('MILS3', 'Mills'), ('FIQE3', 'Unifique'), ('LUPA3', 'Lupatech'), ('BRIT3', 'Brisanet'), ('BLAU3', 'Blau Farmacêutica'), ('PRNR3', 'Priner'), ('EVEN3', 'Even'), ('CTNM4', 'Coteminas'), ('VLID3', 'Valid'), ('TASA4', 'Taurus'), ('HBOR3', 'Helbor'), ('FRAS3', 'Fras-le'), ('SHOW3', 'Time For Fun'), ('HBRE3', 'HBR Realty'), ('ENJU3', 'Enjoei'), ('NGRD3', 'Neogrid'), ('FESA4', 'Ferbasa'), ('ITUB3', 'Itaú Unibanco'), ('PINE4', 'PINE'), ('VIVR3', 'Viver'), ('CTSA4', 'Santanense'), ('JSLG3', 'JSL'), ('CTSA3', 'Santanense'), ('RNEW4', 'Renova Energia'), ('SAPR3', 'Sanepar'), ('VITT3', 'Vittia'), ('TUPY3', 'Tupy'), ('USIM3', 'Usiminas'), ('ROMI3', 'Indústrias ROMI'), ('KRSA3', 'Kora Saúde'), ('ALPK3', 'Estapar'), ('SYNE3', 'SYN'), ('WEST3', 'Westwing'), ('PDTC3', 'Padtec'), ('BMOB3', 'Bemobi'), ('TGMA3', 'Tegma'), ('BRKM3', 'Braskem'), ('UNIP6', 'Unipar'), ('PORT3', 'Wilson Sons'), ('AALR3', 'Alliança'), ('TECN3', 'Technos'), ('TAEE4', 'Taesa'), ('ETER3', 'Eternit'), ('UCAS3', 'Unicasa'), ('TFCO4', 'Track & Field'), ('LPSB3', 'Lopes'), ('ITSA3', 'Itaúsa'), ('MTSA4', 'METISA'), ('SOJA3', 'Boa Safra Sementes'), ('BRAP3', 'Bradespar'), ('POMO3', 'Marcopolo'), ('TCSA3', 'Tecnisa'), ('NINJ3', 'GetNinjas'), ('IGTI3', 'Jereissati Participações'), ('IGTI3', 'Iguatemi'), ('DEXP3', 'Dexxos'), ('SANB4', 'Banco Santander'), ('MELK3', 'Melnick'), ('LAND3', 'Terra Santa'), ('ALLD3', 'Allied'), ('SANB3', 'Banco Santander'), ('TAEE3', 'Taesa'), ('CAMB3', 'Cambuci'), ('RSID3', 'Rossi Residencial'), ('RNEW3', 'Renova Energia'), ('DMVF3', 'D1000 Varejo Farma'), ('CSUD3', 'CSU Cardsystem'), ('ELMD3', 'Eletromidia'), ('DOTZ3', 'Dotz'), ('GGBR3', 'Gerdau'), ('GOAU3', 'Metalúrgica Gerdau'), ('LOGN3', 'Log-In'), ('APER3', 'Alper'), ('TPIS3', 'Triunfo'), ('AGXY3', 'AgroGalaxy'), ('PMAM3', 'Paranapanema'), ('EUCA4', 'Eucatex'), ('BPAC5', 'Banco BTG Pactual'), ('SCAR3', 'São Carlos'), ('OIBR4', 'Oi'), ('BOBR4', 'Bombril'), ('JFEN3', 'João Fortes'), ('INEP4', 'Inepar'), ('TASA3', 'Taurus'), ('ALUP4', 'Alupar'), ('INEP3', 'Inepar'), ('ATMP3', 'Atma'), ('BMEB4', 'Banco Mercantil do Brasil'), ('RPMG3', 'Refinaria de Manguinhos'), ('ALUP3', 'Alupar'), ('CEBR6', 'CEB'), ('ATOM3', 'ATOM'), ('LVTC3', 'WDC Networks'), ('SNSY5', 'Sansuy'), ('EPAR3', 'EPAR3'), ('RAPT3', 'Randon'), ('PTNT4', 'Pettenati'), ('COCE5', 'Coelce'), ('UNIP3', 'Unipar'), ('BEES3', 'Banestes'), ('NUTR3', 'Nutriplant'), ('TELB4', 'Telebras'), ('CEBR3', 'CEB'), ('CGRA4', 'Grazziotin'), ('MNPR3', 'Minupar'), ('ENGI4', 'Energisa'), ('BIOM3', 'Biomm'), ('VSTE3', 'LE LIS BLANC'), ('BPAC3', 'Banco BTG Pactual'), ('BRSR3', 'Banrisul'), ('REDE3', 'Rede Energia'), ('DEXP4', 'Dexxos'), ('FHER3', 'Fertilizantes Heringer'), ('CGRA3', 'Grazziotin'), ('ENGI3', 'Energisa'), ('BEES4', 'Banestes'), ('BRIV4', 'Alfa Investimento'), ('ESTR4', 'Estrela'), ('WHRL3', 'Whirlpool'), ('HAGA3', 'Haga'), ('BAHI3', 'Bahema'), ('MWET4', 'Wetzel'), ('EMAE4', 'EMAE'), ('ALPA3', 'Alpargatas'), ('OSXB3', 'OSX Brasil'), ('EALT4', 'Electro Aço Altona'), ('CRIV3', 'Alfa Financeira'), ('CRIV4', 'Alfa Financeira'), ('EUCA3', 'Eucatex'), ('HOOT4', 'Hotéis Othon'), ('CRPG6', 'Tronox Pigmentos'), ('OFSA3', 'Ourofino Saúde Animal'), ('RDNI3', 'RNI'), ('RSUL4', 'Metalúrgica Riosulense'), ('EQPA3', 'Equatorial Energia Pará'), ('BGIP4', 'Banese'), ('CEBR5', 'CEB'), ('FRTA3', 'Pomi Frutas'), ('TRPL3', 'Transmissão Paulista'), ('CTKA4', 'Karsten'), ('HETA4', 'Hercules'), ('CLSC4', 'Celesc'), ('CEEB3', 'COELBA'), ('CRPG5', 'Tronox Pigmentos'), ('BRKM6', 'Braskem'), ('NEXP3', 'Brasil Brokers'), ('HAGA4', 'Haga'), ('FRIO3', 'Metalfrio'), ('WHRL4', 'Whirlpool'), ('MGEL4', 'Mangels'), ('EQPA5', 'Equatorial Energia Pará'), ('AVLL3', 'Alphaville'), ('WLMM3', 'WLM'), ('BAZA3', 'Banco da Amazônia'), ('TEKA4', 'Teka'), ('BDLL4', 'Bardella'), ('EKTR4', 'Elektro'), ('GEPA4', 'Rio Paranapanema Energia'), ('CPLE5', 'Copel'), ('CTNM3', 'Coteminas'), ('AFLT3', 'Afluente T'), ('TELB3', 'Telebras'), ('MNDL3', 'Mundial'), ('CSRN3', 'COSERN'), ('CEDO4', 'Cedro Têxtil'), ('BMEB3', 'Banco Mercantil do Brasil'), ('BMIN4', 'Banco Mercantil de Investimentos'), ('IGTI4', 'Jereissati Participações'), ('IGTI4', 'Iguatemi'), ('PLAS3', 'Plascar'), ('CGAS5', 'Comgás'), ('EQPA7', 'Equatorial Energia Pará'), ('ENMT3', 'Energisa MT'), ('BALM4', 'Baumer'), ('BAUH4', 'Excelsior'), ('HBTS5', 'Habitasul'), ('WLMM4', 'WLM'), ('PTNT3', 'Pettenati'), ('BNBR3', 'Banco do Nordeste'), ('BGIP3', 'Banese'), ('JOPA3', 'Josapar'), ('CALI3', 'Adolpho Lindenberg'), ('DOHL4', 'Döhler'), ('DTCY3', 'Dtcom'), ('NORD3', 'Nordon'), ('BMKS3', 'Monark'), ('BSLI4', 'Banco de Brasília'), ('FESA3', 'Ferbasa'), ('LUXM4', 'Trevisa'), ('BALM3', 'Baumer'), ('BMIN3', 'Banco Mercantil de Investimentos'), ('PATI3', 'Panatlântica'), ('BRIV3', 'Alfa Investimento'), ('CSAB3', 'Cia. de Seg. Aliança da Bahia'), ('EQMA3B', 'Equatorial Maranhão'), ('CSAB4', 'Cia. de Seg. Aliança da Bahia'), ('CEDO3', 'Cedro Têxtil'), ('BRSR5', 'Banrisul'), ('MERC4', 'Mercantil do Brasil Financeira'), ('DMFN3', 'DMFN3'), ('CEED3', 'CEEE D'), ('BSLI3', 'Banco de Brasília'), ('CGAS3', 'Comgás'), ('UNIP5', 'Unipar'), ('FIEI3', 'FIEI3'), ('RPAD3', 'Alfa Holdings'), ('EALT3', 'Electro Aço Altona'), ('ENMT4', 'Energisa MT'), ('CEED4', 'CEEE D'), ('DOHL3', 'Döhler'), ('CEEB5', 'COELBA'), ('PEAB3', 'Participações Aliança da Bahia'), ('MRSA3B', 'MRS Logística'), ('BRGE12', 'Consórcio Alfa'), ('CLSC3', 'Celesc'), ('RPAD6', 'Alfa Holdings'), ('BRGE6', 'Consórcio Alfa'), ('CRPG3', 'Tronox Pigmentos'), ('SNSY3', 'Sansuy'), ('MRSA5B', 'MRS Logística'), ('MAPT4', 'Cemepe'), ('CTKA3', 'Karsten'), ('CSRN5', 'COSERN'), ('GEPA3', 'Rio Paranapanema Energia'), ('GSHP3', 'General Shopping & Outlets'), ('RPAD5', 'Alfa Holdings'), ('AHEB3', 'São Paulo Turismo'), ('BRGE3', 'Consórcio Alfa'), ('MOAR3', 'Monteiro Aranha'), ('BRGE5', 'Consórcio Alfa'), ('CSRN6', 'COSERN'), ('TKNO4', 'Tekno'), ('BDLL3', 'Bardella'), ('ELET5', 'Eletrobras'), ('SOND6', 'Sondotécnica'), ('CBEE3', 'Ampla Energia'), ('SOND5', 'Sondotécnica'), ('GPAR3', 'CELGPAR'), ('SQIA3', 'Sinqia'), ('ESTR3', 'Estrela'), ('BRGE11', 'Consórcio Alfa'), ('BRGE8', 'Consórcio Alfa'), ('BRGE7', 'Consórcio Alfa'), ('MRSA6B', 'MRS Logística'), ('ALSO3', 'Aliansce Sonae'), ('BRPR3', 'BR Properties'), ('LIPR3', 'Eletropar'), ('PATI4', 'Panatlântica'), ('MTSA3', 'METISA'), ('SLED4', 'Saraiva'), ('SLED3', 'Saraiva'), ('EQPA6', 'Equatorial Energia Pará'), ('AHEB6', 'São Paulo Turismo'), ('PINE3', 'PINE'), ('VIIA3', 'VIIA3'), ('EKTR3', 'Elektro'), ('MWET3', 'Wetzel'), ('USIM6', 'Usiminas'), ('AHEB5', 'São Paulo Turismo'), ('ENBR3', 'EDP Brasil'), ('BOAS3', 'Boa Vista'), ('PEAB4', 'Participações Aliança da Bahia'), ('COCE3', 'Coelce'), ('JOPA4', 'Josapar'), ('MODL3', 'Banco Modal'), ('MERC3', 'Mercantil do Brasil Financeira'), ('CEGR3', 'Naturgy (CEG)'), ('MAPT3', 'Cemepe'), ('CRDE3', 'CR2'), ('IGBR3', 'IGB Eletrônica'), ('MSPA4', 'Melhoramentos'), ('ODER4', 'Conservas Oderich'), ('PARD3', 'Hermes Pardini'), ('CASN3', 'CASAN'), ('WIZS3', 'WIZS3'), ('LLIS3', 'LLIS3'), ('MSPA3', 'Melhoramentos'), ('BRML3', 'BRMalls'), ('DMMO3', 'Dommo Energia'), ('GETT3', 'Getnet'), ('GETT4', 'Getnet'), ('SULA4', 'SulAmérica'), ('SULA3', 'SulAmérica'), ('CEPE5', 'CELPE'), ('TCNO4', 'Tecnosolo'), ('TCNO3', 'Tecnosolo'), ('CEPE6', 'CELPE'), ('BKBR3', 'BKBR3'), ('MTIG4', 'Metalgráfica Iguaçu'), ('BLUT4', 'Blue Tech Solutions'), ('BLUT3', 'Blue Tech Solutions'), ('MODL4', 'Banco Modal'), ('CARD3', 'CARD3'), ('SHUL3', 'Schulz'), ('FIGE3', 'Investimentos Bemge'), ('FNCN3', 'Finansinos'), ('TEKA3', 'Teka'), ('HETA3', 'Hercules'), ('LCAM3', 'Locamerica'), ('BIDI4', 'Banco Inter'), ('BIDI3', 'Banco Inter'), ('EEEL4', 'CEEE GT'), ('EEEL3', 'CEEE GT'), ('BBRK3', 'BBRK3'), ('SOND3', 'Sondotécnica'), ('CESP6', 'CESP'), ('CESP3', 'CESP'), ('CESP5', 'CESP'), ('ECPR4', 'Encorpar'), ('MOSI3', 'Mosaico'), ('POWE3', 'Focus Energia'), ('ECPR3', 'Encorpar'), ('GNDI3', 'NotreDame Intermédica'), ('LAME4', 'Lojas Americanas'), ('LAME3', 'Lojas Americanas'), ('OMGE3', 'Omega Geração'), ('IGTA3', 'IGTA3'), ('JPSA3', 'JPSA3'), ('BRDT3', 'BRDT3'), ('JBDU4', 'JBDU4'), ('JBDU3', 'JBDU3'), ('HGTX3', 'Hering'), ('CCPR3', 'CCPR3'), ('DTEX3', 'DTEX3'), ('VVAR3', 'VVAR3'), ('PNVL4', 'Dimed'), ('TESA3', 'Terra Santa'), ('BTOW3', 'BTOW3'), ('LINX3', 'Linx'), ('BTTL3', 'Embpar'), ('GPCP3', 'GPCP3'), ('GPCP4', 'GPCP4'), ('SMLS3', 'Smiles'), ('MMXM3', 'MMX Mineração'), ('BSEV3', 'Biosev'), ('CNTO3', 'CNTO3'), ('TIET4', 'AES Tietê Energia'), ('TIET3', 'AES Tietê Energia'), ('CORR4', 'Corrêa Ribeiro'), ('CEPE3', 'CELPE'), ('CALI4', 'Adolpho Lindenberg'), ('SNSY6', 'Sansuy'), ('CASN4', 'CASAN'), ('EMAE3', 'EMAE'), ('BPAR3', 'Banpará'), ('APTI4', 'Aliperti'), ('VSPT3', 'FCA'), ('MTIG3', 'Metalgráfica Iguaçu'), ('FIGE4', 'Investimentos Bemge'), ('LUXM3', 'Trevisa'), ('TKNO3', 'Tekno'), ('COCE6', 'Coelce'), ('MGEL3', 'Mangels'), ('CTSA8', 'Santanense'), ('MMAQ4', 'Minasmáquinas')]

# Mapeamento de nomes para tickers
mapeamento_tickers = {nome.lower().replace(" ", ""): ticker for ticker, nome in empresas}

# Função para obter o ticker pelo nome da companhia
def obter_ticker_pelo_nome_da_companhia(nome_companhia):
    nome_companhia = nome_companhia.lower().replace(" ", "")
    return mapeamento_tickers.get(nome_companhia, None)

# Função para adicionar sufixo ".SA" ao ticker
def adicionar_sufixo_sa(ticker):
    return f"{ticker}.SA"

# Breve descrição sobre o projeto
st.write("## Bem-vindo ao Start Investor")
st.write("###### Faça a sua consulta para otimizar seu tempo e aprimorar seu processo de análise.")

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


# Função para obter o ticker pelo nome da companhia
def obter_ticker_pelo_nome_da_companhia(nome_companhia):
    # Adicione lógica real para obter o ticker correspondente ao nome da companhia
    # Pode envolver a consulta de uma fonte de dados, um mapeamento pré-definido, etc.
    # Certifique-se de ajustar conforme necessário com base na sua implementação real.
    # Retorna None se o nome da companhia não for reconhecido
    return None

# Exemplo de uso com Streamlit
st.sidebar.markdown("# Start Investor 📈")  # Adiciona título à barra lateral

# Adiciona os inputs na barra lateral
ticker_interesse = st.sidebar.text_input("Insira o ticker de interesse (ex: MGLU3):").upper()
nome_companhia_interesse = st.sidebar.text_input("Insira o nome da companhia de interesse:").strip()
periodo_interesse = st.sidebar.text_input("Insira o período desejado para o histórico de preços (ex: 3mo):")

if st.sidebar.button("Analisar"):
    if ticker_interesse and nome_companhia_interesse:
        st.sidebar.error("Por favor, preencha apenas um dos campos: 'Ticker' ou 'Nome da companhia'.")
    elif not ticker_interesse and not nome_companhia_interesse:
        st.sidebar.error("Por favor, preencha um dos campos: 'Ticker' ou 'Nome da companhia'.")
    else:
        if ticker_interesse:
            # Criar instância do AnalisadorDadosMercado usando ticker
            analisador = AnalisadorDadosMercado()
            precos, noticias = analisador.baixar_dados(ticker_interesse, periodo_interesse)
        else:
            # Criar instância do AnalisadorDadosMercado usando o nome da companhia
            # Adicione lógica para corrigir espaços, maiúsculas/minúsculas, etc., no nome da companhia
            nome_companhia_interesse = nome_companhia_interesse.lower().replace(" ", "")
            # ... (outras correções conforme necessário)
            ticker_interesse = obter_ticker_pelo_nome_da_companhia(nome_companhia_interesse)  # Substitua com a lógica real
            if not ticker_interesse:
                st.sidebar.error("Nome da companhia não reconhecido. Por favor, verifique e tente novamente.")
            else:
                analisador = AnalisadorDadosMercado()

        # Restante do código permanece o mesmo
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
