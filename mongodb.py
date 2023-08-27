import pymongo

# Conecte-se ao MongoDB com autenticação
client = pymongo.MongoClient("localhost", 27017, username='mongoadmin', password='secret')

# Escolha o banco de dados e a coleção
db = client.questions  # Nome do banco de dados
collection = db.questions  # Nome da coleção


# Lista de perguntas e respostas (agora como dicionários)
questions = [
    {
        "question": "Qual é a capital da França?",
        "options": ["Paris", "Londres", "Berlim", "Madri"],
        "correct_answer": "0"
    },
    {
        "question": "Qual é a capital do Brasil?",
        "options": ["São Paulo", "Brasília", "Amazonas", "Rio de Janeiro"],
        "correct_answer": "1"
    },
    {
        "question": "Qual é o nome de um dos 7 anões?",
        "options": ["Soneca", "João", "Pedro", "José"],
        "correct_answer": "0"
    }
]

# Insira as perguntas no MongoDB
try:
    for question in questions:
        collection.insert_one(question)
    print("Documentos inseridos com sucesso.")
except Exception as e:
    print(f"Erro ao inserir documentos: {e}")

# Feche a conexão com o MongoDB
client.close()
