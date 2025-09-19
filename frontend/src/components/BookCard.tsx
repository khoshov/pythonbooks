import { Calendar, User, Building, FileText } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import BookImage from './BookImage';
import type { Book } from '@/types';

interface BookCardProps {
  book: Book;
  onClick?: (book: Book) => void;
}

export default function BookCard({ book, onClick }: BookCardProps) {
  const handleClick = () => {
    onClick?.(book);
  };

  return (
    <Card 
      className="cursor-pointer transition-all hover:shadow-lg hover:-translate-y-1 overflow-hidden py-0 h-full flex flex-col" 
      onClick={handleClick}
    >
      <CardContent className="p-0 flex flex-col h-full">
        <div className="relative">
          <BookImage
            src={book.cover_image}
            alt={book.title}
            className="w-full h-full object-cover hover:scale-105"
            containerClassName="aspect-[3/4]"
          />
          <div className="absolute top-2 left-2">
            {book.tags?.slice(0, 2).map((tag) => (
              <Badge 
                key={tag.id} 
                variant="secondary" 
                className="mb-1 mr-1 text-xs"
                style={{ backgroundColor: tag.color, color: '#fff' }}
              >
                {tag.name}
              </Badge>
            ))}
          </div>
        </div>
        
        <div className="p-4 flex flex-col flex-1">
          <h3 className="font-semibold text-lg mb-2 line-clamp-2">{book.title}</h3>
          
          <div className="space-y-2 text-sm text-muted-foreground flex-1">
            <div className="flex items-center">
              <User className="h-4 w-4 mr-2 flex-shrink-0" />
              <span className="line-clamp-1">
                {book.author && book.author.length > 0 
                  ? book.author.map(a => `${a.first_name} ${a.last_name}`).join(', ')
                  : 'Автор не указан'
                }
              </span>
            </div>
            
            <div className="flex items-center">
              <Building className="h-4 w-4 mr-2 flex-shrink-0" />
              <span className="line-clamp-1">{book.publisher.name}</span>
            </div>
            
            <div className="flex items-center">
              <Calendar className="h-4 w-4 mr-2 flex-shrink-0" />
              <span>{new Date(book.published_at).getFullYear()}</span>
            </div>
            
            {book.total_pages !== null && book.total_pages !== undefined && book.total_pages > 0 && (
              <div className="flex items-center">
                <FileText className="h-4 w-4 mr-2 flex-shrink-0" />
                <span>{book.total_pages} стр.</span>
              </div>
            )}
          </div>
          
          {book.description && (
            <p className="text-sm text-muted-foreground mt-3 line-clamp-3">
              {book.description}
            </p>
          )}
        </div>
      </CardContent>
    </Card>
  );
}