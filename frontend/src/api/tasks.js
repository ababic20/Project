import axios from "axios";
const API_URL = "https://project-kj3g.onrender.com";

export const getTasks = async (week, category) => {
  const res = await axios.get(`${API_URL}/tasks`, {
    params: { week, category }
  });
  return res.data;
};

export const createTask = async (task) => {
  const res = await axios.post(`${API_URL}/tasks`, task);
  return res.data;
};

export const updateTask = async (taskId, update) => {
  const res = await axios.put(`${API_URL}/tasks/${taskId}`, update);
  return res.data;
};

export const deleteTask = async (taskId) => {
  return axios.delete(`${API_URL}/tasks/${taskId}`);
};
