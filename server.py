import socket
import os

def start_server(host='localhost', port=12345, save_dir='D:/py/Downloads'):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    conn, addr = server_socket.accept()
    print(f"Connection from {addr}")

    while True:
        data = conn.recv(1024)
        if not data:
            break
        data_decoded = data.decode()

        if data_decoded == "FILE":
            # Handle file reception
            file_name = conn.recv(1024).decode()
            file_path = os.path.join(save_dir, file_name)

            with open(file_path, 'wb') as file:
                while True:
                    file_data = conn.recv(1024)
                    if file_data.endswith(b"EOF"):
                        file_data = file_data[:-3]  # Remove the EOF marker
                        if file_data:
                            file.write(file_data)
                        break
                    file.write(file_data)
            print(f"File {file_name} received and saved to {save_dir}")
            conn.sendall(b"File received")
        else:
            print(f"Received: {data_decoded}")
            response = input("Enter response: ")
            conn.sendall(response.encode())

    conn.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()
