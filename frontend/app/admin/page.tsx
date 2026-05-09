"use client";

import { useEffect, useState } from "react";
import {
  getAdminUsers,
  updateUserRole,
  updateUserCredits,
} from "../../lib/api";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export default function AdminPage() {
  const [users, setUsers] = useState<any[]>([]);
  const [waitlist, setWaitlist] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  async function loadUsers() {
    const data = await getAdminUsers();

    if (data.detail) {
      alert(data.detail);
      window.location.href = "/dashboard";
      return;
    }

    setUsers(data);
  }

  async function loadWaitlist() {
    const token = localStorage.getItem("token");

    const res = await fetch(`${API_URL}/agent0-waitlist/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    const data = await res.json();

    if (res.ok && Array.isArray(data)) {
      setWaitlist(data);
    }
  }

  async function loadAdminData() {
    try {
      await loadUsers();
      await loadWaitlist();
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadAdminData();
  }, []);

  function updateLocalUser(userId: number, field: string, value: any) {
    setUsers((prev) =>
      prev.map((user) =>
        user.id === userId ? { ...user, [field]: value } : user
      )
    );
  }

  async function handleManage(user: any) {
    await updateUserRole(user.id, user.role);
    await updateUserCredits(user.id, Number(user.analysis_credits));

    alert("User updated successfully");
    await loadAdminData();
  }

  if (loading) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-gray-50">
        <p className="text-gray-600">Loading admin dashboard...</p>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-6xl mx-auto space-y-8">
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              Admin Dashboard
            </h1>

            <p className="text-gray-500 mt-1">
              Manage users, roles, credits, and waitlists.
            </p>
          </div>

          <div className="flex flex-wrap gap-3">
            <a
              href="/admin/agent0-waitlist"
              className="inline-flex items-center justify-center rounded-xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white hover:bg-slate-800"
            >
              Agent 0 Waitlist
            </a>

            <a
              href="/admin/contact-requests"
              className="inline-flex items-center justify-center rounded-xl bg-blue-600 px-5 py-3 text-sm font-semibold text-white hover:bg-blue-700"
            >
              Contact Requests
            </a>
          </div>
        </div>

        <div className="grid gap-4 md:grid-cols-3">
          <div className="rounded-2xl border bg-white p-5">
            <p className="text-sm text-gray-500">Users</p>
            <p className="mt-2 text-3xl font-bold">{users.length}</p>
          </div>

          <div className="rounded-2xl border bg-white p-5">
            <p className="text-sm text-gray-500">Agent 0 waitlist leads</p>
            <p className="mt-2 text-3xl font-bold">{waitlist.length}</p>
          </div>

          <div className="rounded-2xl border bg-white p-5">
            <p className="text-sm text-gray-500">Latest Agent 0 lead</p>
            <p className="mt-2 text-sm font-semibold">
              {waitlist[0]?.email || "No leads yet"}
            </p>
          </div>
        </div>

        {waitlist.length > 0 && (
          <div className="rounded-2xl border bg-white p-5">
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-lg font-bold text-gray-900">
                Latest Agent 0 Waitlist Leads
              </h2>

              <a
                href="/admin/agent0-waitlist"
                className="text-sm font-medium text-blue-700"
              >
                View all
              </a>
            </div>

            <div className="grid gap-3 md:grid-cols-3">
              {waitlist.slice(0, 3).map((item) => (
                <div key={item.id} className="rounded-xl border p-4 text-sm">
                  <p className="font-semibold">{item.full_name}</p>
                  <p className="text-gray-500">{item.email}</p>
                  <p className="mt-2 text-gray-600">
                    {item.profile || "—"} · {item.interest_level || "—"}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="bg-white border rounded-2xl overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-gray-100 text-gray-600">
              <tr>
                <th className="text-left p-4">ID</th>
                <th className="text-left p-4">Email</th>
                <th className="text-left p-4">Role</th>
                <th className="text-left p-4">Plan</th>
                <th className="text-left p-4">Free Used</th>
                <th className="text-left p-4">Credits</th>
                <th className="text-right p-4">Actions</th>
              </tr>
            </thead>

            <tbody>
              {users.map((user) => (
                <tr key={user.id} className="border-t">
                  <td className="p-4">{user.id}</td>
                  <td className="p-4 font-medium">{user.email}</td>

                  <td className="p-4">
                    <select
                      value={user.role}
                      onChange={(e) =>
                        updateLocalUser(user.id, "role", e.target.value)
                      }
                      className="border rounded-lg px-2 py-1"
                    >
                      <option value="user">user</option>
                      <option value="admin">admin</option>
                    </select>
                  </td>

                  <td className="p-4">{user.plan}</td>
                  <td className="p-4">{user.free_analyses_used}</td>

                  <td className="p-4">
                    <input
                      type="number"
                      value={user.analysis_credits}
                      onChange={(e) =>
                        updateLocalUser(
                          user.id,
                          "analysis_credits",
                          Number(e.target.value)
                        )
                      }
                      className="border rounded-lg px-2 py-1 w-20"
                    />
                  </td>

                  <td className="p-4 text-right">
                    <button
                      onClick={() => handleManage(user)}
                      className="text-blue-700 font-medium"
                    >
                      Manage
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </main>
  );
}
