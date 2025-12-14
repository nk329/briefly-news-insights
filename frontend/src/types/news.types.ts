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
  summary_type?: string;  // GPT, TF-IDF, none
  urlToImage?: string;
  author?: string;
  
  // Phase 7.2: 번역 관련 필드
  translated_title?: string;
  translated_description?: string;
  original_title?: string;
  original_description?: string;
  translation_language?: string;  // ko, en, ja 등
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


