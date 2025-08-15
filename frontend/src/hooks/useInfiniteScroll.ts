import { useCallback } from 'react';
import { useIntersectionObserver } from './useIntersectionObserver';

interface UseInfiniteScrollOptions {
  hasNextPage: boolean;
  isLoading: boolean;
  onLoadMore: () => void;
  rootMargin?: string;
}

export function useInfiniteScroll({
  hasNextPage,
  isLoading,
  onLoadMore,
  rootMargin = '100px',
}: UseInfiniteScrollOptions) {
  const { elementRef, isIntersecting } = useIntersectionObserver({
    rootMargin,
    threshold: 0.1,
  });

  // Trigger load more when the element comes into view
  const handleIntersection = useCallback(() => {
    if (isIntersecting && hasNextPage && !isLoading) {
      onLoadMore();
    }
  }, [isIntersecting, hasNextPage, isLoading, onLoadMore]);

  // Call the handler when intersection changes
  handleIntersection();

  return {
    sentinelRef: elementRef,
  };
}