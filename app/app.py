from prometheus_flask_exporter import PrometheusMetrics
from flask import Flask

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Exemplo de métrica personalizada
metrics.info('app_info', 'Application info', version='1.0.0')

@app.route('/')
def hello():
    return "Hello, DevOps v1.0.0"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)