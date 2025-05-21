// Full Next.js App Entry - pages/index.tsx
"use client";

import { useState } from "react";
import Head from "next/head";

export default function Home() {
  const [repoUrl, setRepoUrl] = useState("");
  const [commitCount, setCommitCount] = useState<number | null>(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [repoAnalyzed, setRepoAnalyzed] = useState(false);
  const [analyzeMessage, setAnalyzeMessage] = useState("");

  const handleAnalyze = async () => {
    setLoading(true);
    setError("");
    setAnalyzeMessage("");
    try {
      const analyzeRes = await fetch("http://codebase-time-traveler-production.up.railway.app/analyze-github", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ repo_url: repoUrl, max_commits: commitCount || 10 }),
      });
      if (!analyzeRes.ok) throw new Error("Failed to analyze repo. Check if the URL is valid and a public Github repository.");
      setRepoAnalyzed(true);
      setAnalyzeMessage("✅ Repository successfully analyzed. You may now ask a question.");
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

  const handleAsk = async () => {
    setLoading(true);
    setAnswer("");
    setError("");
    try {
      const askRes = await fetch("http://codebase-time-traveler-production.up.railway.app/ask-question", {
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
      <div className="min-h-screen flex flex-col">
        <main className="flex-grow max-w-2xl mx-auto mt-12 p-4 space-y-6">
          <h1 className="text-3xl font-bold">Github Codebase Time Traveler</h1>
          <input
            className="w-full border px-3 py-2 rounded"
            placeholder="Enter public GitHub repo URL"
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
          />
          <input
            type="number"
            min={1}
            className="w-full border px-3 py-2 rounded"
            value={commitCount ?? ""}
            onChange={(e) => {
              const val = e.target.value;
              setCommitCount(val === "" ? null : Number(val));
            }}
            placeholder="How many commits to analyze (e.g., 10)"
          />
          <p className="text-sm text-yellow-600">
            ⚠️ Analyzing a large number of commits may take a long time to process.
          </p>
            
          <button
            onClick={handleAnalyze}
            disabled={loading || !repoUrl}
            className="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
          >
            {loading ? "Analyzing Repo..." : "Analyze Repo"}
          </button>

          {repoAnalyzed && (
            <>
              <textarea
                className="w-full border px-3 py-2 rounded"
                placeholder="Ask a question about this repo’s history…"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
              />
              <button
                onClick={handleAsk}
                disabled={loading || !question}
                className="bg-black text-white px-4 py-2 rounded disabled:opacity-50"
              >
                {loading ? "Thinking..." : "Ask"}
              </button>
            </>
          )}
          {analyzeMessage && <p className="text-green-600 font-medium">{analyzeMessage}</p>}
          {answer && (
            <div className="bg-white text-black border border-gray-300 p-4 rounded whitespace-pre-wrap">
              {answer}
            </div>
          )}
          {error && <p className="text-red-600">{error}</p>}
        </main>
        <footer className="border-t px-4 py-6 text-center text-sm text-gray-600 ">
          <p>
            Built by <span className="font-medium">Chris Lew</span> —{" "}
            <a href="https://github.com/chrislkl/codebase-time-traveler" className="text-blue-600 hover:underline" target="_blank">
              GitHub
            </a>{" "}
            |{" "}
            <a href="https://www.linkedin.com/in/christopher-lew-kew-lin/" className="text-blue-600 hover:underline" target="_blank">
              LinkedIn
            </a>{" "}
            |{" "}
            <a href="mailto:christopher.lew916@gmail.com" className="text-blue-600 hover:underline">
              Email
            </a>
          </p>
        </footer>
      </div>
    </>
  );
}
