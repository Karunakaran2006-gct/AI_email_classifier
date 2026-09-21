"use client";

import { useEffect, useState } from "react";

const API_URL = "http://127.0.0.1:8000";

type Message = {
  id: number;
  sender: string;
  subject: string;
  body: string;
  category?: string | null;
  priority?: string | null;
  sentiment?: string | null;
  summary?: string | null;
  suggested_action?: string | null;
};

type Summary = {
  total_messages: number;
  by_category: Record<string, number>;
  by_priority: Record<string, number>;
};

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);

  const [sender, setSender] = useState("");
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");

  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [priority, setPriority] = useState("");

  const [loading, setLoading] = useState(false);
  const [analyzing, setAnalyzing] = useState<number | null>(null);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  async function loadMessages() {
    try {
      const params = new URLSearchParams();

      if (search) params.append("search", search);
      if (category) params.append("category", category);
      if (priority) params.append("priority", priority);

      const response = await fetch(
        `${API_URL}/api/messages/?${params.toString()}`
      );

      if (!response.ok) {
        throw new Error("Failed to fetch messages");
      }

      const data = await response.json();
      setMessages(data);
    } catch {
      setError("Could not connect to the backend.");
    }
  }

  async function loadSummary() {
    try {
      const response = await fetch(
        `${API_URL}/api/messages/summary`
      );

      if (!response.ok) {
        throw new Error("Failed to fetch summary");
      }

      const data = await response.json();
      setSummary(data);
    } catch {
      setError("Could not load dashboard data.");
    }
  }

  useEffect(() => {
    loadMessages();
    loadSummary();
  }, []);

  async function createMessage(e: React.FormEvent) {
    e.preventDefault();

    setError("");
    setSuccess("");

    if (!sender || !subject || !body) {
      setError("Please fill in all message fields.");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(
        `${API_URL}/api/messages/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            sender,
            subject,
            body,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to create message");
      }

      setSender("");
      setSubject("");
      setBody("");

      await loadMessages();
      await loadSummary();

      setSuccess("Message created successfully.");
    } catch {
      setError("Failed to create message.");
    } finally {
      setLoading(false);
    }
  }

  async function analyzeMessage(id: number) {
    setError("");
    setSuccess("");
    setAnalyzing(id);

    try {
      const response = await fetch(
        `${API_URL}/api/messages/${id}/analyze`,
        {
          method: "POST",
        }
      );

      if (!response.ok) {
        throw new Error("Analysis failed");
      }

      await loadMessages();
      await loadSummary();

      setSuccess("Message analyzed successfully.");
    } catch {
      setError("AI analysis failed.");
    } finally {
      setAnalyzing(null);
    }
  }

  async function deleteMessage(id: number) {
    setError("");
    setSuccess("");

    try {
      const response = await fetch(
        `${API_URL}/api/messages/${id}`,
        {
          method: "DELETE",
        }
      );

      if (!response.ok) {
        throw new Error("Delete failed");
      }

      await loadMessages();
      await loadSummary();

      setSuccess("Message deleted successfully.");
    } catch {
      setError("Failed to delete message.");
    }
  }

  async function applyFilters() {
    setError("");
    setSuccess("");
    await loadMessages();
  }

  return (
    <main className="min-h-screen bg-slate-100 px-6 py-8">
      <div className="mx-auto max-w-7xl">

        {/* Header */}
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-slate-900">
            AI Message Classifier
          </h1>

          <p className="mt-2 text-slate-600">
            Classify, prioritize and understand business messages using AI.
          </p>
        </header>

        {/* Success Message */}
        {success && (
          <div className="mb-6 rounded-lg border border-green-200 bg-green-50 px-4 py-3 text-green-700">
            ✓ {success}
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="mb-6 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-red-700">
            {error}
          </div>
        )}

        {/* Dashboard */}
        <section className="mb-8 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">

          <StatCard
            title="Total Messages"
            value={summary?.total_messages ?? 0}
          />

          <StatCard
            title="Critical"
            value={summary?.by_priority?.Critical ?? 0}
          />

          <StatCard
            title="High"
            value={summary?.by_priority?.High ?? 0}
          />

          <StatCard
            title="Medium"
            value={summary?.by_priority?.Medium ?? 0}
          />

        </section>

        <div className="grid gap-8 lg:grid-cols-3">

          {/* Create Message */}
          <section className="rounded-xl bg-white p-6 shadow-sm">

            <h2 className="mb-5 text-xl font-semibold text-slate-900">
              New Message
            </h2>

            <form
              onSubmit={createMessage}
              className="space-y-4"
            >

              <input
                value={sender}
                onChange={(e) => setSender(e.target.value)}
                placeholder="Sender"
                className="w-full rounded-lg border border-slate-300 px-4 py-3 outline-none focus:border-blue-500"
              />

              <input
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                placeholder="Subject"
                className="w-full rounded-lg border border-slate-300 px-4 py-3 outline-none focus:border-blue-500"
              />

              <textarea
                value={body}
                onChange={(e) => setBody(e.target.value)}
                placeholder="Message body"
                rows={7}
                className="w-full rounded-lg border border-slate-300 px-4 py-3 outline-none focus:border-blue-500"
              />

              <button
                type="submit"
                disabled={loading}
                className="w-full rounded-lg bg-blue-600 px-4 py-3 font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {loading ? "Creating..." : "Create Message"}
              </button>

            </form>
          </section>

          {/* Message History */}
          <section className="lg:col-span-2">

            <div className="mb-4 rounded-xl bg-white p-5 shadow-sm">

              <h2 className="mb-4 text-xl font-semibold text-slate-900">
                Message History
              </h2>

              <div className="grid gap-3 md:grid-cols-3">

                <input
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      applyFilters();
                    }
                  }}
                  placeholder="Search..."
                  className="rounded-lg border border-slate-300 px-4 py-2 outline-none focus:border-blue-500"
                />

                <select
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                  className="rounded-lg border border-slate-300 px-4 py-2 outline-none focus:border-blue-500"
                >
                  <option value="">
                    All Categories
                  </option>

                  <option value="Incident">
                    Incident
                  </option>

                  <option value="Request">
                    Request
                  </option>

                  <option value="Complaint">
                    Complaint
                  </option>

                  <option value="Inquiry">
                    Inquiry
                  </option>

                  <option value="General">
                    General
                  </option>
                </select>

                <select
                  value={priority}
                  onChange={(e) => setPriority(e.target.value)}
                  className="rounded-lg border border-slate-300 px-4 py-2 outline-none focus:border-blue-500"
                >
                  <option value="">
                    All Priorities
                  </option>

                  <option value="Critical">
                    Critical
                  </option>

                  <option value="High">
                    High
                  </option>

                  <option value="Medium">
                    Medium
                  </option>

                  <option value="Low">
                    Low
                  </option>
                </select>

              </div>

              <button
                onClick={applyFilters}
                className="mt-3 rounded-lg bg-slate-800 px-4 py-2 text-sm font-medium text-white transition hover:bg-slate-900"
              >
                Search / Filter
              </button>

            </div>

            {/* Messages */}
            <div className="space-y-4">

              {messages.length === 0 ? (

                <div className="rounded-xl bg-white p-8 text-center text-slate-500 shadow-sm">
                  No messages found.
                </div>

              ) : (

                messages.map((message) => (

                  <article
                    key={message.id}
                    className="rounded-xl bg-white p-6 shadow-sm"
                  >

                    {/* Message Header */}
                    <div className="flex items-start justify-between gap-4">

                      <div>

                        <p className="text-sm text-slate-500">
                          {message.sender}
                        </p>

                        <h3 className="mt-1 text-lg font-semibold text-slate-900">
                          {message.subject}
                        </h3>

                      </div>

                      <button
                        onClick={() => deleteMessage(message.id)}
                        className="text-sm text-red-600 transition hover:text-red-800"
                      >
                        Delete
                      </button>

                    </div>

                    {/* Message Body */}
                    <p className="mt-3 whitespace-pre-wrap text-slate-700">
                      {message.body}
                    </p>

                    {/* AI Classification */}
                    {message.category && (

                      <div className="mt-5 grid gap-3 sm:grid-cols-3">

                        <Badge
                          label="Category"
                          value={message.category}
                        />

                        <Badge
                          label="Priority"
                          value={message.priority ?? "N/A"}
                        />

                        <Badge
                          label="Sentiment"
                          value={message.sentiment ?? "N/A"}
                        />

                      </div>

                    )}

                    {/* AI Result */}
                    {message.summary && (

                      <div className="mt-5 rounded-lg bg-slate-50 p-4">

                        <p className="font-semibold text-slate-800">
                          AI Summary
                        </p>

                        <p className="mt-1 text-slate-600">
                          {message.summary}
                        </p>

                        {message.suggested_action && (
                          <>
                            <p className="mt-4 font-semibold text-slate-800">
                              Suggested Action
                            </p>

                            <p className="mt-1 text-slate-600">
                              {message.suggested_action}
                            </p>
                          </>
                        )}

                      </div>

                    )}

                    {/* Analyze Button */}
                    <button
                      onClick={() => analyzeMessage(message.id)}
                      disabled={analyzing === message.id}
                      className="mt-5 rounded-lg bg-emerald-600 px-4 py-2 font-medium text-white transition hover:bg-emerald-700 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                      {analyzing === message.id
                        ? "Analyzing..."
                        : message.category
                        ? "Re-analyze"
                        : "Analyze with AI"}
                    </button>

                  </article>

                ))

              )}

            </div>

          </section>
        </div>
      </div>
    </main>
  );
}


/* Dashboard Card */

function StatCard({
  title,
  value,
}: {
  title: string;
  value: number;
}) {
  return (
    <div className="rounded-xl bg-white p-5 shadow-sm">

      <p className="text-sm text-slate-500">
        {title}
      </p>

      <p className="mt-2 text-3xl font-bold text-slate-900">
        {value}
      </p>

    </div>
  );
}


/* AI Result Badge */

function Badge({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-lg bg-slate-100 p-3">

      <p className="text-xs font-medium uppercase text-slate-500">
        {label}
      </p>

      <p className="mt-1 font-semibold text-slate-800">
        {value}
      </p>

    </div>
  );
}