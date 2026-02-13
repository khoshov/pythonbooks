export interface Author {
  id: number;
  first_name: string;
  last_name: string;
  bio: string;
}

export interface Publisher {
  id: number;
  name: string;
  website: string;
}

export interface Tag {
  id: number;
  name: string;
  slug: string;
  color: string;
}

export interface Comment {
  id: number;
  text: string;
  user: string;
  created: string;
  modified: string;
}

export interface Book {
  id: number;
  title: string;
  author: Author[];
  publisher: Publisher;
  published_at: string;
  cover_image: string;
  description?: string;
  isbn_code?: string;
  total_pages?: number;
  language?: string;
  url?: string;
  tags?: Tag[];
  comments?: Comment[];
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}