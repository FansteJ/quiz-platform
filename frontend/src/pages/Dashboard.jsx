import { useNavigate } from 'react-router-dom';
import useAuthStore from '../store/authStore';

const DashboardPage = () => {
    const navigate = useNavigate();
    const { user, logout } = useAuthStore();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <div className="min-h-screen bg-gray-100">
            <nav className="bg-white shadow-md">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between items-center h-16">
                        <h1 className="text-2xl font-bold text-gray-800">Quiz Platform</h1>
                        <button
                            onClick={handleLogout}
                            className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition"
                        >
                            Logout
                        </button>
                    </div>
                </div>
            </nav>

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <div className="bg-white rounded-lg shadow-md p-8">
                    <h2 className="text-3xl font-bold text-gray-800 mb-4">
                        Welcome, {user?.name}!
                    </h2>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
                        <div className="p-4 bg-blue-50 rounded-lg">
                            <p className="text-sm text-gray-600">Email</p>
                            <p className="text-lg font-semibold">{user?.email}</p>
                        </div>

                        <div className="p-4 bg-green-50 rounded-lg">
                            <p className="text-sm text-gray-600">Role</p>
                            <p className="text-lg font-semibold">{user?.role}</p>
                        </div>
                    </div>

                    <div className="mt-8">
                        <h3 className="text-xl font-semibold mb-4">Quick Actions</h3>
                        <div className="space-y-2">
                            <button className="w-full md:w-auto px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
                                Browse Quizzes
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DashboardPage;