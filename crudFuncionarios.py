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
        mycursor.execute('use mysqlbd002;')

    except Error as e1:
        mycursor.execute('create database if not exists mysqlbd002 default character set utf8 default collate utf8_general_ci;')
        mycursor.execute('use mysqlbd002;')

        mycursor.execute('create table funcionarios (cod_func int not null auto_increment, nome_func varchar(20) not null, snome_func varchar(20) not null, sexo_func enum("M", "F"), cargo_func varchar(20), salario_func decimal(8,2), primary key(cod_func));')

    conn.close()

def cadastrar_func():

    # Conecção com o servidor de BD e a criação de um curso para executar comandos em sql
    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute('use mysqlbd002;')

    print("\nCadastrar Funcionario: ")
    nome = input("Nome: ")
    snome = input("Sobrenome: ")
    sexo = input("Sexo: Masc<M> ou Femi<F>: ")
    sexo.upper()
    cargo = input("Cargo: ")
    salario = input("Salario: ")

    mycursor.execute("INSERT INTO funcionarios (nome_func, snome_func, sexo_func, cargo_func, salario_func) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}');" .format(nome, snome, sexo, cargo, salario))
    #Execução do comando de insert no BD
    conn.commit()
    print("Registro cadastrado!")

    #Fechando conecção com BD
    conn.close()


def listar_func():

    print("\nListar funcionarios:")
    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute('use mysqlbd002;')

    mycursor.execute('select * from funcionarios;')
    myresult = mycursor.fetchall()

    for r in myresult:
        print(r)

    conn.close()


def deletar_func():

    print("\nDeletar funcionario:")
    listar_func()

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute('use mysqlbd002;')

    try:
        id = int(input("Entre com o codigo do funcionario que deseja deletar: "))

    except Error as e1:
        print(e1)

    mycursor.execute("select * from funcionarios where cod_func = '{0}';" .format(id))
    myresult = mycursor.fetchall()
    print("Registro selecionado ->", myresult)

    print("Tem certeza que deseja deletar esse registro?")
    OPCAO = input("Sim<S> ou NAO<N>: ")
    # Erro a função upper não esta funcionando na variavel OPCAO, não sei o pq ela é uma variavel str
    OPCAO.upper()

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

    print("\nAlterar funcionario:")
    listar_func()

    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute('use mysqlbd002;')

    try:
        id = int(input("Entre com o codigo do funcionario que deseja alterar: "))

    except Error as e1:
        print(e1)

    mycursor.execute("select * from funcionarios where cod_func = '{0}';" .format(id))
    myresult = mycursor.fetchall()
    print("Registro selecionado ->", myresult)

    nome = input("Nome: ")
    snome = input("Sobrenome: ")
    sexo = input("Sexo: Masc<M> ou Femi<F>: ")
    sexo.upper()
    cargo = input("Cargo: ")
    salario = input("Salario: ")

    if nome != "":
        mycursor.execute("update funcionarios set nome_func = '{0}' where cod_func = '{1}';" .format(nome, id))

    if snome != "":
        mycursor.execute("update funcionarios set snome_func = '{0}' where cod_func = '{1}';" .format(snome, id))

    if sexo != "":
        mycursor.execute("update funcionarios set sexo_func = '{0}' where cod_func = '{1}';" .format(sexo, id))

    if cargo != "":
        mycursor.execute("update funcionarios set cargo_func = '{0}' where cod_func = '{1}';" .format(cargo, id))

    if salario != "":
        mycursor.execute("update funcionarios set salario_func = '{0}' where cod_func = '{1}';" .format(salario, id))

    conn.commit()
    conn.close()



def menuRelatorios_func():

    while True:
        print('\nMenu de relatorios de funcionarios.')
        print('1. Quantidade de funcioanrios.')
        print('2. Quantidade gasta em salarios.')
        print('3. Buscar funcionarios por cargo.')
        print('4. Buscar funcionarios pelo nome.')
        print('5. Buscar funcionarios pelo sexo.')
        print('0. Sair')

        OPCAO = int(input("Entre com a opcao: "))
        if OPCAO == 1:
            pass
        elif OPCAO == 2:
            pass
        elif OPCAO == 3:
            pass
        elif OPCAO == 4:
            pass
        elif OPCAO == 5:
            pass
        elif OPCAO == 0:
            break
        else:
            print("Entrada invalida!!!")

def menu_func():

    while True:
        print('\nMenu')
        print('1. Cadastar funcionario.')
        print('2. Listar funcionarios.')
        print('3. Deletar funcionario.')
        print('4. Alterar funcionario.')
        print('5. Menu Relatorios.')
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



    # Conecta a a entrada do server a um cursor


    #mycursor.execute('select * from gafanhotos;')

    #myresult = mycursor.fetchall()

    #for x in myresult:
        #print(x)




if __name__ == '__main__':
    main()
