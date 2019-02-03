#-------------------------------------------------------------------------------
# Name:        crudVendas
# Purpose:
#
# Author:      Odenir Gomes
#
# Created:     02/02/2019
# Copyright:   (c) Odenir Gomes 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from decimal import *

from datetime import datetime

import mysql.connector
from mysql.connector import Error

import crudClientes
import crudFuncionarios
import crudProdutos

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
        mycursor.execute("create table if not exists vendas (cod_venda int auto_increment, data_venda date not null, preco decimal(8,2) not null, cliente int, funcionario int not null, foreign key(cliente) references clientes(cod_cliente), foreign key(funcionario) references funcionarios(cod_func), primary key(cod_venda)) ENGINE=InnoDB DEFAULT CHARSET=utf8;")
        mycursor.execute("create table if not exists item_venda (cod_itemVenda int auto_increment, cod_venda int, produto int, foreign key(cod_venda) references vendas(cod_venda), foreign key(produto) references produtos(cod_prod))ENGINE=InnoDB DEFAULT CHARSET=utf8;")

    except:
        mycursor.execute("create database if not exists mbdatabase default character set utf8 default collate utf8_general_ci;")
        mycursor.execute("use mbdatabase;")
        mycursor.execute("create table if not exists vendas (cod_venda int auto_increment, data_venda date not null, preco decimal(8,2) not null, cliente int, funcionario int not null, foreign key(cliente) references clientes(cod_cliente), foreign key(funcionario) references funcionarios(cod_func), primary key(cod_venda)) ENGINE=InnoDB DEFAULT CHARSET=utf8;")
        mycursor.execute("create table if not exists item_venda (cod_itemVenda int auto_increment, cod_venda int not null, produto int not null, foreign key(cod_venda) references vendas(cod_venda), foreign key(produto) references produtos(cod_prod), primary key(cod_itemVenda))ENGINE=InnoDB DEFAULT CHARSET=utf8;")

    conn.close()

def dateNow():
    now = datetime.now()
    return '{0}-{1}-{2}' . format(now.year, now.month, now.day)

def cadastrar():

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute('use mbdatabase;')

    produtos = []

    print('\nCadastrar venda:\n')

    #Selecionando funcionario que esta evetuando a venda.
    while True:
        crudFuncionarios.listar()

        try:
            func = int(input('Selecionar funcionario com o codigo --> '))
        except:
            print('Erro na entrada!!')
            cadastrar()

        mycursor.execute('select * from funcionarios where cod_func = "{0}";' .format(func))
        myresult = mycursor.fetchone()
        if myresult != None:
            print('Funcionario selecionado --> ', myresult)
            break
        else:
            print('Registro na existente!!')

    # Selecionando cliente
    while True:
        crudClientes.listar()
        cliente = input('Selecionar cliente com o codigo --> ')

        try:
            cliente = int(cliente)
        except:
            if cliente != '':
                print('Erro na entrada!!')
                cadastrar()

        if cliente != '':
            mycursor.execute('select * from clientes where cod_cliente = "{0}";' .format(cliente))
            myresult = mycursor.fetchone()
            if myresult != None:
                print('Cliente selecionado --> ', myresult)
                break
            else:
                print('Registro nao existente!!')
        else:
            cliente = None
            print('Cliente selecionado --> Nenhum')
            break

    while True:
        print("\nAdicionar produtos:")
        crudProdutos.listar()

        while True:
            try:
                produto = int(input("Selecionar produto --> "))
                break
            except:
                print('Erro na entrada!!')

        mycursor.execute('select * from produtos where cod_prod = "{0}";' .format(produto))
        myresult = mycursor.fetchone()
        print("Produto selecionado --> ", myresult)

        produtos.append(produto)

        while True:
            OPCAO = input("Deseja adicionar outro produto ? Sim<S> ou Nao<N>: ")
            if OPCAO.upper() == 'N':
                break
            elif OPCAO.upper() == 'S':
                break
            else:
                print("Entrada invalida!!")

        if OPCAO.upper() == 'N':
            break

    print("\nProdutos selecionados:")
    for p in produtos:
        mycursor.execute('select * from produtos where cod_prod = "{0}";' .format(p))
        myresult = mycursor.fetchone()
        print(myresult)

    #Calculando Preco
    preco = 0
    for p in produtos:
        mycursor.execute('select * from produtos where cod_prod = "{0}";' .format(p))
        myresult = mycursor.fetchone()

        preco += myresult[4]

    print("Preco: ", preco)


    while True:
        OPCAO = input("Confirmar venda ? Sim<S> ou Nao<N>: ")
        if OPCAO.upper() == 'N':
            break
        elif OPCAO.upper() == 'S':
            break
        else:
            print("Entrada invalida!!")

    if OPCAO.upper() == 'S':
        mycursor.execute('insert into vendas values (default, "{0}", "{1}", "{2}", "{3}");' .format(dateNow(), preco, cliente, func))
        conn.commit()

        mycursor.execute('select * from vendas;')
        myresult = mycursor.fetchall()

        myresult = myresult.pop()
        cod_venda = myresult[0]

        for p in produtos:
            mycursor.execute('insert into item_venda values (default, "{0}", "{1}");' .format(cod_venda, p))

        conn.commit()
        print("Venda Confirmada!")

    else:
        print("Venda Cancelada!")
        cadastrar()

    conn.close()

def listar():

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute('use mbdatabase;')

    print("Listar vendas: ")

    mycursor.execute('select vendas.cod_venda, funcionarios.nome, clientes.nome, vendas.data_venda, vendas.preco from ((vendas inner join funcionarios on vendas.funcionario = funcionarios.cod_func) inner join clientes on vendas.cliente = clientes.cod_cliente);')
    myresult = mycursor.fetchall()

    for r in myresult:
        print(r)

    conn.close()

def deletar():

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute("use mbdatabase;")

    print("\nDeletar venda:")

    listar()

    try:
        id = int(input("Entre com o codigo da venda que deseja deletar: "))

    except:
        print("Entre com um valor inteiro no codigo!!")
        deletar()

    mycursor.execute("select * from vendas where cod_venda = '{0}';" .format(id))
    myresult = mycursor.fetchall()
    print("Registro selecionado ->", myresult)

    print("Tem certeza que deseja deletar esse registro?")
    OPCAO = input("Sim<S> ou NAO<N>: ")
    OPCAO = OPCAO.upper()

    if OPCAO == 'S':
        mycursor.execute("delete from vendas where cod_venda = '{0}';" .format(id))
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

    print("\nAlterar venda:")
    listar()

    try:
        id = int(input("Entre com o codigo da venda que deseja alterar: "))

    except:
        print("Entre com um valor inteiro no codigo!!")
        alterar()

    mycursor.execute("select * from vendas where cod_venda = '{0}';" .format(id))
    myresult = mycursor.fetchall()
    print("Registro selecionado ->", myresult)

    print("\nAlterar funcionario: ")
    crudFuncionarios.listar()

    while True:
        id_func = input("Entre com o codigo do funcionario: ")

        try:
            id_func = int(id_func)
            break
        except:
            if id_func == '':
                break
            else:
                print("Entrada invalida")



    '''
    if nome != '':
        mycursor.execute("update produtos set nome = '{0}' where cod_prod = '{1}';" .format(nome, id))

    if tipo != '':
        mycursor.execute("update produtos set tipo = '{0}' where cod_prod = '{1}';" .format(tipo, id))

    if quantidade != '':
        mycursor.execute("update produtos set quantidade = '{0}' where cod_prod = '{1}';" .format(quantidade, id))

    if preco != '':
        mycursor.execute("update produtos set preco = '{0}' where cod_prod = '{1}';" .format(preco, id))
    '''
    conn.commit()
    conn.close()


def menu():

    while True:
        print('\nMenu de vendas:')
        print('1. Cadastrar.')
        print('2. Listar.')
        print('3. Deletar.')
        print('4. Alterar.')
        print('0. Sair.')

        OPCAO = int(input('Entre com a opcao: '))
        if OPCAO == 1:
            cadastrar()

        elif OPCAO == 2:
            listar()

        elif OPCAO == 3:
            deletar()

        elif OPCAO == 4:
            alterar()

        elif OPCAO == 0:
            break
        else:
            print("Entrada invalida!!")


def main():

    init_server()
    menu()

if __name__ == '__main__':
    main()
