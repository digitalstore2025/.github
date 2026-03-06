import { useState } from 'react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function PromptPanel() {
  const [prompt, setPrompt] = useState('Write API docs for a payments service.');
  const [result, setResult] = useState('');

  const callApi = async (endpoint, payload) => {
    const res = await fetch(`${API_URL}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    setResult(JSON.stringify(data, null, 2));
  };

  return (
    <div className="container">
      <h1>ExplainLLM</h1>
      <textarea value={prompt} onChange={(e) => setPrompt(e.target.value)} rows={8} />
      <div className="actions">
        <button onClick={() => callApi('/analyze', { prompt })}>Analyze</button>
        <button onClick={() => callApi('/fix', { prompt })}>Fix</button>
        <button onClick={() => callApi('/benchmark', { prompt })}>Benchmark</button>
        <button onClick={() => callApi('/optimize', { task: prompt })}>Optimize</button>
      </div>
      <h2>Optimization Results Panel</h2>
      <pre>{result || 'No results yet.'}</pre>
    </div>
  );
}
