import json


def dump_para_arquivo_falta(arquivo, novo_arquivo):
    with open(arquivo, 'r') as arquivo:
        contador = 0
        saida = '1;<CNPJ_CLIENTE>;3.3\n'
        for linha in arquivo:
            try:
                codigo_produto = linha.split()[0]
                ean = linha.split()[1]
            except:
                continue
            descricao_lista = linha.split()[2::]
            descricao = ' '.join(descricao_lista)
            contador += 1
            saida += f'2;{ean};1;{codigo_produto};{descricao};.;0\n'
        saida += f'9;{contador}'
        print(saida)
        with open(f'{novo_arquivo}', 'w') as arquivo:
            arquivo.write(saida)


def json_para_arquivo_de_falta(arquivo, novo_arquivo):
    with open(arquivo, 'r') as arquivo:
        file = json.load(arquivo)
        clientes = file.get('clientes')
        itens = clientes[0]
        cnpj_cliente = itens['cnpj_cliente']
        itens_dict = itens['itens']
        saida = f'1;{cnpj_cliente};3.3\n'
        for item in itens_dict:
            ean = item['ean']
            codigo_produto = item['codigo_produto']
            descricao = item['descricao_produto']
            quantidade_cotada = item['quantidade_cotada']
            saida += f'2;{ean};{quantidade_cotada};{codigo_produto};{descricao};.;0\n'
        saida += f'9;{len(itens)}'
        print(saida)
        with open(f'{novo_arquivo}', 'w') as arquivo_falta:
            arquivo_falta.write(saida)