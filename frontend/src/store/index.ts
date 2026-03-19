import { create } from 'zustand';

interface Document {
  id: string;
  filename: string;
  status: 'processing' | 'completed' | 'failed';
  size_bytes: number;
  uploaded_at: string;
}

interface DocumentStore {
  documents: Document[];
  selectedDocument: Document | null;
  loading: boolean;
  error: string | null;
  
  setDocuments: (docs: Document[]) => void;
  addDocument: (doc: Document) => void;
  selectDocument: (doc: Document) => void;
  removeDocument: (id: string) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clearError: () => void;
}

export const useDocumentStore = create<DocumentStore>((set) => ({
  documents: [],
  selectedDocument: null,
  loading: false,
  error: null,

  setDocuments: (docs) => set({ documents: docs }),
  addDocument: (doc) => set((state) => ({
    documents: [doc, ...state.documents],
  })),
  selectDocument: (doc) => set({ selectedDocument: doc }),
  removeDocument: (id) => set((state) => ({
    documents: state.documents.filter((d) => d.id !== id),
  })),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
  clearError: () => set({ error: null }),
}));

interface AnalysisStore {
  summary: string | null;
  insights: any | null;
  qaResults: any | null;
  loading: boolean;
  
  setSummary: (summary: string | null) => void;
  setInsights: (insights: any | null) => void;
  setQAResults: (results: any | null) => void;
  setLoading: (loading: boolean) => void;
  clear: () => void;
}

export const useAnalysisStore = create<AnalysisStore>((set) => ({
  summary: null,
  insights: null,
  qaResults: null,
  loading: false,

  setSummary: (summary) => set({ summary }),
  setInsights: (insights) => set({ insights }),
  setQAResults: (qaResults) => set({ qaResults }),
  setLoading: (loading) => set({ loading }),
  clear: () => set({
    summary: null,
    insights: null,
    qaResults: null,
    loading: false,
  }),
}));
