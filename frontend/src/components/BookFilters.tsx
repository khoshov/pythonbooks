import React from 'react';
import { Search } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { useState, useEffect } from 'react';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import type { Publisher, Tag } from '@/types';

interface BookFiltersProps {
  publishers: Publisher[];
  tags: Tag[];
  onSearch: (search: string) => void;
  onCategoryChange: (category: string) => void;
  onPublisherChange: (publisher: string) => void;
  onSortChange: (sort: string) => void;
  onTagChange: (tagId: string) => void;
}

export default function BookFilters({
  publishers,
  tags,
  onSearch,
  onCategoryChange,
  onPublisherChange,
  onSortChange,
  onTagChange
}: BookFiltersProps) {
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(e.target.value);
    onSearch(e.target.value);
  };

  // Фильтруем теги, чтобы исключить пустые значения
  const validTags = Array.isArray(tags) ? tags.filter(tag => tag && tag.id && tag.name) : [];

  console.log('[DEBUG] Tags received in BookFilters:', tags);
  console.log('[DEBUG] Valid tags:', validTags);
  console.log('[DEBUG] Valid tags count:', validTags.length);

  return (
    <Card className="mb-6">
      <CardHeader>
        <CardTitle>Фильтры</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Search Input */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <Input
              placeholder="Поиск по названию..."
              className="pl-10"
              value={searchQuery}
              onChange={handleSearchChange}
            />
          </div>

          {/* Tag Filter - Всегда отображаем, даже если тегов нет */}
          <Select onValueChange={onTagChange}>
            <SelectTrigger>
              <SelectValue placeholder="Тэги" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Все тэги</SelectItem>
              {validTags && validTags.length > 0 && validTags.map((tag) => (
                <SelectItem 
                  key={tag.id} 
                  value={tag.id.toString()}
                >
                  {tag.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>

          {/* Publisher Filter */}
          <Select onValueChange={onPublisherChange}>
            <SelectTrigger>
              <SelectValue placeholder="Издательство" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Все издательства</SelectItem>
              {publishers.map((publisher) => (
                <SelectItem 
                  key={publisher.id} 
                  value={publisher.id.toString()}
                >
                  {publisher.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>

          {/* Sort Filter */}
          <Select onValueChange={onSortChange}>
            <SelectTrigger>
              <SelectValue placeholder="Сортировка" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="-created">Новинки</SelectItem>
              <SelectItem value="title">Название (А-Я)</SelectItem>
              <SelectItem value="-title">Название (Я-А)</SelectItem>
              <SelectItem value="published_at">Дата публикации (старые)</SelectItem>
              <SelectItem value="-published_at">Дата публикации (новые)</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </CardContent>
    </Card>
  );
}