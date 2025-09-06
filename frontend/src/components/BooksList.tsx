import React, { useState, useEffect } from 'react';
import { Loader2 } from 'lucide-react';
import BookCard from './BookCard';
import LazyBookCard from './LazyBookCard';
import BookFilters from './BookFilters';
import { Button } from '@/components/ui/button';
import { useInfiniteScroll } from '@/hooks/useInfiniteScroll';
import { booksApi } from '@/lib/api';
import type { Book, Publisher, Tag } from '@/types';
import type { TagsResponse } from '@/lib/api';

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
    tag: '', // Добавляем фильтр по тегу
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
      const params: Record<string, any> = {
        page: isLoadMore ? filters.page + 1 : 1,
      };

      // Добавляем фильтры только если они не пустые
      if (filters.search) params.search = filters.search;
      if (filters.category && filters.category !== 'all') params.category = filters.category;
      if (filters.publisher && filters.publisher !== 'all') params.publisher = filters.publisher;
      if (filters.tag && filters.tag !== 'all') params.tag = filters.tag; // Исправляем условие для тегов
      if (filters.ordering) params.ordering = filters.ordering;

      console.log('[DEBUG] Загрузка книг с параметрами:', JSON.stringify(params, null, 2));

      const response = await booksApi.getBooks(params);
      console.log('[DEBUG] Получено книг:', response.results.length);
      
      if (isLoadMore) {
        setBooks(prev => [...prev, ...response.results]);
        setFilters(prev => ({ ...prev, page: prev.page + 1 }));
      } else {
        setBooks(response.results);
        setFilters(prev => ({ ...prev, page: 1 }));
      }
      
      setNextPage(response.next);
    } catch (error) {
      console.error('[DEBUG] Ошибка загрузки книг:', error);
    } finally {
      setLoading(false);
      setLoadingMore(false);
    }
  };

  const loadInitialData = async () => {
    try {
      console.log('[DEBUG] Загрузка начальных данных...');
      const [publishersResponse, tagsResponse] = await Promise.all([
        booksApi.getPublishers(),
        booksApi.getTags(),
      ]);
      
      console.log('[DEBUG] Raw publishers response:', publishersResponse);
      console.log('[DEBUG] Raw tags response:', tagsResponse);
      
      // Обрабатываем ответ от API правильно
      const publishersData = publishersResponse.results || publishersResponse;
      const tagsData = tagsResponse.results || tagsResponse;
      
      console.log('[DEBUG] Publishers data type:', typeof publishersData);
      console.log('[DEBUG] Tags data type:', typeof tagsData);
      console.log('[DEBUG] Publishers is array:', Array.isArray(publishersData));
      console.log('[DEBUG] Tags is array:', Array.isArray(tagsData));
      console.log('[DEBUG] Publishers data:', publishersData);
      console.log('[DEBUG] Tags data:', tagsData);
      
      // Убедимся, что мы правильно извлекаем данные
      const finalPublishers = Array.isArray(publishersData) 
        ? publishersData 
        : (publishersData?.results || []);
      
      // Исправленная обработка тегов
      const finalTags = Array.isArray(tagsData) 
        ? tagsData 
        : (tagsData?.results || []);
      
      console.log('[DEBUG] Final publishers:', finalPublishers);
      console.log('[DEBUG] Final tags:', finalTags);
      console.log('[DEBUG] Final tags count:', finalTags.length);
      
      setPublishers(finalPublishers);
      setTags(finalTags);
    } catch (error) {
      console.error('[DEBUG] Ошибка loadInitialData:', error);
      console.error('[DEBUG] Error stack:', error.stack);
    }
  };

  useEffect(() => {
    loadInitialData();
  }, []);

  useEffect(() => {
    console.log('[DEBUG] Перезагрузка книг из-за смены фильтров');
    loadBooks();
  }, [filters.search, filters.category, filters.publisher, filters.tag, filters.ordering]); // Добавляем filters.tag

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

  const handleTagChange = (tag: string) => {
    const tagValue = tag === 'all' ? '' : tag;
    console.log('[DEBUG] Tag filter changed to:', tag, 'Tag value:', tagValue);
    setFilters(prev => ({ ...prev, tag: tagValue, page: 1 }));
  };

  const handleSortChange = (ordering: string) => {
    setFilters(prev => ({ ...prev, ordering, page: 1 }));
  };

  const handleLoadMore = () => {
    console.log('[DEBUG] handleLoadMore вызван, nextPage:', nextPage, 'loadingMore:', loadingMore);
    if (nextPage && !loadingMore) {
      console.log('[DEBUG] Условия выполнены, запускаем loadBooks(true)');
      loadBooks(true);
    } else {
      console.log('[DEBUG] Условия не выполнены для загрузки еще');
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
        tags={tags} // Убираем дополнительную фильтрацию, так как она уже происходит в BookFilters
        onSearch={handleSearch}
        onCategoryChange={handleCategoryChange}
        onPublisherChange={handlePublisherChange}
        onSortChange={handleSortChange}
        onTagChange={handleTagChange} // Добавляем обработчик тегов
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
            <div 
              ref={sentinelRef} 
              className="flex justify-center mt-8 py-4 border-2 border-dashed border-gray-300 bg-gray-50"
              style={{ minHeight: '50px' }}
            >
              {loadingMore ? (
                <div className="flex items-center">
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  <span>Загрузка...</span>
                </div>
              ) : (
                <div className="text-gray-500 text-sm">
                  [DEBUG] Infinite Scroll Sentinel - Прокрутите до этого элемента
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