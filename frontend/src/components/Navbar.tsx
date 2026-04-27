import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { FiSearch, FiFilter, FiUser, FiLogOut, FiMenu, FiX } from 'react-icons/fi';
import { useAuthStore } from '@/stores/authStore';

const Navbar: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuthStore();
  const navigate = useNavigate();
  const location = useLocation();
  const [isOpen, setIsOpen] = React.useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="bg-white shadow-md sticky top-0 z-40">
      <div className="container flex items-center justify-between h-16">
        {/* Logo */}
        <Link to="/" className="font-bold text-2xl text-blue-600">
          🏠 Realty
        </Link>

        {/* Desktop Menu */}
        <div className="hidden md:flex items-center gap-6">
          <Link
            to="/"
            className={`text-sm font-medium ${
              location.pathname === '/' ? 'text-blue-600' : 'text-gray-600'
            }`}
          >
            Home
          </Link>
          <Link
            to="/properties"
            className={`text-sm font-medium ${
              location.pathname === '/properties' ? 'text-blue-600' : 'text-gray-600'
            }`}
          >
            Properties
          </Link>
          <Link
            to="/search"
            className={`text-sm font-medium ${
              location.pathname === '/search' ? 'text-blue-600' : 'text-gray-600'
            }`}
          >
            Search
          </Link>
          <Link
            to="/agents"
            className={`text-sm font-medium ${
              location.pathname === '/agents' ? 'text-blue-600' : 'text-gray-600'
            }`}
          >
            Agents
          </Link>
        </div>

        {/* Right Side */}
        <div className="hidden md:flex items-center gap-4">
          {isAuthenticated ? (
            <>
              <Link to="/profile" className="flex items-center gap-2 text-gray-600 hover:text-blue-600">
                <FiUser size={20} />
                <span className="text-sm">{user?.username}</span>
              </Link>
              <button
                onClick={handleLogout}
                className="flex items-center gap-2 text-gray-600 hover:text-red-600"
              >
                <FiLogOut size={20} />
                <span className="text-sm">Logout</span>
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="btn-secondary text-sm">
                Login
              </Link>
              <Link to="/register" className="btn-primary text-sm">
                Sign Up
              </Link>
            </>
          )}
        </div>

        {/* Mobile Menu Button */}
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="md:hidden flex items-center"
        >
          {isOpen ? <FiX size={24} /> : <FiMenu size={24} />}
        </button>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
        <div className="md:hidden bg-white border-t border-gray-200">
          <div className="container py-4 space-y-3">
            <Link to="/" className="block text-sm font-medium text-gray-600 hover:text-blue-600">
              Home
            </Link>
            <Link to="/properties" className="block text-sm font-medium text-gray-600 hover:text-blue-600">
              Properties
            </Link>
            <Link to="/search" className="block text-sm font-medium text-gray-600 hover:text-blue-600">
              Search
            </Link>
            <Link to="/agents" className="block text-sm font-medium text-gray-600 hover:text-blue-600">
              Agents
            </Link>

            {isAuthenticated ? (
              <>
                <Link to="/profile" className="block text-sm font-medium text-gray-600 hover:text-blue-600">
                  Profile
                </Link>
                <button
                  onClick={handleLogout}
                  className="block w-full text-left text-sm font-medium text-red-600 hover:text-red-700"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="block text-sm font-medium text-gray-600 hover:text-blue-600">
                  Login
                </Link>
                <Link to="/register" className="block text-sm font-medium text-gray-600 hover:text-blue-600">
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
