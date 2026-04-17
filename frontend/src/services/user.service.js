import { apiClient } from "./apiClient";

export function handleRegister(data, type) {
  return apiClient(`/auth/${type}`, {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function getUsers() {
  return apiClient("/users");
}

export function getUserById(id) {
  return apiClient(`/users/${id}`);
}
