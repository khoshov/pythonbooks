import { Search } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { useState } from 'react';
import type { Publisher } from '@/types';

interface BookFiltersProps {
  publishers: Publisher[];
  onSearch: (query: string) => void;
  onCategoryChange: (category: string) => void;
  onPublisherChange: (publisherId: string) => void;
  onSortChange: (sort: string) => void;
}

export default function BookFilters({
  publishers,
  onSearch,
  onCategoryChange,
  onPublisherChange,
  onSortChange,
}: BookFiltersProps) {
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(searchQuery);
  };

  return (
    <Card className="mb-8">
      <CardHeader>
        <CardTitle>Фильтр книг</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="space-y-2">
            <label className="text-sm font-medium">Поиск</label>
            <form onSubmit={handleSearch} className="flex space-x-2">
              <Input
                type="text"
                placeholder="Поиск книг, авторов..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
              <Button type="submit" size="sm">
                <Search className="h-4 w-4" />
              </Button>
            </form>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">Категория</label>
            <Select onValueChange={onCategoryChange}>
              <SelectTrigger>
                <SelectValue placeholder="Все категории" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Все категории</SelectItem>
                <SelectItem value="beginner">Начальный</SelectItem>
                <SelectItem value="intermediate">Средний</SelectItem>
                <SelectItem value="advanced">Продвинутый</SelectItem>
                <SelectItem value="web">Веб-разработка</SelectItem>
                <SelectItem value="data">Наука о данных</SelectItem>
                <SelectItem value="ml">Машинное обучение</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">Издатель</label>
            <Select onValueChange={onPublisherChange}>
              <SelectTrigger>
                <SelectValue placeholder="Все издатели" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Все издатели</SelectItem>
                {publishers.map((publisher) => (
                  <SelectItem key={publisher.id} value={publisher.id.toString()}>
                    {publisher.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">Сортировать по</label>
            <Select defaultValue="-created" onValueChange={onSortChange}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="-created">Новейшие</SelectItem>
                <SelectItem value="title">Название от А до Я</SelectItem>
                <SelectItem value="-title">Название от Я до А</SelectItem>
                <SelectItem value="published_at">Старейшие</SelectItem>
                <SelectItem value="-published_at">Последние опубликованные</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}