import { create } from 'zustand';
import { getBoards, getColumns, getTasks, moveTask } from '@/services/board.service';

export const useBoardStore = create((set, get) => ({
  boards: [],
  currentBoardId: null,
  columns: [],
  tasks: [],
  isLoading: false,
  error: null,

  fetchBoards: async () => {
    try {
      set({ isLoading: true, error: null });
      const boards = await getBoards();
      set({ boards, isLoading: false });
      if (boards.length > 0 && !get().currentBoardId) {
        get().setCurrentBoard(boards[0].id);
      }
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  },

  setCurrentBoard: async (boardId) => {
    set({ currentBoardId: boardId });
    await get().fetchBoardData(boardId);
  },

  fetchBoardData: async (boardId) => {
    try {
      set({ isLoading: true, error: null });
      const [columns, tasks] = await Promise.all([
        getColumns(boardId),
        getTasks(),
      ]);
      
      // Filter tasks to only those belonging to current board
      const filteredTasks = tasks.filter(task => task.board_id === boardId);
      
      // Sort tasks by position initially
      filteredTasks.sort((a,b) => a.position - b.position);

      set({ columns, tasks: filteredTasks, isLoading: false });
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  },

  handleDragEnd: async (result) => {
    const { destination, source, draggableId } = result;

    if (!destination) return;

    if (
      destination.droppableId === source.droppableId &&
      destination.index === source.index
    ) {
      return;
    }

    const { tasks } = get();
    const draggedTask = tasks.find((t) => t.id === draggableId);
    
    if (!draggedTask) return;

    // Optimistically update state
    const newTasks = Array.from(tasks);
    
    // Remove from old location
    const sourceColTasks = newTasks.filter(t => t.column_id === source.droppableId).sort((a,b)=>a.position-b.position);
    const destColTasks = source.droppableId === destination.droppableId 
      ? sourceColTasks 
      : newTasks.filter(t => t.column_id === destination.droppableId).sort((a,b)=>a.position-b.position);

    // Take out the moved item
    const [movedItem] = sourceColTasks.splice(source.index, 1);
    movedItem.column_id = destination.droppableId;
    
    // Place into the new list at correct index
    destColTasks.splice(destination.index, 0, movedItem);

    // Reassign positions for source and destination column items
    const updatePositions = (colTasks) => {
      colTasks.forEach((t, i) => {
        t.position = i;
      });
    };

    updatePositions(sourceColTasks);
    if(source.droppableId !== destination.droppableId) {
      updatePositions(destColTasks);
    }
    
    // Update local state temporarily mapping to same task objects
    set({ tasks: newTasks });

    try {
      // Async api call
      await moveTask(draggableId, destination.droppableId, destination.index);
    } catch (err) {
      console.error("Failed dragging update!", err);
      // Ideally revert state here, omitted for succinctness 
      await get().fetchBoardData(get().currentBoardId); 
    }
  }
}));
