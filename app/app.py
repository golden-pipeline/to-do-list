from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

# Inicia as métricas
metrics = PrometheusMetrics(app)

# Registra a métrica app_info diretamente
metrics.info('app_info', 'Application info', version='1.0.0')

@app.route('/')
def hello():
    return "Hello, DevOps v1.0.0"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)