'use client';

import React, { useState } from 'react';
import DocumentUploader from '@/components/DocumentUploader';

export default function Home() {
  const [uploadedFile, setUploadedFile] = useState<string | null>(null);

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            🤖 AI Document Analysis Engine
          </h1>
          <p className="text-xl text-gray-600 mb-2">
            Extract insights from your documents using advanced AI
          </p>
          <p className="text-lg text-indigo-600">
            Powered by GPT-4, Vector Search &amp; Semantic Analysis
          </p>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
          {/* Upload Section */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-lg p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">
                📤 Upload Documents
              </h2>
              <DocumentUploader onFileUpload={setUploadedFile} />
              
              {uploadedFile && (
                <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
                  <p className="text-green-800">
                    ✅ File uploaded: <strong>{uploadedFile}</strong>
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Features Section */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-lg p-8">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">
                ✨ Features
              </h3>
              <ul className="space-y-4">
                <li className="flex items-start">
                  <span className="text-2xl mr-3">📄</span>
                  <div>
                    <p className="font-semibold text-gray-900">Document Support</p>
                    <p className="text-sm text-gray-600">PDF, DOCX, TXT</p>
                  </div>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">🧠</span>
                  <div>
                    <p className="font-semibold text-gray-900">AI Powered</p>
                    <p className="text-sm text-gray-600">GPT-4 Analysis</p>
                  </div>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">🔍</span>
                  <div>
                    <p className="font-semibold text-gray-900">Smart Search</p>
                    <p className="text-sm text-gray-600">Semantic Search</p>
                  </div>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">⚡</span>
                  <div>
                    <p className="font-semibold text-gray-900">Fast & Reliable</p>
                    <p className="text-sm text-gray-600">Real-time Results</p>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>

        {/* API Status */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">📊 System Status</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-4 bg-blue-50 rounded-lg border-l-4 border-blue-500">
              <p className="text-sm text-gray-600">Backend API</p>
              <p className="text-lg font-bold text-blue-600">✅ Running</p>
              <p className="text-xs text-gray-500 mt-1">http://localhost:8000</p>
            </div>
            <div className="p-4 bg-green-50 rounded-lg border-l-4 border-green-500">
              <p className="text-sm text-gray-600">Database</p>
              <p className="text-lg font-bold text-green-600">✅ Connected</p>
              <p className="text-xs text-gray-500 mt-1">PostgreSQL + Redis</p>
            </div>
            <div className="p-4 bg-purple-50 rounded-lg border-l-4 border-purple-500">
              <p className="text-sm text-gray-600">Frontend</p>
              <p className="text-lg font-bold text-purple-600">✅ Ready</p>
              <p className="text-xs text-gray-500 mt-1">Next.js App</p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-12 text-center text-gray-600">
          <p>© 2026 AI Document Analysis Engine. Built with Next.js, FastAPI &amp; AI</p>
          <p className="text-sm mt-2">
            <a href="http://localhost:8000/docs" target="_blank" rel="noopener noreferrer" className="text-indigo-600 hover:underline">
              View API Docs
            </a>
            {' '} | {' '}
            <a href="http://localhost:8000/health" target="_blank" rel="noopener noreferrer" className="text-indigo-600 hover:underline">
              Check Health
            </a>
          </p>
        </footer>
      </div>
    </main>
  );
}
