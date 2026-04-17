"use client";
import React from 'react';
import { Droppable } from '@hello-pangea/dnd';
import { useBoardStore } from '@/store/boardStore';
import TaskCard from './TaskCard';

export default function Column({ column }) {
  const { tasks } = useBoardStore();
  
  // Filter tasks that belong to this column
  const columnTasks = tasks.filter(task => task.column_id === column.id)
    .sort((a,b) => a.position - b.position);

  return (
    <div className="flex flex-col w-80 flex-shrink-0 bg-[#e4ebf5] rounded-xl max-h-full">
      {/* Column Header */}
      <div className="px-4 pt-4 pb-3 flex items-center justify-between">
        <h3 className="font-semibold text-slate-800 text-[15px] flex items-center">
          {column.title}
          <span className="ml-2 bg-slate-200/80 text-slate-600 text-xs py-0.5 px-2 rounded-full font-medium">
            {columnTasks.length}
          </span>
        </h3>
      </div>

      {/* Droppable Area */}
      <Droppable droppableId={column.id}>
        {(provided, snapshot) => (
          <div
            ref={provided.innerRef}
            {...provided.droppableProps}
            className={`flex-1 overflow-y-auto px-3 pb-3 min-h-[150px] transition-colors ${
              snapshot.isDraggingOver ? "bg-[#d8e2f0]" : ""
            }`}
          >
            {columnTasks.map((task, index) => (
              <TaskCard key={task.id} task={task} index={index} />
            ))}
            {provided.placeholder}
          </div>
        )}
      </Droppable>

      {/* Add Task Button */}
      <div className="p-3 pt-0">
        <button className="w-full text-left text-sm text-slate-500 hover:text-slate-800 hover:bg-slate-200 py-2 px-3 rounded-lg transition-colors flex items-center font-medium">
          <span className="text-lg mr-1 leading-none">+</span> Add a card
        </button>
      </div>
    </div>
  );
}
