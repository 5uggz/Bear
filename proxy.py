import socket
import threading

def proxy_handler(client_socket, remote_host, remote_port):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))  # Added closing parenthesis

    while True:
        data = client_socket.recv(4096)
        if len(data) == 0:
            break
        remote_socket.send(data)

        remote_data = remote_socket.recv(4096)
        if len(remote_data) == 0:
            break
        client_socket.send(remote_data)

    client_socket.close()
    remote_socket.close()

def main():
    remote_host = "duckduckgo.com"  # Use DuckDuckGo's hostname
    remote_port = 80
    remote_path = "/html"  # Specify a path (e.g., the DuckDuckGo HTML page)


    # Set up the listening socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 8888))
    server.listen(5)

    print("Proxy server is listening on port 8888...")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr[0]}:{addr[1]}")

        # Create a thread to handle the client
        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port))
        proxy_thread.start()

if __name__ == '__main__':
    main()
