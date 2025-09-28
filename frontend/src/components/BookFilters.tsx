import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import type { Author, Publisher, Tag } from '@/types';

interface BookFiltersProps {
  authors: Author[];
  publishers: Publisher[];
  tags: Tag[];
  onAuthorChange: (authorId: string) => void;
  onCategoryChange: (category: string) => void;
  onPublisherChange: (publisherId: string) => void;
  onSortChange: (sort: string) => void;
}

export default function BookFilters({
  authors,
  publishers,
  tags,
  onAuthorChange,
  onCategoryChange,
  onPublisherChange,
  onSortChange,
}: BookFiltersProps) {

  return (
    <Card className="mb-8">
      <CardHeader>
        <CardTitle>Фильтр книг</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="space-y-2">
            <label className="text-sm font-medium">Тег</label>
            <Select onValueChange={onCategoryChange}>
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Все теги" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Все теги</SelectItem>
                {tags.map((tag) => (
                  <SelectItem key={tag.id} value={tag.id.toString()}>
                    {tag.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">Автор</label>
            <Select onValueChange={onAuthorChange}>
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Все авторы" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Все авторы</SelectItem>
                {authors.map((author) => (
                  <SelectItem key={author.id} value={author.id.toString()}>
                    {author.first_name} {author.last_name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">Издатель</label>
            <Select onValueChange={onPublisherChange}>
              <SelectTrigger className="w-full">
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
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Новейшие" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="-created">Новейшие</SelectItem>
                <SelectItem value="created">Старейшие</SelectItem>
                <SelectItem value="title">Название от А до Я</SelectItem>
                <SelectItem value="-title">Название от Я до А</SelectItem>
                <SelectItem value="published_at">По дате публикации (возр.)</SelectItem>
                <SelectItem value="-published_at">По дате публикации (убыв.)</SelectItem>
                <SelectItem value="author__last_name">Авторы (А-Я)</SelectItem>
                <SelectItem value="-author__last_name">Авторы (Я-А)</SelectItem>
                <SelectItem value="publisher__name">Издательство (А-Я)</SelectItem>
                <SelectItem value="-publisher__name">Издательство (Я-А)</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}