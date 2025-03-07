import { useEffect, useState } from "react";
import axios from "axios";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const API_URL = "http://localhost:5000/todo"; // Atualize para o endereço correto da API

// Definição do tipo Task
interface Task {
  id: number;
  task: string;
  done: boolean;
}

export default function TodoApp() {
  // Definição do estado com tipagem correta
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTask, setNewTask] = useState<string>("");

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      const response = await axios.get<Task[]>(API_URL);
      setTasks(response.data);
    } catch (error) {
      toast.error("Erro ao carregar tarefas");
    }
  };

  const addTask = async () => {
    if (!newTask.trim()) return toast.warning("Digite uma tarefa");
    try {
      await axios.post(API_URL, { task: newTask });
      setNewTask("");
      fetchTasks();
      toast.success("Tarefa adicionada");
    } catch (error) {
      toast.error("Erro ao adicionar tarefa");
    }
  };

  const markAsDone = async (id: number) => {
    try {
      await axios.put(`${API_URL}/${id}`);
      fetchTasks();
      toast.success("Tarefa concluída");
    } catch (error) {
      toast.error("Erro ao atualizar tarefa");
    }
  };

  const deleteTask = async (id: number) => {
    try {
      await axios.delete(`${API_URL}/${id}`);
      fetchTasks();
      toast.success("Tarefa excluída");
    } catch (error) {
      toast.error("Erro ao excluir tarefa");
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center bg-gray-100 p-4">
      <h1 className="text-2xl font-bold mb-4">To-Do List</h1>
      <div className="flex gap-2 mb-4">
        <input
          type="text"
          value={newTask}
          onChange={(e) => setNewTask(e.target.value)}
          className="border p-2 rounded"
          placeholder="Nova tarefa"
        />
        <button onClick={addTask} className="bg-blue-500 text-white p-2 rounded">Adicionar</button>
      </div>
      <ul className="w-full max-w-md bg-white p-4 shadow rounded">
        {tasks.map((task) => (
          <li key={task.id} className="flex justify-between items-center p-2 border-b">
            <span className={task.done ? "line-through text-gray-500" : ""}>{task.task}</span>
            <div className="flex gap-2">
              {!task.done && (
                <button onClick={() => markAsDone(task.id)} className="bg-green-500 text-white p-1 rounded">✔</button>
              )}
              <button onClick={() => deleteTask(task.id)} className="bg-red-500 text-white p-1 rounded">✖</button>
            </div>
          </li>
        ))}
      </ul>
      <ToastContainer position="top-right" autoClose={2000} />
    </div>
  );
}
