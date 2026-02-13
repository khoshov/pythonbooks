import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Calendar, User, Building, FileText, Barcode, ExternalLink, Heart, MessageCircle, Loader2 } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import BookImage from '@/components/BookImage';
import Layout from '@/components/Layout';
import { booksApi } from '@/lib/api';
import type { Book } from '@/types';

export default function BookDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [book, setBook] = useState<Book | null>(null);
  const [loading, setLoading] = useState(false);
  const [commentText, setCommentText] = useState('');

  useEffect(() => {
    if (id) {
      loadBookDetails();
    }
  }, [id]);

  const loadBookDetails = async () => {
    if (!id) return;
    
    setLoading(true);
    try {
      const bookData = await booksApi.getBook(parseInt(id));
      setBook(bookData);
    } catch (error) {
      console.error('Error loading book details:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitComment = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Implement comment submission
    console.log('Comment submitted:', commentText);
    setCommentText('');
  };

  const handleSearch = (query: string) => {
    // Navigate back to home with search
    navigate(`/?search=${encodeURIComponent(query)}`);
  };

  if (loading) {
    return (
      <Layout onSearch={handleSearch}>
        <div className="flex justify-center items-center py-12">
          <Loader2 className="h-8 w-8 animate-spin" />
        </div>
      </Layout>
    );
  }

  if (!book) {
    return (
      <Layout onSearch={handleSearch}>
        <div className="text-center py-12">
          <p className="text-muted-foreground mb-4">Книга не найдена</p>
          <Button onClick={() => navigate('/')}>
            <ArrowLeft className="mr-2 h-4 w-4" />
            Назад к каталогу
          </Button>
        </div>
      </Layout>
    );
  }

  return (
    <Layout onSearch={handleSearch}>
      {/* Back Button */}
      <div className="mb-6">
        <Button variant="ghost" onClick={() => navigate('/')}>
          <ArrowLeft className="mr-2 h-4 w-4" />
          Назад к каталогу
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-8">
        {/* Book Cover */}
        <div className="lg:col-span-2">
          <div className="sticky top-4">
            <BookImage
              src={book.cover_image}
              alt={book.title}
              className="w-full rounded-lg shadow-lg hover:scale-105"
              containerClassName="rounded-lg"
            />
          </div>
        </div>

        {/* Book Info */}
        <div className="lg:col-span-3">
          <div className="space-y-6">
            <div>
              <h1 className="text-3xl font-bold mb-4">{book.title}</h1>
              
              <div className="flex flex-wrap gap-2 mb-4">
                <Badge variant="outline" className="flex items-center">
                  <User className="mr-1 h-3 w-3" />
                  {book.author && book.author.length > 0 
                    ? book.author.map(a => `${a.first_name} ${a.last_name}`).join(', ')
                    : 'Автор не указан'
                  }
                </Badge>
                <Badge variant="outline" className="flex items-center">
                  <Building className="mr-1 h-3 w-3" />
                  {book.publisher.name}
                </Badge>
                <Badge variant="outline" className="flex items-center">
                  <Calendar className="mr-1 h-3 w-3" />
                  {new Date(book.published_at).getFullYear()}
                </Badge>
                {book.total_pages !== null && book.total_pages !== undefined && book.total_pages > 0 && (
                  <Badge variant="outline" className="flex items-center">
                    <FileText className="mr-1 h-3 w-3" />
                    {book.total_pages} стр.
                  </Badge>
                )}
                {book.isbn_code && (
                  <Badge variant="outline" className="flex items-center">
                    <Barcode className="mr-1 h-3 w-3" />
                    {book.isbn_code}
                  </Badge>
                )}
              </div>

              {/* Tags */}
              {book.tags && book.tags.length > 0 && (
                <div className="flex flex-wrap gap-2 mb-4">
                  {book.tags.map((tag) => (
                    <Badge 
                      key={tag.id} 
                      variant="secondary"
                      style={{ backgroundColor: tag.color, color: '#fff' }}
                    >
                      {tag.name}
                    </Badge>
                  ))}
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex gap-2 mb-6">
                <Button
                  onClick={() => book.url && window.open(book.url, '_blank', 'noopener,noreferrer')}
                  disabled={!book.url}
                >
                  <ExternalLink className="mr-2 h-4 w-4" />
                  Посмотреть на {book.publisher.name}
                </Button>
                <Button variant="secondary">
                  <Heart className="mr-2 h-4 w-4" />
                  В избранное
                </Button>
              </div>
            </div>

            {/* Description */}
            {book.description && (
              <div className="prose max-w-none">
                <h3 className="text-lg font-semibold mb-2">Описание</h3>
                <p className="text-muted-foreground leading-relaxed">{book.description}</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Comments Section */}
      <div className="mt-12 space-y-6">
        <div className="flex items-center">
          <MessageCircle className="mr-2 h-5 w-5" />
          <h3 className="text-xl font-semibold">Комментарии</h3>
        </div>

        {/* Add Comment Form */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Добавить комментарий</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmitComment} className="space-y-4">
              <Textarea
                placeholder="Поделитесь своими мыслями о этой книге..."
                value={commentText}
                onChange={(e) => setCommentText(e.target.value)}
                required
              />
              <Button type="submit">
                <MessageCircle className="mr-2 h-4 w-4" />
                Опубликовать комментарий
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Comments List */}
        {book.comments && book.comments.length > 0 ? (
          <div className="space-y-4">
            {book.comments.map((comment) => (
              <Card key={comment.id}>
                <CardContent className="pt-4">
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <h4 className="font-semibold">{comment.user}</h4>
                      <p className="text-xs text-muted-foreground">
                        {new Date(comment.created).toLocaleDateString('ru-RU')}
                      </p>
                    </div>
                  </div>
                  <p className="text-sm">{comment.text}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-muted-foreground">
            <MessageCircle className="mx-auto h-12 w-12 mb-4 opacity-50" />
            <p>Комментариев пока нет. Станьте первым, кто поделится своими мыслями!</p>
          </div>
        )}
      </div>
    </Layout>
  );
}