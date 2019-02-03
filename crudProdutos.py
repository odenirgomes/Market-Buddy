#-------------------------------------------------------------------------------
# Name:        crudProdutos
# Purpose:
#
# Author:      Odenir Gomes
#
# Created:     28/01/2019
# Copyright:   (c) Odenir Gomes 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import mysql.connector
from mysql.connector import Error

#Conecta ao servidor do MySQL no host local(localhost)
def connect():
    """ Connect to MySQL database """
    try:
        conn = mysql.connector.connect(host='localhost',
                                       user='root',
                                       password='')
        if conn.is_connected():
            print('Connected to MySQL database')

    except Error as e:
        print(e)
        return

    return conn

def init_server():

    conn = connect()
    mycursor = conn.cursor()

    try:
        mycursor.execute("use mbdatabase;")
        mycursor.execute("create table if not exists produtos (cod_prod int auto_increment, nome varchar(20) not null, tipo varchar(20) not null, quantidade int not null, preco decimal(8,2) not null, primary key(cod_prod))")

    except:
        mycursor.execute("create database if not exists mbdatabase default character set utf8 default collate utf8_general_ci;")
        mycursor.execute("use mbdatabase;")
        mycursor.execute("create table if not exists produtos (cod_prod int auto_increment, nome varchar(20) not null, tipo varchar(20) not null, quantidade int not null, preco decimal(8,2) not null, primary key(cod_prod))ENGINE=InnoDB DEFAULT CHARSET=utf8;")

    conn.close()


def cadastrar():

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute("use mbdatabase;")

    print("\nCadastrar produto:")
    try:
        nome = input("Nome: ")
    except:
        print("Erro de entrada!!")
        cadastrar()

    try:
        tipo = input("Tipo: ")
    except:
        print("Erro de entrada!!")
        cadastrar()

    try:
        quantidade = int(input("Quantidade: "))
    except:
        print("Erro de entrada!!")
        cadastrar()

    try:
        preco = float(input("Preço: "))
    except:
        print("Erro de entrada!!")
        cadastrar()

    try:
        mycursor.execute("insert into produtos valeus (default, '{0}', '{1}', '{2}', '{3}')")
    except:
        print("Erro de cadastro!!")
        cadastrar()

    conn.commit()

    conn.close()


def listar():

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute("use mbdatabase;")

    print("\nListar produtos:")

    mycursor.execute("select * from produtos;")
    myresult = mycursor.fetchall()

    for r in myresult:
        print(r)

    conn.close()

def deletar():

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute("use mbdatabase;")

    print("\nDeletar produto:")

    listar()

    try:
        id = int(input("Entre com o codigo do produto que deseja deletar: "))

    except:
        print("Entre com um valor inteiro no codigo!!")
        deletar()

    mycursor.execute("select * from produtos where cod_prod = '{0}';" .format(id))
    myresult = mycursor.fetchall()
    print("Registro selecionado ->", myresult)

    print("Tem certeza que deseja deletar esse registro?")
    OPCAO = input("Sim<S> ou NAO<N>: ")
    OPCAO = OPCAO.upper()

    if OPCAO == 'S':
        mycursor.execute("delete from produtos where cod_prod = '{0}';" .format(id))
        conn.commit()
        print("Registro deletado!")
    elif OPCAO == 'N':
        pass
    else:
        print("Entrada invalida!!")

    conn.close()


def alterar():

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute('use mbdatabase;')

    print("\nAlterar cliente:")
    listar()

    try:
        id = int(input("Entre com o codigo do produto que deseja alterar: "))

    except:
        print("Entre com um valor inteiro no codigo!!")
        alterar()

    mycursor.execute("select * from clientes where cod_cliente = '{0}';" .format(id))
    myresult = mycursor.fetchall()
    print("Registro selecionado ->", myresult)

    try:
        nome = input("Nome: ")
    except:
        print("Erro de entrada!!")
        alterar()

    try:
        tipo = input("Tipo: ")
    except:
        print("Erro de entrada!!")
        alterar()

    try:
        quantidade = input("Quantidade: ")
    except:
        print("Erro de entrada!!")
        alterar()

    try:
        preco = input("Preço: ")
    except:
        print("Erro de entrada!!")
        alterar()

    if nome != '':
        mycursor.execute("update produtos set nome = '{0}' where cod_prod = '{1}';" .format(nome, id))

    if tipo != '':
        mycursor.execute("update produtos set tipo = '{0}' where cod_prod = '{1}';" .format(tipo, id))

    if quantidade != '':
        mycursor.execute("update produtos set quantidade = '{0}' where cod_prod = '{1}';" .format(quantidade, id))

    if preco != '':
        mycursor.execute("update produtos set preco = '{0}' where cod_prod = '{1}';" .format(preco, id))

    conn.commit()
    conn.close()


def buscar():

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute('use mbdatabase;')

    print("\nBuscar clientes:")
    print("1. Nome.")
    print("2. Tipo.")
    print("3. Quantidade.")
    print("4. Preco.")

    try:
        OPCAO = int(input("Entre com a opcao de busca: "))
    except:
        print("Erro de entrada!!")
        buscar()

    if OPCAO == 1:
        OPCAO = 'nome'

    elif OPCAO == 2:
        OPCAO = 'tipo'

    elif OPCAO == 3:
        OPCAO = 'quantidade'

    elif OPCAO == 4:
        OPCAO = 'preco'

    else:
        print("Entrada invalida!!")
        buscar()

    query = input("Pesquisar: ")

    try:
        mycursor.execute("select * from produtos where {0} = '{1}';" .format(OPCAO, query))
    except:
        print("Erro na pesquisa!!")
        buscar()

    myresult = mycursor.fetchall()

    for r in myresult:
        print(r)

    conn.close()


def menuRelatorios():

    while True:
        print("\nProdutos")
        print("Menu Relatorios:")
        print("1. Buscar produto.")
        print("0. Sair.")

        try:
            OPCAO = int(input("Entre com a opcao: "))
        except:
            print("Erro de entrada!!")
            menuRelatorios()

        if OPCAO == 1:
            buscar()

        elif OPCAO == 0:
            break

def menu ():

    while True:
        print("\nMenu dos produtos:")
        print("1. Cadastrar.")
        print("2. Listar.")
        print("3. Deletar.")
        print("4. Alterar.")
        print("5. Relatorios.")
        print("0. Sair.")

        try:
            OPCAO = int(input("Entre com a opcao: "))
        except:
            print("Erro na entrada!!")
            menu()

        if OPCAO == 1:
            cadastrar()

        elif OPCAO == 2:
            listar()

        elif OPCAO == 3:
            deletar()

        elif OPCAO == 4:
            alterar()

        elif OPCAO == 5:
            menuRelatorios()

        elif OPCAO == 0:
            break

        else:
            print("Entrada invalida!!")


def main():

    init_server()
    menu_prod()

if __name__ == '__main__':
    main()
