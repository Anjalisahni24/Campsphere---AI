import React, { useState } from "react";
import {
  Search,
  MapPin,
  Clock,
  DollarSign,
  Bookmark,
} from "lucide-react";

const allJobs = [
  { id: 1, title: "Software Engineer - AI/ML", company: "Neural Systems Inc.", location: "Bangalore, IN", type: "Full-time", salary: "₹18–24 LPA", tags: ["Python", "ML", "TensorFlow"], deadline: "Oct 20", logo: "🤖", featured: true },
  { id: 2, title: "Frontend Developer", company: "Skyline Digital", location: "Mumbai, IN", type: "Full-time", salary: "₹12–18 LPA", tags: ["React", "TypeScript", "CSS"], deadline: "Oct 22", logo: "☁️", featured: false },
  { id: 3, title: "Data Analyst", company: "Global Insight Corp", location: "Hyderabad, IN", type: "Full-time", salary: "₹10–15 LPA", tags: ["SQL", "Python", "Tableau"], deadline: "Oct 25", logo: "📊", featured: false },
  { id: 4, title: "SDE-1", company: "Microsoft Corp.", location: "Hyderabad, IN", type: "Full-time", salary: "₹20–30 LPA", tags: ["DSA", "System Design", "C++"], deadline: "Oct 14", logo: "🪟", featured: true },
  { id: 5, title: 'Backend Engineer', company: 'Fintech Labs', location: 'Pune, IN', type: 'Full-time', salary: '₹15–20 LPA', tags: ['Node.js', 'PostgreSQL', 'AWS'], deadline: 'Oct 28', logo: '💳', featured: false },
  { id: 6, title: 'DevOps Engineer', company: 'CloudBase', location: 'Chennai, IN', type: 'Full-time', salary: '₹14–19 LPA', tags: ['Docker', 'Kubernetes', 'CI/CD'], deadline: 'Nov 1', logo: '☁️', featured: false },
];

function JobRecommendation() {
  const [search, setSearch] = useState("");
  const [saved, setSaved] = useState([]);
  const savedProfile =
    JSON.parse(localStorage.getItem("profile")) || {};
  const filtered = allJobs.filter((job) => {

    const matchesSearch =
      job.title
        .toLowerCase()
        .includes(search.toLowerCase()) ||

      job.company
        .toLowerCase()
        .includes(search.toLowerCase());

    const matchesSkills =
      savedProfile.skills?.some((skill) =>
        job.tags.some((tag) =>
          tag.toLowerCase() ===
          skill.toLowerCase()
        )
      );

    if (search.trim()) {
  return matchesSearch;
}

return matchesSkills;
  });

  return (
    <div className="w-full min-h-screen p-4 md:p-6 lg:p-8 space-y-5 min-h-screen bg-gradient-to-br from-[#eef2ff] via-white to-[#f8fafc] dark:from-[#0f172a] dark:to-[#020617] transition">
      {/* HEADER */}
      <div>
        <h1 className="text-2xl font-bold">Job Listings</h1>
        <p className="text-gray-500 text-sm mt-1">
          {filtered.length} opportunities matched to your skills
        </p>
      </div>

      {/* SEARCH */}
      <div className="relative">
        <Search
          size={16}
          className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
        />
        <input
          type="text"
          placeholder="Search jobs or companies..."
          className="w-full pl-9 pr-3 py-2 border rounded-lg outline-none"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {/* JOB LIST */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">

  {filtered.length === 0 ? (

    <div className="col-span-full bg-white rounded-xl border p-8 text-center text-gray-500">
      No matching jobs found for your skills.
    </div>

  ) : (

    filtered.map((job) => (
      <div
        key={job.id}
        className={`bg-white rounded-xl p-5 border shadow-sm flex gap-4 hover:shadow-md transition ${
          job.featured
            ? "border-blue-300"
            : "border-gray-200"
        }`}
      >

        <div className="w-12 h-12 rounded-xl bg-gray-100 flex items-center justify-center text-2xl">
          {job.logo}
        </div>

        {/* CONTENT */}
        <div className="flex-1">

          <div className="flex justify-between">

            <div>

              <div className="flex items-center gap-2">
                <h3 className="font-semibold">
                  {job.title}
                </h3>

                {job.featured && (
                  <span className="text-xs bg-blue-100 text-blue-600 px-2 py-0.5 rounded">
                    Featured
                  </span>
                )}
              </div>

              <p className="text-sm text-gray-500">
                {job.company}
              </p>

            </div>

            {/* BOOKMARK */}
            <button
              onClick={() =>
                setSaved((s) =>
                  s.includes(job.id)
                    ? s.filter((x) => x !== job.id)
                    : [...s, job.id]
                )
              }
              className={`p-1 ${
                saved.includes(job.id)
                  ? "text-blue-600"
                  : "text-gray-400"
              }`}
            >
              <Bookmark
                size={16}
                fill={
                  saved.includes(job.id)
                    ? "currentColor"
                    : "none"
                }
              />
            </button>

          </div>

          {/* INFO */}
          <div className="flex gap-4 mt-2 text-xs text-gray-500 flex-wrap">

            <span className="flex items-center gap-1">
              <MapPin size={12} />
              {job.location}
            </span>

            <span className="flex items-center gap-1">
              <Clock size={12} />
              {job.type}
            </span>

            <span className="flex items-center gap-1">
              <DollarSign size={12} />
              {job.salary}
            </span>

          </div>

          {/* TAGS + BUTTON */}
          <div className="flex justify-between mt-3 items-center">

            <div className="flex gap-1 flex-wrap">

              {job.tags.map((tag) => (
                <span
                  key={tag}
                  className="text-xs bg-gray-200 px-2 py-0.5 rounded"
                >
                  {tag}
                </span>
              ))}

            </div>

            {/* ACTION */}
            <div className="flex items-center gap-2">

              <span className="text-xs text-gray-500">
                Deadline: {job.deadline}
              </span>

              <button className="text-xs px-4 py-1.5 rounded-md border border-black bg-white text-gray-500 transition-all duration-300 hover:bg-gradient-to-r hover:from-blue-600 hover:to-indigo-600 hover:text-white hover:border-blue-600">

                {saved.includes(job.id)
                  ? "Saved"
                  : "Apply Now"}

              </button>

            </div>

          </div>

        </div>
      </div>
    ))
  )}
</div>
    </div>
  );
}

export default JobRecommendation;