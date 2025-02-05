"use client";

import { useState } from "react";

export default function Home() {
  const [apiKey, setApiKey] = useState("");
  const [event, setEvent] = useState("");
  const [team, setTeam] = useState("editorial");
  const [content, setContent] = useState("");
  const [feedback, setFeedback] = useState(""); // "good" or "bad"
  const [extraPrompt, setExtraPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [feedbackLoading, setFeedbackLoading] = useState(false);
  const [error, setError] = useState("");
  const [regenContent, setRegenContent] = useState("");

  const handleGenerateContent = async () => {
    setLoading(true);
    setError("");
    setContent("");

    try {
      const response = await fetch(`http://localhost:8000/api/v1/generate/${team}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-API-Key": apiKey,
        },
        body: JSON.stringify({ event }),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }

      const data = await response.json();

      let output = "";
      if (data.content) {
        output = data.content;
      } else if (data.script) {
        output = data.script;
      } else if (data.teleprompter_script) {
        output = data.teleprompter_script;
      } else if (data.campaign_ideas || data.analytics_suggestions) {
        output =
            "Campaign Ideas:\n" +
            (data.campaign_ideas || []).join("\n") +
            "\n\nAnalytics Suggestions:\n" +
            (data.analytics_suggestions || []).join("\n");
      } else {
        output = JSON.stringify(data, null, 2);
      }

      setContent(output);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("An unknown error occurred.");
      }
    }
  };

  // Submit feedback (and optionally trigger regeneration if feedback is "bad")
  const handleSubmitFeedback = async () => {
    setFeedbackLoading(true);
    setError("");
    setRegenContent("");

    try {
      const payload = {
        team,
        event,
        original_response: content,
        feedback,
        extra_prompt: feedback === "bad" ? extraPrompt : "", // only send extra prompt when feedback is "bad"
      };

      const response = await fetch("http://localhost:8000/api/v1/feedback", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-API-Key": apiKey,
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`Feedback Error: ${response.statusText}`);
      }

      const data = await response.json();
      if (data.new_response) {
        setRegenContent(data.new_response);
      }
      alert(data.message);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("An unknown error occurred.");
      }
    }
  };

  return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-white text-gray-900 px-4">
        <h1 className="text-4xl font-bold mb-6">Kitco AI Content Gateway</h1>

        <div className="w-full max-w-md space-y-4">
          <input
              type="text"
              placeholder="Enter your API key"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              className="w-full p-3 border rounded-lg shadow-md"
          />

          <input
              type="text"
              placeholder="e.g., A sudden surge in gold prices"
              value={event}
              onChange={(e) => setEvent(e.target.value)}
              className="w-full p-3 border rounded-lg shadow-md"
          />

          <select
              value={team}
              onChange={(e) => setTeam(e.target.value)}
              className="w-full p-3 border rounded-lg shadow-md bg-white"
          >
            <option value="editorial">Editorial</option>
            <option value="video">Video Production</option>
            <option value="anchors">Anchors</option>
            <option value="marketing">Marketing</option>
            <option value="social">Social Media</option>
          </select>

          <button
              onClick={handleGenerateContent}
              className="w-full p-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
              disabled={loading}
          >
            {loading ? "Generating..." : "Generate Content"}
          </button>

          {content && (
              <div className="w-full p-4 border rounded-lg bg-gray-100 mt-4">
                <h2 className="text-lg font-semibold">Generated Content:</h2>
                <p className="whitespace-pre-line">{content}</p>
              </div>
          )}

          {/* Feedback Section */}
          {content && (
              <div className="w-full p-4 border rounded-lg bg-gray-50 mt-4">
                <h2 className="text-lg font-semibold">Feedback</h2>
                <p>Was the generated content good or bad?</p>
                <div className="flex space-x-4 mt-2">
                  <button
                      onClick={() => setFeedback("good")}
                      className={`p-2 border rounded ${feedback === "good" ? "bg-green-300" : ""}`}
                  >
                    Good
                  </button>
                  <button
                      onClick={() => setFeedback("bad")}
                      className={`p-2 border rounded ${feedback === "bad" ? "bg-red-300" : ""}`}
                  >
                    Bad
                  </button>
                </div>

                {/* Extra prompt input shown only when feedback is "bad" */}
                {feedback === "bad" && (
                    <input
                        type="text"
                        placeholder="Enter extra prompt (e.g., make it concise)"
                        value={extraPrompt}
                        onChange={(e) => setExtraPrompt(e.target.value)}
                        className="w-full p-3 border rounded-lg shadow-md mt-2"
                    />
                )}

                <button
                    onClick={handleSubmitFeedback}
                    className="w-full p-3 bg-gray-800 text-white rounded-lg hover:bg-gray-900 transition mt-2"
                    disabled={feedbackLoading}
                >
                  {feedbackLoading ? "Submitting Feedback..." : "Submit Feedback"}
                </button>
              </div>
          )}

          {regenContent && (
              <div className="w-full p-4 border rounded-lg bg-gray-100 mt-4">
                <h2 className="text-lg font-semibold">Regenerated Content:</h2>
                <p className="whitespace-pre-line">{regenContent}</p>
              </div>
          )}

          {error && <p className="text-red-500 text-center">{error}</p>}
        </div>
      </div>
  );
}
