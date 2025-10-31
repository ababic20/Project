import axios from "axios";

//const API_URL = "http://127.0.0.1:9000";
const API_URL = "https://project-kj3g.onrender.com";


const authHeader = () => {
  const token = localStorage.getItem("token");
  return token ? { Authorization: `Bearer ${token}` } : {};
};

export const getTasks = async (week, category) => {
  try {
    const res = await axios.get(`${API_URL}/tasks`, {
      params: { week, category },
      headers: authHeader(),
    });
    return res.data;
  } catch (error) {
    console.error("Error fetching tasks:", error.response?.data || error.message);
    throw error;
  }
};

export const createTask = async (task) => {
  const res = await axios.post(`${API_URL}/tasks`, task, {
    headers: {
      "Content-Type": "application/json",
      ...authHeader(),
    },
  });
  return res.data;
};

export const updateTask = async (taskId, update) => {
  const res = await axios.put(`${API_URL}/tasks/${taskId}`, update, {
    headers: {
      "Content-Type": "application/json",
      ...authHeader(),
    },
  });
  return res.data;
};

export const deleteTask = async (taskId) => {
  return axios.delete(`${API_URL}/tasks/${taskId}`, {
    headers: authHeader(),
  });
};
