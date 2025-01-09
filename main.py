from funcoes import navegador
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dadosProjeto import nomeNavegador

driver = navegador(porta=3542, caminhoChrome=nomeNavegador)

wait = WebDriverWait(driver,0.1)

planilha = 'c:\\Users\\Samuel\\Downloads\\PIRACICABA_CNPJS.xlsx'

fonte = pd.read_excel(planilha)
fonte["CNPJ"] = fonte["CNPJ"].fillna(0).astype(int)

for cnpj in fonte["CNPJ"]: 

    cnpj = str(cnpj)

    while len(cnpj) < 14:
        cnpj = "0" + cnpj
    
    print(cnpj)
        
    campoCnpj = wait.until(EC.presence_of_element_located((By.ID, "DSC_CNPJ")))
    campoCnpj.clear()
    campoCnpj.send_keys(Keys.ARROW_LEFT*20)
    campoCnpj.send_keys(cnpj)

    clicaFiltrar = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="btn_filtrar"]')))
    clicaFiltrar.click()

    try:
        campoDados = campoCnpj = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="LcConteudo"]/div/table')))
        
        infoSite = campoDados.text

        print(infoSite)

        infoSite = infoSite.replace('\n', ';')

        dados = f'{cnpj}'+ ';' + f'{infoSite}' + '\n'

    except:

        dados = f'{cnpj}'+'\n'
        print('CNPJ SEM INFO')

    finally:
        botaoVoltar = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="btn_voltar"]')))
        botaoVoltar.click()

    with open('Dados.txt', 'a', encoding='utf-8') as notas:
        notas.write(dados)
    notas.close()

