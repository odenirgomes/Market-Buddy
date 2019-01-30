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
        mycursor.execute("create table if not exists produtos (cod_prod int auto_increment, nome varchar(20) not null, tipo varchar(20) not null, quantidade int not null, preco decimal(8,2) not null, primary key(cod_prod));")

    except:
        mycursor.execute("create database if not exists mbdatabase default character utf8 default collate utf8_general_ci;")
        mycursor.execute("use mbdatabase;")
        mycursor.execute("create table if not exists produtos (cod_prod int auto_increment, nome varchar(20) not null, tipo varchar(20) not null, quantidade int not null, preco decimal(8,2) not null, primary key(cod_prod));")

    conn.close()


def cadastrar_prod():
    pass


def menu_prod():

    while True:
        print("Menu dos produtos:")
        print("1. Cadastrar.")
        print("2. Listar.")
        print("3. Deletar.")
        print("4. Alterar.")
        print("0. Sair.")

        try:
            OPCAO = int(input("Entre com a opcao: "))
        except:
            print("Erro na entrada!!")
            menu_prod()

        if OPCAO == 1:
            cadastrar_prod()

        elif OPCAO == 0:
            break

        else:
            print("Entrada invalida!!")


def main():

    init_server()
    menu_prod()

if __name__ == '__main__':
    main()
