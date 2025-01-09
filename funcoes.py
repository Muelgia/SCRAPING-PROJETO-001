import os 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import subprocess
import psutil

def navegador(porta, caminhoChrome):
    global driver

    usuarioPc = os.environ.get("USERNAME")
    user_data_dir = f'C://Users/{usuarioPc}/Desktop/navegadorChrome/{caminhoChrome}'
    remote_debugging_port = porta
    chrome_executable_path = 'C://Program Files/Google/Chrome/Application/chrome.exe'

    # Verifica se o Chrome já está aberto com as opções especificadas
    chrome_aberto = False
    for proc in psutil.process_iter(['name', 'cmdline']):
        if (proc.info['name'] and 'chrome' in proc.info['name'] and
                proc.info['cmdline'] and
                f'--remote-debugging-port={remote_debugging_port}' in proc.info['cmdline'] and
                f'--user-data-dir={user_data_dir}' in proc.info['cmdline']):
            chrome_aberto = True
            break

    # Abre o Chrome com as opções especificadas se não estiver aberto
    if not chrome_aberto:
        subprocess.Popen([chrome_executable_path, 
                          f'--remote-debugging-port={remote_debugging_port}', 
                          f'--user-data-dir={user_data_dir}'])

    # Configura as opções do Chrome para o WebDriver
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", f"localhost:{remote_debugging_port}")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    print('\nNavegador Iniciado! \n')
    return driver      
