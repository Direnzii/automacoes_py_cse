from playwright.sync_api import sync_playwright
import time

url = 'https://cnpj.biz/'

def abrir_arquivo(arquivo):
    with open(arquivo) as file:
        arquivo = file.read().replace(",", ' ').split()
    return arquivo

def get_atividades(count):


    site.locator('xpath=/html/body/div[1]/div/div/div[2]/div[1]/div[5]/div/span/b/u').count()


def get_tipo(count):
    for i_tipo in range(1, count + 1):
        tipo_val = site.locator(f'xpath=/html/body/div[1]/div/div/div[2]/div[1]/p[{i_tipo}]').text_content()
        tipo_val = tipo_val.split(':')[0]
        if i_tipo >= count:
            tipo = 'Não foi encontrado tipo'
            return tipo
        if tipo_val != 'Tipo':
            continue
        if tipo_val == 'Tipo':
            tipo = site.locator(f'xpath=/html/body/div[1]/div/div/div[2]/div[1]/p[{i_tipo}]/div/b').text_content()
            return tipo

def get_ie(cnpjs):
    IE = ''
    tipo = ''
    atividades = ''
    for cnpj in cnpjs:
        site.goto(url + cnpj)
        count = site.locator('xpath=/html/body/div[1]/div/div/div[2]/div[1]/p').count()
        if count == 0:
            print(cnpj, ' - Não encontrado no CNPJ.BIZ')
        else:
            for i_ie in range(1, count + 1):
                IE_val = site.locator(f'xpath=/html/body/div[1]/div/div/div[2]/div[1]/p[{i_ie}]').text_content()
                IE_val = IE_val.split(':')[0]
                if i_ie >= count:
                    IE = 'Nenhum registro de IE encontrado'
                    tipo = get_tipo(count)
                    # atividades = get_atividades(count)
                    break
                if IE_val != 'Inscrição Estadual RS':
                    continue
                if IE_val == 'Inscrição Estadual SP':
                    IE = site.locator(f'xpath=/html/body/div[1]/div/div/div[2]/div[1]/p[{i_ie}]/div/b').text_content()
                    tipo = get_tipo(count)
                    # atividades = get_atividades(count)
                break
        print(cnpj, ' - ', IE, ' - ', tipo)

def get_infos(site):
    # arquivo_nome = input('Qual o nome do arquivo que contem os cnpjs válidos ?: ')
    cnpjs = abrir_arquivo('forn.txt')
    get_ie(cnpjs)

with sync_playwright() as p:
    navegador = p.firefox.launch(headless=False)
    site = navegador.new_page()
    get_infos(site)