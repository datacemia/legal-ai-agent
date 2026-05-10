"use client";

import { useEffect, useMemo, useState } from "react";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

const AVAILABLE_AGENTS = [
  {
    slug: "legal",
    label: "Legal Agent",
  },
  {
    slug: "study",
    label: "Study Agent",
  },
  {
    slug: "finance",
    label: "Finance Agent",
  },
  {
    slug: "business",
    label: "Business Agent",
  },
];

export default function AdminEnterprisesPage() {
  const [enterprises, setEnterprises] = useState<any[]>([]);
  const [selectedEnterprise, setSelectedEnterprise] = useState<any | null>(null);
  const [selectedUsage, setSelectedUsage] = useState<any | null>(null);
  const [selectedMembers, setSelectedMembers] = useState<any[]>([]);

  const [loading, setLoading] = useState<boolean>(true);
  const [actionLoading, setActionLoading] = useState<boolean>(false);
  const [message, setMessage] = useState<string>("");

  const [name, setName] = useState<string>("");
}