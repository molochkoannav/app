import socket
import urllib.parse
from pathlib import Path

HOST = '127.0.0.1'
PORT = 8080
BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / 'templates'


def read_html_file(filename):
    """Чтение HTML-файла с помощью контекстного менеджера"""
    file_path = TEMPLATES_DIR / filename
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None


def parse_request(request_data):
    """Разбор HTTP-запроса"""
    lines = request_data.split('\r\n')
    if not lines:
        return 'GET', '/', {}
    
    first_line = lines[0].split()
    method = first_line[0] if len(first_line) > 0 else 'GET'
    path = first_line[1] if len(first_line) > 1 else '/'
    
    body = ''
    body_start = request_data.find('\r\n\r\n')
    if body_start != -1:
        body = request_data[body_start + 4:]
    
    return method, path, body


def handle_get(path):
    """Обработка GET-запросов"""
    print(f"[GET] Запрос к: {path}")
    
    if path == '/' or path == '/contacts':
        html_content = read_html_file('contacts.html')
        if html_content:
            return '200 OK', html_content, 'text/html'
    
    #Страница 404
    html_content = read_html_file('non_page.html')
    if html_content:
        return '404 Not Found', html_content, 'text/html'
    
    return '404 Not Found', '<h1>404 - Страница не найдена</h1>', 'text/html'


def handle_post(path, body):
    """Обработка POST-запросов"""
    print(f"\n[POST] Запрос к: {path}")
    print(f"[POST] Тело запроса: {body}")
    
    if body:
        parsed_data = urllib.parse.parse_qs(body)
        print("=== ДАННЫЕ ИЗ ФОРМЫ ===")
        for key, values in parsed_data.items():
            print(f"{key}: {values[0] if values else ''}")
        print("========================\n")
    
    # После отправки формы показываем страницу контактов с сообщением
    html_content = read_html_file('contacts.html')
    if html_content:
        success_message = '<div class="alert alert-success mt-4">Сообщение отправлено!</div>'
        html_content = html_content.replace('<!-- message -->', success_message)
        return '200 OK', html_content, 'text/html'
    
    return '200 OK', '<h1>Форма отправлена!</h1>', 'text/html'


def handle_request(request_data):
    """Главная обработка запросов"""
    method, path, body = parse_request(request_data)
    
    if method == 'POST':
        return handle_post(path, body)
    else:
        return handle_get(path)


def run_server():
    """Запуск сервера"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    
    print(f"Сервер запущен на http://{HOST}:{PORT}")
    print("Нажмите Ctrl+C для остановки\n")
    
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            
            try:
                request_data = client_socket.recv(4096).decode('utf-8', errors='ignore')
                if not request_data:
                    continue
                
                status, content, content_type = handle_request(request_data)
                
                response = f"""HTTP/1.1 {status}
Content-Type: {content_type}; charset=utf-8
Content-Length: {len(content.encode('utf-8'))}
Connection: close

{content}"""
                
                client_socket.sendall(response.encode('utf-8'))
                
            except Exception as e:
                print(f"Ошибка: {e}")
            finally:
                client_socket.close()
                
    except KeyboardInterrupt:
        print("Сервер остановлен")
    finally:
        server_socket.close()


if __name__ == '__main__':
    run_server()