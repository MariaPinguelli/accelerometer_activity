from flask import Flask, render_template, request
from flask_socketio import SocketIO
import ssl
# Configurações
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('client.html')

@socketio.on('connect')
def handle_connect():
    print(f'Cliente conectado: {request.sid} | IP: {request.remote_addr}')

@socketio.on('disconnect')
def handle_disconnect():
    print(f'Cliente desconectado: {request.sid}')

@socketio.on('accel_data')
def handle_accel_data(data):
    print(f"Dados acelerômetro - X: {data.get('x', 0):.2f}, Y: {data.get('y', 0):.2f}, Z: {data.get('z', 0):.2f}")

if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('local-ca.crt', 'local-ca.key')
    
    print("Servidor HTTPS rodando em https://localhost:5000")
    socketio.run(app, 
                host='0.0.0.0', 
                port=5000, 
                ssl_context=context,
                debug=True)