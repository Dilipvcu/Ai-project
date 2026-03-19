import React, { useState } from 'react';

interface DocumentUploaderProps {
  onUpload: (file: File) => Promise<void>;
  isLoading?: boolean;
}

export const DocumentUploader: React.FC<DocumentUploaderProps> = ({
  onUpload,
  isLoading = false,
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = async (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    
    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      await handleFileUpload(files[0]);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.currentTarget.files;
    if (files && files.length > 0) {
      handleFileUpload(files[0]);
    }
  };

  const handleFileUpload = async (file: File) => {
    try {
      setError(null);
      
      // Validate file
      const maxSize = 50 * 1024 * 1024; // 50MB
      if (file.size > maxSize) {
        setError('File size exceeds 50MB limit');
        return;
      }

      const supportedTypes = ['pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg'];
      const fileExt = file.name.split('.').pop()?.toLowerCase();
      
      if (!fileExt || !supportedTypes.includes(fileExt)) {
        setError(`File type not supported. Supported: ${supportedTypes.join(', ')}`);
        return;
      }

      await onUpload(file);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed');
    }
  };

  return (
    <div
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
        isDragging
          ? 'border-blue-500 bg-blue-50'
          : 'border-gray-300 hover:border-gray-400'
      } ${isLoading ? 'opacity-50 pointer-events-none' : ''}`}
    >
      <div className="space-y-4">
        <div className="text-4xl">📄</div>
        <div>
          <h3 className="text-lg font-semibold text-gray-900">
            Drag and drop your document
          </h3>
          <p className="text-sm text-gray-500 mt-1">
            or click to select from your computer
          </p>
        </div>
        
        <input
          type="file"
          onChange={handleFileChange}
          disabled={isLoading}
          className="hidden"
          id="file-input"
        />
        
        <label htmlFor="file-input">
          <button
            type="button"
            onClick={() => document.getElementById('file-input')?.click()}
            disabled={isLoading}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {isLoading ? 'Uploading...' : 'Select File'}
          </button>
        </label>

        <p className="text-xs text-gray-500">
          Supported formats: PDF, DOCX, TXT, PNG, JPG (Max 50MB)
        </p>

        {error && (
          <div className="mt-4 p-3 bg-red-100 text-red-700 rounded text-sm">
            {error}
          </div>
        )}
      </div>
    </div>
  );
};
