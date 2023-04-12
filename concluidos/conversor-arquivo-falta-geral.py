import json
import re

arquivo = 'json.txt'

saida = '1;<CNPJ CLIENTE>;3.3\n'
# saida = ""

with open(arquivo, 'r', encoding='utf8') as file:
    try:
        arquivo_dict = json.load(file)
    except Exception as e:
        print(e)

    clientes = arquivo_dict['clientes']
    teste = clientes[0]
    clientes = teste['itens']

    contador = 0
    for item in clientes:

        ean = item.get('ean')
        codigo_produto = item.get('codigo_produto')
        if not codigo_produto:
            codigo_produto = ean
        descricao = item.get('descricao_produto')
        fabricante = item.get('Fabricante')

        saida += f'2;{ean};1;{codigo_produto};{descricao};.;0\n'

        contador += 1
    saida += f'9;{contador}'

print(saida)

with open("novo_arquivo.txt", 'w', encoding='utf8') as arquivo_falta:
    arquivo_falta.write(saida)