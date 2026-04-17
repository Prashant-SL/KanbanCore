"use client";
import React from 'react';
import { Draggable } from '@hello-pangea/dnd';
import { AlignLeft, CheckSquare } from 'lucide-react';

export default function TaskCard({ task, index }) {
  return (
    <Draggable draggableId={task.id} index={index}>
      {(provided, snapshot) => (
        <div
          ref={provided.innerRef}
          {...provided.draggableProps}
          {...provided.dragHandleProps}
          className={`bg-white p-3 rounded-lg shadow-sm border border-slate-200 mb-2.5 transition-shadow cursor-grab active:cursor-grabbing ${
            snapshot.isDragging ? "shadow-md ring-2 ring-[#648DE5] ring-opacity-60 rotate-2" : "hover:shadow-md"
          }`}
        >
          <div className="flex justify-between items-start mb-2">
            <h4 className="text-sm font-medium text-slate-800 leading-snug">
              {task.title}
            </h4>
          </div>
          
          {task.description && (
            <p className="text-xs text-slate-500 line-clamp-2 mt-1 mb-3">
              {task.description}
            </p>
          )}

          <div className="flex items-center justify-between mt-3 text-slate-400">
            <div className="flex items-center space-x-3">
              {task.description && <AlignLeft size={14} className="hover:text-slate-600" />}
              <div className="flex items-center text-xs hover:text-slate-600">
                <CheckSquare size={13} className="mr-1" />
                <span>0/3</span>
              </div>
            </div>
            
            {/* Mock Avatar */}
            <div className="w-6 h-6 rounded-full bg-gradient-to-tr from-[#648DE5] to-[#A1C2F7] flex items-center justify-center text-[10px] text-white font-bold border-2 border-white shadow-sm ring-1 ring-slate-100">
              {task.assigned_to ? task.assigned_to.substring(0, 2).toUpperCase() : 'U'}
            </div>
          </div>
        </div>
      )}
    </Draggable>
  );
}
