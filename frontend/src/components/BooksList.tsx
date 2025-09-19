import { useState, useEffect } from 'react';
import { Loader2 } from 'lucide-react';
import BookCard from './BookCard';
import LazyBookCard from './LazyBookCard';
import BookFilters from './BookFilters';
import { Button } from '@/components/ui/button';
import { useInfiniteScroll } from '@/hooks/useInfiniteScroll';
import { booksApi } from '@/lib/api';
import type { Book, Publisher, Tag } from '@/types';

interface BooksListProps {
  onBookClick: (book: Book) => void;
  enableLazyLoading?: boolean;
  enableInfiniteScroll?: boolean;
}

export default function BooksList({ 
  onBookClick, 
  enableLazyLoading = true, 
  enableInfiniteScroll = true 
}: BooksListProps) {
  const [books, setBooks] = useState<Book[]>([]);
  const [publishers, setPublishers] = useState<Publisher[]>([]);
  const [tags, setTags] = useState<Tag[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [nextPage, setNextPage] = useState<string | null>(null);
  const [filters, setFilters] = useState({
    search: '',
    category: '',
    publisher: '',
    ordering: '-created',
    page: 1,
  });

  const loadBooks = async (isLoadMore = false) => {
    if (isLoadMore) {
      setLoadingMore(true);
    } else {
      setLoading(true);
      setBooks([]);
    }

    try {
      // Create a new params object without the category property
      const { category, ...restFilters } = filters;
      const params = {
        ...restFilters,
        // Map category filter to tag parameter for backend
        tag: category,
        page: isLoadMore ? filters.page + 1 : 1,
      };

      const response = await booksApi.getBooks(params);
      
      if (isLoadMore) {
        setBooks(prev => [...prev, ...response.results]);
        setFilters(prev => ({ ...prev, page: prev.page + 1 }));
      } else {
        setBooks(response.results);
        setFilters(prev => ({ ...prev, page: 1 }));
      }
      
      setNextPage(response.next);
    } catch (error) {
      console.error('Error loading books:', error);
    } finally {
      setLoading(false);
      setLoadingMore(false);
    }
  };

  const loadInitialData = async () => {
    try {
      const [publishersResponse, tagsResponse] = await Promise.all([
        booksApi.getPublishers(),
        booksApi.getTags()
      ]);
      
      setPublishers(publishersResponse);
      setTags(tagsResponse);
    } catch (error) {
      console.error('Error loading initial data:', error);
    }
  };

  useEffect(() => {
    loadInitialData();
  }, []);

  useEffect(() => {
    loadBooks();
  }, [filters.search, filters.category, filters.publisher, filters.ordering]);

  const handleSearch = (search: string) => {
    setFilters(prev => ({ ...prev, search, page: 1 }));
  };

  const handleCategoryChange = (category: string) => {
    const categoryValue = category === 'all' ? '' : category;
    setFilters(prev => ({ ...prev, category: categoryValue, page: 1 }));
  };

  const handlePublisherChange = (publisher: string) => {
    const publisherValue = publisher === 'all' ? '' : publisher;
    setFilters(prev => ({ ...prev, publisher: publisherValue, page: 1 }));
  };

  const handleSortChange = (ordering: string) => {
    setFilters(prev => ({ ...prev, ordering, page: 1 }));
  };

  const handleLoadMore = () => {
    if (nextPage && !loadingMore) {
      loadBooks(true);
    }
  };

  // Use infinite scroll hook
  const { sentinelRef } = useInfiniteScroll({
    hasNextPage: !!nextPage,
    isLoading: loadingMore,
    onLoadMore: handleLoadMore,
  });

  return (
    <div>
      <BookFilters
        publishers={publishers}
        tags={tags}
        onSearch={handleSearch}
        onCategoryChange={handleCategoryChange}
        onPublisherChange={handlePublisherChange}
        onSortChange={handleSortChange}
      />

      {loading ? (
        <div className="flex justify-center items-center py-12">
          <Loader2 className="h-8 w-8 animate-spin" />
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {books.map((book) => (
              enableLazyLoading ? (
                <LazyBookCard
                  key={book.id}
                  book={book}
                  onClick={onBookClick}
                />
              ) : (
                <BookCard
                  key={book.id}
                  book={book}
                  onClick={onBookClick}
                />
              )
            ))}
          </div>

          {books.length === 0 && !loading && (
            <div className="text-center py-12">
              <p className="text-muted-foreground">Книги не найдены</p>
            </div>
          )}

          {/* Infinite scroll sentinel */}
          {enableInfiniteScroll && nextPage && (
            <div ref={sentinelRef} className="flex justify-center mt-8 py-4">
              {loadingMore && (
                <div className="flex items-center">
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  <span>Загрузка...</span>
                </div>
              )}
            </div>
          )}

          {/* Manual load more button (fallback or when infinite scroll is disabled) */}
          {!enableInfiniteScroll && nextPage && (
            <div className="flex justify-center mt-8">
              <Button 
                onClick={handleLoadMore} 
                disabled={loadingMore}
                variant="outline"
              >
                {loadingMore ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Загрузка...
                  </>
                ) : (
                  'Загрузить ещё'
                )}
              </Button>
            </div>
          )}
        </>
      )}
    </div>
  );
}