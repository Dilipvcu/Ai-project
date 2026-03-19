'use client';

import React, { useState } from 'react';

interface DocumentUploaderProps {
  onFileUpload: (fileName: string) => void;
}

export default function DocumentUploader({ onFileUpload }: DocumentUploaderProps) {
  const [file, setFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [analytics, setAnalytics] = useState<any>(null);
  const [searchResults, setSearchResults] = useState<any>(null);
  const [showAnalytics, setShowAnalytics] = useState(false);
  const [showSearch, setShowSearch] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      setError(null);
      setSuccess(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file');
      return;
    }

    setIsLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('http://localhost:8000/api/documents/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      const data = await response.json();
      setSuccess(`✅ Document uploaded successfully! ID: ${data.document_id}`);
      onFileUpload(file.name);
      setFile(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed');
    } finally {
      setIsLoading(false);
    }
  };

  const handleViewAnalytics = async () => {
    try {
      setShowAnalytics(true);
      setIsLoading(true);
      const response = await fetch('http://localhost:8000/api/analysis/analytics', {
        method: 'GET',
      });

      if (!response.ok) {
        throw new Error('Failed to fetch analytics');
      }

      const data = await response.json();
      setAnalytics(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch analytics');
      setShowAnalytics(false);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearchDocuments = async () => {
    try {
      setShowSearch(true);
      setIsLoading(true);
      const response = await fetch('http://localhost:8000/api/search/documents', {
        method: 'GET',
      });

      if (!response.ok) {
        throw new Error('Failed to search documents');
      }

      const data = await response.json();
      setSearchResults(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to search documents');
      setShowSearch(false);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* File Input */}
      <div className="border-2 border-dashed border-indigo-300 rounded-lg p-8 text-center hover:border-indigo-500 transition">
        <label className="cursor-pointer">
          <div className="text-4xl mb-3">📁</div>
          <p className="text-lg font-semibold text-gray-700 mb-2">
            Drop your document here or click to browse
          </p>
          <p className="text-sm text-gray-500 mb-4">
            Supported formats: PDF, DOCX, TXT
          </p>
          <input
            type="file"
            onChange={handleFileChange}
            accept=".pdf,.docx,.txt"
            className="hidden"
            disabled={isLoading}
          />
        </label>
      </div>

      {/* Selected File Display */}
      {file && (
        <div className="bg-indigo-50 border border-indigo-200 rounded-lg p-4">
          <p className="text-sm text-gray-700">
            <strong>Selected file:</strong> {file.name}
          </p>
          <p className="text-xs text-gray-500 mt-1">
            Size: {(file.size / 1024).toFixed(2)} KB
          </p>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-700">❌ Error: {error}</p>
        </div>
      )}

      {/* Success Message */}
      {success && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <p className="text-green-700">{success}</p>
        </div>
      )}

      {/* Upload Button */}
      <button
        type="submit"
        disabled={!file || isLoading}
        className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white font-bold py-3 px-4 rounded-lg transition duration-200"
      >
        {isLoading ? '⏳ Uploading...' : '🚀 Upload Document'}
      </button>

      {/* Additional Features */}
      <div className="grid grid-cols-2 gap-4 mt-6">
        <button
          type="button"
          onClick={handleViewAnalytics}
          disabled={isLoading}
          className="bg-blue-100 hover:bg-blue-200 disabled:bg-gray-300 text-blue-700 font-semibold py-2 px-4 rounded-lg transition"
        >
          {showAnalytics && isLoading ? '⏳ Loading...' : '📊 View Analytics'}
        </button>
        <button
          type="button"
          onClick={handleSearchDocuments}
          disabled={isLoading}
          className="bg-green-100 hover:bg-green-200 disabled:bg-gray-300 text-green-700 font-semibold py-2 px-4 rounded-lg transition"
        >
          {showSearch && isLoading ? '⏳ Searching...' : '🔍 Search Documents'}
        </button>
      </div>

      {/* Analytics Display */}
      {showAnalytics && analytics && (
        <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-bold text-blue-900">📊 Analytics</h3>
            <button
              type="button"
              onClick={() => {
                setShowAnalytics(false);
                setAnalytics(null);
              }}
              className="text-blue-600 hover:text-blue-900 font-bold"
            >
              ✕
            </button>
          </div>
          <pre className="bg-white p-4 rounded border border-blue-200 text-sm overflow-auto max-h-96">
            {JSON.stringify(analytics, null, 2)}
          </pre>
        </div>
      )}

      {/* Search Results Display */}
      {showSearch && searchResults && (
        <div className="mt-6 bg-green-50 border border-green-200 rounded-lg p-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-bold text-green-900">🔍 Search Results</h3>
            <button
              type="button"
              onClick={() => {
                setShowSearch(false);
                setSearchResults(null);
              }}
              className="text-green-600 hover:text-green-900 font-bold"
            >
              ✕
            </button>
          </div>
          <pre className="bg-white p-4 rounded border border-green-200 text-sm overflow-auto max-h-96">
            {JSON.stringify(searchResults, null, 2)}
          </pre>
        </div>
      )}
    </form>
  );
}
