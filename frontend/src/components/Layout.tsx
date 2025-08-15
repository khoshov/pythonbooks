import React, { useState } from 'react';
import { Search, Book, Sun, Moon, Menu } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

interface LayoutProps {
  children: React.ReactNode;
  onSearch?: (query: string) => void;
}

export default function Layout({ children, onSearch }: LayoutProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [isDark, setIsDark] = useState(false);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch?.(searchQuery);
  };

  const toggleTheme = () => {
    setIsDark(!isDark);
    document.documentElement.classList.toggle('dark');
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto px-4">
          <div className="flex h-16 items-center justify-between">
            <div className="flex items-center space-x-2">
              <Book className="h-6 w-6 text-primary" />
              <span className="text-xl font-bold">Книги по Python</span>
            </div>

            <div className="hidden md:flex items-center space-x-4">
              <form onSubmit={handleSearch} className="flex items-center space-x-2">
                <Input
                  type="text"
                  placeholder="Поиск книг..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-64"
                />
                <Button type="submit" size="sm">
                  <Search className="h-4 w-4" />
                </Button>
              </form>

              <Button
                variant="ghost"
                size="sm"
                onClick={toggleTheme}
              >
                {isDark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
              </Button>
            </div>

            <div className="md:hidden">
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="sm">
                    <Menu className="h-4 w-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuItem>
                    <Search className="mr-2 h-4 w-4" />
                    Поиск
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={toggleTheme}>
                    {isDark ? <Sun className="mr-2 h-4 w-4" /> : <Moon className="mr-2 h-4 w-4" />}
                    {isDark ? 'Светлая тема' : 'Тёмная тема'}
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {children}
      </main>

      {/* Footer */}
      <footer className="border-t border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 mt-auto">
        <div className="container mx-auto px-4 py-8">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <div className="flex space-x-6">
              <a href="#" className="text-sm text-muted-foreground hover:text-foreground">О нас</a>
              <a href="#" className="text-sm text-muted-foreground hover:text-foreground">Контакты</a>
              <a href="#" className="text-sm text-muted-foreground hover:text-foreground">Добавить книгу</a>
            </div>
            <div className="text-sm text-muted-foreground">
              © 2024 Книги по Python. Все права защищены.
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}