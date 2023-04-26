import string
from playwright.sync_api import sync_playwright
import time
import re
import os
from datetime import datetime


class liberarForn:
    lista_matrizes = []

    lista_filiais = []

    lista_nao_clientes = []

    def autenticar(self):
        print("Inserindo as credenciais ...")
        time.sleep(0.5)
        usuario = os.getenv(key='USUARIO_OFICIAL')
        senha = os.getenv(key='SENHA_OFICIAL')
        site.fill('xpath=//*[@id="frmLogin:username"]', usuario)
        site.fill('xpath=//*[@id="frmLogin:password"]', senha)
        site.locator('xpath=//*[@id="frmLogin:loginButton"]').click()
        time.sleep(0.2)

    def abrir_arquivo(self, nome='JMF.txt'):
        with open(nome) as file:
            arquivo = file.read().replace(",", ' ').split()
        return arquivo

    def validar_se_da_para_ver_elemento(self, caminho_elemento_xpath, cliente):
        print("Validando se da pra ver elemento...")
        da_para_ver = False
        while da_para_ver == False:
            try:
                da_para_ver = site.locator(f'xpath={caminho_elemento_xpath}').is_visible()
                if da_para_ver == False:
                    print("Não deu, tentando de novo...")
                    time.sleep(0.5)
                if da_para_ver == True:
                    print("Deu certo a validação da pra ver elemento...")
                    # //*[@id="pesquisarClientes:cnpj"]
                    validar_se_ja_ta_na_aba_cliente = site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody'
                                                                   '/tr/td[2]/div/table[1]/tbody/tr[1]/td/form'
                                                                   '/table[1]/tbody/tr/td[1]/input').is_visible()
                    if validar_se_ja_ta_na_aba_cliente == True:
                        validar_se_preencheu = site.locator(
                            'xpath=//*[@id="pesquisarClientes:cnpj"]').input_value()
                        if not validar_se_preencheu:
                            #########
                            return da_para_ver
                    if validar_se_ja_ta_na_aba_cliente == False:
                        break
            except Exception as e:
                print("Erro na validação se da pra ver elemento...")
                continue
        return da_para_ver

    def inserir_no_arquivo(self, conteudo, arquivo):
        try:  # validar se o arquivo existe
            f = open(arquivo)
            f.close()
            with open(arquivo, 'w') as arquivo:
                arquivo.write("\n".join(conteudo))
        except:
            print('O arquivo de cache não existe!, criando')
            with open(arquivo, 'w') as arquivo:
                arquivo.write("\n".join(conteudo))

    def validar_listas(self, cliente):
        matriz = cliente in self.lista_matrizes
        filial = cliente in self.lista_filiais
        nao_cliente = cliente in self.lista_nao_clientes
        if matriz == True:
            return True
        if filial == True:
            return True
        if nao_cliente == True:
            return True
        else:
            return False

    def get_filiais(self):
        site.locator('xpath=//*[@id="administrarCliente:tabFiliais_cell"]').click()  # clicar na aba filiais
        for i in range(1, 11):  # 10 tentativas para ver se é falso ou nao
            print(f"Tentativa numero {i} de ver a aba filiais")
            eh_visivel_contar_filiais = site.locator(
                'xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody/tr[1]/td/form'
                '/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[1]/td/div'
                '/div/table/tbody/tr[1]').is_visible()
            if eh_visivel_contar_filiais == True:
                break
            if eh_visivel_contar_filiais == False:
                time.sleep(0.5)

        print("Deu certo, contando filiais pra pegar todas...")
        contar_filiais = site.locator(
            'xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody/tr[1]/td/form'
            '/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[1]/td/div'
            '/div/table/tbody/tr').count()

        if contar_filiais != 0:
            print("Filial é diferente de zero, pegando todas...")
            for numero in range(1, contar_filiais + 1):  # range usado para usar um for na quantidade de filiais
                try:
                    filial = site.locator(
                        f'xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody/tr[1]/td/form'
                        '/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[1]/td/div'
                        f'/div/table/tbody/tr[{numero}]').text_content()
                    filial = filial.split()[0]
                    filial = self.remover_string(filial)
                    validacao_filial = self.validar_listas(
                        int(filial))  # validar se a filial ja esta na lista das filiais
                    if validacao_filial == False:
                        self.lista_filiais.append(int(filial))
                    if validacao_filial == True:
                        continue
                except Exception as e:
                    print(f"Deu pau pra pegar a filial com o caminho numero {numero}...")
                    continue
            return
        else:
            print("Nenhuma filial encontrada, saindo da aba filial...")
            return

    def remover_string(self, valor):
        valor = re.sub('[^0-9]', '', valor)
        return int(valor)

    def resolver_zeros(self, numero):
        numero = str(numero)
        contador = 0
        for i in numero:
            contador += 1
        numero = int(numero)
        if contador != 14:
            zeros = 14 - contador
            if zeros == 1:
                numero = numero * 10
                return numero
            elif zeros == 2:
                numero = numero * 100
                return numero
            elif zeros == 3:
                numero = numero * 1000
                return numero
            elif zeros == 4:
                numero = numero * 10000
                return numero
            elif zeros == 5:
                numero = numero * 100000
                return numero
            elif zeros == 6:
                numero = numero * 1000000
                return numero
            elif zeros == 7:
                numero = numero * 10000000
                return numero
            elif zeros == 8:
                numero = numero * 100000000
                return numero
            elif zeros == 9:
                numero = numero * 1000000000
                return numero
            elif zeros == 10:
                numero = numero * 10000000000
                return numero
            elif zeros == 11:
                numero = numero * 100000000000
                return numero
        else:
            return numero

    def comparar_se_cliente_cote(self, cliente):
        contador = 0
        contador2 = 0
        while True:
            try:
                linha_cliente_ver = site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]'
                                                 '/div/table[1]/tbody/tr[1]/td/form/table[2]/tbody/tr[3]/td/div'
                                                 '/div[2]/div/div/table/tbody/tr').is_visible()
                for i in range(1, 4):
                    if linha_cliente_ver == False:
                        print(f"Não deu pra ver se é cliente cotefacil ou não, tentando de novo, tentativa {i} de 3...")
                        time.sleep(5)
                        linha_cliente_ver = site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]'
                                                         '/div/table[1]/tbody/tr[1]/td/form/table[2]/tbody/tr[3]/td/div'
                                                         '/div[2]/div/div/table/tbody/tr').is_visible()
                    if linha_cliente_ver == True:
                        print("Deu certo a validação é cliente cotefacil sim...")
                        return linha_cliente_ver
                return linha_cliente_ver
            except Exception as e:
                time.sleep(1)
                contador += 1
                if contador == 1:  # 10
                    try:
                        loading = self.validar_se_da_pra_ver_loading()
                        if loading == False:
                            site.locator('xpath=//*[@id="pesquisarClientes:btnPesquisar"]').click()
                            contador = 0
                            contador2 += 1
                            if contador2 == 2:
                                self.comparar_cliente_linha_cliente(cliente, validar_se_e_cliente_cote=False)
                                return True
                    except:
                        continue

    def comparar_cliente_linha_cliente(self, cliente, validar_se_e_cliente_cote=True):
        print("Inicio da comparação cliente linha cliente...")
        time.sleep(2)
        while True:
            if validar_se_e_cliente_cote == True:
                linha_cliente_ver = self.comparar_se_cliente_cote(cliente)
                if linha_cliente_ver == True:
                    try:
                        time.sleep(2)
                        linha_cliente = site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]'
                                                     '/div/table[1]/tbody/tr[1]/td/form/table[2]/tbody/tr[3]/td/div'
                                                     '/div[2]/div/div/table/tbody/tr').text_content()
                        linha_cliente = linha_cliente.split()[0]
                        linha_cliente = self.remover_string(linha_cliente)
                        if int(cliente) == int(linha_cliente):
                            return True
                    except:
                        linha_cliente_err = site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]'
                                                         '/div/table[1]/tbody/tr[1]/td/form/table[2]/tbody/tr[3]/td/div'
                                                         '/div[2]/div/div/table/tbody/tr').count()
                        if linha_cliente_err != 1:
                            linha_cliente = site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]'
                                                         '/div/table[1]/tbody/tr[1]/td/form/table[2]/tbody/tr[3]/td/div'
                                                         '/div[2]/div/div/table/tbody/tr[1]').text_content()
                            linha_cliente = linha_cliente.split()[0]
                            linha_cliente = self.remover_string(linha_cliente)
                            if int(cliente) == int(linha_cliente):
                                return True
                            else:
                                linha_cliente = self.resolver_zeros(linha_cliente)
                                cliente = self.resolver_zeros(cliente)
                                if cliente == linha_cliente:
                                    return True
                                else:
                                    linha_cliente2 = site.locator(
                                        'xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]'
                                        '/div/table[1]/tbody/tr[1]/td/form/table[2]/tbody/tr[3]/td'
                                        '/div/div[2]/div/div/table/tbody/tr[2]').text_content()
                                    linha_cliente2 = linha_cliente2.split()[0]
                                    linha_cliente2 = self.remover_string(linha_cliente2)
                                    if int(cliente) == int(linha_cliente2):
                                        return True
                                    else:
                                        linha_cliente2 = self.resolver_zeros(linha_cliente2)
                                        cliente = self.resolver_zeros(cliente)
                                        if cliente == linha_cliente2:
                                            return True
                        if linha_cliente_err == 1:
                            return False
                if linha_cliente_ver == False:
                    return False
            if validar_se_e_cliente_cote == False:
                try:
                    time.sleep(0.2)
                    linha_cliente = site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]'
                                                 '/div/table[1]/tbody/tr[1]/td/form/table[2]/tbody/tr[3]/td/div'
                                                 '/div[2]/div/div/table/tbody/tr').text_content()
                    linha_cliente = linha_cliente.split()[0]
                    linha_cliente = self.remover_string(linha_cliente)
                    if int(cliente) == int(linha_cliente):
                        return True
                except:
                    linha_cliente_err = site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]'
                                                     '/div/table[1]/tbody/tr[1]/td/form/table[2]/tbody/tr[3]/td/div'
                                                     '/div[2]/div/div/table/tbody/tr').count()
                    if linha_cliente_err != 1:
                        linha_cliente = site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]'
                                                     '/div/table[1]/tbody/tr[1]/td/form/table[2]/tbody/tr[3]/td/div'
                                                     '/div[2]/div/div/table/tbody/tr[1]').text_content()
                        linha_cliente = linha_cliente.split()[0]
                        linha_cliente = self.remover_string(linha_cliente)
                        if int(cliente) == int(linha_cliente):
                            return True
                        else:
                            linha_cliente = self.resolver_zeros(linha_cliente)
                            cliente = self.resolver_zeros(cliente)
                            if cliente == linha_cliente:
                                return True
                            else:
                                linha_cliente2 = site.locator(
                                    'xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]'
                                    '/div/table[1]/tbody/tr[1]/td/form/table[2]/tbody/tr[3]/td'
                                    '/div/div[2]/div/div/table/tbody/tr[2]').text_content()
                                linha_cliente2 = linha_cliente2.split()[0]
                                linha_cliente2 = self.remover_string(linha_cliente2)
                                if int(cliente) == int(linha_cliente2):
                                    return True
                                else:
                                    linha_cliente2 = self.resolver_zeros(linha_cliente2)
                                    cliente = self.resolver_zeros(cliente)
                                    if cliente == linha_cliente2:
                                        return True
                                    else:
                                        caminho_do_input = '//*[@id="pesquisarClientes:cnpj"]'
                                        caminho_erro = '/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div' \
                                                       '/table[1]/tbody/tr[1]/td/form/span/div/div/table/tbody' \
                                                       '/tr/td/table/tbody/tr/td[2]/table'
                                        da_pra_ver = self.validar_se_da_para_ver_elemento(caminho_do_input, cliente)
                                        if da_pra_ver == True:
                                            site.locator('xpath=//*[@id="pesquisarClientes:btnPesquisar"]').click()

    def clicar_aba_inicio(self, cliente):
        print("Clicando na aba de inicio...")
        caminho_imagem_aba_inicio = '/html/body/table/tbody/tr[1]/td/div/form[2]/ul/li[1]/a/img'
        caminho_conteudo_aba_inicio = '//*[@id="esConteudo"]'
        da_para_ver = self.validar_se_da_para_ver_elemento(caminho_imagem_aba_inicio, cliente)
        if da_para_ver == True:  # validar se da pra ver imagem aba inicio
            site.locator('xpath=/html/body/table/tbody/tr[1]/td/div/form[2]/ul/li[1]').click()  # clicar na aba inicio
            time.sleep(1)
            while True:
                print("Validando se da pra ver aba de inicio...")
                da_para_ver = self.validar_se_da_para_ver_elemento(caminho_conteudo_aba_inicio, cliente)
                if da_para_ver == True:
                    return

    def clicar_aba_cliente(self, cliente):
        print("Clicando na aba cliente...")
        caminho_imagem_aba_clientes = '/html/body/table/tbody/tr[1]/td/div/form[2]/ul/li[2]/a/img'
        caminho_botao_liberacao_aba_cliente = '/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]' \
                                              '/tbody/tr[1]/td/form/table[1]/tbody/tr/td[1]/input'
        da_para_ver = self.validar_se_da_para_ver_elemento(caminho_imagem_aba_clientes, cliente)
        if da_para_ver == True:  # validar se da pra ver imagem aba clientes
            site.locator('xpath=/html/body/table/tbody/tr[1]/td/div/form[2]/ul/li[2]').click()  # clicar na aba clientes
            time.sleep(0.5)
            da_para_ver1 = self.validar_se_da_para_ver_elemento(caminho_botao_liberacao_aba_cliente, cliente)
            if da_para_ver1 == True:
                return

    def reiniciar_a_tela(self, cliente):
        print("Reiniciando a tela...")
        self.clicar_aba_inicio(cliente)
        self.clicar_aba_cliente(cliente)
        return

    def validar_se_da_pra_ver_loading(self):
        caminho = '//*[@id="loadMessageFirstHref"]'
        da_para_ver = True
        print("Validando se da pra ver o loading...")
        while da_para_ver == True:
            try:
                da_para_ver = site.locator(f'xpath={caminho}').is_visible()
                if da_para_ver == True:
                    print("Ainda da pra ver o loading, tentando de novo...")
                    time.sleep(0.5)
                if da_para_ver == False:
                    print("Não da mais pra ver o loading, ok...")
                    break
            except Exception as e:
                print("Deu pau na hora de validar se da pra ver o loading...")
                continue
        return da_para_ver

    def validar_se_da_pra_ver_erro(self, caminho_elemento_xpath):
        time.sleep(0.5)
        da_para_ver = site.locator(f'xpath={caminho_elemento_xpath}').is_visible()
        if da_para_ver == False:
            time.sleep(0.5)
            return da_para_ver
        if da_para_ver == True:
            return da_para_ver

    def dentro_aba_cliente(self, cliente):

        caminho_erro = '/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody/tr[1]/td/form/span' \
                       '/div/div/table/tbody/tr/td/table/tbody/tr/td[2]/table'
        time.sleep(1)
        validar_se_checkbox_ta_on = site.locator('xpath=//*[@id="pesquisarClientes:mostrarFiliais"]').is_checked()
        if validar_se_checkbox_ta_on == False:
            site.locator('xpath=//*[@id="pesquisarClientes:mostrarFiliais"]').click()
        site.fill('xpath=//*[@id="pesquisarClientes:cnpj"]', str(cliente))
        time.sleep(2)
        site.locator('xpath=//*[@id="pesquisarClientes:btnPesquisar"]').click()  # clicar em pesquisar
        while True:
            time.sleep(1)
            site.locator('xpath=//*[@id="pesquisarClientes:btnPesquisar"]').click()  # clicar em pesquisar
            deu_erro = self.validar_se_da_pra_ver_erro(caminho_erro)
            if deu_erro == True:
                self.reiniciar_a_tela(cliente)
                time.sleep(0.5)
                validacao_cliente_cotefacil = self.dentro_aba_cliente(cliente)
                if validacao_cliente_cotefacil == True:  #### esta dando erro aqui, pois quando o cliente nao é da cote e da erro, cai aqui e nao tem validação
                    return True
                if validacao_cliente_cotefacil == False:
                    return False

            comparacao = self.comparar_cliente_linha_cliente(cliente)
            if comparacao == True:
                load = self.validar_se_da_pra_ver_loading()  # validar se da pra ver o loading
                if load == False:
                    try:
                        site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody'
                                     '/tr/td[2]/div/table[1]/tbody/tr[1]/td/form/table[2]'
                                     '/tbody/tr[3]/td/div/div[2]/div/div/table/tbody/tr'
                                     '/td[4]/input').click(timeout=60000)  # clicar no editar
                        time.sleep(0.5)
                        return True
                    except:
                        site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]'
                                     '/tbody/tr[1]/td/form/table[2]/tbody/tr[3]/td/div/div[2]/div/div'
                                     '/table/tbody/tr[1]/td[4]/input').click(timeout=60000)  # clicar no editar
                        time.sleep(0.5)
                        return True
            if comparacao == False:
                print(f"Cliente {cliente} não cadastrado na cotefacil.")
                return False

    def organizar_listas(self):
        self.autenticar()
        while True:
            try:
                print("Logado ...")
                arquivo = self.abrir_arquivo()  # abrir arquivo
                caminho_botao_ativar_inativar = '/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]' \
                                                '/tbody/tr[1]/td/form/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]' \
                                                '/td/table/tbody/tr/td/input'
                for cliente in arquivo:  # percorrer a lista de clientes (arquivo)
                    mega_validacao = len(cliente)
                    if mega_validacao >= 10:
                        self.cliente = cliente
                        print(f"Processando cliente {cliente} ...")
                        cliente = int(cliente.translate(str.maketrans('', '', string.punctuation)))
                        validacao = self.validar_listas(cliente)
                        if not validacao:
                            caminho_botao_liberacao_aba_cliente = '/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]' \
                                                                  '/tbody/tr[1]/td/form/table[1]/tbody/tr/td[1]/input'

                            ja_ta_dentro = site.locator(f'xpath={caminho_botao_liberacao_aba_cliente}').is_visible()
                            if not ja_ta_dentro:
                                self.clicar_aba_cliente(cliente)
                            validacao_cliente_cotefacil = self.dentro_aba_cliente(cliente)
                            if validacao_cliente_cotefacil:
                                da_para_ver_botao_ativar_inativar = self.validar_se_da_para_ver_elemento(
                                    caminho_botao_ativar_inativar, cliente)
                                if da_para_ver_botao_ativar_inativar:
                                    input_matriz = site.locator(
                                        'xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]'
                                        '/tbody/tr[1]/td/form/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td'
                                        '/table/tbody/tr/td/div/div[2]/table/tbody/tr[2]/td[2]/input').input_value()  # pegar o valor do campo "cnpj matriz"
                                    if not input_matriz:
                                        validacao_matriz_1 = self.validar_listas(int(cliente))
                                        if not validacao_matriz_1:
                                            self.lista_matrizes.append(
                                                int(cliente))  # validou que o cnpj não possui matriz setada (logo é uma matriz)
                                        print(f"Pegando as filiais do cnpj {cliente}")
                                        self.get_filiais()
                                        self.reiniciar_a_tela(cliente)
                                    else:
                                        print("É matriz, ver se tem filiais...")
                                        self.lista_filiais.append(int(cliente))  # colocando a filial na lista filiais
                                        validacao_matriz_2 = self.validar_listas(int(input_matriz))
                                        if not validacao_matriz_2:
                                            self.lista_matrizes.append(
                                                int(input_matriz))  # validou que o cnpj possui matriz setada (logo é uma filial), estou colocando o input da matriz na lista matrizes
                                            self.reiniciar_a_tela(cliente)
                                            time.sleep(0.5)
                                            print(f"Logando na matriz...{input_matriz}")
                                            self.dentro_aba_cliente(input_matriz)
                                            print("Pegando as filiais da matriz...")
                                            self.get_filiais()
                                            self.reiniciar_a_tela(cliente)
                            if not validacao_cliente_cotefacil:
                                self.lista_nao_clientes.append(int(cliente))
                                self.reiniciar_a_tela(cliente)
                                continue
                        if validacao:
                            continue
                    if mega_validacao < 10:
                        print('Cliente não considerado por ter menos de 10 caracteres')
                        self.lista_nao_clientes.append(cliente)

                now = datetime.now()
                fim = now.strftime("%H:%M:%S")
                print('Fim do processo: ', fim)
                a = 'saiu do for'
                self.reiniciar_a_tela(self.cliente)
                # da_para_ver_botao_ativar_inativar = self.validar_se_da_para_ver_elemento(caminho_botao_ativar_inativar, self.cliente)
                # if da_para_ver_botao_ativar_inativar == True:
                #     site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody/'
                #                  'tr[1]/td/form/table/tbody/tr[2]/td/div/div/table/tbody/tr[1]/td/table/tbody/tr'
                #                  '/td[8]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr/td[2]').click()
                #     self.validar_se_da_pra_ver_loading()
                return self.lista_matrizes
            except Exception as e:
                print('Deu pau, segue o baileEEEEEEEE....')
                site.goto('https://sistemas.cotefacil.com/CTFLLogan-webapp/login.jsf')
                continue

    def liberar_fornecedor(self, lista_matriz):
        for cliente in lista_matriz:
            self.dentro_aba_cliente(str(cliente))
            site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody/tr[1]/td'
                         '/form/table/tbody/tr[2]/td/div/div/table/tbody/tr[1]/td/table/tbody/tr/td[8]/table/tbody'
                         '/tr/td[2]/table/tbody/tr/td/table/tbody/tr/td[2]').click(timeout=60000)
            time.sleep(0.5)
            loading = self.validar_se_da_pra_ver_loading()
            if not loading:
                check_box_filiais = '//*[@id="administrarCliente:chkTodasFiliais"]'
                check_box_compradores = '//*[@id="administrarCliente:chkTodosCompradores"]'
                validar_se_checkbox_filiais_ta_checada = site.locator(f'xpath={check_box_filiais}').is_checked()
                validar_se_checkbox_compradores_ta_checada = site.locator(f'xpath={check_box_compradores}').is_checked()
                if validar_se_checkbox_filiais_ta_checada == False:
                    site.locator(f'xpath={check_box_filiais}').click()
                if validar_se_checkbox_compradores_ta_checada == False:
                    site.locator(f'xpath={check_box_compradores}').click()

                    site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody'
                                 '/tr[1]/td/form/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/table/tbody'
                                 '/tr/td/div[1]/div[2]/table/tbody/tr/td[2]/span/div/table/tbody/tr').count()

    def liberar_semi_auto(self):
        self.autenticar()
        arquivo = self.abrir_arquivo(nome='matriz.txt')
        for cliente in arquivo:
            cliente = cliente.replace("'", "")
            # site.locator('xpath=/html/body/table/tbody/tr[1]/td/div/form[2]/ul/li[1]/a/img').click()  ######BREAK
            site.fill(
                'xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody/tr[4]/td/form/table'
                '/tbody/tr[1]/td/div/div[2]/table/tbody/tr[2]/td[2]/input'
                , cliente)
            time.sleep(1)
            site.locator('xpath=//*[@id="pesquisarUsuarios:btnPesquisar"]').click()  # clicar em pesquisar

            print(cliente)
            try:
                time.sleep(2)
                site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody/tr[4]'
                             '/td/form/table/tbody/tr[3]/td/div/div[2]/table/tbody/tr/td[6]/a').click()  # editar
            except:
                a = 'mais de um'  #####
                input('Tem mais de um editar, clique em um e press enter ...')

            site.locator(
                'xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody/tr[1]/td/form/table/tbody/tr[2]'
                '/td/div/div/table/tbody/tr[1]/td/table/tbody/tr/td[8]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr/td[2]').click()
            fornecedor = '08241229000200 - MILFARMA - SP'
            representante = '39926 - On-line - cotefacil@milfarma.com.br'
            representante_add = '101385 - REPRESENTANTE COMERCIAL - no-reply@cotefacil.com'
            site.fill(
                'xpath=//*[@id="administrarCliente:fornecedor"]'
                , fornecedor)
            site.fill(
                'xpath=//*[@id="administrarCliente:sggRepresentante"]'
                , representante)
            a = 'esperando para remover'  #####
            input('Remova o representante e press enter ...')
            site.fill(
                'xpath=//*[@id="administrarCliente:fornecedor"]'
                , fornecedor)
            site.fill(
                'xpath=//*[@id="administrarCliente:sggRepresentante"]'
                , representante_add)
            a = 'clicar em adicionar'  #####
            input('Adicione o representante e press enter ...')
            site.locator('xpath=/html/body/table/tbody/tr[1]/td/div/form[2]/ul/li[1]').click()  # voltar


liberar_forn = liberarForn()

with sync_playwright() as p:
    navegador = p.firefox.launch(
        headless=False)  # por padrão esse modo é headless = True (não mostra o navegador abrindo)
    site = navegador.new_page()
    site.goto('https://sistemas.cotefacil.com/CTFLLogan-webapp/login.jsf')

    now = datetime.now()
    inicio = now.strftime("%H:%M:%S")
    print('Inicio do processo: ', inicio)

    # parametro_1 = input('Voce quer só realizar a liberação do fornecedor de forma semiautomatica ? (S) (N): ')
    parametro_1 = 'N'  ########## APAGAR
    if parametro_1 == 'S' or parametro_1 == 's':
        liberar_forn.liberar_semi_auto()
    else:
        try:
            lista = liberar_forn.organizar_listas()
            liberar_forn.liberar_fornecedor(lista)
        except Exception as Error:
            print(Error)