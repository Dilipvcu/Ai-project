import axios, { AxiosInstance } from 'axios';

class APIClient {
  private client: AxiosInstance;

  constructor(baseURL: string = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api') {
    this.client = axios.create({
      baseURL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  // Document endpoints
  async uploadDocument(file: File): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);
    
    return this.client.post('/documents/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  }

  async getDocument(documentId: string): Promise<any> {
    return this.client.get(`/documents/${documentId}`);
  }

  async listDocuments(skip: number = 0, limit: number = 10): Promise<any> {
    return this.client.get('/documents', {
      params: { skip, limit },
    });
  }

  async deleteDocument(documentId: string): Promise<any> {
    return this.client.delete(`/documents/${documentId}`);
  }

  // Analysis endpoints
  async summarizeDocument(documentId: string, maxLength: number = 500): Promise<any> {
    return this.client.post('/analysis/summarize', {
      document_id: documentId,
      max_length: maxLength,
    });
  }

  async extractInsights(documentId: string): Promise<any> {
    return this.client.post('/analysis/extract-insights', {
      document_id: documentId,
    });
  }

  async questionAnswer(documentId: string, question: string): Promise<any> {
    return this.client.post('/analysis/qa', {
      document_id: documentId,
      question,
    });
  }

  // Search endpoints
  async semanticSearch(query: string, topK: number = 5): Promise<any> {
    return this.client.post('/search/semantic', {
      query,
      top_k: topK,
    });
  }

  async getSearchSuggestions(prefix: string): Promise<any> {
    return this.client.get('/search/suggestions', {
      params: { prefix },
    });
  }
}

export const apiClient = new APIClient();
