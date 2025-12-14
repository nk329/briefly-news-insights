/**
 * 뉴스 목록 컴포넌트
 * 검색된 뉴스 기사들을 카드 형태로 표시
 */

import React from 'react';
import { NewsArticle } from '../types/news.types';

interface NewsListProps {
  articles: NewsArticle[];
  loading?: boolean;
  onLoadMore?: () => void;
  hasMore?: boolean;
  loadingMore?: boolean;
}

export const NewsList: React.FC<NewsListProps> = ({ 
  articles, 
  loading, 
  onLoadMore, 
  hasMore = false, 
  loadingMore = false 
}) => {
  const [showOriginal, setShowOriginal] = React.useState<{ [key: number]: boolean }>({});

  const toggleOriginal = (index: number) => {
    setShowOriginal(prev => ({ ...prev, [index]: !prev[index] }));
  };

  if (loading) {
    return (
      <div style={styles.message}>
        <div style={styles.spinner}></div>
        <p>뉴스를 불러오는 중...</p>
      </div>
    );
  }

  if (articles.length === 0) {
    return (
      <div style={styles.message}>
        <p style={styles.emptyIcon}>📰</p>
        <p>검색 결과가 없습니다.</p>
        <p style={styles.emptyHint}>다른 키워드로 검색해보세요.</p>
      </div>
    );
  }

  return (
    <>
      <style>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
      <div style={styles.container}>
        <div style={styles.header}>
          <h2 style={styles.title}>검색 결과</h2>
          <span style={styles.count}>{articles.length}건</span>
        </div>
      
      <div style={styles.list}>
        {articles.map((article, index) => (
          <div key={index} style={styles.card}>
            {article.urlToImage && (
              <div style={styles.imageContainer}>
                <img
                  src={article.urlToImage}
                  alt={article.title}
                  style={styles.image}
                  onError={(e) => {
                    (e.target as HTMLImageElement).style.display = 'none';
                  }}
                />
              </div>
            )}
            
            <div style={styles.content}>
              {/* 번역된 제목 (있으면 표시, 없으면 원본) */}
              <h3 style={styles.cardTitle}>
                <a
                  href={article.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={styles.link}
                >
                  {showOriginal[index] && article.original_title
                    ? article.original_title
                    : (article.translated_title || article.title)}
                </a>
              </h3>
              
              {/* 번역 배지 (번역된 경우만 표시) */}
              {article.translated_title && (
                <div style={styles.translationBadge}>
                  🌐 번역됨 ({article.translation_language === 'ko' ? '한국어' : 
                    article.translation_language === 'en' ? '영어' : 
                    article.translation_language === 'ja' ? '일본어' : '번역'})
                  <button
                    onClick={() => toggleOriginal(index)}
                    style={styles.toggleButton}
                  >
                    {showOriginal[index] ? '번역 보기' : '원문 보기'}
                  </button>
                </div>
              )}
              
              <div style={styles.meta}>
                <span style={styles.source}>🏢 {article.source.name}</span>
                <span style={styles.date}>
                  📅 {new Date(article.publishedAt).toLocaleDateString('ko-KR', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                  })}
                </span>
              </div>
              
              {/* GPT 요약 (있으면 표시) */}
              {article.summary && article.summary_type === 'gpt' && (
                <div style={styles.gptSummarySection}>
                  <div style={styles.gptSummaryBadge}>🤖 GPT-4 요약</div>
                  <p style={styles.gptSummary}>{article.summary}</p>
                </div>
              )}
              
              {/* TF-IDF 요약 (GPT 아닌 경우) */}
              {article.summary && article.summary_type !== 'gpt' && (
                <div style={styles.summarySection}>
                  <div style={styles.summaryBadge}>✨ AI 요약 (TF-IDF)</div>
                  <p style={styles.summary}>{article.summary}</p>
                </div>
              )}
              
              {/* 설명 (번역 여부에 따라) */}
              <p style={styles.description}>
                {showOriginal[index] && article.original_description
                  ? article.original_description
                  : (article.translated_description || article.description || article.content?.slice(0, 200) + '...' || '내용 없음')}
              </p>
              
              <a
                href={article.url}
                target="_blank"
                rel="noopener noreferrer"
                style={styles.readMore}
              >
                자세히 보기 →
              </a>
            </div>
          </div>
        ))}
      </div>
      
      {/* 더 보기 버튼 */}
      {hasMore && onLoadMore && (
        <div style={styles.loadMoreContainer}>
          {loadingMore ? (
            <div style={styles.loadingWrapper}>
              <div style={styles.loadingSpinner}></div>
              <span style={styles.loadingText}>뉴스를 불러오는 중...</span>
              <span style={styles.loadingSubtext}>잠시만 기다려주세요</span>
            </div>
          ) : (
            <button
              onClick={onLoadMore}
              style={styles.loadMoreButton}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = '#0056b3';
                e.currentTarget.style.transform = 'translateY(-2px)';
                e.currentTarget.style.boxShadow = '0 6px 16px rgba(0, 123, 255, 0.4)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = '#007bff';
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = '0 4px 12px rgba(0, 123, 255, 0.3)';
              }}
            >
              📰 더 보기 (5개)
            </button>
          )}
        </div>
      )}
    </div>
    </>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    marginTop: '30px',
  },
  header: {
    display: 'flex',
    alignItems: 'center',
    gap: '15px',
    marginBottom: '25px',
  },
  title: {
    fontSize: '28px',
    fontWeight: 700,
    color: '#333',
    margin: 0,
  },
  count: {
    fontSize: '18px',
    color: '#007bff',
    backgroundColor: '#e7f3ff',
    padding: '6px 16px',
    borderRadius: '20px',
    fontWeight: 600,
  },
  list: {
    display: 'flex',
    flexDirection: 'column',
    gap: '20px',
  },
  card: {
    display: 'flex',
    gap: '20px',
    padding: '20px',
    border: '1px solid #e8e8e8',
    borderRadius: '12px',
    backgroundColor: '#fff',
    boxShadow: '0 2px 8px rgba(0,0,0,0.06)',
    transition: 'all 0.3s',
    cursor: 'pointer',
  },
  imageContainer: {
    flexShrink: 0,
    width: '200px',
    height: '150px',
    overflow: 'hidden',
    borderRadius: '8px',
  },
  image: {
    width: '100%',
    height: '100%',
    objectFit: 'cover',
  },
  content: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
  },
  cardTitle: {
    fontSize: '20px',
    fontWeight: 600,
    margin: 0,
    lineHeight: '1.4',
  },
  link: {
    color: '#222',
    textDecoration: 'none',
    transition: 'color 0.3s',
  },
  meta: {
    display: 'flex',
    gap: '20px',
    fontSize: '14px',
    color: '#666',
  },
  source: {
    fontWeight: 600,
  },
  date: {},
  translationBadge: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    backgroundColor: '#f0fdf4',
    padding: '8px 12px',
    borderRadius: '8px',
    marginBottom: '10px',
    border: '1px solid #86efac',
    fontSize: '13px',
    color: '#15803d',
    fontWeight: 600,
  },
  toggleButton: {
    marginLeft: 'auto',
    padding: '4px 12px',
    fontSize: '12px',
    backgroundColor: '#10b981',
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    fontWeight: 600,
    transition: 'all 0.3s',
  },
  summarySection: {
    backgroundColor: '#f0f8ff',
    padding: '15px',
    borderRadius: '8px',
    marginBottom: '15px',
    border: '1px solid #d0e8ff',
  },
  summaryBadge: {
    display: 'inline-block',
    backgroundColor: '#007bff',
    color: 'white',
    padding: '4px 12px',
    borderRadius: '12px',
    fontSize: '12px',
    fontWeight: 600,
    marginBottom: '10px',
  },
  summary: {
    color: '#2c3e50',
    lineHeight: '1.8',
    margin: 0,
    fontSize: '15px',
    fontWeight: 500,
  },
  gptSummarySection: {
    backgroundColor: '#fff5f5',
    padding: '15px',
    borderRadius: '8px',
    marginBottom: '15px',
    border: '2px solid #ff6b6b',
    boxShadow: '0 2px 4px rgba(255, 107, 107, 0.1)',
  },
  gptSummaryBadge: {
    display: 'inline-block',
    background: 'linear-gradient(135deg, #ff6b6b 0%, #ff8787 100%)',
    color: 'white',
    padding: '5px 14px',
    borderRadius: '14px',
    fontSize: '12px',
    fontWeight: 700,
    marginBottom: '12px',
    boxShadow: '0 2px 4px rgba(255, 107, 107, 0.3)',
  },
  gptSummary: {
    color: '#2c3e50',
    lineHeight: '1.9',
    margin: 0,
    fontSize: '15px',
    fontWeight: 500,
  },
  description: {
    color: '#777',
    lineHeight: '1.7',
    margin: 0,
    fontSize: '14px',
  },
  readMore: {
    color: '#007bff',
    textDecoration: 'none',
    fontWeight: 600,
    fontSize: '14px',
    marginTop: 'auto',
  },
  message: {
    textAlign: 'center',
    padding: '60px 20px',
    color: '#666',
  },
  spinner: {
    width: '40px',
    height: '40px',
    margin: '0 auto 20px',
    border: '4px solid #f3f3f3',
    borderTop: '4px solid #007bff',
    borderRadius: '50%',
    animation: 'spin 1s linear infinite',
  },
  emptyIcon: {
    fontSize: '64px',
    margin: '0 0 20px 0',
  },
  emptyHint: {
    fontSize: '14px',
    color: '#999',
  },
  loadMoreContainer: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: '40px',
    marginBottom: '20px',
  },
  loadMoreButton: {
    padding: '14px 40px',
    fontSize: '16px',
    fontWeight: 600,
    color: 'white',
    backgroundColor: '#007bff',
    border: 'none',
    borderRadius: '10px',
    cursor: 'pointer',
    transition: 'all 0.3s',
    boxShadow: '0 4px 12px rgba(0, 123, 255, 0.3)',
  },
  loadingWrapper: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '15px',
    padding: '20px',
  },
  loadingSpinner: {
    width: '40px',
    height: '40px',
    border: '4px solid #f3f3f3',
    borderTop: '4px solid #007bff',
    borderRadius: '50%',
    animation: 'spin 1s linear infinite',
  },
  loadingText: {
    fontSize: '16px',
    color: '#666',
    fontWeight: 500,
  },
  loadingSubtext: {
    fontSize: '14px',
    color: '#999',
    fontStyle: 'italic',
  },
};


