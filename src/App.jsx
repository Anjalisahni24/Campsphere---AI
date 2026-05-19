import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LandingPage from "./components/pages/LandingPage";
import Login from "./components/pages/Login";
import StudentPortal from "./components/pages/StudentPortal";
import RecruiterPortal from "./components/pages/RecruiterPortal";
import AdminPortal from "./components/pages/AdminPortal";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage/>} />
        <Route path="/login" element={<Login/>} />
        <Route path="/student-dashboard/*" element={<StudentPortal/>} />
        <Route path="/recruiter-dashboard/*" element={<RecruiterPortal/>} />
        <Route path="/admin-dashboard/*" element={<AdminPortal/>} />
      </Routes>
    </Router>
  );
}

export default App;