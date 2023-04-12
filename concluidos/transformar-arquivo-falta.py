import json
import sys
import time


class ConversorArquivoDeFalta:

    def dump_para_arquivo_falta(self, arquivo, novo_arquivo):
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
            with open(f'{novo_arquivo}', 'w') as arquivo:
                arquivo.write(saida)

    def json_para_arquivo_de_falta(self, arquivo, novo_arquivo):
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

    def json_dto_para_arquivo_falta(self, arquivo, novo_arquivo):
        with open(arquivo, 'r') as arquivo:
            i = 0
            json_dict = json.load(arquivo)
            cnpj_cliente = json_dict['fornecedorDTO'].get('cnpj')
            lista_de_itens_geral = json_dict['fornecedorDTO'].get('itens', {})
            total_de_produtos = len(lista_de_itens_geral)  # numero_de_produtos

            saida = ''

            #### COMEÇO DO ARQUIVO DE FALTA ####
            saida += f'1;{cnpj_cliente};3.3\n'

            while total_de_produtos > i:
                codigo_de_barras = lista_de_itens_geral[i]['codigoDeBarras']
                descricao_do_produto = lista_de_itens_geral[i]['descricaoDoProduto']
                descricao_do_fabricante = lista_de_itens_geral[i]['descricaoDoFabricante']

                saida += f'2;{codigo_de_barras};1;{codigo_de_barras};{descricao_do_produto.upper()};{descricao_do_fabricante}\n;0'  # 0000 é o codigo do produto, não encontrei no json
                i += 1

            saida += f'9;{total_de_produtos}'

            with open(novo_arquivo, 'w') as arquivo_falta:
                arquivo_falta.write(saida)

            return saida
            #### FINAL DO ARQUIVO DE FALTA ####

    def deu_ruim(self):
        print(
            "\nComandos:\npython transformar-arquivo-falta.py 1 <nome-do-arquivo.txt> <nome-do-novo-arquivo.txt>  ---JSON do middleware para arquivo de falta\n"
            "python transformar-arquivo-falta.py 2 <nome-do-arquivo.txt> <nome-do-novo-arquivo.txt>  ---JSON DTO do crawler para arquivo de falta\n"
            "python transformar-arquivo-falta.py 3 <nome-do-arquivo.txt> <nome-do-novo-arquivo.txt>  ---Copia da base do fornecedor para arquivo de falta\n\n"
            "SELECT para o dump da base (Opção 3):\n\nselect produtorepresentante.id, produto.codbarras, produtorepresentante.descricao\n"
            "from representantefornecedor rf\ninner join fornecedor f on f.id = rf.idfornecedor\ninner join representante r on r.id = RF.IDREPRESENTANTE\n"
            "inner join conta c on c.id = r.id\ninner join contato cont on cont.id = C.IDCONTATO\ninner join produtorepresentante on produtorepresentante.idrepresentante = r.id\n"
            "inner join produto on produto.id = produtorepresentante.idproduto\nwhere R.TIPORESPOSTA <> 0 AND f.cnpj in ('66438011000166')\n"
            "and CONT.NOME like '%REPRE%' AND PRODUTOREPRESENTANTE.ATIVO = 1 AND r.ativo = 1; --- DUMP DOS PRODUTOS COM O CNPJ DO FORNECEDOR E REPRESENTANTE (OL)\n\n"
            "select pf.codprodutofornecedor, p.codbarras, pf.descricao\nfrom produtofornecedor pf\ninner join fornecedor f on f.id = pf.idfornecedor\n"
            "inner join produto p on p.id = pf.idproduto\nwhere f.cnpj = '43214055000107'\nand pf.ativo = 1\n"
            "order by F.DATAATUALIZACAO desc;  --- DUMP DOS PRODUTOS COM O CNPJ DO FORNECEDOR E REPRESENTANTE\n")


def main():
    converter = ConversorArquivoDeFalta()
    # arquivo = 'dump.txt'
    # converter.dump_para_arquivo_falta(arquivo, 'arquivo-falta.txt')
    if len(sys.argv) != 4:
        converter.deu_ruim()
        time.sleep(2)
        input("Pressione qualquer tecla para iniciar...\n**** CONVERSOR DE JSON E BASE PARA ARQUIVO DE FALTA ****")
        argumento1 = input(
            '(1) - JSON (mid) para Arquivo de falta\n(2) - JSON (DTO saida) para Arquivo de falta\n(3) - DUMP da base no modelo para Arquivo de falta\nInsira a opção: ')
        file = input("Insira o nome do arquivo JSON ou DUMP: ")  # nome do arquivo json ou dump
        nome_arquivo = input("Insira o nome do novo arquivo que o programa irá gerar: ")  # nome do arquivo novo
        if argumento1 == 1:
            converter.json_para_arquivo_de_falta(file, nome_arquivo)
        elif argumento1 == 2:
            converter.json_dto_para_arquivo_falta(file, nome_arquivo)
        elif argumento1 == 3:
            converter.dump_para_arquivo_falta(file, nome_arquivo)
        else:
            converter.deu_ruim()
    else:
        try:
            argumento1 = int(sys.argv[1])
            file = sys.argv[2]  # nome do arquivo json ou dump
            nome_arquivo = sys.argv[3]  # nome do arquivo novo
            # (1 = json do mid, 2 = DTO, 3 = dump)
            if argumento1 == 1:
                converter.json_para_arquivo_de_falta(file, nome_arquivo)
            elif argumento1 == 2:
                converter.json_dto_para_arquivo_falta(file, nome_arquivo)
            elif argumento1 == 3:
                converter.dump_para_arquivo_falta(file, nome_arquivo)
            else:
                converter.deu_ruim()
        except:
            converter.deu_ruim()
    input("Pressione qualquer tecla para iniciar...\n**** CONVERSOR DE JSON E BASE PARA ARQUIVO DE FALTA ****")
    argumento1 = input(
        '(1) - JSON (mid) para Arquivo de falta\n(2) - JSON (DTO saida) para Arquivo de falta\n(3) - DUMP da base no modelo para Arquivo de falta\nInsira a opção: ')
    file = input("Insira o nome do arquivo JSON ou DUMP: ")  # nome do arquivo json ou dump
    nome_arquivo = input("Insira o nome do novo arquivo que o programa irá gerar: ")  # nome do arquivo novo
    if argumento1 == 1:
        converter.json_para_arquivo_de_falta(file, nome_arquivo)
    elif argumento1 == 2:
        converter.json_dto_para_arquivo_falta(file, nome_arquivo)
    elif argumento1 == 3:
        converter.dump_para_arquivo_falta(file, nome_arquivo)
    else:
        converter.deu_ruim()

if __name__ == '__main__':
    main()
