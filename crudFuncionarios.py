#-------------------------------------------------------------------------------
# Name:        crudFuncionarios
# Purpose:
#
# Author:      Odenir Gomes
#
# Created:     17/01/2019
# Copyright:   (c) Odenir Gomes 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import mysql.connector
from mysql.connector import Error
import string

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
        mycursor.execute('create table if not exists funcionarios (cod_func int not null auto_increment, nome varchar(20) not null, snome varchar(20) not null, sexo enum("M", "F"), cargo varchar(20), salario decimal(8,2), primary key(cod_func));')

    except Error as e1:
        mycursor.execute('create database if not exists mbdatabase default character set utf8 default collate utf8_general_ci;')
        mycursor.execute('use mbdatabase;')

        mycursor.execute('create table funcionarios (cod_func int not null auto_increment, nome varchar(20) not null, snome varchar(20) not null, sexo enum("M", "F"), cargo varchar(20), salario decimal(8,2), primary key(cod_func));')

    conn.close()

def cadastrar_func():

    # Conecção com o servidor de BD e a criação de um curso para executar comandos em sql
    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute('use mbdatabase;')

    print("\nCadastrar Funcionario: ")

    try:
        nome = input("Nome: ")
    except:
        print("Erro na entrada!!")
        cadastrar_func()

    try:
        snome = input("Sobrenome: ")
    except:
        print("Erro na entrada!!")
        cadastrar_func()

    sexo = input("Sexo: Masc<M> ou Femi<F>: ")
    sexo = sexo.upper()
    if sexo != 'M' and sexo != 'F':
        print("\nEntrada invalida!!!")
        print("Entre com o valor certo do sexo!")
        cadastrar_func()

    try:
        cargo = input("Cargo: ")
    except:
        print("Erro na entrada!!")
        cadastrar_func()

    try:
        salario = float(input("Salario: "))

    except:
        print("\nEntrada invalida!!!")
        print("Entre com o tipo correto de salario!")
        cadastrar_func()

    salario = str(salario)

    mycursor.execute("INSERT INTO funcionarios (nome, snome, sexo, cargo, salario) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}');" .format(nome, snome, sexo, cargo, salario))
    #Execução do comando de insert no BD
    conn.commit()
    print("Registro cadastrado!")

    #Fechando conecção com BD
    conn.close()


def listar_func():

    print("\nListar funcionarios:")
    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute('use mbdatabase;')

    mycursor.execute('select * from funcionarios;')
    myresult = mycursor.fetchall()

    for r in myresult:
        print(r)

    conn.close()


def deletar_func():

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute('use mbdatabase;')

    print("\nDeletar funcionario:")
    listar_func()

    try:
        id = int(input("Entre com o codigo do funcionario que deseja deletar: "))

    except:
        print("Entre com um valor inteiro no codigo!!")
        deletar_func()

    mycursor.execute("select * from funcionarios where cod_func = '{0}';" .format(id))
    myresult = mycursor.fetchall()
    print("Registro selecionado ->", myresult)

    print("Tem certeza que deseja deletar esse registro?")
    OPCAO = input("Sim<S> ou NAO<N>: ")
    OPCAO = OPCAO.upper()

    if OPCAO == 'S':
        mycursor.execute("delete from funcionarios where cod_func = '{0}';" .format(id))
        conn.commit()
        print("Registro deletado!")
    elif OPCAO == 'N':
        pass
    else:
        print("Entrada invalida")

    conn.close()


def alterar_func():

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute('use mbdatabase;')

    print("\nAlterar funcionario:")
    listar_func()

    try:
        id = int(input("Entre com o codigo do funcionario que deseja alterar: "))

    except Error as E1:
        print("Entre com valor inteiro em codigo")
        alterar_func()

    mycursor.execute("select * from funcionarios where cod_func = '{0}';" .format(id))
    myresult = mycursor.fetchall()
    print("Registro selecionado ->", myresult)

    try:
        nome = input("Nome: ")
    except:
        print("Erro na entrada!!")
        alterar_func()

    try:
        snome = input("Sobrenome: ")
    except:
        print("Erro na entrada!!")
        alterar_func()

    sexo = input("Sexo: Masc<M> ou Femi<F>: ")
    sexo.upper()
    if sexo != 'M' and sexo != 'F' and sexo != "":
        print("\nEntrada invalida!!!")
        print("Entre com o valor certo do sexo!")
        alterar_func()

    try:
        cargo = input("Cargo: ")
    except:
        print("Erro na entrada!!")
        alterar_func()


    salario = input("Salario: ")
    if salario in string.ascii_letters and salario != '':
        print("Tipo de entrada invalida!!!")
        alterar_func()

    if nome != "":
        mycursor.execute("update funcionarios set nome = '{0}' where cod_func = '{1}';" .format(nome, id))

    if snome != "":
        mycursor.execute("update funcionarios set snome = '{0}' where cod_func = '{1}';" .format(snome, id))

    if sexo != "":
        mycursor.execute("update funcionarios set sexo = '{0}' where cod_func = '{1}';" .format(sexo, id))

    if cargo != "":
        mycursor.execute("update funcionarios set cargo = '{0}' where cod_func = '{1}';" .format(cargo, id))

    if salario != "":
        mycursor.execute("update funcionarios set salario = '{0}' where cod_func = '{1}';" .format(salario, id))

    conn.commit()
    conn.close()


def quant_func():

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute('use mbdatabase;')

    mycursor.execute('select count(*) from funcionarios;')
    myresult = mycursor.fetchone()
    print("\nNumeros de funcionarios: ", myresult[0])

    conn.close()


def quantGastaSalario_func():

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute('use mbdatabase;')

    mycursor.execute('select sum(salario) from funcionarios;')
    myresult = mycursor.fetchone()
    print("\nQuantidade gasta em salarios: ", myresult[0])

    conn.close()


def buscaCargo():

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute('use mbdatabase;')

    print("\nBuscar funcionarios pelo cargo:")

    try:
        query = input("Entre com o cargo: ")
    except:
        print("Erro na entrada!!")
        buscaCargo()

    mycursor.execute("select * from funcionarios where cargo = '{0}';" .format(query))
    myresult = mycursor.fetchall()

    for r in myresult:
        print(r)

    conn.close()


def buscaNome():

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute('use mbdatabase;')

    print("\nBuscar funcionarios pelo nome:")

    try:
        query = input("Entre com o cargo: ")
    except:
        print("Erro na entrada!!")
        buscaNome()

    mycursor.execute("select * from funcionarios where nome = '{0}';" .format(query))
    myresult = mycursor.fetchall()

    for r in myresult:
        print(r)

    conn.close()


def buscaSexo():

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute('use mbdatabase;')

    print("\nBuscar funcionarios pelo sexo:")
    print("Entre com o sexo: ")
    query = input("Masc<M> ou Femi<F>: ")
    query = query.upper()

    if query == 'M' or query == 'F':
        mycursor.execute("select * from funcionarios where sexo = '{0}';" .format(query))
        myresult = mycursor.fetchall()

        for r in myresult:
            print(r)

    else:
        print("Entrada invalida!!!")

    conn.close()


def menuRelatorios_func():

    while True:
        print('\nRelatorios:')
        print('1. Quantidade de funcioanrios.')
        print('2. Quantidade gasta em salarios.')
        print('3. Buscar funcionarios por cargo.')
        print('4. Buscar funcionarios pelo nome.')
        print('5. Buscar funcionarios pelo sexo.')
        print('0. Sair')

        try:
            OPCAO = int(input("Entre com a opcao: "))

        except:
            print("Entrada invalida!!")
            menuRelatorios_func()

        if OPCAO == 1:
            quant_func()

        elif OPCAO == 2:
            quantGastaSalario_func()

        elif OPCAO == 3:
            buscaCargo()

        elif OPCAO == 4:
            buscaNome()

        elif OPCAO == 5:
            buscaSexo()
        elif OPCAO == 0:
            break
        else:
            print("Entrada invalida!!!")


def menu_func():

    while True:
        print('\nMenu dos Funcionarios:')
        print('1. Cadastar.')
        print('2. Listar.')
        print('3. Deletar.')
        print('4. Alterar.')
        print('5. Relatorios.')
        print('0. Sair.')

        OPCAO = int(input("Entre com a opcao: "))

        if OPCAO == 1:
            cadastrar_func()

        elif OPCAO == 2:
            listar_func()

        elif OPCAO == 3:
            deletar_func()

        elif OPCAO == 4:
            alterar_func()

        elif OPCAO == 5:
            menuRelatorios_func()

        elif OPCAO == 0:
            break

        else:
            print("Entrada Invalida!!!")


def main():

    init_server()
    menu_func()


if __name__ == '__main__':
    main()
