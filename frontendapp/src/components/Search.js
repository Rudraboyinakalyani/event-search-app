import React, { useState } from 'react';
import axios from 'axios';
import './Search.css'; // Ensure this file exists

const SearchEvents = () => {
  const [query, setQuery] = useState('');
  const [startTime, setStartTime] = useState('');
  const [endTime, setEndTime] = useState('');
  const [limit, setLimit] = useState('');
  const [results, setResults] = useState([]);
  const [searchTime, setSearchTime] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    setLoading(true);
    try {
      const payload = {
        query,
        start_time: parseInt(startTime) || 0,
        end_time: parseInt(endTime) || 9999999999,
      };

      const parsedLimit = parseInt(limit);
      if (!isNaN(parsedLimit) && parsedLimit > 0) {
        payload.limit = parsedLimit;
      }

      const res = await axios.post('http://127.0.0.1:8000/api/search/', payload);
      setResults(res.data.results || []);
      setSearchTime(res.data.search_time || 0);
    } catch (error) {
      console.error(' Search failed:', error);
      alert('Search failed. Check input values or backend connection.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2> Search Event Logs</h2>

      <div className="form-group">
        <input
          type="text"
          placeholder="Query (IP, Account ID, Action)"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <input
          type="number"
          placeholder="Start Time (epoch)"
          value={startTime}
          onChange={(e) => setStartTime(e.target.value)}
        />
        <input
          type="number"
          placeholder="End Time (epoch)"
          value={endTime}
          onChange={(e) => setEndTime(e.target.value)}
        />
        <input
          type="number"
          placeholder="Limit (optional)"
          value={limit}
          onChange={(e) => setLimit(e.target.value)}
        />
        <button onClick={handleSearch} disabled={loading}>
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>

      {searchTime !== null && (
        <p className="message"> Search took {searchTime}s</p>
      )}

      {results.length > 0 && (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Account ID</th>
                <th>Source IP</th>
                <th>Destination IP</th>
                <th>Action</th>
                <th>Start</th>
                <th>End</th>
                <th>File</th>
              </tr>
            </thead>
            <tbody>
              {results.map((event, index) => (
                <tr key={index}>
                  <td>{event.account_id}</td>
                  <td>{event.srcaddr}</td>
                  <td>{event.dstaddr}</td>
                  <td>{event.action}</td>
                  <td>{event.starttime}</td>
                  <td>{event.endtime}</td>
                  <td>{event.file_name}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {results.length === 0 && searchTime !== null && !loading && (
        <p className="message"> No results found.</p>
      )}
    </div>
  );
};

export default SearchEvents;
