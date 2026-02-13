import axios from 'axios';
import type { Author, Book, Publisher, Tag, PaginatedResponse } from '@/types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const booksApi = {
  getBooks: async (params?: {
    author?: string;
    tag?: string;
    publisher?: string;
    ordering?: string;
    page?: number;
  }): Promise<PaginatedResponse<Book>> => {
    const response = await api.get('/books/', { params });
    return response.data;
  },

  searchBooks: async (params?: {
    search?: string;
    author?: string;
    tag?: string;
    publisher?: string;
    ordering?: string;
    page?: number;
  }): Promise<PaginatedResponse<Book>> => {
    const response = await api.get('/search/', { params });
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

  getAuthors: async (): Promise<Author[]> => {
    const allAuthors: Author[] = [];
    let page = 1;
    let hasMore = true;

    while (hasMore) {
      const response = await api.get('/authors/', { params: { page } });
      const data = response.data;

      if (data.results) {
        allAuthors.push(...data.results);
        hasMore = !!data.next;
        page++;
      } else {
        // Non-paginated response
        allAuthors.push(...data);
        hasMore = false;
      }
    }

    return allAuthors;
  },
};

export default api;