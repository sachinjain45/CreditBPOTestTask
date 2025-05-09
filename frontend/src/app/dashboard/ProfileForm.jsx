import React, { useState, useEffect } from 'react';

const FormField = ({ label, name, value, onChange, type = 'text', required = false, step }) => (
  <div className="mb-4">
    <label htmlFor={name} className="block text-sm font-medium text-gray-700 mb-1">
      {label}
    </label>
    {type === 'textarea' ? (
      <textarea
        id={name}
        name={name}
        value={value || ''} // Ensure value is not undefined for controlled components
        onChange={onChange}
        rows={3}
        required={required}
        className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
      />
    ) : (
      <input
        type={type}
        id={name}
        name={name}
        value={value || ''} // Ensure value is not undefined
        onChange={onChange}
        required={required}
        step={step}
        className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
      />
    )}
  </div>
);


const ProfileForm = ({ initialData, userRole, onSubmit, onCancel, isLoading }) => {
  const [formData, setFormData] = useState({});

  useEffect(() => {
    if (initialData) {
      const { id, user, created_at, updated_at, ...editableData } = initialData;
      setFormData(editableData || {}); // Ensure formData is an object
    }
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    if ((name === 'experience_years' || name === 'hourly_rate') && type === 'number') {
      setFormData(prev => ({ ...prev, [name]: value === '' ? null : parseFloat(value) }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await onSubmit(formData);
  };

  const commonFields = (
    <>
      <FormField label="Bio" name="bio" value={formData.bio} onChange={handleChange} type="textarea" />
      <FormField label="Location" name="location" value={formData.location} onChange={handleChange} />
    </>
  );

  const seekerFields = userRole === 'seeker' && (
    <>
      <h3 className="text-lg font-semibold mt-6 mb-3 text-gray-700">Seeker Specifics</h3>
      <FormField label="Industry Interest" name="industry_interest" value={formData.industry_interest} onChange={handleChange} />
      <FormField label="Required Services (comma-separated)" name="required_services" value={formData.required_services} onChange={handleChange} type="textarea" />
      <FormField label="Project Description" name="project_description" value={formData.project_description} onChange={handleChange} type="textarea" />
      <FormField label="Budget Range" name="budget_range" value={formData.budget_range} onChange={handleChange} />
    </>
  );

  const providerFields = userRole === 'provider' && (
    <>
      <h3 className="text-lg font-semibold mt-6 mb-3 text-gray-700">Provider Specifics</h3>
      <FormField label="Company Name" name="company_name" value={formData.company_name} onChange={handleChange} />
      <FormField label="Services Offered (comma-separated)" name="services_offered" value={formData.services_offered} onChange={handleChange} type="textarea" />
      <FormField label="Years of Experience" name="experience_years" value={formData.experience_years} onChange={handleChange} type="number" />
      <FormField label="Portfolio URL" name="portfolio_url" value={formData.portfolio_url} onChange={handleChange} type="url" />
      <FormField label="Industry Focus" name="industry_focus" value={formData.industry_focus} onChange={handleChange} />
      <FormField label="Company Size" name="company_size" value={formData.company_size} onChange={handleChange} />
      <FormField label="Rating Report URL" name="rating_report_url" value={formData.rating_report_url} onChange={handleChange} type="url" />
      <FormField label="Hourly Rate" name="hourly_rate" value={formData.hourly_rate} onChange={handleChange} type="number" step="0.01"/>
    </>
  );

  return (
    <form onSubmit={handleSubmit} className="bg-white shadow-md rounded-lg p-6">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Edit Your Profile ({userRole.toUpperCase()})</h2>
      {commonFields}
      {seekerFields}
      {providerFields}
      <div className="mt-8 flex justify-end space-x-3">
        <button
          type="button"
          onClick={onCancel}
          disabled={isLoading}
          className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={isLoading}
          className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
        >
          {isLoading ? 'Saving...' : 'Save Changes'}
        </button>
      </div>
    </form>
  );
};

export default ProfileForm;