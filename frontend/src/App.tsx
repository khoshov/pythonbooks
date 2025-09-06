import { useState } from 'react';
import Layout from '@/components/Layout';
import BooksList from '@/components/BooksList';
import BookDetailModal from '@/components/BookDetailModal';
import { Button } from '@/components/ui/button';
import type { Book } from '@/types';

function App() {
  const [selectedBookId, setSelectedBookId] = useState<number | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleBookClick = (book: Book) => {
    setSelectedBookId(book.id);
    setIsModalOpen(true);
  };

  const handleSearch = (query: string) => {
    // This will be handled by the BooksList component
    console.log('Search query:', query);
  };

  return (
    <Layout onSearch={handleSearch}>
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-primary/10 to-primary/20 rounded-lg p-8 mb-8 text-center">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">Книги по Python</h1>
        <p className="text-lg text-muted-foreground mb-6 max-w-2xl mx-auto">
          Откройте для себя лучшие книги по программированию на Python для любого уровня навыков. 
          От новичков до экспертов - найдите свою следующую отличную книгу.
        </p>
        <Button 
          size="lg"
          onClick={() => {
            const searchInput = document.querySelector('input[type="text"]') as HTMLInputElement;
            searchInput?.focus();
          }}
        >
          Начать исследование
        </Button>
      </div>

      {/* Books List */}
      <BooksList onBookClick={handleBookClick} />

      {/* Book Detail Modal */}
      <BookDetailModal
        bookId={selectedBookId}
        open={isModalOpen}
        onOpenChange={setIsModalOpen}
      />
    </Layout>
  );
}

export default App;