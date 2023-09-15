import datetime
import oracledb
import os
import io


def hora():
    now = datetime.datetime.now().time()
    return now.strftime("%H:%M:%S")


def conectar_ao_banco():
    user = os.getenv('ORACLE_USER')
    password = os.getenv('ORACLE_PASSWORD')
    host = os.getenv('ORACLE_HOST')
    port = os.getenv('ORACLE_PORT')
    db_name = os.getenv('ORACLE_DB_NAME')

    connection = oracledb.connect(
        user=user,
        password=password,
        dsn=f"{host}:{port}/{db_name}"
    )
    cursor = connection.cursor()
    return cursor


def transformar_cnpjs_em_consultavel(lista_filiais):
    saida = ', '.join(f"'{cnpj}'" for cnpj in lista_filiais)  # aqui eu uso a função join para concatenar os cnpj
    return saida


def consultar_base_cliente_matriz(cursor, lista_filiais=None, get_matriz_from_filial=False):
    if not get_matriz_from_filial:
        query_origin = """select distinct cli.cnpj, cli.ativo from cliente cli
                            where cli.idmatriz is null and cli.tipo = 'M'
                            and length(cli.cnpj) >= 12"""

        cursor.execute(query_origin)
        result = cursor.fetchall()

        dict_banco = {}
        for cli, ativo in result:
            dict_banco[int(cli)] = ativo
            # check = len(dict_banco)  # apenas para validar no banco (var sem uso)
        return dict_banco
    if get_matriz_from_filial:
        consulta_filial = transformar_cnpjs_em_consultavel(lista_filiais)
        query_get_matriz = f"""select cli_1.cnpj from cliente cli_1 where cli_1.id in 
                                (select cli.idmatriz from cliente cli
                                where cli.tipo = 'F'
                                and length(cli.cnpj) >= 12
                                and cli.cnpj in ({consulta_filial}))
                                and cli_1.tipo = 'M'
                                and length(cli_1.cnpj) >= 12
                                and cli_1.ativo = 1"""  # select da validacao matriz_filial
        cursor.execute(query_get_matriz)
        result = cursor.fetchall()
        matrizes_das_filiais = []
        for cnpj in result:
            matrizes_das_filiais.append(cnpj[0])
        return matrizes_das_filiais


def tranformar_em_inteiros(lista):
    lista_int = []
    for i in lista:
        lista_int.append(int(i))
    return lista_int


def abrir_arquivo(caminho):
    try:
        with open(caminho) as file:
            arquivo = file.read().replace(",", ' ').split()
    except Exception as error_file:
        print("Arquivo com cnpjs não encontrado: ", error_file)
        return 'Error'
    return arquivo


def validar_removendo_caracteres(cnpj_para_ser_validado, dict_banco):
    for _ in cnpj_para_ser_validado:
        if int(cnpj_para_ser_validado) in dict_banco:
            if dict_banco[int(cnpj_para_ser_validado)] == 0:  # mesmo depois de remover, se for inativo, desconsiderar
                return False
            else:
                return True  # essa primeiro validação mantive mais por desencargo
        if len(cnpj_para_ser_validado) <= 11:  # considerado não cliente e excluido
            return False
        cnpj_para_ser_validado = cnpj_para_ser_validado[:-1]  # - ultimo digito
    return False


def considerar_matriz(cnpj, validar_matrizes_de_filiais=False):
    arquivo_validacao = abrir_arquivo('cnpj_matriz.txt')

    if not validar_matrizes_de_filiais:
        lista_matrizes.append(cnpj)
        if arquivo_validacao == 'Error':
            with io.open('cnpj_matriz.txt', 'a', encoding='utf-8') as file:
                file.write(f'{cnpj}\n')
                print(f"{cnpj}: OK")
        else:
            if cnpj not in arquivo_validacao:
                with io.open('cnpj_matriz.txt', 'a', encoding='utf-8') as file:
                    file.write(f'{cnpj}\n')
                    print(f"{cnpj}: OK")

    if validar_matrizes_de_filiais:
        if cnpj not in arquivo_validacao:  # primeira verificação se o cnpj esta na lista das ja consideradas matriz
            considerar_matriz(cnpj)
        lista_full_int = tranformar_em_inteiros(arquivo_validacao)
        if not int(cnpj) in lista_full_int:  # segunda verificacao com inteiros
            considerar_matriz(cnpj)
        else:
            if not validar_removendo_caracteres(cnpj, arquivo_validacao):
                considerar_matriz(cnpj)
            else:
                nao_considerado_matriz(cnpj)


def nao_considerado_matriz(cnpj):
    lista_nao_considerados.append(cnpj)
    print(f"{cnpj}: X")


def pegar_matrizes_das_filiais(cursor_oracle_get, lista_matrizes_filiais):
    matrizes_das_filiais = consultar_base_cliente_matriz(cursor_oracle_get, lista_matrizes_filiais,
                                                         get_matriz_from_filial=True)
    for cnpj_matriz_by_filial in matrizes_das_filiais:
        considerar_matriz(cnpj_matriz_by_filial, validar_matrizes_de_filiais=True)


def comparar_listas(nome_arquivo):
    lista_arquivo = abrir_arquivo(nome_arquivo)
    if lista_arquivo == 'Error':
        return
    else:
        cursor_oracle_comp = conectar_ao_banco()
        dict_banco = consultar_base_cliente_matriz(cursor_oracle_comp)
    for cnpj in lista_arquivo:
        if int(cnpj) in dict_banco:  # primeira verificação se o cnpj esta na lista do banco
            considerar_matriz(cnpj)
        else:
            if validar_removendo_caracteres(cnpj, dict_banco):  # aqui eu verifico de forma mais especifica
                considerar_matriz(cnpj)
            else:
                nao_considerado_matriz(cnpj)
    return cursor_oracle_comp  # final do processo de pegar as matrizes a partir da comparação com o banco


lista_matrizes = []
lista_nao_considerados = []
print('Inicio: ', hora())
cursor_oracle = comparar_listas("cnpjs_para_validar.txt")
pegar_matrizes_das_filiais(cursor_oracle, lista_nao_considerados)
print('Fim: ', hora())
