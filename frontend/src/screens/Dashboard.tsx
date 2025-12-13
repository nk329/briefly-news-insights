/**
 * 대시보드 메인 화면
 * 검색 바와 뉴스 목록을 포함하는 메인 페이지
 */

import React, { useState } from 'react';
import { UserHeader } from '../components/UserHeader';
import { SearchBar } from '../components/SearchBar';
import { NewsList } from '../components/NewsList';
// import { KeywordChart } from '../components/KeywordChart'; // 주석 처리 (속도 개선)
// import { WordCloud } from '../components/WordCloud'; // 주석 처리 (속도 개선)
import { SearchHistory } from '../components/SearchHistory';
import { searchNews, createSearchHistory } from '../services/api.service';
// import { completeAnalysis } from '../services/api.service'; // 주석 처리 (속도 개선)
import { NewsArticle } from '../types/news.types';
import { useAuth } from '../contexts/AuthContext';

export const Dashboard: React.FC = () => {
  const { isAuthenticated } = useAuth();
  const [articles, setArticles] = useState<NewsArticle[]>([]);
  // const [keywords, setKeywords] = useState<any[]>([]); // 주석 처리 (속도 개선)
  // const [wordcloudUrl, setWordcloudUrl] = useState<string>(''); // 주석 처리 (속도 개선)
  const [searchKeyword, setSearchKeyword] = useState<string>('');
  const [loading, setLoading] = useState(false);
  // const [keywordLoading, setKeywordLoading] = useState(false); // 주석 처리 (속도 개선)
  // const [wordcloudLoading, setWordcloudLoading] = useState(false); // 주석 처리 (속도 개선)
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (keyword: string, fromDate?: string, toDate?: string, useGpt?: boolean) => {
    setLoading(true);
    setError(null);
    // setKeywords([]); // 주석 처리 (속도 개선)
    // setWordcloudUrl(''); // 주석 처리 (속도 개선)
    setSearchKeyword(keyword);

    try {
      // 1. 뉴스 검색 (GPT 옵션 포함)
      const response = await searchNews(keyword, fromDate, toDate, 10, useGpt || false);
      
      if (response.status === 'success') {
        const fetchedArticles = response.data.articles;
        setArticles(fetchedArticles);
        
        // 로그인한 사용자면 검색 히스토리 저장
        if (isAuthenticated) {
          try {
            await createSearchHistory(
              keyword,
              fromDate,
              toDate,
              fetchedArticles.length
            );
          } catch (err) {
            console.error('검색 히스토리 저장 실패:', err);
          }
        }
        
        // ======== 키워드 분석 & 워드클라우드 주석 처리 (속도 개선) ========
        // 2. 통합 분석 (키워드 + 워드클라우드)
        // if (fetchedArticles && fetchedArticles.length > 0) {
        //   setKeywordLoading(true);
        //   setWordcloudLoading(true);
        //   
        //   try {
        //     const analysisResponse = await completeAnalysis(fetchedArticles, 20);
        //     
        //     if (analysisResponse.status === 'success') {
        //       // 키워드 상위 6개만 표시
        //       setKeywords(analysisResponse.data.keywords?.slice(0, 6) || []);
        //       
        //       // 워드클라우드 URL 설정
        //       setWordcloudUrl(analysisResponse.data.wordcloudUrl || '');
        //     }
        //   } catch (analysisErr) {
        //     console.error('분석 에러:', analysisErr);
        //     // 분석 실패해도 뉴스는 표시
        //   } finally {
        //     setKeywordLoading(false);
        //     setWordcloudLoading(false);
        //   }
        // }
        // ================================================================
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
      // setKeywords([]); // 주석 처리 (속도 개선)
      // setWordcloudUrl(''); // 주석 처리 (속도 개선)
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <div style={styles.headerContent}>
          <div style={styles.titleSection}>
            <h1 style={styles.title}>Briefly News Insights</h1>
            <p style={styles.subtitle}>뉴스 검색 및 분석 대시보드</p>
          </div>
          <UserHeader />
        </div>
      </header>

      <main style={styles.main}>
        {/* 로그인한 사용자에게만 검색 히스토리 표시 */}
        {isAuthenticated && (
          <SearchHistory 
            onSelectHistory={(keyword, fromDate, toDate) => {
              handleSearch(keyword, fromDate, toDate);
            }}
          />
        )}
        
        <SearchBar onSearch={handleSearch} loading={loading} />
        
        {error && (
          <div style={styles.error}>
            <span style={styles.errorIcon}>⚠️</span>
            <span>{error}</span>
          </div>
        )}
        
        {/* 뉴스 목록만 표시 (간단한 레이아웃) */}
        <NewsList articles={articles} loading={loading} />
        
        {/* ======== 아래는 주석 처리된 키워드 차트 & 워드클라우드 코드 ======== 
        {articles.length > 0 ? (
          <div style={styles.contentLayout}>
            <div style={styles.keywordSection}>
              <KeywordChart 
                keywords={keywords} 
                loading={keywordLoading} 
                searchKeyword={searchKeyword}
              />
            </div>
            
            <div style={styles.newsSection}>
              <WordCloud 
                imageUrl={wordcloudUrl}
                loading={wordcloudLoading}
                searchKeyword={searchKeyword}
              />
              
              <NewsList articles={articles} loading={loading} />
            </div>
          </div>
        ) : (
          <NewsList articles={articles} loading={loading} />
        )}
        ================================================================ */}
      </main>

      <footer style={styles.footer}>
        <p style={styles.footerText}>
          Powered by NewsAPI | Phase 4: 워드클라우드 완료 ✅
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
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  titleSection: {
    display: 'flex',
    flexDirection: 'column',
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


