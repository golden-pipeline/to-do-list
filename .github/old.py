from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
import psutil

app = Flask(__name__)
metrics = PrometheusMetrics(app)

metrics.info('app_info', 'Application info', version='1.0.0')

@app.route('/')
def hello():
    return "Hello, DevOps v1.0.0"

#Métricas de CPU e Memória.
@metrics.gauge('cpu_percent', 'CPU usage percent')
def cpu_percent():
    return psutil.cpu_percent()

@metrics.gauge('memory_percent', 'Memory usage percent')
def memory_percent():
    return psutil.virtual_memory().percent

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)