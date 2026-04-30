import { getToken } from "./auth";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

// 🔼 helper pour headers
function getAuthHeaders() {
  const token = getToken();

  return {
    Authorization: token ? `Bearer ${token}` : "",
  };
}

export async function uploadDocument(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_URL}/documents/upload`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: formData,
  });

  return res.json();
}

// ✅ support language + auth
export async function runAnalysis(
  documentId: number,
  language: string = "en"
) {
  const res = await fetch(
    `${API_URL}/analysis/${documentId}/run?output_language=${language}`,
    {
      method: "POST",
      headers: getAuthHeaders(),
    }
  );

  return res.json();
}

export async function getAnalysis(documentId: number) {
  const res = await fetch(`${API_URL}/analysis/${documentId}`, {
    headers: getAuthHeaders(),
  });

  return res.json();
}

export async function getDocuments() {
  const res = await fetch(`${API_URL}/documents/`, {
    headers: getAuthHeaders(),
  });

  return res.json();
}

//
// 🔥 ADMIN API
//

export async function getAdminUsers() {
  const res = await fetch(`${API_URL}/admin/users`, {
    headers: getAuthHeaders(),
  });

  return res.json();
}

export async function updateUserRole(userId: number, role: string) {
  const res = await fetch(
    `${API_URL}/admin/users/${userId}/role?role=${role}`,
    {
      method: "PATCH",
      headers: getAuthHeaders(),
    }
  );

  return res.json();
}

export async function updateUserCredits(userId: number, credits: number) {
  const res = await fetch(
    `${API_URL}/admin/users/${userId}/credits?credits=${credits}`,
    {
      method: "PATCH",
      headers: getAuthHeaders(),
    }
  );

  return res.json();
}

//
// 💳 PAYMENT API
//

export async function createCheckoutSession() {
  const res = await fetch(`${API_URL}/payments/create-checkout-session`, {
    method: "POST",
    headers: getAuthHeaders(),
  });

  return res.json();
}

// 2 deuxieme agent
//
// 💰 FINANCE AGENT API
//

export async function analyzeFinanceStatement(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_URL}/finance/analyze-statement`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: formData,
  });

  if (!res.ok) {
    const error = await res.json().catch(() => null);
    throw new Error(error?.detail || `API error ${res.status}`);
  }

  return res.json();
}

export async function getFinanceHistory() {
  const res = await fetch(`${API_URL}/finance/history`, {
    headers: getAuthHeaders(),
  });

  return res.json();
}

export async function getStudyHistory() {
  const res = await fetch(`${API_URL}/study/history`, {
    headers: getAuthHeaders(),
  });

  return res.json();
}