import sqlite3


def creating_tables():
    try:
        #CRIANDO O BANCO
        conn = sqlite3.connect('registro_de_operacoes.db')
        cursor = conn.cursor()
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS lojas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        nome VARCHAR(150) NOT NULL)
                ''')

        cursor.execute('''
                    INSERT OR IGNORE INTO lojas (id, nome) VALUES 
                    (1, 'Centro'), 
                    (2, 'Shopping'), 
                    (3, 'Orla')
                    ''')


        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS operacao (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        tipo VARCHAR(150) NOT NULL
                        )''')
        cursor.execute('''
                    INSERT OR IGNORE INTO operacao (id, tipo) VALUES 
                    (1, 'Venda'), 
                    (2, 'Troca')
                    ''')

        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS vendedor (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        nome VARCHAR(150) NOT NULL
                        )''')
        cursor.execute('''
                    INSERT OR IGNORE INTO vendedor (id, nome) VALUES 
                    (1, 'Bruno'), 
                    (2, 'Cleriston'), 
                    (3, 'Danilo'), 
                    (4, 'Ingryd'), 
                    (5, 'Michel')
                    ''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS registro (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        data_venda DATE NOT NULL,
                        operacao INTEGER NOT NULL,
                        vendedor INTEGER NOT NULL,
                        loja INTEGER NOT NULL,
                        valor FLOAT NOT NULL,
                        FOREIGN KEY (operacao) REFERENCES operacao(id),
                        FOREIGN KEY (vendedor) REFERENCES vendedor(id),
                        FOREIGN KEY (loja) REFERENCES lojas(id))
            ''')

        conn.commit()

        print("Tables Created")
    
    except Exception as e:
        print("Tables not created", e)

if __name__ == "__main__":
    creating_tables()