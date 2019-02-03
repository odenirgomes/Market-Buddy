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
        mycursor.execute('create table if not exists clientes (cod_cliente int not null auto_increment, nome varchar(20) not null, snome varchar(20) not null, sexo enum("M", "F"), tel varchar(15), endereco varchar(50), primary key(cod_cliente))ENGINE=InnoDB DEFAULT CHARSET=utf8;')

    except Error as e1:
        mycursor.execute('create database if not exists mysqlbd002 default character set utf8 default collate utf8_general_ci;')
        mycursor.execute('use mbdatabase;')
        mycursor.execute('create table if not exists clientes (cod_cliente int not null auto_increment, nome varchar(20) not null, snome varchar(20) not null, sexo enum("M", "F"), tel varchar(15), endereco varchar(50), primary key(cod_cliente))ENGINE=InnoDB DEFAULT CHARSET=utf8;')

    conn.close()


def cadastrar():

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute('use mbdatabase;')

    print("\nCadastrar Cliente:")

    try:
        nome = input("Nome: ")
    except:
        print("Erro de entrada!!")
        cadastrar()

    try:
        snome = input("Sobrenome: ")
    except:
        print("Erro de entrada!!")
        cadastrar()

    try:
        sexo = input("Sexo: ")
    except:
        print("Erro de entrada!!")
        cadastrar()
    sexo = sexo.upper()
    if sexo != 'M' and sexo != 'F':
        print("Erro de entrada!!")
        cadastrar()

    try:
        tel = input("Telefone: ")
    except:
        print("Erro de entrada!!")
        cadastrar()

    try:
        end = input("Endereco: ")
    except:
        print("Erro de entrada!!")
        cadastrar()

    try:
        mycursor.execute("insert into clientes values (Default ,'{0}', '{1}', '{2}', '{3}', '{4}');" .format(nome, snome, sexo, tel, end))
    except:
        print("Erro de cadastro!!")
        cadastrar()
    conn.commit()
    print("Cliente cadastrado!")

    conn.close()


def listar():

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute("use mbdatabase;")

    print("\nListar clientes:")
    mycursor.execute("select * from clientes;")
    myresult = mycursor.fetchall()

    for r in myresult:
        print(r)

    conn.close()


def deletar():

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute("use mbdatabase;")

    print("\nDeletar cliente:")
    listar()

    try:
        id = int(input("Entre com o codigo do cliente que deseja deletar: "))

    except:
        print("Entre com um valor inteiro no codigo!!")
        deletar()

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


def alterar():

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute('use mbdatabase;')

    print("\nAlterar cliente:")
    listar()

    try:
        id = int(input("Entre com o codigo do cliente que deseja alterar: "))

    except Error as E1:
        print("Entre com valor inteiro em codigo")
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
        snome = input("Sobrenome: ")
    except:
        print("Erro de entrada!!")
        alterar()

    try:
        sexo = input("Sexo: Masc<M> ou Femi<F>: ")
    except:
        print("Erro de entrada!!")
        alterar()
    sexo.upper()
    if sexo != 'M' and sexo != 'F' and sexo != "":
        print("\nEntrada invalida!!!")
        print("Entre com o valor certo do sexo!")
        alterar()

    try:
        tel = input("Telefone: ")
    except:
        print("Erro de entrada!!")
        alterar()

    try:
        end = input("Endereco: ")
    except:
        print("Erro de entrada!!")
        alterar()

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

def buscar():

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute('use mbdatabase;')

    print("\nBuscar clientes:")
    print("1. Nome.")
    print("2. Sobrenome.")
    print("3. Sexo.")
    print("4. Telefone.")
    print("5. Endereço.")

    try:
        OPCAO = int(input("Entre com a opcao de busca: "))
    except:
        print("Erro de entrada!!")
        buscar()

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
        buscar()

    query = input("Pesquisar: ")

    try:
        mycursor.execute("select * from clientes where {0} = '{1}';" .format(OPCAO, query))
    except:
        print("Erro na pesquisa!!")
        buscar()

    myresult = mycursor.fetchall()

    for r in myresult:
        print(r)

    conn.close()

def quant():

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute("use mbdatabase;")

    mycursor.execute("select count(*) from clientes;")
    myresult = mycursor.fetchone()

    print("Quantidade de clientes -> {0}" .format(myresult[0]))

    conn.close()

def menuRelatorios():

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
            menuRelatorios()

        if OPCAO == 1:
            buscar()

        elif OPCAO == 2:
            quant()

        elif OPCAO == 0:
            break

        else:
            print("Entrada invalida!!")

def menu():

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



def main():

    init_server()
    menu()

if __name__ == '__main__':
    main()
