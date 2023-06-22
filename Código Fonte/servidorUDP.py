# -------------------
# Servidor Socket UDP
# -------------------

# importando a biblioteca
import socket
import sqlite3
import json
import random

from supportFunctions import verifica_padrao, main_clients

def servidor_banco(HOST, PORT=9000):
    with open('server.json', 'r+') as file:
            data = json.load(file)
            data['server'] = HOST
            data['PORT'] = PORT
            file.seek(0)
            json.dump(data, file)
            file.truncate()

def ini_server_UDP(from_client: bool = False, HOST='', PORT=9000):
    
    if from_client == False:
        print("Eu sou o SERVIDOR UDP!")

        # Pegando IP dinamicamente
        hostname = socket.gethostname()
        HOST = socket.gethostbyname(hostname)
        print(HOST)
        servidor_banco(HOST)

        # Porta que o Servidor ficará escutando
        PORT = 9000

        # Criando o socket e associando ao endereço e porta
        servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        servidor.bind((HOST, PORT))


    else:
        print("Startando servidor temporario!")

        print(f"Eu sou o Servidor Temporario no cliente -> {HOST}:{PORT}")
        
        # Criando o socket e associando ao endereço e porta
        servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        servidor.bind((HOST, PORT))
        
        with open('clients.json', 'r') as j_data:
            clients_connected = json.load(j_data)
            
        clients_max = len(clients_connected['clients'])
    
    # cli_eleito_number = random.randrange(0, clients_max)
    
        
    
    
        for c in range(clients_max):
            try:
                client_host = clients_connected['clients'][c].split(':')[0]
                client_port = clients_connected['ports'][c]
                servidor.sendto("Sou o novo servidor".encode("utf-8"), (client_host,client_port))
            except:
                next

    print("Aguardando cliente...")


    conn = sqlite3.connect('registro_de_operacoes.db')
    cursor = conn.cursor()


    while (True):
        try:

            # cliente conectou - recuperando informações do cliente
            msg, enderecoCliente = servidor.recvfrom(PORT)

            main_clients(method='add', enderecoCliente=enderecoCliente)

            mensagem = msg.decode("utf-8")

            if mensagem == 'LOGIN':
                print(f"Cliente {enderecoCliente} se logou.")
                with open('clients.json', 'r') as j_data:
                    clients_connected = json.load(j_data)
                    clients_max = len(clients_connected['clients'])-1
                    porta_cliente = clients_connected['ports'][clients_max]
                    servidor.sendto(str(porta_cliente).encode("utf-8"), enderecoCliente)

            else:
                print(f"Cliente {enderecoCliente} enviou mensagem")
                print(f"Mensagem enviada pelo cliente: {mensagem}")
                print(f"Este servidor vai devolver a mensagem ao cliente {enderecoCliente}")

                solicitacao = mensagem.split('+')
                print(solicitacao)

                if (solicitacao[0] == 'G'):
                
                    if solicitacao[1] == '1':
                        consulta = cursor.execute(f'''
                        SELECT 
                        v.nome, 
                        SUM(r.valor) 
                        FROM registro r 
                        INNER JOIN vendedor v 
                            ON v.id = r.vendedor 
                        WHERE r.vendedor = {int(solicitacao[2])};
                        ''').fetchall()
                    
                        nome_vendedor = str(consulta[0][0])
                        valor_acumulado = str(round(consulta[0][1], 2))
                        resposta = f"O total de vendas do vendedor {nome_vendedor} é R$ {valor_acumulado}"
                        servidor.sendto(resposta.encode("utf-8"), enderecoCliente)
        
                    elif solicitacao[1] == '2':
                        consulta = cursor.execute(f'''
                        SELECT 
                        l.nome, 
                        SUM(r.valor) 
                        FROM registro r 
                        INNER JOIN lojas l 
                            ON l.id = r.loja 
                        WHERE r.loja = {int(solicitacao[2])};
                        ''').fetchall()
                    
                        nome_loja = str(consulta[0][0])
                        valor_acumulado = str(round(consulta[0][1], 2))
                        resposta = f"O total de vendas da loja {nome_loja} é R$ {valor_acumulado}"
                        servidor.sendto(resposta.encode("utf-8"), enderecoCliente)
        
                    elif solicitacao[1] == '3':
                        data_inicial = solicitacao[2]
                        data_final = solicitacao[3]
                        consulta = cursor.execute(f'''
                        SELECT 
                        sum(valor)
                        FROM registro 
                        WHERE data_venda BETWEEN '{data_inicial}' AND '{data_final}';
                        ''').fetchall()
                    
                        valor_total = str(round(consulta[0][0], 2))
                        resposta = f"O valor total das vendas da rede no período informado é R$ {valor_total}"
                        servidor.sendto(resposta.encode("utf-8"), enderecoCliente)
        
                    elif solicitacao[1] == '4':
                        consulta = cursor.execute(f'''
                        SELECT 
                        v.nome,
                        SUM(r.valor) 
                        FROM registro r 
                        INNER JOIN vendedor v 
                            ON r.vendedor = v.id 
                        GROUP BY v.nome 
                        ORDER BY SUM(r.valor) DESC 
                        LIMIT 1;
                        ''').fetchall()
                    
                        nome_vendedor = str(consulta[0][0])
                        valor_acumulado = str(round(consulta[0][1],2))
                        resposta = f"O melhor vendedor é {nome_vendedor} com um valor acumulado de R$ {valor_acumulado}"
                        servidor.sendto(resposta.encode("utf-8"), enderecoCliente)
        
                    elif solicitacao[1] == '5':
                        consulta = cursor.execute(f'''
                        SELECT 
                        l.nome, 
                        SUM(r.valor) 
                        FROM registro r 
                        INNER JOIN lojas l 
                        ON r.loja = l.id 
                        GROUP BY l.nome 
                        ORDER BY SUM(r.valor) DESC 
                        LIMIT 1;
                        ''').fetchall()
                    
                        nome_loja = str(consulta[0][0])
                        valor_acumulado = str(round(consulta[0][1],2))
                        resposta = f"A loja com mais vendeu é a loja {nome_loja} com um valor acumulado de R$ {valor_acumulado}"
                        servidor.sendto(resposta.encode("utf-8"), enderecoCliente)
                    
            
                elif (solicitacao[0] == 'V'):
                    cursor.execute(f'''
                    INSERT INTO 
                    registro (data_venda, operacao, vendedor, loja, valor) 
                    VALUES ("{solicitacao[1]}", {int(solicitacao[2])}, {int(solicitacao[3])}, {int(solicitacao[4])}, {solicitacao[5]})
                    ''')
                    conn.commit()
                    consulta = cursor.execute('''
                    SELECT 
                    R.data_venda AS "Data da Operação", 
                    O.tipo AS "Tipo de Operação", 
                    V.nome AS "Nome do Vendedor", 
                    L.nome AS "Nome da Loja", 
                    R.valor 
                    FROM registro R 
                    INNER JOIN lojas L 
                        ON R.loja = L.id 
                    INNER JOIN operacao O 
                        ON R.operacao = O.id 
                    INNER JOIN vendedor V 
                        ON R.vendedor = V.id;
                    ''').fetchall()
        
                    print(consulta)
                    resposta = "Resposta do servidor: OK - Operação registrada com sucesso\n"
                    servidor.sendto(resposta.encode("utf-8"), enderecoCliente)
            

                elif (solicitacao[0] == "S"):
                    # Fim da conversa. Servidor vai encerrar.
                    main_clients(method='delete', enderecoCliente=enderecoCliente)
                    resposta = "OFF"
                    servidor.sendto(resposta.encode("utf-8"), enderecoCliente)
        except:
            # servidor.close()
            # ini_server_UDP(from_client = True, HOST=HOST, PORT=PORT)
            next
    # print("Encerrando o servidor...")
    # servidor.close()


if __name__ == "__main__":
    ini_server_UDP()