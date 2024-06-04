import socket
import os

def send_file(client_socket, file_path):
    file_name = os.path.basename(file_path)
    client_socket.sendall(b"FILE")
    client_socket.sendall(file_name.encode())

    with open(file_path, 'rb') as file:
        while (file_data := file.read(1024)):
            client_socket.sendall(file_data)
    client_socket.sendall(b"EOF")  # Send EOF marker to indicate end of file
    print(client_socket.recv(1024).decode())

def start_client(host='localhost', port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connected to {host}:{port}")

    try:
        while True:
            choice = input("Enter 'msg' to send message or 'file' to send a file: ").strip().lower()
            if choice == 'msg':
                message = input("Enter message: ")
                if message.lower() == 'exit':
                    break
                client_socket.sendall(message.encode())
                data = client_socket.recv(1024)
                print(f"Received: {data.decode()}")
            elif choice == 'file':
                file_path = input("Enter the path of the file to send: ").strip()
                if os.path.exists(file_path):
                    send_file(client_socket, file_path)
                else:
                    print("File does not exist.")
            else:
                print("Invalid choice.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()
