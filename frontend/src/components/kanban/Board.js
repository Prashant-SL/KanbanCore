"use client";
import React from "react";
import { DragDropContext } from "@hello-pangea/dnd";
import { useBoardStore } from "@/store/boardStore";
import Column from "./Column";

export default function KanbanBoard() {
  const { columns, handleDragEnd } = useBoardStore();

  return (
    <DragDropContext onDragEnd={handleDragEnd}>
      <div className="flex space-x-6 h-full items-start">
        {columns.map((column) => (
          <Column key={column.id} column={column} />
        ))}

        {/* Placeholder for "Add Column" */}
        <button className="shrink-0 w-72 bg-slate-200/50 hover:bg-slate-200/80 border-2 border-dashed border-slate-300 rounded-xl h-14 flex items-center justify-center text-slate-500 font-medium transition-colors cursor-pointer">
          + Add New Column
        </button>
      </div>
    </DragDropContext>
  );
}
