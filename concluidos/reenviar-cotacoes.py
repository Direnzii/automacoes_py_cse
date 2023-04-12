from os import getenv
from playwright.sync_api import sync_playwright
import time
import sys


class reenviar:
    def autenticar(self):
        login = getenv(key='USUARIO_MMONITORAMENTO')
        senha = getenv(key='SENHA_MONITORAMENTO')
        print('Tentando inserir as credenciais.')
        pagina.fill('xpath=//*[@id="username"]', login)
        pagina.fill('xpath=//*[@id="password"]', senha)
        time.sleep(0.3)
        pagina.locator(
            'xpath=/html/body/form/div/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td/button/span').click()  # clica para entrar/login
        time.sleep(1)

    def cotacoes(self):
        time.sleep(1)
        self.autenticar()
        print('Login realizado com sucesso')
        time.sleep(0.5)
        print('Setando Data e CNPJ do fornecedor')
        # cnpj_fornecedor = input("Insira o CNPJ do fornecedor sem pontos: ")
        # data = input("Insira a Data que quer realizar os reenvios, use essa formatação 01/01/2022: ")
        # pagina.fill('xpath=//*[@id="form:j_idt69_input"]', data)
        # time.sleep(0.5)
        # pagina.fill('xpath=//*[@id="form:j_idt72_input"]', data)
        # time.sleep(0.5)
        # pagina.fill('xpath=//*[@id="form:j_idt104"]', cnpj_fornecedor)
        # time.sleep(0.5)
        # pagina.locator(
        #     'xpath=/html/body/div[3]/form[1]/div[2]/div/table/tbody/tr[1]/td[1]/table[4]/tbody/tr/td[1]/input').click()  # clicar na checkbox
        # time.sleep(0.5)
        # pagina.locator('xpath=/html/body/div[3]/form[1]/div[2]/div/table/tbody/tr[1]/td[2]/table/tbody/tr/td['
        #                '1]/div/ul/li[2]').click()  # clicar no em andamento
        time.sleep(0.5)
        pagina.locator(
            'xpath=/html/body/div[3]/form[1]/div[2]/div/table/tbody/tr[2]/td/center/button[2]/span').click()  # clicar em buscar
        print('Carregando...')
        reload = pagina.locator('xpath=/html/body/div[3]/form[1]/div[5]/img').is_visible()
        while reload == True:
            time.sleep(1)
            reload = pagina.locator('xpath=//*[@id="form:j_idt57_blocker"]').is_visible()
        if self.verificar_se_retornou_algo():  # True quer dizer que retornou sim algo na primeira busca
            self.reenviar_cotacoes()
        else:
            print('Programa não encontrou nada.')
            return False

    def verificar_se_retornou_algo(self):
        botoes_enviar = pagina.locator(
            'xpath=/html/body/div[3]/form[1]/div[3]/div/div[3]/table/tbody/tr').count()  # contar a quantidade de botões enviar tem na pagina
        contador = 0
        for botao in range(1, botoes_enviar):
            contador += 1
        contador = contador + 1  # quantidade exata de botões enviar na pagina
        if contador == 1:
            return False
        if contador > 0:
            return True
        else:
            return

    def contar_enviar(self):
        botoes_enviar = pagina.locator(
            'xpath=/html/body/div[3]/form[1]/div[3]/div/div[3]/table/tbody/tr').count()  # contar a quantidade de botões enviar tem na pagina
        time.sleep(0.5)
        if botoes_enviar == 1:
            primeiro_enviar = pagina.locator(
                'xpath=/html/body/div[3]/form[1]/div[3]/div/div[3]/table/tbody/tr/td[6]/div/button/span').get_attribute(
                'class')
        contador = 0
        for i in range(1, botoes_enviar):
            contador += 1
        contador = contador + 1  # quantidade exata de botões enviar na pagina
        return int(contador)

    def reenviar_cotacoes(self):
        diminuir = self.contar_enviar()
        qtd_botoes = self.contar_enviar()
        print('Reenviando cotacoes...')
        while diminuir <= qtd_botoes:
            if diminuir == 0:
                break
            else:
                pagina.locator(
                    f'xpath=/html/body/div[3]/form[1]/div[3]/div/div[3]/table/tbody/tr[{diminuir}]/td[6]/div/button/span').click()  # clica em enviar
                time.sleep(1)
                # pagina.locator(
                #     'xpath=/html/body/div[3]/form[1]/div[3]/div/div[2]/div[1]/a/span').click() # fecha a modal PARA TESTES SEM REENVIAR
                pagina.locator(
                    'xpath=/html/body/div[3]/form[1]/div[3]/div/div[2]/div[3]/button[1]/span').click()  # clica em sim na modal de confirmação
                time.sleep(1)
                diminuir -= 1

        botao_avancar = pagina.locator(
            'xpath=/html/body/div[3]/form[1]/div[3]/div/div[3]/table/tfoot/tr/td/span[4]').get_attribute(
            'class')  # ver se da pra clicar no botão de passar a pagina
        if botao_avancar == 'ui-paginator-next ui-state-default ui-corner-all ui-state-disabled':
            print("Não existem mais paginas com cotações\nTodas as cotações foram reenviadas\nFechando o programa.")
            return
        if botao_avancar == 'ui-paginator-next ui-state-default ui-corner-all':
            pagina.locator(
                'xpath=/html/body/div[3]/form[1]/div[3]/div/div[3]/table/tfoot/tr/td/span[4]').click()  # tenta avançar na pagina
            time.sleep(1)
            self.reenviar_cotacoes()


def erro_para_rodar_o_programa():
    print(
        'Você fez merda, para rodar o programa são necessarios 2 argumentos, Data que quer reenviar e CNPJ do fornecedor.')


reenviar = reenviar()  # parametrizando a classe

with sync_playwright() as p:
    ##### VARIAVEIS DO PLAYWRIGHT #####
    navegador = p.firefox.launch(
        headless=False)  # por padrão esse modo é headless = True (não mostra o navegador abrindo)
    pagina = navegador.new_page()
    pagina.goto('http://monitoramento.apicotefacil.com:8280/CTFL-Monitoramento/login.jsf')
    ###################################
    reenviar.cotacoes()