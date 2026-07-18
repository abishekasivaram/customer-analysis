export const API_BASE_URL = 'http://localhost:8000';

export async function fetchAPI(endpoint: string) {
  try {
    const res = await fetch(`${API_BASE_URL}${endpoint}`);
    if (!res.ok) throw new Error(`API returned ${res.status}`);
    return await res.json();
  } catch (error) {
    console.error(`Failed fetching ${endpoint}:`, error);
    return null;
  }
}
