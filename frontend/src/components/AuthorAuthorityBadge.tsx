import { Award, BookOpen, Building2, Quote, Sparkles } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';

interface Credentials {
  publications?: string[];
  citations?: number;
  awards?: string[];
  positions?: string[];
  companies?: string[];
  expertise?: string[];
}

interface Author {
  authority_score?: number;
  credentials?: Credentials;
}

interface AuthorAuthorityBadgeProps {
  author: Author;
  showTooltip?: boolean;
}

export function AuthorAuthorityBadge({
  author,
  showTooltip = true,
}: AuthorAuthorityBadgeProps) {
  const score = author.authority_score ?? 0;
  const creds = author.credentials || {};

  // Color based on score
  const getScoreColor = (s: number): string => {
    if (s >= 80) return 'bg-emerald-500 hover:bg-emerald-600';
    if (s >= 60) return 'bg-blue-500 hover:bg-blue-600';
    if (s >= 40) return 'bg-amber-500 hover:bg-amber-600';
    if (s > 0) return 'bg-gray-500 hover:bg-gray-600';
    return 'bg-gray-300 hover:bg-gray-400';
  };

  // Label based on score
  const getScoreLabel = (s: number): string => {
    if (s >= 80) return 'Эксперт';
    if (s >= 60) return 'Специалист';
    if (s >= 40) return 'Практик';
    if (s > 0) return 'Начинающий';
    return 'Без оценки';
  };

  const hasCredentials =
    (creds.publications?.length ?? 0) > 0 ||
    (creds.citations ?? 0) > 0 ||
    (creds.awards?.length ?? 0) > 0 ||
    (creds.positions?.length ?? 0) > 0;

  const badge = (
    <Badge
      className={`${getScoreColor(score)} text-white text-xs font-medium cursor-help transition-colors`}
    >
      <Sparkles className="mr-1 h-3 w-3" />
      {getScoreLabel(score)} ({score})
    </Badge>
  );

  if (!showTooltip || !hasCredentials) {
    return badge;
  }

  return (
    <TooltipProvider delayDuration={200}>
      <Tooltip>
        <TooltipTrigger asChild>{badge}</TooltipTrigger>
        <TooltipContent
          side="bottom"
          className="max-w-xs p-4 bg-white dark:bg-gray-900 border shadow-lg"
        >
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <h4 className="font-semibold text-sm">Регалии автора</h4>
              <span
                className={`text-xs px-2 py-0.5 rounded-full text-white ${getScoreColor(score)}`}
              >
                {score}/100
              </span>
            </div>

            <div className="space-y-2 text-sm">
              {creds.publications && creds.publications.length > 0 && (
                <div className="flex items-start gap-2">
                  <BookOpen className="h-4 w-4 mt-0.5 text-muted-foreground shrink-0" />
                  <div>
                    <span className="text-muted-foreground">Публикаций:</span>{' '}
                    <span className="font-medium">{creds.publications.length}</span>
                  </div>
                </div>
              )}

              {creds.citations && creds.citations > 0 && (
                <div className="flex items-start gap-2">
                  <Quote className="h-4 w-4 mt-0.5 text-muted-foreground shrink-0" />
                  <div>
                    <span className="text-muted-foreground">Цитирований:</span>{' '}
                    <span className="font-medium">{creds.citations.toLocaleString()}</span>
                  </div>
                </div>
              )}

              {creds.awards && creds.awards.length > 0 && (
                <div className="flex items-start gap-2">
                  <Award className="h-4 w-4 mt-0.5 text-muted-foreground shrink-0" />
                  <div>
                    <span className="text-muted-foreground">Награды:</span>
                    <ul className="mt-0.5 space-y-0.5">
                      {creds.awards.slice(0, 3).map((award, idx) => (
                        <li key={idx} className="text-xs text-muted-foreground">
                          • {award}
                        </li>
                      ))}
                      {creds.awards.length > 3 && (
                        <li className="text-xs text-muted-foreground">
                          и еще {creds.awards.length - 3}...
                        </li>
                      )}
                    </ul>
                  </div>
                </div>
              )}

              {creds.positions && creds.positions.length > 0 && (
                <div className="flex items-start gap-2">
                  <Building2 className="h-4 w-4 mt-0.5 text-muted-foreground shrink-0" />
                  <div>
                    <span className="text-muted-foreground">Должности:</span>
                    <p className="text-xs text-muted-foreground mt-0.5">
                      {creds.positions.slice(0, 2).join(', ')}
                      {creds.positions.length > 2 && '...'}
                    </p>
                  </div>
                </div>
              )}

              {creds.github_stats && (creds.github_stats.stars || creds.github_stats.followers) && (
                <div className="flex items-start gap-2">
                  <div className="h-4 w-4 mt-0.5 text-muted-foreground shrink-0">⭐</div>
                  <div>
                    <span className="text-muted-foreground">GitHub:</span>
                    <div className="text-xs text-muted-foreground mt-0.5 space-y-0.5">
                      {creds.github_stats.stars && (
                        <div>⭐ {creds.github_stats.stars.toLocaleString()} звезд</div>
                      )}
                      {creds.github_stats.followers && (
                        <div>👥 {creds.github_stats.followers.toLocaleString()} подписчиков</div>
                      )}
                      {creds.github_stats.contributions && (
                        <div>📊 {creds.github_stats.contributions.toLocaleString()} контрибуций</div>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {creds.pypi_stats && creds.pypi_stats.total_downloads && (
                <div className="flex items-start gap-2">
                  <div className="h-4 w-4 mt-0.5 text-muted-foreground shrink-0">📦</div>
                  <div>
                    <span className="text-muted-foreground">PyPI:</span>{' '}
                    <span className="font-medium">{creds.pypi_stats.total_downloads.toLocaleString()} скачиваний</span>
                  </div>
                </div>
              )}

              {creds.stackoverflow && creds.stackoverflow.reputation && (
                <div className="flex items-start gap-2">
                  <div className="h-4 w-4 mt-0.5 text-muted-foreground shrink-0">💬</div>
                  <div>
                    <span className="text-muted-foreground">Stack Overflow:</span>{' '}
                    <span className="font-medium">{creds.stackoverflow.reputation.toLocaleString()} репутации</span>
                  </div>
                </div>
              )}

              {creds.conferences && creds.conferences.length > 0 && (
                <div className="flex items-start gap-2">
                  <div className="h-4 w-4 mt-0.5 text-muted-foreground shrink-0">🎤</div>
                  <div>
                    <span className="text-muted-foreground">Конференции:</span>
                    <p className="text-xs text-muted-foreground mt-0.5">
                      {creds.conferences.slice(0, 2).join(', ')}
                      {creds.conferences.length > 2 && '...'}
                    </p>
                  </div>
                </div>
              )}

              {creds.certifications && creds.certifications.length > 0 && (
                <div className="flex items-start gap-2">
                  <div className="h-4 w-4 mt-0.5 text-muted-foreground shrink-0">🏆</div>
                  <div>
                    <span className="text-muted-foreground">Сертификаты:</span>
                    <p className="text-xs text-muted-foreground mt-0.5">
                      {creds.certifications.slice(0, 2).join(', ')}
                      {creds.certifications.length > 2 && '...'}
                    </p>
                  </div>
                </div>
              )}
            </div>

            <p className="text-xs text-muted-foreground border-t pt-2">
              Оценка сформирована автоматически с помощью ИИ
            </p>
          </div>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}
