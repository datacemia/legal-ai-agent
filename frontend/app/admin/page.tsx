"use client";

import { useEffect, useState } from "react";
import {
  getAdminUsers,
  updateUserRole,
  updateUserCredits,
} from "../../lib/api";

export default function AdminPage() {
  const [users, setUsers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  async function loadUsers() {
    const data = await getAdminUsers();

    if (data.detail) {
      alert(data.detail);
      window.location.href = "/dashboard";
      return;
    }

    setUsers(data);
    setLoading(false);
  }

  useEffect(() => {
    loadUsers();
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
    await loadUsers();
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

          <a
            href="/admin/agent0-waitlist"
            className="inline-flex items-center justify-center rounded-xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white hover:bg-slate-800"
          >
            Agent 0 Waitlist
          </a>
        </div>

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
