import api from './../lib/api';

export const fetchMyProfile = async () => {
  const response = await api.get('/profiles/me/');
  return response?.data;
};

export const updateMyProfile = async (profileData) => {
  const response = await api.patch('/profiles/me/', profileData);
  return response?.data;
};

export const setMyProfile = async (profileData) => {
  const response = await api.put('/profiles/me/', profileData);
  return response?.data;
};