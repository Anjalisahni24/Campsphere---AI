import React from 'react';

const Navbar = () => {
  const scrollToSection = (id) => {
    const section = document.getElementById(id);
    if (section) {
      section.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <nav className="flex justify-between items-center px-10 py-2 sticky top-0 z-40 backdrop-blur-md">
      <h1 className="text-2xl font-bold text-blue-700 cursor-pointer">CampSphere</h1>

      <div className="space-x-8 hidden md:flex ">
        <button onClick={() => scrollToSection("home")} className="hover:text-blue-600 transition">
          Home
        </button>

        <button onClick={() => scrollToSection("process")} className="hover:text-blue-600 transition">
          Process
        </button>

        <button onClick={() => scrollToSection("companies")} className="hover:text-blue-600 transition">
          Companies
        </button>

        <button onClick={() => scrollToSection("success")} className="hover:text-blue-600 transition">
          Success Stories
        </button>

        <button onClick={() => scrollToSection("help")} className="hover:text-blue-600 transition">
          Help
        </button>
      </div>

    </nav>
  );
};


export default Navbar;
