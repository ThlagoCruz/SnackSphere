import tkinter as tk
from tkinter import messagebox
import sqlite3
import time
import os
import pandas as pd
import numpy as np
from colorama import init, Fore, Style
import hashlib
from tabulate import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

init(autoreset=True)

def limpar():
    os.system('cls' if os.name == 'nt' else 'clear')

def colorama_print(text, color):
    colors = {
        'red': Fore.RED,
        'green': Fore.GREEN,
        'yellow': Fore.YELLOW,
        'blue': Fore.BLUE,
        'cyan': Fore.CYAN,
        'magenta': Fore.MAGENTA,
        'white': Fore.WHITE,
    }
    color_code = colors.get(color, Fore.WHITE)
    print(color_code + text + Style.RESET_ALL)

limpar()
colorama_print('''
██╗░░░░░░█████╗░░██████╗░██╗███╗░░██╗
██║░░░░░██╔══██╗██╔════╝░██║████╗░██║
██║░░░░░██║░░██║██║░░██╗░██║██╔██╗██║
██║░░░░░██║░░██║██║░░╚██╗██║██║╚████║
███████╗╚█████╔╝╚██████╔╝██║██║░╚███║
╚══════╝░╚════╝░░╚═════╝░╚═╝╚═╝░░╚══╝''', 'blue')

def check_login(usuario, senha):
    conn = sqlite3.connect('databases\data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM login WHERE nome = ? AND senha = ?', (usuario, senha))
    user = cursor.fetchone()

    conn.close()

    if user:
        print(Fore.GREEN + "Login bem-sucedido!" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Login ou senha incorretos." + Style.RESET_ALL)
        exit()

# Coleta as informações do usuário
print("Usuário:")
usr = input('$_ ')
print("Senha:")
passwd = input('$_ ')
check_login(usr, passwd)



time.sleep(0.3)
limpar()

def logo():
    colorama_print("\n░██████╗███╗░░██╗░█████╗░░█████╗░██╗░░██╗░██████╗██████╗░██╗░░██╗███████╗██████╗░███████╗\n██╔════╝████╗░██║██╔══██╗██╔══██╗██║░██╔╝██╔════╝██╔══██╗██║░░██║██╔════╝██╔══██╗██╔════╝\n╚█████╗░██╔██╗██║███████║██║░░╚═╝█████═╝░╚█████╗░██████╔╝███████║█████╗░░██████╔╝█████╗░░\n░╚═══██╗██║╚████║██╔══██║██║░░██╗██╔═██╗░░╚═══██╗██╔═══╝░██╔══██║██╔══╝░░██╔══██╗██╔══╝░░\n██████╔╝██║░╚███║██║░░██║╚█████╔╝██║░╚██╗██████╔╝██║░░░░░██║░░██║███████╗██║░░██║███████╗\n╚═════╝░╚═╝░░╚══╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚═════╝░╚═╝░░░░░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝╚══════╝", 'blue')

def menu():
    colorama_print("[01]Adicionar produto", 'blue')
    colorama_print("[02]Remover produto", 'red')
    colorama_print("[03]Adicionar fornecedor",'green')
    colorama_print("[04]Remover fornecedor", 'red')
    colorama_print("[05]Preços acima da média dos demais", 'yellow')
    colorama_print("[06]Preços abaixo da média dos demais", 'green')
    colorama_print("[07]Filtrar fornecedores sem email", 'magenta')
    colorama_print("[08]Filtrar produtos por setores", 'cyan')
    colorama_print("[09]Filtrar produtos por preço", 'yellow')
    colorama_print("[10]Filtrar produtos por marca", 'red')
    colorama_print("[11]alterar nome de usuário", 'blue')
    colorama_print("[12]alterar senha", 'cyan')
    colorama_print("[13]Importar json", 'yellow')
    colorama_print("[14]Importar csv", 'green')
    colorama_print("[15]Mostrar tabela", 'magenta')
    colorama_print("[16]Mostrar item específico em tabela", 'yellow')
    colorama_print("[17]Enviar email", 'blue')
    colorama_print("[18]Importar excel", 'green')
    colorama_print("[00]Sair", 'red')
    a = input('>_')

    if a == '01' or a == '1':
        addprod()
    elif a == '02' or a == '2':
        reprod()
    elif a == '03' or a == '3':
        addfor()
    elif a == '04' or a == '4':
        refor()
    elif a == '05' or a == '5':
        acimamedia()
    elif a == '06' or a == '6':
        abaixomedia()
    elif a == '07' or a == '7':
        filtroemail()
    elif a == '08' or a == '8':
        setores()
    elif a == '09' or a == '9':
        preco()
    elif a == '10':
        marca()
    elif a == '11':
        alterarusuario()
    elif a == '12':
        alterarsenha()
    elif a == '13':
        json()
    elif a == '14':
        csv()
    elif a == '15':
        mostrartabela()
    elif a == '16':
        especificotabela()
    elif a == '17':
        enviar()
    elif a == '18':
        excel()

def enviar():
    def enviar_email():
        usuario = entry_usuario.get()
        senha = entry_senha.get()
        destinatario = entry_destinatario.get()
        assunto = entry_assunto.get()
        corpo = text_corpo.get("1.0", tk.END)

        # Configurações do servidor SMTP do Gmail
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        try:
            # Configura a mensagem do email
            msg = MIMEMultipart()
            msg["From"] = usuario
            msg["To"] = destinatario
            msg["Subject"] = assunto
            msg.attach(MIMEText(corpo, "plain"))

            # Conecta ao servidor SMTP
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(usuario, senha)
            server.sendmail(usuario, destinatario, msg.as_string())
            server.quit()

            messagebox.showinfo("Sucesso", "Email enviado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao enviar o email: {e}")

    def quitar():
        janela.destroy()
        limpar()
        logo()
        menu()

    # Configuração da janela Tkinter
    janela = tk.Tk()
    janela.title("Enviar Email")

    tk.Label(janela, text="Usuário:").grid(row=0, column=0, padx=10, pady=5)
    entry_usuario = tk.Entry(janela, width=50)
    entry_usuario.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(janela, text="Senha:").grid(row=1, column=0, padx=10, pady=5)
    entry_senha = tk.Entry(janela, width=50, show="*")
    entry_senha.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(janela, text="Destinatário:").grid(row=2, column=0, padx=10, pady=5)
    entry_destinatario = tk.Entry(janela, width=50)
    entry_destinatario.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(janela, text="Assunto:").grid(row=3, column=0, padx=10, pady=5)
    entry_assunto = tk.Entry(janela, width=50)
    entry_assunto.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(janela, text="Corpo do Email:").grid(row=4, column=0, padx=10, pady=5)
    text_corpo = tk.Text(janela, width=50, height=10)
    text_corpo.grid(row=4, column=1, padx=10, pady=5)

    tk.Button(janela, text="Enviar", command=enviar_email).grid(row=5, column=1, padx=10, pady=10)

    tk.Button(janela, text="Sair", command=quitar).grid(row=6, column=1, padx=10, pady=5)

    janela.mainloop()

def addprod():
    with sqlite3.connect("databases/data.db") as connect:
        print("Conexão estabelecida com o banco de dados.")
        cursor = connect.cursor()

        nm = input("Insira o nome do produto: ")
        
        while True:
            try:
                pre = float(input("Insira o preço do produto: "))
                break  # Exit loop if valid input
            except ValueError:
                print("Por favor, insira um número válido para o preço.")

        cat = input("Insira a categoria do produto: ")
        marca = input("Insira a marca do produto: ")

        try:
            print("Inserindo produto...")
            cursor.execute('''
            INSERT INTO produtos (nome, categoria, preco, marca)
            VALUES (?, ?, ?, ?)
            ''', (nm, cat, pre, marca))
            print("Produto inserido com sucesso.")
        except Exception as e:
            print(f"Erro ao inserir produto. Erro: {e}")
        
        connect.commit()
        limpar()
        logo()
        menu()




def reprod():
    connect = sqlite3.connect('databases\data.db')
    cursor = connect.cursor()

    id = float(input("Insira o id do produto: "))

    try:
        connect.execute('''
        DELETE FROM produtos WHERE ID = ?
        ''', (id,))
    except Exception as e:
        colorama_print(f"Erro ao remover produto. Erro: {e}")
        input("Pressione enter para voltar ao menu")
        limpar()
        logo()
        menu()
    finally:
        connect.commit()
        connect.close()
        colorama_print(f"Produto com id {id} deletado com sucesso!", 'green')
        input("Pressione enter para voltar ao menu:")
        limpar()
        logo()
        menu()


def addfor():
    connect = sqlite3.connect('databases\data.db')
    cursor = connect.cursor()

    nm = input("Insira o nome do fornecedor: ")
    ctt = input("Insira o contato do fornecedor: ")
    email = input("Insira o email do fornecedor(opicional): ")
    estado = input("Insira o estado do fornecedor: ")
    cidade = input("Insira a cidade do fornecedor: ")
    tempo = input("Insira o tempo médio de entrega do fornecedor(em dias): ")

    try:
        cursor.execute('''
        INSERT INTO fornecedores(
            nome, contato, email, estado, cidade, tempoespera
        )
        VALUES (?, ?, ?, ?, ?, ?)
        ''',(nm, ctt, email, estado, cidade, tempo))
    except Exception as e:
        colorama_print(f"Erro ao inserir fornecedor. Erro:{e}", 'red')
        input("Pressione enter para voltar ao menu")
        limpar()
        logo()
        menu()
    finally:
        connect.commit()
        connect.close()
        colorama_print(f"Fornecedor {nm} Inserido com sucesso!", 'green')
        input("Pressione enter para voltar ao menu")
        limpar()
        logo()
        menu()
def refor():
    connect = sqlite3.connect('databases\data.db')
    cursor = connect.cursor()

    id = float(input("Insira o ID do fornecedor: "))

    try:
        cursor.execute('''
        DELETE FROM fornecedores WHERE ID = ?
        ''', (id,))
    except Exception as e:
        colorama_print(f"Erro ao remover fornecedor. Erro: {e}", 'red')
        input("Pressione enter para voltar ao menu: ")
        limpar()
        logo()
        menu()
    finally:
        connect.commit()
        connect.close()
        colorama_print(f"Fornecedor removido com sucesso!", "green")
        input("Pressione enter para voltar ao menu: ")
        limpar()
        logo()
        menu()

def acimamedia():
    connect = sqlite3.connect('databases/data.db')
    cursor = connect.cursor()

    try:
        # Consulta para obter produtos com preço acima da média e a média em si
        cursor.execute('''
        SELECT *, (SELECT AVG(preco) FROM produtos) AS media_preco
        FROM produtos 
        WHERE preco > (SELECT AVG(preco) FROM produtos)
        ''')
        produtos = cursor.fetchall()

        # Verificando se há produtos e exibindo-os em formato de tabela
        if produtos:
            headers = [desc[0] for desc in cursor.description]
            print(tabulate(produtos, headers, tablefmt="grid"))
            # Mostrando a média do preço
            media_preco = produtos[0][-1]  # O último elemento é a média
            print(f"\nMédia do preço dos produtos: {media_preco:.2f}")
        else:
            print("Nenhum produto com preço acima da média foi encontrado.")

    except Exception as e:
        colorama_print(f"Erro ao selecionar. Erro: {e}", 'red')
        input("Pressione enter para voltar ao menu: ")
        logo()
        menu()
    finally:
        connect.close()
        input("Pressione enter para voltar ao menu: ")
        logo()
        menu()



def abaixomedia():
    connect = sqlite3.connect('databases/data.db')
    cursor = connect.cursor()

    try:
        # Consulta para obter produtos com preço acima da média e a média em si
        cursor.execute('''
        SELECT *, (SELECT AVG(preco) FROM produtos) AS media_preco
        FROM produtos 
        WHERE preco < (SELECT AVG(preco) FROM produtos)
        ''')
        produtos = cursor.fetchall()

        # Verificando se há produtos e exibindo-os em formato de tabela
        if produtos:
            headers = [desc[0] for desc in cursor.description]
            print(tabulate(produtos, headers, tablefmt="grid"))
            # Mostrando a média do preço
            media_preco = produtos[0][-1]  # O último elemento é a média
            print(f"\nMédia do preço dos produtos: {media_preco:.2f}")
        else:
            print("Nenhum produto com preço abaixo da média foi encontrado.")

    except Exception as e:
        colorama_print(f"Erro ao selecionar. Erro: {e}", 'red')
        input("Pressione enter para voltar ao menu: ")
        logo()
        menu()
    finally:
        connect.close()
        input("Pressione enter para voltar ao menu: ")
        logo()
        menu()

def filtroemail():
    connect = sqlite3.connect('databases\data.db')
    cursor = connect.cursor()

    cursor.execute('''
    SELECT * FROM FORNECEDORES
    WHERE email = IS NULL
    ''')
    fornecedores = cursor.fetchall()
    if fornecedores:
            headers = [desc[0] for desc in cursor.description]
            print(tabulate(produtos, headers, tablefmt="grid"))
            input("Pressione enter para voltar ao menu:")
            limpar()
            logo()
            menu()

def setores():
    connect = sqlite3.connect('databases\data.db')
    cursor = connect.cursor

    a = input("Insira o setor: ")

    cursor.execute('''
    SELECT * FROM produtos WHERE setor = ?
    ''', (a,))
    setores = cursor.fetchall()
    if fornecedores:
        headers = [desc[0] for desc in cursor.description]
        print(tabulate(setores, headers, tablefmt='grid'))
        input("Pressione enter para voltar ao menu:")
        limpar()
        logo()
        menu()

def preco():
    connect = sqlite3.connect('databases\data.db')
    cursor = connect.cursor

    a = input("Insira o preço do produto: ")

    cursor.execute('''
    SELECT * FROM produtos WHERE preco = ?
    ''', (a,))
    setores = cursor.fetchall()
    if fornecedores:
        headers = [desc[0] for desc in cursor.description]
        print(tabulate(setores, headers, tablefmt='grid'))
        input("Pressione enter para voltar ao menu:")
        limpar()
        logo()
        menu()


def marca():
    connect = sqlite3.connect('databases\data.db')
    cursor = connect.cursor

    a = input("Insira a marca do produto: ")

    cursor.execute('''
    SELECT * FROM produtos WHERE marca = ?
    ''', (a,))
    setores = cursor.fetchall()
    if fornecedores:
        headers = [desc[0] for desc in cursor.description]
        print(tabulate(setores, headers, tablefmt='grid'))
        input("Pressione enter para voltar ao menu:")
        limpar()
        logo()
        menu()

def alterarusuario():
    connect = sqlite3.connect('databases\data.db')
    cursor = connect.cursor
    a = input("Insira como será o novo nome de usuário: ")
    try:
        cursor.execute('''
        UPDATE login
        SET nome = ?
        ''', (a,))
    except Exception as e:
        colorama_print(f"Erro ao mudar nome de usuario. Erro: {e}", 'red')
        limpar()
        logo()
        menu()
    finally:
        colorama_print(f"Nome de usuário trocado para {a}!", 'green')


def alterarsenha():
    connect = sqlite3.connect('databases\data.db')
    cursor = connect.cursor
    a = input("Insira como será a será a nova senha: ")
    try:
        cursor.execute('''
        UPDATE login
        SET senha = ?
        ''', (a,))
    except Exception as e:
        colorama_print(f"Erro ao mudar senha. Erro: {e}", 'red')
        input("Pressione enter para voltar ao menu: ")
        limpar()
        logo()
        menu()
    finally:
        colorama_print(f"Senha trocada para {a}!", 'green')
        input("Pressione enter para voltar ao menu: ")
        limpar()
        logo()
        menu()

def json():
    a = input("Produto ou fornecedor?[P/F]: ").strip().upper()
    if a == 'P':
        tabela = 'produtos'
    elif a == 'F':
        tabela = 'fornecedores'
    else:
        colorama_print("ERRO: Opção inválida.", 'red')
        time.sleep(0.2)
        limpar()
        logo()
        menu()
        return  # Use return para sair da função se a entrada for inválida

    json_file = 'Uploads/json.json'  # Use '/' ou '\\' para caminhos de arquivo
    data = pd.read_json(json_file)
    conn = sqlite3.connect('databases/data.db')
    data.to_sql(tabela, conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()
    colorama_print("Dados importados com sucesso!", 'green')
    input("Pressione enter para voltar ao menu:")
    limpar()
    logo()
    menu()


def csv():
    a = input("Produto ou fornecedor?[P/F]: ").strip().upper()
    if a == 'P':
        tabela = 'produtos'
    elif a == 'F':
        tabela = 'fornecedores'
    else:
        colorama_print("ERRO: Opção inválida.", 'red')
        time.sleep(0.2)
        limpar()
        logo()
        menu()
        return  # Use return para sair da função se a entrada for inválida

    csv_file = 'Uploads/csv.csv'  # Use '/' ou '\\' para caminhos de arquivo
    data = pd.read_csv(csv_file)
    conn = sqlite3.connect('databases/data.db')
    data.to_sql(tabela, conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()
    colorama_print("Dados importados com sucesso!", 'green')
    input("Pressione enter para voltar ao menu:")
    limpar()
    logo()
    menu()

def mostrartabela():
    connect = sqlite3.connect('databases/data.db')
    cursor = connect.cursor()
    
    a = input("Produto ou fornecedor?[P/F]: ").strip().upper()
    if a == 'P':
        tabela = 'produtos'
    elif a == 'F':
        tabela = 'fornecedores'
    else:
        colorama_print("ERRO: Opção inválida.", 'red')
        time.sleep(0.2)
        limpar()
        logo()
        menu()
        return  # Saia da função se a entrada for inválida

    # Correção na consulta SQL
    cursor.execute(f'SELECT * FROM {tabela}')  # Use f-string para incluir o nome da tabela
    b = cursor.fetchall()
    
    if b:
        headers = [desc[0] for desc in cursor.description]
        print(tabulate(b, headers, tablefmt='grid'))
    else:
        print("Nenhum registro encontrado.")

    input("Pressione enter para voltar ao menu:")
    limpar()
    logo()
    menu()

def excel():
    a = input("Produto ou fornecedor?[P/F]: ").strip().upper()
    if a == 'P':
        tabela = 'produtos'
    elif a == 'F':
        tabela = 'fornecedores'
    else:
        colorama_print("ERRO: Opção inválida.", 'red')
        time.sleep(0.2)
        limpar()
        logo()
        menu()
        return  # Use return para sair da função se a entrada for inválida

    excel_file = 'Uploads/excel.xlsx'  # Use '/' ou '\\' para caminhos de arquivo
    data = pd.read_excel(excel_file)
    conn = sqlite3.connect('databases/data.db')
    data.to_sql(tabela, conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()
    colorama_print("Dados importados com sucesso!", 'green')
    input("Pressione enter para voltar ao menu:")
    limpar()
    logo()
    menu()

def especificotabela():
    a = input("Produto ou fornecedor?[P/F]: ").strip().upper()
    if a == 'P':
        tabela = 'produtos'
    elif a == 'F':
        tabela = 'fornecedores'
    else:
        colorama_print("ERRO: Opção inválida.", 'red')
        time.sleep(0.2)
        limpar()
        logo()
        menu()
    conn = sqlite3.connect('databases/data.db')
    cursor = conn.cursor()
    ID = input("Indira o id: ")
    cursor.execute(f'''
        SELECT * FROM {tabela} WHERE ID = ?
    ''', (ID,))
    
    

logo()
menu()
