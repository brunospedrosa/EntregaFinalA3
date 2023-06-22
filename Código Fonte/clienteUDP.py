# ------------------
# Cliente Socket UDP
# ------------------

print("Eu sou um CLIENTE UDP!")

# Importando a biblioteca
import socket
from datetime import date
import json
from servidorUDP import ini_server_UDP
from supportFunctions import main_clients


def servidor_banco(HOST, PORT=9000):
    with open('server.json', 'r+') as file:
            data = json.load(file)
            data['server'] = HOST
            data['PORT'] = PORT
            file.seek(0)
            json.dump(data, file)
            file.truncate()

def eleicao(HOST, PORT):
    # Criando o socket e associando ao endereço e porta
    PORTACLIENTE = PORT
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor.bind((HOST, PORT))
    with open('clients.json', 'r') as j_data:
            clients_connected = json.load(j_data)
        
    clients_max = len(clients_connected['clients'])
    print('clientes max', clients_max)
    
    # cli_eleito_number = random.randrange(0, clients_max)
    cli_eleito_number = clients_max - 1
    
    client_eleito = clients_connected['clients'][cli_eleito_number]
    porta_cliente = clients_connected['ports'][cli_eleito_number]
    
    HOST, PORT = [client_eleito.split(':')[0], porta_cliente]
    servidor_banco(HOST, PORT)
    if PORTACLIENTE == PORT:
        servidor.close()
        ini_server_UDP(from_client=True, HOST=HOST, PORT=PORT)
    else:
        msg, endereco = servidor.recvfrom(PORT)
        servidor.close()
        ini_clientUDP(HOST, PORT)
    
    
    


def menu():

    perfil = ''
    opcao = ''
    parametro = ''

    while perfil not in ['V', 'v', 'G', 'g', 's', 'S']:
        perfil = input("Selecione seu perfil:\n G - Gerente\n V - Vendedor\n S - Sair\n")
  
    if perfil.upper() == 'G':

        while opcao not in ['1', '2', '3', '4', '5']:
            opcao = input("Por favor, selecione uma das seguintes opções:\n 1 - Total de vendas de um vendedor\n 2 - Total de vendas de uma loja\n 3 - Total de vendas da rede de lojas em um período\n 4 - Melhor vendedor\n 5 - Melhor loja\n")
        if opcao == '1':
            while parametro not in ['1', '2', '3', '4', '5']:
                parametro = input("Por favor selecione um dos seguintes vendedores:\n 1 - Bruno\n 2 - Cleriston\n 3 - Danilo\n 4 - Ingryd\n 5 - Michel\n")
        elif opcao == '2':
            while parametro not in ['1', '2', '3']:
                parametro = input("Por favor selecione uma das seguintes lojas:\n 1 - Centro\n 2 - Shopping\n 3 - Orla\n")
        elif opcao == '3':
            dtIni = input("Por favor informe a data inicial: FORMATO => AAAA-MM-DD\n")
            dtFim = input("Por favor informe a data final: FORMATO => AAAA-MM-DD\n")
            parametro = dtIni + '+' + dtFim
   
        return (perfil + '+' + opcao + '+' + parametro).upper()

    elif perfil.upper() == 'V':
        
        data = date.today().strftime("%Y-%m-%d")
        venda = '1'
        loja = input("Por favor selecione uma das seguintes lojas:\n 1 - Centro\n 2 - Shopping\n 3 - Orla\n")
        vendedor = input("Por favor selecione um dos seguintes vendedores:\n 1 - Bruno\n 2 - Cleriston\n 3 - Danilo\n 4 - Ingryd\n 5 - Michel\n")
        valor = input("Resposta do servidor: Por favor, informe o valor da venda no formato => ##.##\n")

        if ',' in valor:
            valor = valor.replace(',','.')
   
        return (perfil + '+' + data + '+' + venda + '+' + vendedor + '+' + loja + '+' + valor).upper()
    else:

        return perfil



# Definindo ip e porta
# hostname = socket.gethostname()

def ini_clientUDP(HOST='', PORT=''):
    
    if HOST == '' and PORT == '':
        with open('server.json', 'r') as j_data:
            server_connected = json.load(j_data)
    
        HOST = server_connected['server']
        PORT = server_connected['PORT']
    
    # print(HOST, PORT)
    
   
    # Criando o socket
    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Define o endereco do servidor (Ip e porta)
    enderecoServidor = (HOST, PORT)

    print("Vou começar a mandar mensagens para o servidor.")

    # Aqui começa a conversa
    print("Entrando com mensagem de texto para enviar")

    cliente.sendto("LOGIN".encode("utf-8"), enderecoServidor)
    msg, endereco = cliente.recvfrom(PORT)
    PORTACLIENTE = int(msg.decode("utf-8"))

    mensagem = menu()

    while (True):
        try:
            # Enviando mensagem ao servidor
            print("... Vou mandar uma mensagem para o servidor")
            cliente.sendto(mensagem.encode("utf-8"), enderecoServidor)

            # Recebendo resposta do servidor
            # try:
            msg, endereco = cliente.recvfrom(PORT)
            print("... O servidor me respondeu:", msg.decode("utf-8"))
            # except Exception as e:
                # next
            if msg.decode("utf-8") == 'OFF':
                print("... Encerrando o cliente")
                cliente.close()
                break

            # Obtendo nova mensagem do usuário
            print("... Entrando com nova mensagem de texto para enviar")
            mensagem = menu()
        except Exception as e:
            print(e)
            eleicao(HOST, PORTACLIENTE)
            
            



ini_clientUDP(HOST='', PORT='')