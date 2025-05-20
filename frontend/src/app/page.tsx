"use client";

import { useState } from "react";
import Head from "next/head";

export default function Home() {
  const [repoUrl, setRepoUrl] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAsk = async () => {
    setLoading(true);
    setAnswer("");
    setError("");
    try {
      const analyzeRes = await fetch("http://localhost:8000/analyze-github", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ repo_url: repoUrl, max_commits: 30 }),
      });
      if (!analyzeRes.ok) throw new Error("Failed to analyze repo");

      const askRes = await fetch("http://localhost:8000/ask-question", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ repo_url: repoUrl, question }),
      });
      if (!askRes.ok) throw new Error("Failed to get answer");

      const data = await askRes.json();
      setAnswer(data.answer);
    } catch (err) {
        if (err instanceof Error) {
            setError(err.message);
        } else {
            setError("An unknown error occurred");
        }
    } finally {
    setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>Github Codebase Time Traveler</title>
        <meta name="description" content="Ask questions about GitHub repo history using LLMs" />
      </Head>
      <main className="max-w-2xl mx-auto mt-12 p-4 space-y-6">
        <h1 className="text-3xl font-bold">Codebase Time Traveler</h1>
        <input
          className="w-full border px-3 py-2 rounded"
          placeholder="Enter public GitHub repo URL"
          value={repoUrl}
          onChange={(e) => setRepoUrl(e.target.value)}
        />
        <textarea
          className="w-full border px-3 py-2 rounded"
          placeholder="Ask a question about this repo’s history…"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <button
          onClick={handleAsk}
          disabled={loading || !repoUrl || !question}
          className="bg-black text-white px-4 py-2 rounded disabled:opacity-50"
        >
          {loading ? "Thinking..." : "Ask"}
        </button>
        {answer && (
          <div className="bg-black text-white border border-gray-300 p-4 rounded whitespace-pre-wrap">
            {answer}
          </div>
        )}
        {error && <p className="text-red-600">{error}</p>}
      </main>
    </>
  );
}
