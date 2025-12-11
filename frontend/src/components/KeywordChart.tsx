/**
 * 키워드 랭킹 컴포넌트
 * 검색어 기반 인기 키워드 TOP 6
 */

import React from 'react';

interface Keyword {
  word: string;
  count: number;
}

interface KeywordChartProps {
  keywords: Keyword[];
  loading?: boolean;
  searchKeyword?: string;
}

export const KeywordChart: React.FC<KeywordChartProps> = ({ 
  keywords, 
  loading, 
  searchKeyword 
}) => {
  if (loading) {
    return (
      <div style={styles.container}>
        <div style={styles.message}>키워드를 분석하는 중...</div>
      </div>
    );
  }

  if (!keywords || keywords.length === 0) {
    return null;
  }

  // 상위 6개만 추출
  const topKeywords = keywords.slice(0, 6);
  
  // 현재 날짜
  const today = new Date();
  const dateStr = `${today.getMonth() + 1}/${today.getDate()}`;

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h2 style={styles.title}>
          {searchKeyword ? `"${searchKeyword}" 관련 인기 키워드` : '인기 키워드'}
        </h2>
        <span style={styles.date}>{dateStr} 기준</span>
      </div>

      <div style={styles.list}>
        {topKeywords.map((keyword, index) => (
          <div key={index} style={styles.item}>
            <span style={styles.rank}>{index + 1}</span>
            <span style={styles.keyword}>{keyword.word}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    padding: '25px 20px',
    backgroundColor: '#fff',
    borderRadius: '12px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
    position: 'sticky',
    top: '20px', // 스크롤 시 상단에 고정
  },
  header: {
    marginBottom: '20px',
  },
  title: {
    fontSize: '18px',
    fontWeight: 700,
    color: '#333',
    margin: '0 0 8px 0',
  },
  date: {
    fontSize: '14px',
    color: '#999',
  },
  list: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0',
  },
  item: {
    display: 'flex',
    alignItems: 'center',
    gap: '16px',
    padding: '16px 0',
    borderBottom: '1px solid #f0f0f0',
    transition: 'background-color 0.2s',
    cursor: 'pointer',
  },
  rank: {
    fontSize: '20px',
    fontWeight: 700,
    color: '#6c5ce7',
    minWidth: '20px',
  },
  keyword: {
    fontSize: '17px',
    color: '#2d3436',
    fontWeight: 500,
  },
  message: {
    textAlign: 'center',
    padding: '40px 20px',
    color: '#666',
    fontSize: '16px',
  },
};

