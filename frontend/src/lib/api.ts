import axios from 'axios';
import type { Book, Publisher, Tag, PaginatedResponse } from '@/types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const booksApi = {
  getBooks: async (params?: {
    search?: string;
    category?: string;
    publisher?: string;
    sort?: string;
    page?: number;
  }): Promise<PaginatedResponse<Book>> => {
    const response = await api.get('/books/', { params });
    return response.data;
  },

  getBook: async (id: number): Promise<Book> => {
    const response = await api.get(`/books/${id}/`);
    return response.data;
  },

  getPublishers: async (): Promise<Publisher[]> => {
    const response = await api.get('/publishers/');
    return response.data.results || response.data;
  },

  getTags: async (): Promise<Tag[]> => {
    const response = await api.get('/tags/');
    return response.data.results || response.data;
  },
};

export default api;