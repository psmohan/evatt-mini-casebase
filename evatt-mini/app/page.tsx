"use client";

import React, { useState } from "react";
import axios from "axios";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Loader2, Search, Upload } from "lucide-react";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [msg, setMsg] = useState("");
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const upload = async () => {
    if (!file) return alert("Choose a file first");
    const fd = new FormData();
    fd.append("file", file);
    setMsg("Uploading...");
    setLoading(true);
    try {
      const res = await axios.post("http://localhost:8000/ingest", fd, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setMsg(`Ingested ${res.data.ingested_chunks} chunks`);
    } catch (err: any) {
      setMsg("Upload failed: " + (err?.message || err));
    } finally {
      setLoading(false);
    }
  };

  const doSearch = async () => {
    if (!query) return;
    setMsg("Searching...");
    setLoading(true);
    try {
      const res = await axios.post("http://localhost:8000/search", {
        q: query,
        top_k: 5,
      });
      setResults(res.data.results);
      setMsg(`🔍 Found ${res.data.results.length} results`);
    } catch (err: any) {
      setMsg("Search failed: " + (err?.message || err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center p-8">
      <Card className="w-full max-h-screen max-w-3xl shadow-lg border border-gray-200">
        <CardHeader>
          <CardTitle className="text-2xl font-semibold text-center text-gray-800">
            Evatt Mini Casebase — AI Legal Search
          </CardTitle>
        </CardHeader>

        <CardContent>
          {/* Upload Section */}
          <section className="mb-8">
            <h2 className="text-lg font-medium mb-3 text-gray-700">
              Upload PDF / Text File
            </h2>
            <div className="flex gap-3 items-center">
              <Input
                type="file"
                onChange={(e) =>
                  setFile(e.target.files ? e.target.files[0] : null)
                }
                className="flex-1 cursor-pointer"
              />
              <Button
                onClick={upload}
                disabled={loading}
                className="bg-blue-600 hover:bg-blue-700 text-white"
              >
                {loading ? (
                  <Loader2 className="animate-spin mr-2 h-4 w-4" />
                ) : (
                  <Upload className="mr-2 h-4 w-4" />
                )}
                Upload & Ingest
              </Button>
            </div>
            <p className="text-sm text-gray-500 mt-2">{msg}</p>
          </section>

          {/* Search Section */}
          <section>
            <h2 className="text-lg font-medium mb-3 text-gray-700">Search</h2>
            <div className="flex gap-3 items-center">
              <Input
                type="text"
                placeholder="Enter a query, e.g. breach of contract"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="flex-1"
              />
              <Button
                onClick={doSearch}
                disabled={loading}
                className="bg-green-600 hover:bg-green-700 text-white"
              >
                {loading ? (
                  <Loader2 className="animate-spin mr-2 h-4 w-4" />
                ) : (
                  <Search className="mr-2 h-4 w-4" />
                )}
                Search
              </Button>
            </div>
          </section>

          {/* Results Section */}
          <section className="mt-6">
            {results.length > 0 && (
              <div className="mt-4 space-y-4  max-h-[45vh]  overflow-auto">
                {results.map((r) => (
                  <Card
                    key={r.id}
                    className="border border-gray-300 shadow-sm hover:shadow-md transition-shadow"
                  >
                    <CardContent className="p-4">
                      <div className="text-sm text-gray-600 mb-2">
                        <strong>Source:</strong> {r.source} —{" "}
                        <em>score: {r.score.toFixed(3)}</em>
                      </div>
                      <p className="text-gray-800 leading-relaxed">{r.text}</p>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </section>
        </CardContent>
      </Card>
    </div>
  );
}
