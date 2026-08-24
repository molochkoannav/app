import socket
import urllib.parse
from pathlib import Path

HOST = '127.0.0.1'
PORT = 8081
BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / 'templates'
STATIC_DIR = BASE_DIR / 'static'


def read_html_file(filename):
    """Чтение HTML-файла с помощью контекстного менеджера"""
    file_path = TEMPLATES_DIR / filename
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None


def read_static_file(path):
    """Чтение статических файлов (CSS, JS, изображения)"""
    relative_path = path[8:]  
    file_path = STATIC_DIR / relative_path
    
    if not file_path.exists():
        return None, None
    
    
    ext = file_path.suffix.lower()
    content_type = {
        '.css': 'text/css',
        '.js': 'application/javascript',
        '.html': 'text/html',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.svg': 'image/svg+xml',
        '.ico': 'image/x-icon',
        '.txt': 'text/plain'
    }.get(ext, 'application/octet-stream')
    
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
        return content, content_type
    except Exception:
        return None, None


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
    
    # Обработка статических файлов
    if path.startswith('/static/'):
        content, content_type = read_static_file(path)
        if content:
            return '200 OK', content, content_type
        else:
            return '404 Not Found', b'File not found', 'text/plain'
    
    # Страница контактов
    if path == '/' or path == '/contacts':
        html_content = read_html_file('contacts.html')
        if html_content:
            return '200 OK', html_content, 'text/html'
    
    # Страница 404
    html_content = read_html_file('non_page.html')
    if html_content:
        return '404 Not Found', html_content, 'text/html'
    
    return '404 Not Found', '<h1>404 - Страница не найдена</h1>', 'text/html'


def handle_post(path, body):
    """Обработка POST-запросов"""
    print(f"\n[POST] Запрос к: {path}")
    print(f"[POST] Тело запроса: {body}")
    
    # Парсим данные формы
    form_data = {}
    if body:
        parsed_data = urllib.parse.parse_qs(body)
        print("=== ДАННЫЕ ИЗ ФОРМЫ ===")
        for key, values in parsed_data.items():
            value = values[0] if values else ''
            form_data[key] = value
            print(f"{key}: {value}")
        print("========================\n")
    
    # Читаем шаблон
    html_content = read_html_file('contacts.html')
    if html_content:
       
        if form_data:
            data_block = f'''
            <div class="form-data" style="margin-top: 20px; padding: 15px; background: #f0f7ff; border-radius: 8px; border-left: 4px solid #2b1b40;">
                <h3 style="margin-top: 0; color: #2b1b40;">Данные успешно отправлены!</h3>
                <p style="margin: 8px 0;"><strong>Имя:</strong> {form_data.get('name', '')}</p>
                <p style="margin: 8px 0;"><strong>Email:</strong> {form_data.get('email', '')}</p>
                <p style="margin: 8px 0;"><strong>Сообщение:</strong> {form_data.get('message', '')}</p>
            </div>
            '''
    
            html_content = html_content.replace('<!-- form_data -->', data_block)
        else:
          
            html_content = html_content.replace('<!-- form_data -->', '')
        
        return '200 OK', html_content, 'text/html'
    
    return '200 OK', '<h1>Форма отправлена!</h1>', 'text/html'


def handle_request(request_data):
    """Главная обработка запросов"""
    method, path, body = parse_request(request_data)
    
    if method == 'POST':
        return handle_post(path, body)
    else:
        return handle_get(path)


def build_response(status, content, content_type):
    """Создание HTTP ответа"""
    # Определяем статус
    status_code = status.split()[0]
    
    # Если content - строка, кодируем в байты
    if isinstance(content, str):
        content = content.encode('utf-8')
    elif content is None:
        content = b''
    
    response = f"""HTTP/1.1 {status}
Content-Type: {content_type}; charset=utf-8
Content-Length: {len(content)}
Connection: close

"""
    return response.encode('utf-8') + content


def run_server():
    """Запуск сервера"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    
    print(f"🚀 Сервер запущен на http://{HOST}:{PORT}")
    print(f"📁 Templates: {TEMPLATES_DIR}")
    print(f"📁 Static: {STATIC_DIR}")
    print(f"📄 Страница контактов: http://{HOST}:{PORT}/contacts")

    
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            
            try:
                request_data = client_socket.recv(4096).decode('utf-8', errors='ignore')
                if not request_data:
                    continue
                
                status, content, content_type = handle_request(request_data)
                response = build_response(status, content, content_type)
                client_socket.sendall(response)
                
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