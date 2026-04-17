import { apiClient } from "./apiClient";

export function getBoards() {
  return apiClient("/boards");
}

export function createBoard(data) {
  return apiClient("/boards", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function getColumns(boardId) {
  return apiClient(`/boards/${boardId}/columns`);
}

export function createColumn(boardId, data) {
  return apiClient(`/boards/${boardId}/columns`, {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function getTasks() {
  return apiClient("/tasks");
}

export function createTask(data) {
  return apiClient("/tasks", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function moveTask(taskId, targetColumnId, newPosition) {
  return apiClient(`/tasks/${taskId}/move`, {
    method: "PATCH",
    body: JSON.stringify({
      column_id: targetColumnId,
      position: newPosition,
    }),
  });
}
