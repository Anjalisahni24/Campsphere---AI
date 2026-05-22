import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import Navbar from "../common/navbar";
import AnimatedBackground from "../common/AnimatedBackground";
import { chatSupport } from "../../api/camspherApi";


const LandingPage = () => {
  const navigate = useNavigate();

  const students =
    JSON.parse(localStorage.getItem("students") || "[]");

  const recruiters =
    JSON.parse(localStorage.getItem("recruiters") || "[]");

  const dynamicCompanies =
    JSON.parse(localStorage.getItem("companies") || "[]");

  const dynamicStories =
    JSON.parse(localStorage.getItem("successStories") || "[]");

  const stats = [
    {
      value: `${Math.max(100, students.length * 10)}+`,
      label: "Students Joined",
      color: "text-blue-600",
    },

    {
      value: `${Math.max(20, recruiters.length * 5)}+`,
      label: "Recruiters",
      color: "text-green-600",
    },

    {
      value: "95%",
      label: "AI Match Accuracy",
      color: "text-purple-600",
    },
  ];

  const [showChatbot, setShowChatbot] = useState(false);

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "Hi 👋 I'm your AI Career Assistant. Ask me about resumes, interviews, ATS scores, or placements.",
    },
  ]);

  const [input, setInput] = useState("");

  const cards = [
    {
      title: "Students",
      desc: "Build Profile & Apply to Dream Jobs",
      path: "/login?role=student",
      icon: "🎓",
    },
    {
      title: "Recruiters",
      desc: "Find Top Talent with AI Filters",
      path: "/login?role=recruiter",
      icon: "💼",
    },
    {
      title: "TPOs",
      desc: "Manage Placements & Analytics",
      path: "/login?role=admin",
      icon: "🏫",
    },
  ];

  const stories = [
    {
      name: "Priya Sharma",
      role: "Software Engineer @ Infosys",
      text: "CampSphere helped me improve my resume and land interviews faster.",
    },
    {
      name: "Aman Verma",
      role: "Data Analyst @ TCS",
      text: "The AI readiness score showed exactly what skills I needed to improve.",
    },
  ];

  const handleSend = async () => {

    if (!input.trim()) return;

    const userMessage = input;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        text: userMessage,
      },
    ]);

    setInput("");

    try {

      const res = await chatSupport(
        userMessage
      );

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text:
            res.reply ||
            "Sorry, I couldn't respond.",
        },
      ]);

    } catch (err) {

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text:
            "AI assistant unavailable right now.",
        },
      ]);

      console.error(err);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#eef2ff] via-white to-[#f8fafc] dark:from-[#0f172a] dark:to-[#020617] transition">

      <Navbar />

      <div id="home" className="grid md:grid-cols-2 px-10 py-20 items-center gap-10">

        {/* LEFT */}
        <motion.div
          initial={{ opacity: 0, x: -40 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 1 }}
        >
          <p className="bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 inline-block px-4 py-1 rounded-full text-xs font-semibold mb-5">
            AI-POWERED INTELLIGENCE
          </p>

          <AnimatedBackground />
          <div className="flex gap-6 mt-8 flex-wrap">

            {stats.map((item, index) => (

              <div
                key={index}
                className="bg-white/70 backdrop-blur border rounded-2xl px-5 py-3 shadow-sm"
              >
                <h3 className={`text-2xl font-bold ${item.color}`}>
                  {item.value}
                </h3>

                <p className="text-sm text-gray-500">
                  {item.label}
                </p>
              </div>

            ))}

          </div>

          <p className="text-gray-600 dark:text-gray-300 mt-6 max-w-lg leading-relaxed">
            CampSphere uses advanced neural matching to connect the right
            students with the right opportunities.
          </p>
        </motion.div>

        {/* RIGHT */}
        <motion.div
          className="relative"
          initial={{ opacity: 0, x: 40 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 1 }}
        >
          <div className="absolute -top-10 -right-10 w-72 h-72 bg-blue-300 opacity-20 blur-3xl rounded-full"></div>

          <div className="backdrop-blur-xl bg-white/70 dark:bg-white/10 border border-white/30 shadow-xl rounded-3xl p-8 relative z-10">

            <h2 className="text-2xl font-bold mb-8 text-center text-gray-800 dark:text-white">
              Select Your Path
            </h2>

            {cards.map((item, index) => (
              <motion.div
                key={index}
                whileHover={{ scale: 1.05 }}
                onClick={() => navigate(item.path)}
                className="flex items-center gap-4 p-5 mb-4 rounded-xl bg-white/60 dark:bg-white/10 border hover:bg-blue-600 hover:text-white cursor-pointer transition"
              >
                <div className="text-xl">{item.icon}</div>
                <div>
                  <h3 className="font-semibold text-base">{item.title}</h3>
                  <p className="text-xs opacity-80">{item.desc}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* PROCESS SECTION */}
        <section id="process" className="py-16 px-6 md:px-10 bg-white">
          <h2 className="text-2xl md:text-4xl font-bold text-center mb-10">Our Process</h2>
          <div className="grid md:grid-cols-4 gap-6">
            {["Create Profile", "Upload Resume", "Get AI Insights", "Apply & Get Placed"].map((step, i) => (
              <div key={i} className="bg-blue-50 p-6 rounded-2xl shadow-sm text-center">
                <div className="text-3xl font-bold text-blue-600 mb-3">0{i + 1}</div>
                <p className="font-medium">{step}</p>
              </div>
            ))}
          </div>
        </section>

        {/* COMPANIES */}
        <section id="companies" className="py-20 px-6 md:px-10 bg-slate-50">
          <h2 className="text-4xl font-bold text-center mb-14">Top Hiring Companies</h2>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-6">
            {(dynamicCompanies.length
              ? dynamicCompanies
              : ["Google", "Microsoft", "Amazon", "Infosys", "TCS"]
            ).map((company, i) => (
              <div key={i} className="bg-white rounded-2xl shadow px-8 py-6 text-center font-semibold flex items-center justify-center min-h-[100px]">
                {company}
              </div>
            ))}
          </div>
        </section>

        {/* SUCCESS STORIES */}
        <section id="success" className="px-6 md:px-10 py-20 bg-white">
          <h2 className="text-4xl font-bold text-center mb-14">Success Stories</h2>
          <div className="grid md:grid-cols-2 gap-8">
            {(dynamicStories.length
              ? dynamicStories
              : stories
            ).map((story, index) => (
              <div key={index} className="bg-blue-50 rounded-3xl p-8 shadow-md">
                <p className="text-gray-700 mb-6 italic">“{story.text}”</p>
                <h3 className="text-xl font-bold text-blue-700">{story.name}</h3>
                <p className="text-gray-500">{story.role}</p>
              </div>
            ))}
          </div>
        </section>


        {/* HELP */}
        <section id="help" className="py-20 px-6 md:px-10 bg-[#dbe4f0]  text-center">
          <h2 className="text-4xl font-bold mb-6 text-black">Need Help?</h2>
          <p className="max-w-2xl mx-auto text-black mb-8">
            Our AI assistant helps you with resumes, placement preparation,
            mock interviews, and job applications.
          </p>

          <button
            onClick={() => setShowChatbot(true)}
            className="bg-[#1d4ed8] hover:bg-black text-white px-8 py-3 rounded-xl font-semibold transition"
          >
            Launch AI Assistant
          </button>
        </section>
        {showChatbot && (

          <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">

            <div className="bg-white w-[95%] max-w-md rounded-3xl shadow-2xl p-5">

              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-bold">
                  AI Career Assistant
                </h2>

                <button
                  onClick={() => setShowChatbot(false)}
                  className="text-gray-500 text-sm"
                >
                  Close
                </button>
              </div>

              <div className="h-80 overflow-y-auto space-y-3 border rounded-2xl p-3 bg-gray-50">

                {messages.map((msg, index) => (

                  <div
                    key={index}
                    className={`p-3 rounded-2xl max-w-[80%] text-sm ${msg.role === "user"
                        ? "bg-blue-600 text-white ml-auto"
                        : "bg-white border"
                      }`}
                  >
                    {msg.text}
                  </div>

                ))}

              </div>

              <div className="flex gap-2 mt-4">

                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      handleSend();
                    }
                  }}
                  placeholder="Ask something..."
                  className="flex-1 border rounded-xl px-3 py-2 outline-none"
                />

                <button
                  onClick={handleSend}
                  className="bg-blue-600 text-white px-4 rounded-xl"
                >
                  Send
                </button>

              </div>
            </div>
          </div>

        )}
      </div>
    </div>
  );
};

export default LandingPage;