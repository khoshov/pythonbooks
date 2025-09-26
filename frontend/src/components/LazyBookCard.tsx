import BookCard from './BookCard';
import { useIntersectionObserver } from '@/hooks/useIntersectionObserver';
import { cn } from '@/lib/utils';
import type { Book } from '@/types';

interface LazyBookCardProps {
  book: Book;
  onClick?: (book: Book) => void;
  placeholder?: React.ReactNode;
  className?: string;
}

export default function LazyBookCard({ 
  book, 
  onClick, 
  placeholder,
  className 
}: LazyBookCardProps) {
  const { elementRef, hasIntersected } = useIntersectionObserver({
    triggerOnce: true,
    threshold: 0.1,
    rootMargin: '100px',
  });

  const defaultPlaceholder = (
    <div className={cn(
      "animate-pulse bg-gray-200 rounded-lg w-full h-full min-h-[400px]",
      className
    )} />
  );

  return (
    <div ref={elementRef} className="w-full h-full">
      {hasIntersected ? (
        <BookCard book={book} onClick={onClick} />
      ) : (
        placeholder || defaultPlaceholder
      )}
    </div>
  );
}