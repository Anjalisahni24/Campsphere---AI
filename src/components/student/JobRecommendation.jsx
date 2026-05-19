import React, { useMemo, useState } from "react";
import {
  Search,
  MapPin,
  Clock,
  DollarSign,
  Bookmark,
  TrendingUp,
  AlertTriangle,
} from "lucide-react";
import { usePlacement } from "../context/PlacementContext";
import { getStudentProfile } from "../../api/camspherApi";

function JobRecommendation() {
  const [search, setSearch] = useState("");
  const [saved, setSaved] = useState([]);
  const { jobData, resumeData, loading } = usePlacement();
  const savedProfile = getStudentProfile();

  const recommendations = jobData?.top_recommendations || [];
  const missingSkills = useMemo(() => {
    const gaps = new Set();
    recommendations.slice(0, 5).forEach((rec) => {
      (rec.skill_gaps || []).slice(0, 3).forEach((g) => gaps.add(g));
    });
    return [...gaps];
  }, [recommendations]);

  const filtered = useMemo(() => {
    if (!search.trim()) return recommendations;
    const q = search.toLowerCase();
    return recommendations.filter((rec) => {
      const job = rec.job || {};
      return (
        job.title?.toLowerCase().includes(q) ||
        job.company?.toLowerCase().includes(q) ||
        (rec.required_skills_matched || []).some((s) =>
          s.toLowerCase().includes(q)
        )
      );
    });
  }, [recommendations, search]);

  return (
    <div className="w-full min-h-screen p-4 md:p-6 lg:p-8 space-y-5 bg-gradient-to-br from-[#eef2ff] via-white to-[#f8fafc]">
      <div>
        <h1 className="text-2xl font-bold">Job Recommendations</h1>
        <p className="text-gray-500 text-sm mt-1">
          {resumeData
            ? `${jobData?.total_jobs_matched ?? 0} jobs matched via AI (cosine similarity + skill gaps)`
            : "Upload your resume on the Dashboard to get personalized matches"}
        </p>
      </div>

      {!resumeData && !loading && (
        <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 text-sm text-amber-800 flex gap-2">
          <AlertTriangle size={18} className="shrink-0" />
          <span>
            No AI recommendations yet. Go to Dashboard → Upload Resume to run the full pipeline.
          </span>
        </div>
      )}

      {missingSkills.length > 0 && (
        <div className="bg-white rounded-xl border p-4 shadow-sm">
          <h3 className="font-semibold text-sm mb-2 flex items-center gap-2">
            <TrendingUp size={16} className="text-blue-600" />
            Top Missing Skills
          </h3>
          <div className="flex flex-wrap gap-2">
            {missingSkills.map((skill) => (
              <span
                key={skill}
                className="text-xs bg-red-50 text-red-700 border border-red-100 px-2 py-1 rounded-full"
              >
                {skill}
              </span>
            ))}
          </div>
        </div>
      )}

      <div className="relative">
        <Search
          size={16}
          className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
        />
        <input
          type="text"
          placeholder="Search recommended jobs..."
          className="w-full pl-9 pr-3 py-2 border rounded-lg outline-none bg-white"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
        {filtered.length === 0 ? (
          <div className="col-span-full bg-white rounded-xl border p-8 text-center text-gray-500">
            {resumeData
              ? "No jobs match your search."
              : `Profile skills (${savedProfile.skills?.length || 0}) — upload resume for AI job matching.`}
          </div>
        ) : (
          filtered.map((rec) => {
            const job = rec.job || {};
            const jobId = job.id ?? rec.job_id;
            return (
              <div
                key={jobId}
                className="bg-white rounded-xl p-5 border shadow-sm flex gap-4 hover:shadow-md transition border-gray-200"
              >
                <div className="w-12 h-12 rounded-xl bg-blue-50 flex items-center justify-center text-lg font-bold text-blue-700">
                  {(job.company || "?").charAt(0)}
                </div>

                <div className="flex-1 min-w-0">
                  <div className="flex justify-between gap-2">
                    <div>
                      <h3 className="font-semibold truncate">{job.title}</h3>
                      <p className="text-sm text-gray-500">{job.company}</p>
                    </div>
                    <button
                      type="button"
                      onClick={() =>
                        setSaved((s) =>
                          s.includes(jobId)
                            ? s.filter((x) => x !== jobId)
                            : [...s, jobId]
                        )
                      }
                      className={
                        saved.includes(jobId) ? "text-blue-600" : "text-gray-400"
                      }
                    >
                      <Bookmark
                        size={16}
                        fill={saved.includes(jobId) ? "currentColor" : "none"}
                      />
                    </button>
                  </div>

                  <div className="mt-2 flex items-center gap-2 flex-wrap">
                    <span className="text-xs font-bold text-blue-600 bg-blue-50 px-2 py-0.5 rounded">
                      {Math.round(rec.match_score ?? 0)}% match
                    </span>
                    <span className="text-xs text-gray-500 capitalize">
                      {rec.confidence || rec.match_category}
                    </span>
                  </div>

                  <div className="flex gap-3 mt-2 text-xs text-gray-500 flex-wrap">
                    {job.location && (
                      <span className="flex items-center gap-1">
                        <MapPin size={12} />
                        {job.location}
                      </span>
                    )}
                    {job.experience_level && (
                      <span className="flex items-center gap-1">
                        <Clock size={12} />
                        {job.experience_level}
                      </span>
                    )}
                    {job.salary_range && (
                      <span className="flex items-center gap-1">
                        <DollarSign size={12} />
                        {job.salary_range}
                      </span>
                    )}
                  </div>

                  {(rec.skill_gaps || []).length > 0 && (
                    <p className="text-xs text-red-600 mt-2">
                      Missing: {(rec.skill_gaps || []).slice(0, 4).join(", ")}
                    </p>
                  )}

                  <div className="flex gap-1 flex-wrap mt-2">
                    {(job.required_skills || []).slice(0, 4).map((tag) => (
                      <span
                        key={tag}
                        className="text-xs bg-gray-100 px-2 py-0.5 rounded"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}

export default JobRecommendation;
