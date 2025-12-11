/**
 * 대시보드 메인 화면
 * 검색 바와 뉴스 목록을 포함하는 메인 페이지
 */

import React, { useState } from 'react';
import { SearchBar } from '../components/SearchBar';
import { NewsList } from '../components/NewsList';
import { KeywordChart } from '../components/KeywordChart';
import { searchNews, analyzeArticlesKeywords } from '../services/api.service';
import { NewsArticle } from '../types/news.types';

export const Dashboard: React.FC = () => {
  const [articles, setArticles] = useState<NewsArticle[]>([]);
  const [keywords, setKeywords] = useState<any[]>([]);
  const [searchKeyword, setSearchKeyword] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [keywordLoading, setKeywordLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (keyword: string, fromDate?: string, toDate?: string) => {
    setLoading(true);
    setError(null);
    setKeywords([]);
    setSearchKeyword(keyword);

    try {
      // 1. 뉴스 검색
      const response = await searchNews(keyword, fromDate, toDate);
      
      if (response.status === 'success') {
        const fetchedArticles = response.data.articles;
        setArticles(fetchedArticles);
        
        // 2. 키워드 분석 (백그라운드)
        if (fetchedArticles && fetchedArticles.length > 0) {
          setKeywordLoading(true);
          try {
            const keywordResponse = await analyzeArticlesKeywords(fetchedArticles, 6);
            if (keywordResponse.status === 'success') {
              setKeywords(keywordResponse.data.keywords || []);
            }
          } catch (keywordErr) {
            console.error('키워드 분석 에러:', keywordErr);
            // 키워드 분석 실패해도 뉴스는 표시
          } finally {
            setKeywordLoading(false);
          }
        }
      } else {
        setError(response.message || '뉴스 검색에 실패했습니다.');
      }
    } catch (err: any) {
      console.error('검색 에러:', err);
      setError(
        err.response?.data?.detail ||
        err.message ||
        '뉴스 검색에 실패했습니다. 잠시 후 다시 시도해주세요.'
      );
      setArticles([]);
      setKeywords([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <div style={styles.headerContent}>
          <h1 style={styles.title}>📰 Briefly News Insights</h1>
          <p style={styles.subtitle}>뉴스 검색 및 분석 대시보드</p>
        </div>
      </header>

      <main style={styles.main}>
        <SearchBar onSearch={handleSearch} loading={loading} />
        
        {error && (
          <div style={styles.error}>
            <span style={styles.errorIcon}>⚠️</span>
            <span>{error}</span>
          </div>
        )}
        
        {/* 좌우 레이아웃: 키워드 차트(1) + 뉴스 목록(3) */}
        {articles.length > 0 ? (
          <div style={styles.contentLayout}>
            {/* 왼쪽: 키워드 차트 (flex: 1) */}
            <div style={styles.keywordSection}>
              <KeywordChart 
                keywords={keywords} 
                loading={keywordLoading} 
                searchKeyword={searchKeyword}
              />
            </div>
            
            {/* 오른쪽: 뉴스 목록 (flex: 3) */}
            <div style={styles.newsSection}>
              <NewsList articles={articles} loading={loading} />
            </div>
          </div>
        ) : (
          /* 검색 결과가 없을 때는 중앙에 표시 */
          <NewsList articles={articles} loading={loading} />
        )}
      </main>

      <footer style={styles.footer}>
        <p style={styles.footerText}>
          Powered by NewsAPI | Phase 3: 키워드 분석 완료 ✅
        </p>
      </footer>
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    minHeight: '100vh',
    backgroundColor: '#f8f9fa',
    display: 'flex',
    flexDirection: 'column',
  },
  header: {
    backgroundColor: '#fff',
    padding: '30px 20px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
    borderBottom: '3px solid #007bff',
  },
  headerContent: {
    maxWidth: '1200px',
    margin: '0 auto',
  },
  title: {
    fontSize: '36px',
    fontWeight: 700,
    margin: '0 0 10px 0',
    color: '#222',
    background: 'linear-gradient(135deg, #007bff 0%, #0056b3 100%)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
  },
  subtitle: {
    fontSize: '16px',
    color: '#666',
    margin: 0,
  },
  main: {
    flex: 1,
    maxWidth: '1200px',
    width: '100%',
    margin: '0 auto',
    padding: '40px 20px',
  },
  error: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    padding: '16px 20px',
    backgroundColor: '#fff3cd',
    color: '#856404',
    border: '1px solid #ffeaa7',
    borderRadius: '8px',
    marginBottom: '20px',
    fontSize: '15px',
  },
  errorIcon: {
    fontSize: '20px',
  },
  // 좌우 레이아웃 스타일
  contentLayout: {
    display: 'flex',
    gap: '20px',
    alignItems: 'flex-start',
    marginTop: '20px',
  },
  keywordSection: {
    flex: 1,
    minWidth: '250px',
  },
  newsSection: {
    flex: 3,
    minWidth: 0, // flex 아이템이 overflow 될 수 있도록
  },
  footer: {
    backgroundColor: '#fff',
    padding: '20px',
    textAlign: 'center',
    borderTop: '1px solid #e0e0e0',
    marginTop: 'auto',
  },
  footerText: {
    margin: 0,
    color: '#999',
    fontSize: '14px',
  },
};


