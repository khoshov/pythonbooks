import React, { useState, useEffect } from 'react';
import { Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useIntersectionObserver } from '@/hooks/useIntersectionObserver';

interface BookImageProps {
  src: string;
  alt: string;
  className?: string;
  containerClassName?: string;
  enableIntersectionObserver?: boolean;
}

export default function BookImage({ 
  src, 
  alt, 
  className, 
  containerClassName, 
  enableIntersectionObserver = true 
}: BookImageProps) {
  const [isLoading, setIsLoading] = useState(true);
  const [hasError, setHasError] = useState(false);
  const [shouldLoad, setShouldLoad] = useState(!enableIntersectionObserver);

  const { elementRef, hasIntersected } = useIntersectionObserver({
    triggerOnce: true,
    threshold: 0.1,
    rootMargin: '50px',
  });

  // Load image when it comes into view or immediately if intersection observer is disabled
  useEffect(() => {
    if (enableIntersectionObserver && hasIntersected) {
      setShouldLoad(true);
    }
  }, [enableIntersectionObserver, hasIntersected]);

  const handleLoad = () => {
    setIsLoading(false);
  };

  const handleError = (e: React.SyntheticEvent<HTMLImageElement>) => {
    setIsLoading(false);
    setHasError(true);
    const target = e.target as HTMLImageElement;
    target.src = '/placeholder.svg';
  };

  return (
    <div 
      ref={enableIntersectionObserver ? elementRef : null}
      className={cn("relative bg-gray-100 overflow-hidden", containerClassName)}
    >
      {(!shouldLoad || isLoading) && !hasError && (
        <div className="absolute inset-0 flex items-center justify-center bg-gray-100">
          <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
        </div>
      )}
      {shouldLoad && (
        <img
          src={src || '/placeholder.svg'}
          alt={alt}
          className={cn("transition-all duration-300", className)}
          onLoad={handleLoad}
          onError={handleError}
          loading="lazy"
        />
      )}
    </div>
  );
}