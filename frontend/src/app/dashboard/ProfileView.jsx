import React from 'react';

const DetailItem = ({ label, value, isLink }) => {
  if (!value && value !== '') return null;
  return (
    <div className="mb-3">
      <p className="text-sm font-medium text-gray-500">{label}</p>
      {isLink && value ? (
        <a href={value} target="_blank" rel="noopener noreferrer" className="text-indigo-600 hover:text-indigo-800 break-all">
          {value}
        </a>
      ) : (
        <p className="text-md text-gray-800 whitespace-pre-wrap">{value || <span className="italic text-gray-400">Not provided</span>}</p>
      )}
    </div>
  );
};


const ProfileView = ({ profile, userRole }) => {
  if (!profile || !profile.user) {
    return <div className="text-center p-4">Loading profile details...</div>;
  }

  const commonFields = (
    <>
      <DetailItem label="Email" value={profile.user.email} />
      <DetailItem label="Username" value={profile.user.username} />
      <DetailItem label="Full Name" value={`${profile.user.first_name || ''} ${profile.user.last_name || ''}`.trim() || undefined} />
      <DetailItem label="Bio" value={profile.bio} />
      <DetailItem label="Location" value={profile.location} />
    </>
  );

  const seekerFields = userRole === 'seeker' && profile && (
    <>
      <h3 className="text-lg font-semibold mt-4 mb-2 text-gray-700">Seeker Details</h3>
      <DetailItem label="Industry Interest" value={profile.industry_interest} />
      <DetailItem label="Required Services" value={profile.required_services} />
      <DetailItem label="Project Description" value={profile.project_description} />
      <DetailItem label="Budget Range" value={profile.budget_range} />
    </>
  );

  const providerFields = userRole === 'provider' && profile && (
    <>
      <h3 className="text-lg font-semibold mt-4 mb-2 text-gray-700">Provider Details</h3>
      <DetailItem label="Company Name" value={profile.company_name} />
      <DetailItem label="Services Offered" value={profile.services_offered} />
      <DetailItem label="Years of Experience" value={profile.experience_years?.toString()} />
      <DetailItem label="Portfolio URL" value={profile.portfolio_url} isLink />
      <DetailItem label="Industry Focus" value={profile.industry_focus} />
      <DetailItem label="Company Size" value={profile.company_size} />
      <DetailItem label="Rating Report URL" value={profile.rating_report_url || undefined} isLink />
      <DetailItem label="Hourly Rate" value={profile.hourly_rate?.toString()} />
    </>
  );

  return (
    <div className="bg-white shadow-md rounded-lg p-6">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Your Profile ({userRole.toUpperCase()})</h2>
      {commonFields}
      {seekerFields}
      {providerFields}
      <p className="text-xs text-gray-500 mt-4">Joined: {profile.user.date_joined ? new Date(profile.user.date_joined).toLocaleDateString() : 'N/A'}</p>
      <p className="text-xs text-gray-500">Profile Last Updated: {profile.updated_at ? new Date(profile.updated_at).toLocaleString() : 'N/A'}</p>
    </div>
  );
};

export default ProfileView;