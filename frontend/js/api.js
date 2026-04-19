const API_BASE = 'http://localhost:8000';

async function apiCall(endpoint, method='GET', body=null) {
    try {
        const options = { method };
        if (body) {
            if (body instanceof FormData) options.body = body;
            else { options.body = JSON.stringify(body); options.headers = { 'Content-Type': 'application/json' }; }
        }
        const res = await fetch(`${API_BASE}${endpoint}`, options);
        if (!res.ok) {
            if (res.status===401) throw new Error("Authentication failed");
            if (res.status===404) throw new Error("Resource not found");
            if (res.status===500) throw new Error("Server error — try again");
            throw new Error(`HTTP Error ${res.status}`);
        }
        return await res.json();
    } catch(err) {
        console.error("API Error:", err);
        showToast(err.message || "Cannot reach server", "error");
        throw err;
    }
}
