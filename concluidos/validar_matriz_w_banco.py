import datetime
import oracledb
import os
import io


def hora():
    now = datetime.datetime.now().time()
    return now.strftime("%H:%M:%S")


def consultar_base_cliente_matriz():
    usr = os.getenv(key='USER_ORACLE_OFICIAL')
    psswrd = os.getenv(key='SENHA_ORACLE_OFICIAL')
    dns_port_SID = os.getenv(key='DNS_ORACLE_OFICIAL')

    connection = oracledb.connect(user=usr, password=psswrd,
                                  dsn=dns_port_SID)
    cursor = connection.cursor()

    query_origin = """select distinct cli.cnpj, cli.ativo from cliente cli
                        where cli.idmatriz is null and cli.tipo = 'M'
                        and length(cli.cnpj) >= 12"""

    cursor.execute(query_origin)
    result = cursor.fetchall()

    dict_banco = {}
    for cli, ativo in result:
        dict_banco[int(cli)] = ativo
    return dict_banco


def abrir_arquivo(caminho):
    with open(caminho) as file:
        arquivo = file.read().replace(",", ' ').split()
    return arquivo


def validar_removendo_caracteres(cnpj_para_ser_validado, dict_banco):
    for i in cnpj_para_ser_validado:
        if int(cnpj_para_ser_validado) in dict_banco:
            if dict_banco[int(cnpj_para_ser_validado)] == 0:  # mesmo depois de remover, se for inativo, desconsiderar
                return False
            else:
                return True  # essa primeiro validação mantive mais por desencargo
        if len(cnpj_para_ser_validado) <= 11:  # considerado não cliente e excluido
            return False
        cnpj_para_ser_validado = cnpj_para_ser_validado[:-1]  # - ultimo digito
    return False


def considerar_matriz(cnpj):
    lista_matrizes.append(cnpj)
    with io.open('cnpj_matriz.txt', 'a', encoding='utf-8') as file:
        file.write(f'{cnpj}\n')
        print(f"{cnpj}: OK")


def nao_considerado_matriz(cnpj):
    print(f"{cnpj}: X")


def comparar_listas():
    lista_arquivo = abrir_arquivo("teste_excluir.txt")
    dict_banco = consultar_base_cliente_matriz()
    # lista_arquivo = ['0083754590001550', '928638000014700', '0083754590001810', '52405391992643', '26917288624363']

    for cnpj in lista_arquivo:
        if int(cnpj) in dict_banco:  # primeira verificação se o cnpj esta na lista do banco
            considerar_matriz(cnpj)
        else:
            if validar_removendo_caracteres(cnpj, dict_banco):  # aqui eu verifico de forma mais especifica
                considerar_matriz(cnpj)
            else:
                nao_considerado_matriz(cnpj)


lista_matrizes = []
print('Inicio: ', hora())
comparar_listas()
print('Fim: ', hora())