"use client";
import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { handleRegister } from "@/services/user.service";

const Login = () => {
  const router = useRouter();
  const [showLogin, setShowLogin] = useState(false);
  const [data, setData] = useState({
    email: "",
    password: "",
    username: "",
  });

  const handleChange = (e) => {
    setData({ ...data, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = { ...data };
    if (showLogin) {
      delete payload.email;
    }

    try {
      const response = await handleRegister(
        payload,
        showLogin ? "login" : "register",
      );
      
      if (showLogin && response.access_token) {
        localStorage.setItem("access_token", response.access_token);
        router.push("/dashboard");
      } else if (!showLogin) {
        // Registered successfully, switch to login
        setShowLogin(true);
      }
    } catch (err) {
      alert("Error: " + err.message);
    }
  };
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-white font-sans">
      {/* Logo Area */}
      <div className="flex items-center mb-8">
        <svg
          width="36"
          height="36"
          viewBox="0 0 32 32"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          className="mr-2"
        >
          {/* Left tall rectangle */}
          <path
            d="M4 10C4 6.68629 6.68629 4 10 4H12C15.3137 4 18 6.68629 18 10V22C18 25.3137 15.3137 28 12 28H10C6.68629 28 4 25.3137 4 22V10Z"
            fill="#A1C2F7"
          />
          {/* Top right circle */}
          <circle cx="23" cy="9" r="5" fill="#A1C2F7" />
          {/* Bottom right darker shape */}
          <path
            d="M18 19C18 16.2386 20.2386 14 23 14H25C27.7614 14 30 16.2386 30 19V23C30 25.7614 27.7614 28 25 28H23C20.2386 28 18 25.7614 18 23V19Z"
            fill="#648DE5"
          />
        </svg>
        <span className="text-[28px] font-bold tracking-tight text-[#83a6eb]">
          kanban<span className="text-[#648DE5]">Core</span>
        </span>
      </div>

      {/* Heading */}
      <h1 className="text-[26px] font-semibold text-slate-800 mb-6">
        {showLogin ? "Sign in to your account" : "Register your account"}
      </h1>

      {/* Form Card */}
      <div className="w-full max-w-[420px] rounded-xl border border-[#c4d7f5] bg-[#f4f7fb] p-8 shadow-sm">
        <form className="space-y-5">
          {/* Username */}
          <div className="space-y-1.5">
            <label
              className="block text-[15px] font-medium text-slate-800"
              htmlFor="username"
            >
              Username
            </label>
            <input
              onChange={(e) => handleChange(e)}
              id="username"
              name="username"
              type="text"
              placeholder="Enter your username"
              className="w-full rounded-md border border-[#c4d7f5] bg-transparent px-3 py-2.5 text-sm outline-none placeholder-slate-400 focus:border-[#648DE5] focus:ring-1 focus:ring-[#648DE5] transition-all"
            />
          </div>

          {/* Email */}
          {!showLogin && (
            <div className="space-y-1.5">
              <label
                className="block text-[15px] font-medium text-slate-800"
                htmlFor="email"
              >
                Email
              </label>
              <input
                onChange={(e) => handleChange(e)}
                id="email"
                name="email"
                type="email"
                placeholder="name@company.com"
                className="w-full rounded-md border border-[#c4d7f5] bg-transparent px-3 py-2.5 text-sm outline-none placeholder-slate-400 focus:border-[#648DE5] focus:ring-1 focus:ring-[#648DE5] transition-all"
              />
            </div>
          )}

          {/* Password */}
          <div className="space-y-1.5">
            <label
              className="block text-[15px] font-medium text-slate-800"
              htmlFor="password"
            >
              Password
            </label>
            <input
              onChange={(e) => handleChange(e)}
              id="password"
              name="password"
              type="password"
              placeholder="Minimum 8 characters"
              className="w-full rounded-md border border-[#c4d7f5] bg-transparent px-3 py-2.5 text-sm outline-none placeholder-slate-400 focus:border-[#648DE5] focus:ring-1 focus:ring-[#648DE5] transition-all"
            />
          </div>

          {/* Log In Button */}
          <button
            onClick={handleSubmit}
            type="submit"
            className="w-full rounded-md bg-[#7198e9] hover:bg-[#618ae3] py-2.5 text-[15px] font-medium cursor-pointer text-white transition-colors outline-none focus:ring-2 focus:ring-[#7198e9] focus:ring-offset-2 focus:ring-offset-[#f4f7fb]"
          >
            {showLogin ? "Sign In" : "Sign Up"}
          </button>
        </form>
      </div>
      <a
        onClick={() => setShowLogin(!showLogin)}
        className="text-sm mt-3 text-[#7198e9] hover:text-[#5a80d1] font-medium transition-colors cursor-pointer"
      >
        {showLogin
          ? "Don't have an account? Sign up"
          : "Already have an account? Sign in"}
      </a>
    </div>
  );
};

export default Login;
