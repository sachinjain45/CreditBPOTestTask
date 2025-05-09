'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '../../../app/store/authStore';
import { fetchMyProfile, updateMyProfile } from '../../../app/services/profile';
import ProfileView from '../ProfileView';
import ProfileForm from '../ProfileForm';

const MyProfilePage = () => {
  const router = useRouter();
  const { user, isAuthenticated, isLoading: authLoading } = useAuthStore();

  const [profileData, setProfileData] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [isLoadingData, setIsLoadingData] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [authLoading, isAuthenticated, router]);

  useEffect(() => {
    if (isAuthenticated && user) {
      const loadProfile = async () => {
        setIsLoadingData(true);
        setError(null);
        try {
          const data = await fetchMyProfile();
          setProfileData(data);
        } catch (err) {
          console.error('Failed to fetch profile:', err);
          let errorMessage = 'Failed to load profile. Your profile might not be created yet.';
          if (err.response?.data?.detail) {
            errorMessage = err.response.data.detail;
          } else if (typeof err.response?.data === 'object') {
            errorMessage = Object.values(err.response.data).flat().join(' ');
          }
          setError(errorMessage);

          if (err.response?.status === 404) {
             setIsEditing(true);
             const emptyBase = { id: 0, user: user, bio: '', location: '' };
             if(user.role === 'seeker') setProfileData({...emptyBase, industry_interest: '', required_services: ''});
             if(user.role === 'provider') setProfileData({...emptyBase, company_name: '', services_offered: ''});
          }
        } finally {
          setIsLoadingData(false);
        }
      };
      loadProfile();
    }
  }, [isAuthenticated, user, authLoading]); // Re-fetch if user changes

  const handleSaveProfile = async (data) => {
    if (!profileData && !isEditing) return; // Should not happen if isEditing is true
    setIsSaving(true);
    setError(null);
    try {
      // If profileData was null (creating new), ensure user is part of data if needed by backend
      // However, our backend /profiles/me/ should handle user association.
      const dataToSave = { ...data };

      const updatedProfile = await updateMyProfile(dataToSave);
      setProfileData(updatedProfile);
      setIsEditing(false);
      alert('Profile updated successfully!');
    } catch (err) {
      console.error('Failed to update profile:', err);
      let errorMsg = 'Failed to update profile.';
      if (err.response?.data?.detail) {
        errorMsg = err.response.data.detail;
      } else if (typeof err.response?.data === 'object') {
          errorMsg = Object.entries(err.response.data).map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : value}`).join('\n');
      }
      setError(errorMsg);
      alert(`Error: ${errorMsg}`);
    } finally {
      setIsSaving(false);
    }
  };

  if (authLoading || (isLoadingData && !profileData && !isEditing) ) {
    return <div className="container mx-auto px-4 py-8 text-center">Loading profile...</div>;
  }

  if (!isAuthenticated || !user) {
    return <div className="container mx-auto px-4 py-8 text-center">Please log in to view your profile.</div>;
  }

  if (!profileData && !isEditing) {
      return (
          <div className="container mx-auto px-4 py-8 text-center">
              {error && <p className="text-red-500 mb-4">{error}</p>}
              <p>Could not load your profile. You might need to complete it.</p>
              <button
                onClick={() => {
                    setIsEditing(true);
                    const emptyBase = { id: 0, user: user, bio: '', location: '' };
                    if(user.role === 'seeker') setProfileData({...emptyBase, industry_interest: '', required_services: ''});
                    if(user.role === 'provider') setProfileData({...emptyBase, company_name: '', services_offered: ''});
                }}
                className="mt-4 px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
              >
                Complete Your Profile
              </button>
          </div>
      );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {error && <div className="mb-4 p-3 bg-red-100 text-red-700 border border-red-300 rounded-md whitespace-pre-line">{error}</div>}

      {isEditing && profileData ? (
        <ProfileForm
          initialData={profileData}
          userRole={user.role}
          onSubmit={handleSaveProfile}
          onCancel={() => {
            setIsEditing(false);
            setError(null);
            // Optionally re-fetch original data
            if (isAuthenticated && user) {
                setIsLoadingData(true); // Show loading indicator while re-fetching
                fetchMyProfile().then(setProfileData).catch(console.error).finally(() => setIsLoadingData(false));
            }
          }}
          isLoading={isSaving}
        />
      ) : profileData ? (
        <>
          <ProfileView profile={profileData} userRole={user.role} />
          <div className="mt-6 text-right">
            <button
              onClick={() => setIsEditing(true)}
              className="px-6 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Edit Profile
            </button>
          </div>
        </>
      ) : (
        <div className="text-center">No profile data available. Consider completing your profile.</div>
      )}
    </div>
  );
};

export default MyProfilePage;