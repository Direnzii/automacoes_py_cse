import string
from playwright.sync_api import sync_playwright
import time
import re
import os
import io
from datetime import datetime

lista_matrizes = []

lista_filiais = []

lista_nao_clientes = []


def autenticar():
    print("Inserindo as credenciais ...")
    time.sleep(0.5)
    usuario = os.getenv(key='USUARIO_OFICIAL')
    senha = os.getenv(key='SENHA_OFICIAL')
    site.fill('xpath=//*[@id="frmLogin:username"]', usuario)
    site.fill('xpath=//*[@id="frmLogin:password"]', senha)
    site.locator('xpath=//*[@id="frmLogin:loginButton"]').click()
    time.sleep(0.2)


def abrir_arquivo(nome):
    with open(nome) as file:
        arquivo = file.read().replace(",", ' ').split()
    return arquivo


def validar_se_da_para_ver_elemento(caminho_elemento_xpath):
    print("Validando se da pra ver elemento...")
    da_para_ver = False
    contador_validar_se_da_para_ver_elemento = 0
    while not da_para_ver:
        try:
            contador_validar_se_da_para_ver_elemento += 1
            if contador_validar_se_da_para_ver_elemento >= 31:
                site.close()
                return 'Error'
            da_para_ver = site.locator(f'xpath={caminho_elemento_xpath}').is_visible()
            if not da_para_ver:
                print("Não deu, tentando de novo...")
                time.sleep(0.5)
            if da_para_ver:
                print("Deu certo a validação da pra ver elemento...")
                # //*[@id="pesquisarClientes:cnpj"]
                validar_se_ja_ta_na_aba_cliente = site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody'
                                                               '/tr/td[2]/div/table[1]/tbody/tr[1]/td/form'
                                                               '/table[1]/tbody/tr/td[1]/input').is_visible()
                if validar_se_ja_ta_na_aba_cliente:
                    validar_se_preencheu = site.locator(
                        'xpath=//*[@id="pesquisarClientes:cnpj"]').input_value()
                    if not validar_se_preencheu:
                        #########
                        return da_para_ver
                if not validar_se_ja_ta_na_aba_cliente:
                    break
        except ValueError:
            continue
    return da_para_ver


def inserir_no_arquivo(conteudo, arquivo):
    try:  # validar se o arquivo existe
        f = open(arquivo)
        f.close()
        with open(arquivo, 'w') as arquivo:
            arquivo.write("\n".join(conteudo))
    except ValueError:
        print('O arquivo de cache não existe!, criando')
        with open(arquivo, 'w') as arquivo:
            arquivo.write("\n".join(conteudo))


def validar_listas(cliente, liberar=False):
    matriz = cliente in lista_matrizes
    filial = cliente in lista_filiais
    nao_cliente = cliente in lista_nao_clientes
    condicao = str(cliente) in abrir_arquivo('cnpjs_filial.txt')
    condicao2 = str(cliente) in abrir_arquivo('cnpjs_nao_cliente.txt')
    condicao3 = str(cliente) in abrir_arquivo('cnpjs_com_distribuidor_cadastrado.txt')
    condicao4 = str(cliente) in abrir_arquivo('cnpjs_matrizes.txt')
    if any([condicao3, matriz, filial, nao_cliente]):
        return True
    if liberar:
        if not any([condicao, condicao2,
                    condicao3]):
            return False
    if any([condicao, condicao2,
            condicao3, condicao4]):
        return True
    else:
        return False


def get_filiais():
    site.locator('xpath=//*[@id="administrarCliente:tabFiliais_cell"]').click()  # clicar na aba filiais
    for i in range(1, 11):  # 10 tentativas para ver se é falso ou nao
        print(f"Tentativa numero {i} de ver a aba filiais")
        eh_visivel_contar_filiais = site.locator(
            'xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody/tr[1]/td/form'
            '/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[1]/td/div'
            '/div/table/tbody/tr[1]').is_visible()
        if eh_visivel_contar_filiais:
            break
        if not eh_visivel_contar_filiais:
            time.sleep(0.5)
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
                filial = remover_string(filial)
                validacao_filial = validar_listas(
                    int(filial))  # validar se a filial ja esta na lista das filiais
                if not validacao_filial:
                    if not validar_listas(int(filial)):
                        with io.open('cnpjs_filial.txt',
                                     'a', encoding='utf-8') as file:
                            file.write(f'{int(filial)}\n')
                    lista_filiais.append(int(filial))
                if validacao_filial:
                    continue
            except ValueError:
                continue
        return
    else:
        print("Nenhuma filial encontrada, saindo da aba filial...")
        return


def remover_string(valor):
    valor = re.sub('[^0-9]', '', valor)
    return int(valor)


def verificar_chat(site_verificar_chat):
    return site_verificar_chat.locator('xpath=/html/body/jdiv/jdiv/jdiv[3]/jdiv[1]/jdiv/jdiv').is_visible()


def resolver_zeros(numero):
    numero_str = str(numero)
    zeros = 14 - len(numero_str)
    if zeros > 0:
        return numero * (10 ** zeros)
    else:
        return numero


def comparar_se_cliente_cote(cliente):
    contador = 0
    contador2 = 0
    while True:
        try:
            linha_cliente_ver = site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]'
                                             '/div/table[1]/tbody/tr[1]/td/form/table[2]/tbody/tr[3]/td/div'
                                             '/div[2]/div/div/table/tbody/tr').is_visible()
            for i in range(1, 4):
                if not linha_cliente_ver:
                    print(f"Não deu pra ver se é cliente cotefacil ou não, tentando de novo, tentativa {i} de 3...")
                    time.sleep(3.5)
                    linha_cliente_ver = site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]'
                                                     '/div/table[1]/tbody/tr[1]/td/form/table[2]/tbody/tr[3]/td/div'
                                                     '/div[2]/div/div/table/tbody/tr').is_visible()
                if linha_cliente_ver:
                    print("Deu certo a validação é cliente cotefacil sim...")
                    return linha_cliente_ver
            return linha_cliente_ver
        except ValueError:
            time.sleep(1)
            contador += 1
            if contador == 1:  # 10
                try:
                    loading = validar_se_da_pra_ver_loading()
                    if not loading:
                        site.locator('xpath=//*[@id="pesquisarClientes:btnPesquisar"]').click()
                        contador = 0
                        contador2 += 1
                        if contador2 == 2:
                            comparar_cliente_linha_cliente(cliente, validar_se_e_cliente_cote=False)
                            return True
                except ValueError:
                    continue


def comparar_cliente_linha_cliente(cliente, validar_se_e_cliente_cote=True):
    print("Inicio da comparação cliente linha cliente...")
    time.sleep(2)
    contador_cnpj_faltando_numero = 0
    while True:
        if validar_se_e_cliente_cote:
            linha_cliente_ver = comparar_se_cliente_cote(cliente)
            if linha_cliente_ver:
                try:
                    contador_cnpj_faltando_numero += 1
                    if contador_cnpj_faltando_numero >= 10:  # Cnpj que esteja aparecendo for diferente do pesquisado
                        return True
                    time.sleep(2)
                    linha_cliente = site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]'
                                                 '/div/table[1]/tbody/tr[1]/td/form/table[2]/tbody/tr[3]/td/div'
                                                 '/div[2]/div/div/table/tbody/tr').text_content()
                    linha_cliente = linha_cliente.split()[0]
                    linha_cliente = remover_string(linha_cliente)
                    if int(cliente) == int(linha_cliente):
                        return True
                except ValueError:
                    linha_cliente_err = site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]'
                                                     '/div/table[1]/tbody/tr[1]/td/form/table[2]/tbody/tr[3]/td/div'
                                                     '/div[2]/div/div/table/tbody/tr').count()
                    if linha_cliente_err != 1:
                        linha_cliente = site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]'
                                                     '/div/table[1]/tbody/tr[1]/td/form/table[2]/tbody/tr[3]/td/div'
                                                     '/div[2]/div/div/table/tbody/tr[1]').text_content()
                        linha_cliente = linha_cliente.split()[0]
                        linha_cliente = remover_string(linha_cliente)
                        if int(cliente) == int(linha_cliente):
                            return True
                        else:
                            linha_cliente = resolver_zeros(linha_cliente)
                            cliente = resolver_zeros(cliente)
                            if cliente == linha_cliente:
                                return True
                            else:
                                linha_cliente2 = site.locator(
                                    'xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]'
                                    '/div/table[1]/tbody/tr[1]/td/form/table[2]/tbody/tr[3]/td'
                                    '/div/div[2]/div/div/table/tbody/tr[2]').text_content()
                                linha_cliente2 = linha_cliente2.split()[0]
                                linha_cliente2 = remover_string(linha_cliente2)
                                if int(cliente) == int(linha_cliente2):
                                    return True
                                else:
                                    linha_cliente2 = resolver_zeros(linha_cliente2)
                                    cliente = resolver_zeros(cliente)
                                    if cliente == linha_cliente2:
                                        return True
                    if linha_cliente_err == 1:
                        return False
            if not linha_cliente_ver:
                return False
        if not validar_se_e_cliente_cote:
            try:
                time.sleep(0.2)
                linha_cliente = site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]'
                                             '/div/table[1]/tbody/tr[1]/td/form/table[2]/tbody/tr[3]/td/div'
                                             '/div[2]/div/div/table/tbody/tr').text_content()
                linha_cliente = linha_cliente.split()[0]
                linha_cliente = remover_string(linha_cliente)
                if int(cliente) == int(linha_cliente):
                    return True
            except ValueError:
                linha_cliente_err = site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]'
                                                 '/div/table[1]/tbody/tr[1]/td/form/table[2]/tbody/tr[3]/td/div'
                                                 '/div[2]/div/div/table/tbody/tr').count()
                if linha_cliente_err != 1:
                    linha_cliente = site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]'
                                                 '/div/table[1]/tbody/tr[1]/td/form/table[2]/tbody/tr[3]/td/div'
                                                 '/div[2]/div/div/table/tbody/tr[1]').text_content()
                    linha_cliente = linha_cliente.split()[0]
                    linha_cliente = remover_string(linha_cliente)
                    if int(cliente) == int(linha_cliente):
                        return True
                    else:
                        linha_cliente = resolver_zeros(linha_cliente)
                        cliente = resolver_zeros(cliente)
                        if cliente == linha_cliente:
                            return True
                        else:
                            linha_cliente2 = site.locator(
                                'xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]'
                                '/div/table[1]/tbody/tr[1]/td/form/table[2]/tbody/tr[3]/td'
                                '/div/div[2]/div/div/table/tbody/tr[2]').text_content()
                            linha_cliente2 = linha_cliente2.split()[0]
                            linha_cliente2 = remover_string(linha_cliente2)
                            if int(cliente) == int(linha_cliente2):
                                return True
                            else:
                                linha_cliente2 = resolver_zeros(linha_cliente2)
                                cliente = resolver_zeros(cliente)
                                if cliente == linha_cliente2:
                                    return True
                                else:
                                    caminho_do_input = '//*[@id="pesquisarClientes:cnpj"]'
                                    da_pra_ver = validar_se_da_para_ver_elemento(caminho_do_input)
                                    if da_pra_ver:
                                        site.locator('xpath=//*[@id="pesquisarClientes:btnPesquisar"]').click()


def clicar_aba_inicio():
    print("Clicando na aba de inicio...")
    caminho_imagem_aba_inicio = '/html/body/table/tbody/tr[1]/td/div/form[2]/ul/li[1]/a/img'
    caminho_conteudo_aba_inicio = '//*[@id="esConteudo"]'
    da_para_ver = validar_se_da_para_ver_elemento(caminho_imagem_aba_inicio)
    if da_para_ver:  # validar se da pra ver imagem aba inicio
        site.locator('xpath=/html/body/table/tbody/tr[1]/td/div/form[2]/ul/li[1]').click()  # clicar na aba inicio
        time.sleep(1)
        while True:
            print("Validando se da pra ver aba de inicio...")
            da_para_ver = validar_se_da_para_ver_elemento(caminho_conteudo_aba_inicio)
            if da_para_ver:
                return


def clicar_aba_cliente():
    print("Clicando na aba cliente...")
    caminho_imagem_aba_clientes = '/html/body/table/tbody/tr[1]/td/div/form[2]/ul/li[2]/a/img'
    caminho_botao_liberacao_aba_cliente = '/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]' \
                                          '/tbody/tr[1]/td/form/table[1]/tbody/tr/td[1]/input'
    da_para_ver = validar_se_da_para_ver_elemento(caminho_imagem_aba_clientes)
    if da_para_ver:  # validar se da pra ver imagem aba clientes
        site.locator('xpath=/html/body/table/tbody/tr[1]/td/div/form[2]/ul/li[2]').click()  # clicar na aba clientes
        time.sleep(0.5)
        da_para_ver1 = validar_se_da_para_ver_elemento(caminho_botao_liberacao_aba_cliente)
        if da_para_ver1:
            return


def reiniciar_a_tela(liberar=False):
    if not liberar:
        print("Reiniciando a tela...")
        clicar_aba_inicio()
        clicar_aba_cliente()
    if liberar:
        print("Reiniciando a tela...")
        clicar_aba_inicio()
    return


def validar_se_da_pra_ver_loading():
    caminho = '//*[@id="loadMessageFirstHref"]'
    contador_exception_loading = 0
    if contador_exception_loading >= 8:  # 8 tentativar
        site.close()
        return 'Error_close'
    da_para_ver = True
    while da_para_ver:
        try:
            da_para_ver = site.locator(f'xpath={caminho}').is_visible()
            if da_para_ver:
                time.sleep(0.5)
            if not da_para_ver:
                break
        except ValueError:
            contador_exception_loading += 1
            continue
    return da_para_ver


def validar_se_da_pra_ver_erro(caminho_elemento_xpath):
    time.sleep(0.5)
    da_para_ver = site.locator(f'xpath={caminho_elemento_xpath}').is_visible()
    if not da_para_ver:
        time.sleep(0.5)
        return da_para_ver
    if da_para_ver:
        return da_para_ver


def dentro_aba_cliente(cliente):
    caminho_erro = '/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody/tr[1]/td/form/span' \
                   '/div/div/table/tbody/tr/td/table/tbody/tr/td[2]/table'
    time.sleep(1)
    validar_se_checkbox_ta_on = site.locator('xpath=//*[@id="pesquisarClientes:mostrarFiliais"]').is_checked()
    if not validar_se_checkbox_ta_on:
        site.locator('xpath=//*[@id="pesquisarClientes:mostrarFiliais"]').click()
    site.fill('xpath=//*[@id="pesquisarClientes:cnpj"]', str(cliente))
    time.sleep(2)
    site.locator('xpath=//*[@id="pesquisarClientes:btnPesquisar"]').click()  # clicar em pesquisar
    while True:
        time.sleep(1)
        site.locator('xpath=//*[@id="pesquisarClientes:btnPesquisar"]').click()  # clicar em pesquisar
        deu_erro = validar_se_da_pra_ver_erro(caminho_erro)
        if deu_erro:
            reiniciar_a_tela(cliente)
            time.sleep(0.5)
            validacao_cliente_cotefacil = dentro_aba_cliente(cliente)
            if validacao_cliente_cotefacil:  # posivel erro caso não seja cliente
                return True
            if not validacao_cliente_cotefacil:
                return False

        comparacao = comparar_cliente_linha_cliente(cliente)
        if comparacao:
            load = validar_se_da_pra_ver_loading()  # validar se da pra ver o loading
            if not load:
                try:
                    site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody'
                                 '/tr/td[2]/div/table[1]/tbody/tr[1]/td/form/table[2]'
                                 '/tbody/tr[3]/td/div/div[2]/div/div/table/tbody/tr'
                                 '/td[4]/input').click(timeout=60000)  # clicar no editar
                    time.sleep(0.5)
                    return True
                except ValueError:
                    site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]'
                                 '/tbody/tr[1]/td/form/table[2]/tbody/tr[3]/td/div/div[2]/div/div'
                                 '/table/tbody/tr[1]/td[4]/input').click(timeout=60000)  # clicar no editar
                    time.sleep(0.5)
                    return True
        if not comparacao:
            print(f"Cliente {cliente} não cadastrado na cotefacil.")
            return False


def organizar_listas():
    while True:
        try:
            print("Logado ...")
            nome_arquivo = 'JMF.txt'
            arquivo = abrir_arquivo(nome_arquivo)  # abrir arquivo
            caminho_botao_ativar_inativar = '/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]' \
                                            '/tbody/tr[1]/td/form/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]' \
                                            '/td/table/tbody/tr/td/input'
            for cliente in arquivo:  # percorrer a lista de clientes (arquivo)
                mega_validacao = len(cliente)
                if mega_validacao >= 10:
                    cliente = cliente
                    cliente = int(cliente.translate(str.maketrans('', '', string.punctuation)))
                    validacao = validar_listas(cliente)
                    if not validacao:
                        # time.sleep(4)
                        validacao_chat = verificar_chat(site)
                        if validacao_chat:
                            site.locator('xpath=/html/body/jdiv/jdiv/jdiv[3]/jdiv[1]/jdiv/jdiv').click()
                            time.sleep(1)
                        print(f"Processando cliente {cliente} ...")
                        caminho_botao_liberacao_aba_cliente = '/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]' \
                                                              '/div/table[1]/tbody/tr[1]/td/form/table[1]/tbody/tr' \
                                                              '/td[1]/input'

                        ja_ta_dentro = site.locator(f'xpath={caminho_botao_liberacao_aba_cliente}').is_visible()
                        if not ja_ta_dentro:
                            clicar_aba_cliente()
                        validacao_cliente_cotefacil = dentro_aba_cliente(cliente)
                        if validacao_cliente_cotefacil:
                            da_para_ver_botao_ativar_inativar = validar_se_da_para_ver_elemento(
                                caminho_botao_ativar_inativar)
                            if da_para_ver_botao_ativar_inativar:
                                input_matriz = site.locator(
                                    'xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]'
                                    '/tbody/tr[1]/td/form/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td'
                                    '/table/tbody/tr/td/div/div[2]/table/tbody/tr[2]/td[2]/input').input_value()
                                if not input_matriz:
                                    validacao_matriz_1 = validar_listas(int(cliente))
                                    if not validacao_matriz_1:
                                        with io.open('cnpjs_matrizes.txt',
                                                     'a', encoding='utf-8') as file:
                                            file.write(f'{int(cliente)}\n')
                                        lista_matrizes.append(
                                            int(cliente))  # Cnpj não possui matriz setada (matriz)
                                    print(f"Pegando as filiais do cnpj {cliente}")
                                    get_filiais()
                                    reiniciar_a_tela()
                                else:
                                    print("É matriz, ver se tem filiais...")

                                    if not validar_listas(int(cliente)):
                                        with io.open('cnpjs_filial.txt',
                                                     'a', encoding='utf-8') as file:
                                            file.write(f'{int(cliente)}\n')

                                    lista_filiais.append(int(cliente))  # colocando a filial na lista filiais

                                    if not validar_listas(int(input_matriz)):
                                        with io.open('cnpjs_matrizes.txt',
                                                     'a', encoding='utf-8') as file:
                                            file.write(f'{input_matriz}\n')

                                        lista_matrizes.append(
                                            int(input_matriz))  # Cnpj possui matriz setada (filial)

                                    reiniciar_a_tela()
                                    time.sleep(0.5)
                                    if not validar_listas(int(input_matriz)):
                                        print(f"Logando na matriz...{input_matriz}")
                                        dentro_aba_cliente(input_matriz)
                                        print("Pegando as filiais da matriz...")
                                        get_filiais()
                                    reiniciar_a_tela()
                        if not validacao_cliente_cotefacil:

                            if not validar_listas(int(cliente)):
                                with io.open('cnpjs_nao_cliente.txt',
                                             'a', encoding='utf-8') as file:
                                    file.write(f'{int(cliente)}\n')

                            lista_nao_clientes.append(int(cliente))
                            reiniciar_a_tela()
                            continue
                    if validacao:
                        continue
                if mega_validacao < 10:
                    print('Cliente não considerado por ter menos de 10 caracteres')
                    lista_nao_clientes.append(cliente)

                    with io.open('cnpjs_nao_cliente.txt',
                                 'a', encoding='utf-8') as file:
                        file.write(f'{int(cliente)}\n')

            now_time = datetime.now()
            fim = now_time.strftime("%H:%M:%S")
            print('Fim do processo: ', fim)
            return True
        except ValueError:
            print('Travou o processo, continuando.')
            site.goto('https://sistemas.cotefacil.com/CTFLLogan-webapp/login.jsf')
            continue


def liberar_fornecedor(lista_matriz):
    for cliente in lista_matriz:
        if not validar_listas(cliente, liberar=True):
            reiniciar_a_tela(liberar=True)
            site.fill('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody/tr[4]/td/form'
                      '/table/tbody/tr[1]/td/div/div[2]/table/tbody/tr[2]/td[2]/input', cliente)
            validacao_chat = verificar_chat(site)
            if validacao_chat:
                site.locator('xpath=/html/body/jdiv/jdiv/jdiv[3]/jdiv[1]/jdiv/jdiv').click()
                time.sleep(1)
            site.locator('xpath=//*[@id="pesquisarUsuarios:btnPesquisar"]').click()
            time.sleep(1.5)
            editar = site.locator(
                'xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody/tr[4]'
                '/td/form/table/tbody/tr[3]/td/div/div[2]/table/tbody/tr').count()
            try:
                if editar != 1 and editar > 0:
                    site.locator(
                        'xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody/tr[4]'
                        '/td/form/table/tbody/tr[3]/td/div/div[2]/table/tbody/tr[1]/td[6]/a').click()
                if editar == 1:
                    site.locator(
                        'xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody/tr[4]'
                        '/td/form/table/tbody/tr[3]/td/div/div[2]/table/tbody/tr/td[6]/a').click()
            except ValueError:
                site.locator('xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody/tr[4]'
                             '/td/form/table/tbody/tr[3]/td/div/div[2]/table/tbody/tr[1]/td[6]/a').click()
            site.locator(
                'xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody/tr[1]/td/form'
                '/table/tbody/tr[2]/td/div/div/table/tbody/tr[1]/td/table/tbody/tr/td[8]/table/tbody/tr/td[2]'
                '/table/tbody/tr/td/table/tbody/tr/td[2]').click()  # aba fornecedor
            time.sleep(0.5)
            loading = validar_se_da_pra_ver_loading()
            if not loading:
                check_box_filiais = '//*[@id="administrarCliente:chkTodasFiliais"]'
                check_box_compradores = '//*[@id="administrarCliente:chkTodosCompradores"]'
                validar_se_checkbox_filiais_e_visivel = site.locator(f'xpath={check_box_filiais}').is_visible()
                if validar_se_checkbox_filiais_e_visivel:
                    validar_se_checkbox_filiais_ta_checada = site.locator(
                        f'xpath={check_box_filiais}').is_checked()
                    if not validar_se_checkbox_filiais_ta_checada:
                        site.locator(f'xpath={check_box_filiais}').click()
                validar_se_checkbox_compradores_ta_checada = site.locator(
                    f'xpath={check_box_compradores}').is_checked()
                if not validar_se_checkbox_compradores_ta_checada:
                    site.locator(f'xpath={check_box_compradores}').click()
                select_element = site.locator(
                    'xpath=/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table[1]/tbody'
                    '/tr[1]/td/form/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/table/tbody'
                    '/tr/td/div[2]/div[2]/span[1]/select')
                select_handle = select_element.element_handle()
                opcao_desejada = select_handle.query_selector('option[value="7983"]')

                if not opcao_desejada:
                    fornecedor = '20069042000196 - JMF - SP'
                    representante = '122360 - On-line - no-reply@cotefacil.com'
                    site.fill('xpath=//*[@id="administrarCliente:fornecedor"]', fornecedor)
                    site.fill('xpath=//*[@id="administrarCliente:sggRepresentante"]', representante)
                    element = site.query_selector('input[type="button"][value="Adicionar"]')
                    element.click()
                    time.sleep(1)
                    print(f'cliente: {cliente} - OK')
                    with io.open('cnpjs_com_distribuidor_cadastrado.txt',
                                 'a', encoding='utf-8') as file:
                        file.write(f'{cliente}\n')
                if opcao_desejada:
                    if not validar_listas(int(cliente)):
                        with io.open('cnpjs_com_distribuidor_cadastrado.txt',
                                     'a', encoding='utf-8') as file:
                            file.write(f'{cliente}\n')
    print("final do processo")


with sync_playwright() as p:
    navegador = p.firefox.launch(
        headless=False)  # por padrão esse modo é headless = True (não mostra o navegador abrindo)
    site = navegador.new_page()
    site.goto('https://sistemas.cotefacil.com/CTFLLogan-webapp/login.jsf')

    now = datetime.now()
    inicio = now.strftime("%H:%M:%S")
    print('Inicio do processo: ', inicio)
    try:
        autenticar()
        lista = abrir_arquivo("teste_excluir.txt")
        liberar_fornecedor(lista)
    except Exception as Error:
        site.close()
        print(Error)
