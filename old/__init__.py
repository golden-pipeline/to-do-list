from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
import psutil
from old.database import db, init_db
from old.routes import bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ncdferr:Nic11089@postgres-service.postgres:5432/flask-app-db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)

metrics = PrometheusMetrics(app)

metrics.info('app_info', 'Application info', version='1.0.0')

@metrics.gauge('cpu_percent', 'CPU usage percent')
def cpu_percent():
    return psutil.cpu_percent()

@metrics.gauge('memory_percent', 'Memory usage percent')
def memory_percent():
    return psutil.virtual_memory().percent

app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)