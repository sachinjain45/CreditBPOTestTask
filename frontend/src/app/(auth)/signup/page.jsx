'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '../../store/authStore';
import { registerUser } from '../../services/auth';

export default function SignupPage() {
  const router = useRouter();
  const { isAuthenticated, isLoading: authIsLoading } = useAuthStore();

  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    password2: '',
    role: 'SEEKER', // Default role
    first_name: '',
    last_name: '',
  });
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (!authIsLoading && isAuthenticated) {
      router.push('/dashboard');
    }
  }, [isAuthenticated, router, authIsLoading]);

  if (authIsLoading) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
  }
  if (isAuthenticated) {
    return null;
  }

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.password !== formData.password2) {

      setError("Passwords do not match.");
      return;
    }

    setError(null);
    setIsLoading(true);

    try {
      await registerUser({...formData, consent_given: true});
      alert('Registration successful! Please log in.');
      router.push('/login');
    } catch (err) {

      if (err.response?.data) {
        const backendErrors = err.response.data;
        let messages = [];
        for (const key in backendErrors) {
          if (Array.isArray(backendErrors[key])) {
            messages = messages.concat(backendErrors[key].map((msg) => `${key}: ${msg}`));
          } else {
            messages.push(`${key}: ${backendErrors[key]}`);
          }
        }
        const errorMsg = messages.join('\n') || 'Registration failed. Please try again.';
        setError(errorMsg);
      } else {
        setError('Registration failed. An unknown error occurred.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 p-10 bg-white shadow-xl rounded-lg">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Create your account
          </h2>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="rounded-md bg-red-50 p-4">
              <p className="text-sm font-medium text-red-700 whitespace-pre-line">{error}</p>
            </div>
          )}
          <AuthInput label="Username" name="username" type="text" value={formData.username} onChange={handleChange} required />
          <AuthInput label="Email address" name="email" type="email" value={formData.email} onChange={handleChange} required />
          <AuthInput label="First Name" name="first_name" type="text" value={formData.first_name} onChange={handleChange} />
          <AuthInput label="Last Name" name="last_name" type="text" value={formData.last_name} onChange={handleChange} />
          <AuthInput label="Password" name="password" type="password" value={formData.password} onChange={handleChange} required />
          <AuthInput label="Confirm Password" name="password2" type="password" value={formData.password2} onChange={handleChange} required />
          <div>
            <label htmlFor="role" className="block text-sm font-medium text-gray-700 mb-1">I am a:</label>
            <select
              id="role"
              name="role"
              value={formData.role}
              onChange={handleChange}
              required
              className="block w-full px-3 py-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            >
              <option value="ADMIN">Admin</option>
              <option value="SEEKER">Seeker (looking for services)</option>
              <option value="PROVIDER">Provider (offering services)</option>
            </select>
          </div>
          <div>
            <button
              type="submit"
              disabled={isLoading || authIsLoading}
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
            >
              {isLoading ? 'Creating account...' : 'Create Account'}
            </button>
          </div>
        </form>
        <p className="mt-4 text-center text-sm text-gray-600">
          Already have an account?{' '}
          <Link href="/login" className="font-medium text-indigo-600 hover:text-indigo-500">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}

const AuthInput = ({ label, name, type, value, onChange, placeholder, required }) => (
  <div>
    <label htmlFor={name} className="block text-sm font-medium text-gray-700 mb-1">
      {label}
    </label>
    <input
      id={name}
      name={name}
      type={type}
      autoComplete={name.includes('password') ? 'new-password' : name}
      required={required}
      value={value}
      onChange={onChange}
      className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
      placeholder={placeholder || label}
    />
  </div>
);