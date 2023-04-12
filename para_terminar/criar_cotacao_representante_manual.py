from os import getenv
from playwright.sync_api import sync_playwright
import time

xpath_ways = {'user_input_first_screen': '/html/body/table/tbody/tr[2]'
                                         '/td/table/tbody/tr/td[2]/div'
                                         '/table[1]/tbody/tr[4]/td/form'
                                         '/table/tbody/tr[1]/td/div/div[2]'
                                         '/table/tbody/tr[1]/td[2]/input',
              'button_pesquisar': '//*[@id="pesquisarUsuarios:btnPesquisar"]',
              'css_log_button_first': '#pesquisarUsuarios\:dtUsuarios\:0\:j_id101 > a:nth-child(1)',
              'build_quotation_button': '/html/body/div/div/div/div[1]/div[1]/div[1]',
              'build_quotation_inside_button': '/html/body/table/tbody/tr[2]/td/table'
                                               '/tbody/tr[1]/td[2]/div/table[1]/tbody'
                                               '/tr[15]/td/form/table/tbody/tr/td/table'
                                               '/tbody/tr[2]/td/table/tbody/tr/td/table'
                                               '/tbody/tr[2]/td[2]/div/input[1]'}


def autenticar():
    usuario = getenv(key='USUARIO_DEMO')
    senha = getenv(key='SENHA_DEMO')
    cote.fill('xpath=//*[@id="frmLogin:username"]', usuario)
    cote.fill('xpath=//*[@id="frmLogin:password"]', senha)
    cote.locator('xpath=//*[@id="frmLogin:loginButton"]').click()


def can_see(xpath_way, full_true=None):
    if full_true:
        i_can_see = cote.locator(f'xpath={xpath_way}').is_visible()
        while True:
            if not i_can_see:
                time.sleep(1)
                i_can_see = cote.locator(f'xpath={xpath_way}').is_visible()
            if i_can_see:
                return True
    i_can_see = cote.locator(f'xpath={xpath_way}').is_visible()
    return i_can_see


def handle_page():
    cote.wait_for_load_state()
    print(cote.title())


def insert_infos_and_log():
    cote.fill(f'xpath={xpath_ways["user_input_first_screen"]}', 'thiago.direnzi')
    can_see(xpath_way=xpath_ways['button_pesquisar'], full_true=True)
    cote.locator(f'xpath={xpath_ways["button_pesquisar"]}').click()
    cote.locator(f'{xpath_ways["css_log_button_first"]}').click()  # momento em que uma nova aba é aberta

    cote.context.on('page', handle_page)

    can_see(xpath_way=xpath_ways['build_quotation_button'], full_true=True)
    cote.locator(f'xpath={xpath_ways["build_quotation_button"]}').click()
    can_see(xpath_way=xpath_ways['build_quotation_inside_button'], full_true=True)


def build_quote():
    autenticar()
    can_see(xpath_way=xpath_ways['user_input_first_screen'], full_true=True)
    insert_infos_and_log()


with sync_playwright() as p:
    navegador = p.firefox.launch(
        headless=False)  # por padrão esse modo é headless = True (não mostra o navegador abrindo)
    cote = navegador.new_page()
    cote.goto('http://52.201.113.49:8084/CTFLLogan-webapp/Logout')

    try:
        build_quote()
    except Exception as e:
        pass