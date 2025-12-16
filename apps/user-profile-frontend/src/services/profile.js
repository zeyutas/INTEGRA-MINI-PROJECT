import api from './api';

export async function getProfile() {
  const { data } = await api.get('/user/profile/');
  return data;
}

export async function updateProfile(updates) {
  const payload = {
    first_name: updates.first_name || '',
    last_name: updates.last_name || '',
    bio: updates.bio || '',
    avatar_url: updates.avatar_url || ''
  };
  const { data } = await api.patch('/user/profile/', payload);
  return data;
}
