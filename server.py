import socket
import threading
from pymongo import MongoClient

client = MongoClient("mongodb://mongoadmin:secret@localhost:27017/")
db = client['questions']
questions_collection = db['questions']

def handle_client(client_socket):
    score = 0  # Inicializa a pontuação do cliente

    for question in questions_collection.find().limit(3):
        question_text = question['question'] + "\n"
        options = question['options']

        for idx, choice in enumerate(options):
            question_text += f"{idx}) {choice}\n"

        client_socket.sendall(str.encode(question_text))

        while True:
            user_answer = client_socket.recv(1024).decode().strip()
            if user_answer.isdigit() and 0 <= int(user_answer) < len(options):
                break
            else:
                client_socket.sendall(str.encode("Opção inválida. Por favor, insira um número válido.\n"))

        correct_answer_index = int(question['correct_answer'])

        if user_answer == str(correct_answer_index):
            score += 1  # Incrementa a pontuação se a resposta estiver correta
            feedback = "\nResposta correta!\n"
        else:
            feedback = f"\nResposta Errada! A resposta correta é a opção {correct_answer_index}\n"

        client_socket.sendall(str.encode(feedback))

    # Após todas as questões terem sido respondidas, envie a pontuação final
    final_message = f"Você acertou {score} de 3 questões.\n"
    client_socket.sendall(str.encode(final_message))

    print("Fechando conexão...")
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 20000))
    server.listen(5)

    print("Aguardando conexão...")

    while True:
        client_socket, addr = server.accept()
        print("Conexão estabelecida:", addr)

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    main()
