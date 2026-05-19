import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  Radar,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

import {
  CheckCircle,
  AlertCircle,
  TrendingUp,
  Target,
  Zap,
  BookOpen,
  Bell,
  Settings,
} from "lucide-react";
/* UI */
const Badge = ({ children }) => (
  <span className="px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-600 font-semibold">
    {children}
  </span>
);

const Button = ({ children }) => (
  <button className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition">
    {children}
  </button>
);

const ReadinessChart = ({ value }) => (
  <div className="w-24 h-24 sm:w-28 sm:h-28 md:w-32 md:h-32 rounded-full border-4 border-blue-600 flex items-center justify-center text-xl font-bold text-blue-600">
    {value}%
  </div>
);


function ReadinessScore() {
  const navigate = useNavigate();

  const user =
    JSON.parse(localStorage.getItem("user")) || {};
  const savedProfile =
    JSON.parse(localStorage.getItem("profile")) || {};
  const [showNotifications, setShowNotifications] =
    useState(false);

  const [showSettings, setShowSettings] =
    useState(false);

  /* DATA */
  const radarData = [
    {
      skill: "Skills",
      score: Math.min(
        (savedProfile.skills?.length || 0) * 15,
        100
      ),
    },

    {
      skill: "Projects",
      score: Math.min(
        (savedProfile.projects?.length || 0) * 20,
        100
      ),
    },

    {
      skill: "Academics",
      score: (savedProfile.cgpa || 0) * 10,
    },

    {
      skill: "Profile",
      score: savedProfile.bio ? 85 : 40,
    },

    {
      skill: "Experience",
      score:
        savedProfile.projects?.length > 2
          ? 90
          : 50,
    },
  ];

  const categoryScores = [
    {
      label: "Technical Skills",
      score: Math.min(
        (savedProfile.skills?.length || 0) * 15,
        100
      ),
      icon: Zap,
    },

    {
      label: "Academic Performance",
      score: (savedProfile.cgpa || 0) * 10,
      icon: BookOpen,
    },

    {
      label: "Project Experience",
      score: Math.min(
        (savedProfile.projects?.length || 0) * 20,
        100
      ),
      icon: Target,
    },

    {
      label: "Profile Completion",
      score: savedProfile.bio ? 90 : 40,
      icon: TrendingUp,
    },
  ];

  const improvements = [
    {
      text: savedProfile.skills?.length
        ? "Add more advanced skills"
        : "Add your first skill",
      done: savedProfile.skills?.length >= 3,
    },

    {
      text: savedProfile.projects?.length
        ? "Improve project portfolio"
        : "Add your first project",
      done: savedProfile.projects?.length >= 2,
    },

    {
      text: savedProfile.cgpa
        ? "Maintain academic consistency"
        : "Add your CGPA",
      done: savedProfile.cgpa >= 8,
    },

    {
      text: savedProfile.bio
        ? "Profile description completed"
        : "Complete profile bio",
      done: !!savedProfile.bio,
    },
  ];

  const tierData = [
    {
      tier: "Startups",
      match: Math.min(
        50 +
        (savedProfile.projects?.length || 0) * 10,
        100
      ),
    },

    {
      tier: "MNCs",
      match: Math.min(
        40 +
        (savedProfile.skills?.length || 0) * 10,
        100
      ),
    },

    {
      tier: "Tier 1",
      match: Math.min(
        (savedProfile.cgpa || 0) * 10,
        100
      ),
    },

    {
      tier: "FAANG",
      match: Math.min(
        ((savedProfile.cgpa || 0) * 8) +
        (savedProfile.projects?.length || 0) * 10,
        100
      ),
    },
  ];

  const [tasks, setTasks] = useState(improvements);

  const toggle = (i) => {
    setTasks((prev) =>
      prev.map((t, idx) =>
        idx === i ? { ...t, done: !t.done } : t
      )
    );
  };

  const completed = tasks.filter((t) => t.done).length;
  const score = Math.min(
    Math.round(
      ((savedProfile.skills?.length || 0) * 15) +
      ((savedProfile.projects?.length || 0) * 20) +
      ((savedProfile.cgpa || 0) * 5) +
      (savedProfile.bio ? 10 : 0)
    ),
    100
  );
  const notifications = [

    savedProfile.skills?.length
      ? `${savedProfile.skills.length} skills added`
      : "Add skills to improve readiness",

    savedProfile.projects?.length
      ? `${savedProfile.projects.length} projects added`
      : "No projects added yet",

    savedProfile.cgpa
      ? `CGPA score: ${savedProfile.cgpa}`
      : "Add academic details",

    score >= 80
      ? "You are placement ready"
      : "Complete tasks to improve score",

  ];

  return (
    <div className="w-full p-4 md:p-6 lg:p-8 space-y-5">

      {/* NAVBAR */}
      <header className="bg-white border rounded-2xl px-6 py-4 flex items-center justify-between shadow-sm">
        <h2 className="font-semibold text-lg">Readiness Score</h2>
        <div className="flex items-center gap-3">
          {/* Notifications */}
          <div className="relative">

            <button
              onClick={() => {
                setShowNotifications(!showNotifications);
                setShowSettings(false);
              }}
              className="p-2 rounded-lg hover:bg-gray-100"
            >
              <Bell size={18} />
            </button>

            {showNotifications && (
              <div className="absolute right-0 mt-2 w-72 bg-white border rounded-2xl shadow-lg p-4 z-50">
                <h4 className="font-semibold mb-3">
                  Notifications
                </h4>

                <div className="space-y-3 text-sm">

                  {notifications.map(
                    (notification, index) => (
                      <div
                        key={index}
                        className="border-b pb-2 last:border-none"
                      >
                        {notification}
                      </div>
                    ))}
                </div>
              </div>
            )}
          </div>

          {/* Settings */}
          <div className="relative">

            <button
              onClick={() => {
                setShowSettings(!showSettings);
                setShowNotifications(false);
              }}
              className="p-2 rounded-lg hover:bg-gray-100"
            >
              <Settings size={18} />
            </button>

            {showSettings && (
              <div className="absolute right-0 mt-2 w-56 bg-white border rounded-2xl shadow-lg p-2 z-50">

                <button
                  onClick={() =>
                    navigate("/student-dashboard/profile")
                  }
                  className="w-full text-left px-3 py-2 rounded-lg hover:bg-gray-100 text-sm"
                >
                  Profile Settings
                </button>

                <button
                  onClick={() =>
                    navigate("/student-dashboard/readiness-score")
                  }
                  className="w-full text-left px-3 py-2 rounded-lg hover:bg-gray-100 text-sm"
                >
                  Readiness Analytics
                </button>

                <button
                  onClick={() => {
                    localStorage.removeItem("user");
                    navigate("/login");
                  }}
                  className="w-full text-left px-3 py-2 rounded-lg hover:bg-gray-100 text-sm text-red-500"
                >
                  Logout
                </button>

              </div>
            )}
          </div>
          <div
            onClick={() => navigate("/student-dashboard/profile")}
            className="w-9 h-9 rounded-full bg-blue-600 flex items-center justify-center text-white text-sm font-semibold cursor-pointer"
          >
            {(user?.fullName || "User")
              .charAt(0)
              .toUpperCase()}
          </div>
        </div>
      </header>

      <div className="w-full space-y-6">

        <div>
          <h1 className="text-2xl md:text-3xl font-bold">
            Readiness Score
          </h1>
          <p className="text-gray-500 text-sm">
            AI-powered placement analysis
          </p>
        </div>

        {/* HERO SECTION */}
        <div className="bg-white rounded-xl border shadow p-4 sm:p-6 flex flex-col lg:flex-row gap-6">
          <div className="flex flex-col items-center justify-center min-w-[120px]">
            <ReadinessChart value={score} />
            <div className="mt-2">
              <Badge>AI Verified</Badge>
            </div>
          </div>

          <div className="flex-1 space-y-4">
            <div>
              <h2 className="font-bold text-lg">
                Your Profile is{" "}
                <span className="text-blue-600">
                  {
                    score >= 80
                      ? "Highly Competitive"
                      : score >= 60
                        ? "Placement Ready"
                        : "Needs Improvement"
                  }
                </span>
              </h2>
              <p className="text-sm text-gray-500">
                Improve your score by completing tasks below.
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {categoryScores.map((cat) => (
                <div
                  key={cat.label}
                  className="flex items-center gap-3 p-3 border rounded-lg"
                >
                  <cat.icon className="text-blue-600" size={18} />
                  <div className="flex-1">
                    <div className="flex justify-between text-xs mb-1">
                      <span>{cat.label}</span>
                      <span className="font-bold text-blue-600">
                        {cat.score}%
                      </span>
                    </div>
                    <div className="bg-gray-200 h-1.5 rounded-full">
                      <div
                        className="bg-blue-600 h-1.5 rounded-full"
                        style={{ width: `${cat.score}%` }}
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>

        {/* CHARTS */}
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
          <div className="bg-white rounded-xl border shadow p-5 min-w-0">
            <h3 className="text-sm font-semibold mb-4">Skill Radar</h3>
            <div className="w-full min-h-[260px] ">
              <ResponsiveContainer width="100%" height={300}>
                <RadarChart data={radarData}>
                  <PolarGrid />
                  <PolarAngleAxis dataKey="skill" />
                  <Radar
                    dataKey="score"
                    fill="#2563eb"
                    fillOpacity={0.3}
                    stroke="#2563eb"
                  />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* BAR */}
          <div className="bg-white rounded-xl border shadow p-5 min-h-0">
            <h3 className="text-sm font-semibold mb-4">
              Company Match %
            </h3>
            <div className="w-full min-h-[260px]">
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={tierData} layout="vertical">
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis type="number" />
                  <YAxis dataKey="tier" type="category" />
                  <Tooltip />
                  <Bar dataKey="match" fill="#2563eb" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

        </div>

        {/* TASKS */}
        <div className="bg-white rounded-xl border shadow p-5">
          <div className="flex justify-between mb-4">
            <h3 className="font-semibold">Improvement Tasks</h3>
            <Badge>{completed}/{tasks.length}</Badge>
          </div>

          <div className="space-y-2">
            {tasks.map((task, i) => (
              <button
                key={i}
                onClick={() => toggle(i)}
                className={`w-full flex items-center gap-3 p-3 border rounded-lg transition ${task.done
                  ? "bg-blue-50"
                  : "hover:bg-gray-100"
                  }`}
              >
                {task.done ? (
                  <CheckCircle className="text-blue-600" />
                ) : (
                  <AlertCircle className="text-gray-400" />
                )}
                <span
                  className={`text-sm ${task.done
                    ? "line-through text-gray-400"
                    : ""
                    }`}
                >
                  {task.text}
                </span>
              </button>
            ))}
          </div>

          <div className="mt-4">
            <Button>Generate Full AI Report</Button>
          </div>
        </div>

      </div>
    </div>
  );
}

export default ReadinessScore;