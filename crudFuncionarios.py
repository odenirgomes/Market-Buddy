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
        mycursor.execute('create table if not exists funcionarios (cod_func int not null auto_increment, nome varchar(20) not null, snome varchar(20) not null, sexo enum("M", "F"), cargo varchar(20), salario decimal(8,2), primary key(cod_func))ENGINE=InnoDB DEFAULT CHARSET=utf8;')

    except Error as e1:
        mycursor.execute('create database if not exists mbdatabase default character set utf8 default collate utf8_general_ci;')
        mycursor.execute('use mbdatabase;')
        mycursor.execute('create table funcionarios (cod_func int not null auto_increment, nome varchar(20) not null, snome varchar(20) not null, sexo enum("M", "F"), cargo varchar(20), salario decimal(8,2), primary key(cod_func))ENGINE=InnoDB DEFAULT CHARSET=utf8;')

    conn.close()

def cadastrar():

    # Conecção com o servidor de BD e a criação de um curso para executar comandos em sql
    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute('use mbdatabase;')

    print("\nCadastrar Funcionario: ")

    try:
        nome = input("Nome: ")
    except:
        print("Erro na entrada!!")
        cadastrar()

    try:
        snome = input("Sobrenome: ")
    except:
        print("Erro na entrada!!")
        cadastrar()

    sexo = input("Sexo: Masc<M> ou Femi<F>: ")
    sexo = sexo.upper()
    if sexo != 'M' and sexo != 'F':
        print("\nEntrada invalida!!!")
        print("Entre com o valor certo do sexo!")
        cadastrar()

    try:
        cargo = input("Cargo: ")
    except:
        print("Erro na entrada!!")
        cadastrar()

    try:
        salario = float(input("Salario: "))

    except:
        print("\nEntrada invalida!!!")
        print("Entre com o tipo correto de salario!")
        cadastrar()

    try:
        mycursor.execute("INSERT INTO funcionarios (nome, snome, sexo, cargo, salario) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}');" .format(nome, snome, sexo, cargo, salario))
    except:
        print("Erro de cadastro!!")
        cadastrar()
    #Execução do comando de insert no BD
    conn.commit()
    print("Registro cadastrado!")

    #Fechando conecção com BD
    conn.close()


def listar():

    print("\nListar funcionarios:")
    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute('use mbdatabase;')

    mycursor.execute('select * from funcionarios;')
    myresult = mycursor.fetchall()

    for r in myresult:
        print(r)

    conn.close()


def deletar():

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute('use mbdatabase;')

    print("\nDeletar funcionario:")
    listar()

    try:
        id = int(input("Entre com o codigo do funcionario que deseja deletar: "))

    except:
        print("Entre com um valor inteiro no codigo!!")
        deletar()

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


def alterar():

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute('use mbdatabase;')

    print("\nAlterar funcionario:")
    listar()

    try:
        id = int(input("Entre com o codigo do funcionario que deseja alterar: "))

    except Error as E1:
        print("Entre com valor inteiro em codigo")
        alterar()

    mycursor.execute("select * from funcionarios where cod_func = '{0}';" .format(id))
    myresult = mycursor.fetchall()
    print("Registro selecionado ->", myresult)

    try:
        nome = input("Nome: ")
    except:
        print("Erro na entrada!!")
        alterar()

    try:
        snome = input("Sobrenome: ")
    except:
        print("Erro na entrada!!")
        alterar()

    sexo = input("Sexo: Masc<M> ou Femi<F>: ")
    sexo.upper()
    if sexo != 'M' and sexo != 'F' and sexo != "":
        print("\nEntrada invalida!!!")
        print("Entre com o valor certo do sexo!")
        alterar()

    try:
        cargo = input("Cargo: ")
    except:
        print("Erro na entrada!!")
        alterar()


    salario = input("Salario: ")
    if salario in string.ascii_letters and salario != '':
        print("Tipo de entrada invalida!!!")
        alterar()

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


def quant():

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute('use mbdatabase;')

    mycursor.execute('select count(*) from funcionarios;')
    myresult = mycursor.fetchone()
    print("\nNumeros de funcionarios: ", myresult[0])

    conn.close()


def quantGastaSalario():

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute('use mbdatabase;')

    mycursor.execute('select sum(salario) from funcionarios;')
    myresult = mycursor.fetchone()
    print("\nQuantidade gasta em salarios: ", myresult[0])

    conn.close()


def buscar():

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute('use mbdatabase;')

    print("\nBuscar funcioanrios: ")
    print("1. Nome.")
    print("2. Sobrenome.")
    print("3. Sexo")
    print("4. Cargo.")
    print("5. Salario.")

    try:
        OPCAO = int(input("Entre com a opcao de busca: "))
    except:
        print("Erro de entrada!!")
        buscar()

    if OPCAO == 1:
        OPCAO = 'nome'

    elif OPCAO == 2:
        OPCAO = 'snome'

    elif OPCAO == 3:
        OPCAO = 'sexo'

    elif OPCAO == 4:
        OPCAO = 'cargo'

    elif OPCAO == 5:
        OPCAO = 'salario'

    else:
        print("Entrada invalida!!")
        buscar()

    try:
        query = input("Pesquisar: ")
    except:
        print("Erro de entrada!!")
        buscar()

    try:
        mycursor.execute("select * from funcionarios where {0} = '{1}';" .format(OPCAO, query))
    except:
        print("Erro de pesquisa!!")
        buscar()

    myresult = mycursor.fetchall()

    for r in myresult:
        print(r)

    conn.close()


def menuRelatorios():

    while True:
        print('\nFuncionarios')
        print('Menu Relatorios:')
        print('1. Quantidade de funcioanrios.')
        print('2. Quantidade gasta em salarios.')
        print('3. Buscar funcionarios.')
        print('0. Sair')

        try:
            OPCAO = int(input("Entre com a opcao: "))

        except:
            print("Entrada invalida!!")
            menuRelatorios()

        if OPCAO == 1:
            quant()

        elif OPCAO == 2:
            quantGastaSalario()

        elif OPCAO == 3:
            buscar()

        elif OPCAO == 0:
            break
        else:
            print("Entrada invalida!!!")


def menu():

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
            print("Entrada Invalida!!!")


def main():

    init_server()
    menu()


if __name__ == '__main__':
    main()
