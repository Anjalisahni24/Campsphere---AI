import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import {
    Mail,
    User,
    ArrowLeft,
    Save,
    X,
    ShieldCheck,
    Building2,
} from "lucide-react";

function AdminProfile() {
    const navigate = useNavigate();

    const storedUser = JSON.parse(localStorage.getItem("user"));

    const [isEditing, setIsEditing] = useState(false);

    const [profile, setProfile] = useState({
        fullName: storedUser?.fullName || "",
        email: storedUser?.email || "",
        role: storedUser?.role || "admin",
        collegeName: storedUser?.collegeName || "",
    });

    const handleChange = (e) => {
        setProfile({
            ...profile,
            [e.target.name]: e.target.value,
        });
    };

    const handleSave = () => {
        localStorage.setItem("user", JSON.stringify(profile));

        setIsEditing(false);

        alert("Admin profile updated successfully!");
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-[#eef2ff] via-white to-[#f8fafc] p-6">

            {/* TOP BAR */}
            <div className="max-w-5xl mx-auto flex justify-between items-center mb-6">

                <button
                    onClick={() => navigate("/admin-dashboard")}
                    className="flex items-center gap-2 text-sm text-blue-600 hover:underline"
                >
                    <ArrowLeft size={18} />
                    Back to Dashboard
                </button>

                <div className="flex gap-3">

                    {isEditing ? (
                        <>
                            <button
                                onClick={handleSave}
                                className="flex items-center gap-2 px-4 py-2 bg-[#24389c] text-white rounded-xl hover:bg-[#1e2f85] transition"
                            >
                                <Save size={18} />
                                Save
                            </button>

                            <button
                                onClick={() => setIsEditing(false)}
                                className="flex items-center gap-2 px-4 py-2 border rounded-xl hover:bg-gray-100 transition"
                            >
                                <X size={18} />
                                Cancel
                            </button>
                        </>
                    ) : (
                        <button
                            onClick={() => setIsEditing(true)}
                            className="px-5 py-2 bg-[#24389c] text-white rounded-xl hover:bg-[#1e2f85] transition"
                        >
                            Edit Profile
                        </button>
                    )}

                </div>
            </div>

            {/* PROFILE CARD */}
            <div className="max-w-5xl mx-auto bg-white rounded-3xl shadow-lg overflow-hidden border border-gray-100">

                {/* HEADER */}
                <div className="bg-gradient-to-r from-[#24389c] to-[#4f46e5] px-8 py-10">

                    <div className="flex items-center gap-6">

                        {/* AVATAR */}
                        <div className="w-24 h-24 rounded-2xl bg-white/20 backdrop-blur-md border border-white/30 flex items-center justify-center text-4xl font-bold text-white shadow-lg">
                            {profile.fullName?.charAt(0).toUpperCase()}
                        </div>

                        {/* INFO */}
                        <div className="text-white">

                            <h2 className="text-3xl font-bold">
                                {profile.fullName || "Admin"}
                            </h2>

                            <p className="text-sm text-white/90 mt-1">
                                Placement Administrator •{" "}
                                {profile.collegeName || "College"}
                            </p>

                            <p className="text-sm text-white/70 mt-2">
                                Managing campus placements, recruitment drives,
                                and student analytics
                            </p>

                        </div>
                    </div>
                </div>

                {/* CONTENT */}
                <div className="p-8">

                    {/* DETAILS */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

                        {/* FULL NAME */}
                        <div className="bg-gray-50 p-5 rounded-2xl border border-gray-100">

                            <div className="flex items-center gap-2 mb-3 text-gray-500">
                                <User size={18} />
                                <span>Full Name</span>
                            </div>

                            {isEditing ? (
                                <input
                                    type="text"
                                    name="fullName"
                                    value={profile.fullName}
                                    onChange={handleChange}
                                    className="w-full p-3 rounded-xl border outline-none focus:ring-2 focus:ring-blue-300"
                                />
                            ) : (
                                <p className="font-semibold text-lg text-gray-800">
                                    {profile.fullName}
                                </p>
                            )}
                        </div>

                        {/* EMAIL */}
                        <div className="bg-gray-50 p-5 rounded-2xl border border-gray-100">

                            <div className="flex items-center gap-2 mb-3 text-gray-500">
                                <Mail size={18} />
                                <span>Email Address</span>
                            </div>

                            <p className="font-semibold text-lg text-gray-800 break-all">
                                {profile.email}
                            </p>
                        </div>

                        {/* COLLEGE */}
                        <div className="bg-gray-50 p-5 rounded-2xl border border-gray-100">

                            <div className="flex items-center gap-2 mb-3 text-gray-500">
                                <Building2 size={18} />
                                <span>College Name</span>
                            </div>

                            {isEditing ? (
                                <input
                                    type="text"
                                    name="collegeName"
                                    value={profile.collegeName}
                                    onChange={handleChange}
                                    className="w-full p-3 rounded-xl border outline-none focus:ring-2 focus:ring-blue-300"
                                />
                            ) : (
                                <p className="font-semibold text-lg text-gray-800">
                                    {profile.collegeName}
                                </p>
                            )}
                        </div>

                        {/* ROLE */}
                        <div className="bg-gray-50 p-5 rounded-2xl border border-gray-100">

                            <div className="flex items-center gap-2 mb-3 text-gray-500">
                                <ShieldCheck size={18} />
                                <span>Role</span>
                            </div>

                            <p className="font-semibold text-lg capitalize text-gray-800">
                                {profile.role}
                            </p>
                        </div>

                    </div>

                    {/* LOGOUT */}
                    <div className="mt-10 flex justify-end">

                        <button
                            onClick={() => {
                                localStorage.removeItem("user");
                                localStorage.removeItem("role");

                                navigate("/login?role=admin");
                            }}
                            className="px-6 py-3 border border-red-300 text-red-600 rounded-xl hover:bg-red-50 transition"
                        >
                            Logout
                        </button>

                    </div>
                </div>
            </div>
        </div>
    );
}

export default AdminProfile;