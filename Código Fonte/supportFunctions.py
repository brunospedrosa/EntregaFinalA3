import re
import json

# Função para verificar o padrão da data e valor
def verifica_padrao(registro):
    data = r"\d{2}-\d{2}-\d{4}"
    valor = r"\d{2}\,\d{2}"
    # valor = r"R\$ \d+\,\d{2}"
    return re.match(data, registro['Data']) and re.match(valor, registro['Valor'])


def main_clients(method, enderecoCliente):
    with open('clients.json', 'r') as j_data:
        clients_j = json.load(j_data)
        
    
    cli_id = enderecoCliente[0]+":"+str(enderecoCliente[1])


    if method == 'add':
        if cli_id not in clients_j['clients']:
            clients_j['clients'].append(cli_id)
    
    elif method == 'delete':
        if cli_id in clients_j['clients']:
            clients_j['clients'].remove(cli_id)


    with open('clients.json', 'w') as outfile:
        json.dump(clients_j, outfile)
