"use client";
import React, { useEffect } from "react";
import { useBoardStore } from "@/store/boardStore";
import KanbanBoard from "@/components/kanban/Board";
import { LogOut } from "lucide-react";
import { useRouter } from "next/navigation";

export default function Dashboard() {
  const router = useRouter();
  const { fetchBoards, boards, currentBoardId, setCurrentBoard, isLoading, error } = useBoardStore();

  useEffect(() => {
    // Check auth simply
    if (!localStorage.getItem("access_token")) {
      router.push("/auth");
      return;
    }
    fetchBoards();
  }, [fetchBoards, router]);

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    router.push("/auth");
  };

  if (isLoading && !boards.length) {
    return <div className="min-h-screen flex items-center justify-center bg-[#f4f7fb]">Loading Dashboard...</div>;
  }

  if (error) {
    return <div className="min-h-screen flex items-center justify-center text-red-500">Error: {error}</div>;
  }

  return (
    <div className="min-h-screen bg-[#f4f7fb] flex flex-col font-sans">
      {/* Header */}
      <header className="bg-white border-b border-[#c4d7f5] px-6 py-4 flex items-center justify-between shadow-sm">
        <div className="flex items-center">
          <span className="text-[24px] font-bold tracking-tight text-[#83a6eb]">
            kanban<span className="text-[#648DE5]">Core</span>
          </span>
          
          {boards.length > 0 && (
            <select
              value={currentBoardId || ""}
              onChange={(e) => setCurrentBoard(e.target.value)}
              className="ml-8 border border-[#c4d7f5] rounded-md px-3 py-1.5 text-sm text-slate-700 bg-[#f4f7fb] outline-none focus:ring-2 focus:ring-[#648DE5] cursor-pointer"
            >
              {boards.map(b => (
                <option key={b.id} value={b.id}>{b.title}</option>
              ))}
            </select>
          )}
        </div>

        <button
          onClick={handleLogout}
          className="flex items-center text-sm font-medium text-slate-600 hover:text-red-500 transition-colors"
        >
          <LogOut size={16} className="mr-1.5" />
          Logout
        </button>
      </header>

      {/* Main Board Area */}
      <main className="flex-1 overflow-x-auto p-6 h-[calc(100vh-73px)]">
        {currentBoardId ? (
          <KanbanBoard />
        ) : (
          <div className="text-center text-slate-500 mt-20">No boards created yet.</div>
        )}
      </main>
    </div>
  );
}
