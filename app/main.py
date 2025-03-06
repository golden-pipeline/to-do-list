from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics
import psutil
import os

app = Flask(__name__)
metrics = PrometheusMetrics(app)

metrics.info('app_info', 'Application info', version='1.0.0')

# Configuração do PostgreSQL
POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
POSTGRES_DB = os.getenv("POSTGRES_DB", "todo_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres-service.postgress")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Modelo da Tabela
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)
    done = db.Column(db.Boolean, default=False)

# Criar tabelas automaticamente
with app.app_context():
    db.create_all()

# Contador de tarefas adicionadas
task_counter = metrics.counter("todo_tasks", "Number of tasks in the To-Do List")

@app.route("/")
def hello():
    return "Hello, DevOps v1.0.0 - To-Do List API"

# Criar nova tarefa
@app.route("/todo", methods=["POST"])
@task_counter
def create_task():
    data = request.json
    if "task" not in data:
        return jsonify({"error": "Task is required"}), 400

    new_task = Task(task=data["task"])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"id": new_task.id, "task": new_task.task, "done": new_task.done}), 201

# Listar todas as tarefas
@app.route("/todo", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{"id": t.id, "task": t.task, "done": t.done} for t in tasks])

# Atualizar uma tarefa (marcar como concluída)
@app.route("/todo/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    task.done = True
    db.session.commit()
    return jsonify({"id": task.id, "task": task.task, "done": task.done})

# Excluir uma tarefa
@app.route("/todo/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200

# Métricas de CPU e Memória
@metrics.gauge("cpu_percent", "CPU usage percent")
def cpu_percent():
    return psutil.cpu_percent()

@metrics.gauge("memory_percent", "Memory usage percent")
def memory_percent():
    return psutil.virtual_memory().percent

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
