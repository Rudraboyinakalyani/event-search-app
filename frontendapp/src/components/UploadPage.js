import React, { useState } from 'react';
import axios from 'axios';
import './Upload.css'; // Optional CSS

const UploadFile = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [status, setStatus] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setStatus('');
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first.");
      return;
    }

    setUploading(true);
    setStatus('Uploading...');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post('http://127.0.0.1:8000/api/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      console.log(' Upload success:', res.data);
      setStatus(' Uploaded successfully!');
    } catch (error) {
      console.error(' Upload failed:', error);
      setStatus(' Upload failed!');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-card">
      <h2> Upload Log File</h2>

      <input
        type="file"
        onChange={handleFileChange}
        className="upload-input"
      />

      <button onClick={handleUpload} disabled={uploading}>
        {uploading ? 'Uploading...' : 'Upload'}
      </button>

      {status && <p className="upload-status">{status}</p>}
    </div>
  );
};

export default UploadFile;
