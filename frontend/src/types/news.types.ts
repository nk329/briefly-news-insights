/**
 * 뉴스 관련 TypeScript 타입 정의
 */

export interface NewsArticle {
  title: string;
  source: {
    name: string;
  };
  url: string;
  publishedAt: string;
  content: string;
  description: string;
  summary?: string;  // Phase 2: 요약 추가
  urlToImage?: string;
  author?: string;
}

export interface NewsSearchResponse {
  status: string;
  data: {
    total: number;
    articles: NewsArticle[];
  };
  message?: string;
}

export interface SearchParams {
  keyword: string;
  fromDate?: string;
  toDate?: string;
  pageSize?: number;
}


