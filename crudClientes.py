#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Odenir Gomes
#
# Created:     21/01/2019
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
        mycursor.execute('use mbdatabase;')
        mycursor.execute('create table if not exists clientes (cod_cliente int not null auto_increment, nome varchar(20) not null, snome varchar(20) not null, sexo enum("M", "F"), tel varchar(15), endereco varchar(50), primary key(cod_cliente));')

    except Error as e1:
        mycursor.execute('create database if not exists mysqlbd002 default character set utf8 default collate utf8_general_ci;')
        mycursor.execute('use mbdatabase;')
        mycursor.execute('create table if not exists clientes (cod_cliente int not null auto_increment, nome varchar(20) not null, snome varchar(20) not null, sexo enum("M", "F"), tel varchar(15), endereco varchar(50), primary key(cod_cliente));')

    conn.close()


def cadastrar_cliente():

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute('use mbdatabase;')

    print("\nCadastrar Cliente:")

    try:
        nome = input("Nome: ")
    except:
        print("Erro de entrada!!")
        cadastrar_cliente()

    try:
        snome = input("Sobrenome: ")
    except:
        print("Erro de entrada!!")
        cadastrar_cliente()

    try:
        sexo = input("Sexo: ")
    except:
        print("Erro de entrada!!")
        cadastrar_cliente()
    sexo = sexo.upper()
    if sexo != 'M' and sexo != 'F':
        print("Erro de entrada!!")
        cadastrar_cliente()

    try:
        tel = input("Telefone: ")
    except:
        print("Erro de entrada!!")
        cadastrar_cliente()

    try:
        end = input("Endereco: ")
    except:
        print("Erro de entrada!!")
        cadastrar_cliente()

    mycursor.execute("insert into clientes values (Default ,'{0}', '{1}', '{2}', '{3}', '{4}');" .format(nome, snome, sexo, tel, end))
    conn.commit()
    print("Cliente cadastrado!")

    conn.close()


def listar_clientes():

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute("use mbdatabase;")

    print("\nListar clientes:")
    mycursor.execute("select * from clientes;")
    myresult = mycursor.fetchall()

    for r in myresult:
        print(r)

    conn.close()


def deletar_cliente():

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute("use mbdatabase;")

    print("\nDeletar cliente:")
    listar_clientes()

    try:
        id = int(input("Entre com o codigo do cliente que deseja deletar: "))

    except:
        print("Entre com um valor inteiro no codigo!!")
        deletar_cliente()

    mycursor.execute("select * from clientes where cod_cliente = '{0}';" .format(id))
    myresult = mycursor.fetchall()
    print("Registro selecionado ->", myresult)

    print("Tem certeza que deseja deletar esse registro?")
    OPCAO = input("Sim<S> ou NAO<N>: ")
    OPCAO = OPCAO.upper()

    if OPCAO == 'S':
        mycursor.execute("delete from clientes where cod_cliente = '{0}';" .format(id))
        conn.commit()
        print("Registro deletado!")
    elif OPCAO == 'N':
        pass
    else:
        print("Entrada invalida")

    conn.close()


def alterar_cliente():

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute('use mbdatabase;')

    print("\nAlterar cliente:")
    listar_clientes()

    try:
        id = int(input("Entre com o codigo do cliente que deseja alterar: "))

    except Error as E1:
        print("Entre com valor inteiro em codigo")
        alterar_cliente()

    mycursor.execute("select * from clientes where cod_cliente = '{0}';" .format(id))
    myresult = mycursor.fetchall()
    print("Registro selecionado ->", myresult)

    try:
        nome = input("Nome: ")
    except:
        print("Erro de entrada!!")
        alterar_cliente()

    try:
        snome = input("Sobrenome: ")
    except:
        print("Erro de entrada!!")
        alterar_cliente()

    try:
        sexo = input("Sexo: Masc<M> ou Femi<F>: ")
    except:
        print("Erro de entrada!!")
        alterar_cliente()
    sexo.upper()
    if sexo != 'M' and sexo != 'F' and sexo != "":
        print("\nEntrada invalida!!!")
        print("Entre com o valor certo do sexo!")
        alterar_cliente()

    try:
        tel = input("Telefone: ")
    except:
        print("Erro de entrada!!")
        alterar_cliente()

    try:
        end = input("Endereco: ")
    except:
        print("Erro de entrada!!")
        alterar_cliente()

    if nome != "":
        mycursor.execute("update clientes set nome = '{0}' where cod_cliente = '{1}';" .format(nome, id))

    if snome != "":
        mycursor.execute("update clientes set snome = '{0}' where cod_cliente = '{1}';" .format(snome, id))

    if sexo != "":
        mycursor.execute("update clientes set sexo = '{0}' where cod_cliente = '{1}';" .format(sexo, id))

    if cargo != "":
        mycursor.execute("update clientes set tel = '{0}' where cod_cliente = '{1}';" .format(tel, id))

    if salario != "":
        mycursor.execute("update clientes set endereco = '{0}' where cod_cliente = '{1}';" .format(end, id))

    conn.commit()
    conn.close()

def buscar_clientes():

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute('use mbdatabase;')

    print("Buscar clientes:")
    print("1. Nome.")
    print("2. Sobrenome.")
    print("3. Sexo.")
    print("4. Telefone.")
    print("5. Endereço.")

    OPCAO = int(input("Deseja buscar cliente pelo: "))
    if OPCAO == 1:
        OPCAO = "nome"

    elif OPCAO == 2:
        OPCAO = "snome"

    elif OPCAO == 3:
        OPCAO = "sexo"

    elif OPCAO == 4:
        OPCAO = "tel"

    elif OPCAO == 5:
        OPCAO = "endereco"

    else:
        print("Entrada invalida!!")
        buscar_clientes()

    try:
        query = input("Pesquisar: ")
    except:
        print("Erro de entrada!!")
        buscar_clientes()

    try:
        mycursor.execute("select * from clientes where {0} = '{1}';" .format(OPCAO, query))
    except:
        print("Erro na pesquisa!!")
        buscar_clientes()

    myresult = mycursor.fetchall()

    for r in myresult:
        print(r)

    conn.close()

def quant_clientes():

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute("use mbdatabase;")

    mycursor.execute("select count(*) from clientes;")
    myresult = mycursor.fetchone()

    print("Quantidade de clientes -> {0}" .format(myresult[0]))

    conn.close()

def menuRelatorios_clientes():

    while True:
        print("\nClientes")
        print("Menu Relatorios:")
        print("1. Buscar clientes.")
        print("2. Quantidade de clientes.")
        print("0. Sair")

        try:
            OPCAO = int(input("Entre com a opcao: "))
        except:
            print("Erro na entrada!!")
            menuRelatorios_clientes()

        if OPCAO == 1:
            buscar_clientes()

        elif OPCAO == 2:
            quant_clientes()

        elif OPCAO == 0:
            break

        else:
            print("Entrada invalida!!")

def menu_clientes():

    while True:
        print("\nMenu dos Clientes:")
        print("1. Cadastar.")
        print("2. Listar.")
        print("3. Deletar.")
        print("4. Alterar.")
        print("5. Relatorios.")
        print("0. Sair.")

        try:
            OPCAO = int(input("Entre com a opcao: "))
        except:
            print("Erro na entrada!!")
            menu_clientes()

        if OPCAO == 1:
            cadastrar_cliente()

        elif OPCAO == 2:
            listar_clientes()

        elif OPCAO == 3:
            deletar_cliente()

        elif OPCAO == 4:
            alterar_cliente()

        elif OPCAO == 5:
            menuRelatorios_clientes()

        elif OPCAO == 0:
            break



def main():

    init_server()
    menu_clientes()

if __name__ == '__main__':
    main()
