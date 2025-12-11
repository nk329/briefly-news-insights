/**
 * 워드클라우드 컴포넌트
 * 키워드 시각화 이미지 표시
 */

import React from 'react';

interface WordCloudProps {
  imageUrl: string;
  loading?: boolean;
  searchKeyword?: string;
}

export const WordCloud: React.FC<WordCloudProps> = ({
  imageUrl,
  loading,
  searchKeyword,
}) => {
  if (loading) {
    return (
      <div style={styles.container}>
        <div style={styles.loadingContainer}>
          <div style={styles.spinner}></div>
          <p style={styles.loadingText}>워드클라우드 생성 중...</p>
        </div>
      </div>
    );
  }

  if (!imageUrl) {
    return null;
  }

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
  const fullImageUrl = `${API_BASE_URL}${imageUrl}`;

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h3 style={styles.title}>
          {searchKeyword ? `"${searchKeyword}" 워드클라우드` : '워드클라우드'}
        </h3>
      </div>
      <div style={styles.imageContainer}>
        <img
          src={fullImageUrl}
          alt="워드클라우드"
          style={styles.image}
          onError={(e) => {
            console.error('워드클라우드 이미지 로드 실패');
            e.currentTarget.style.display = 'none';
          }}
        />
      </div>
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    backgroundColor: '#fff',
    borderRadius: '12px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
    padding: '20px',
    marginBottom: '20px',
  },
  header: {
    marginBottom: '15px',
  },
  title: {
    fontSize: '18px',
    fontWeight: 700,
    color: '#333',
    margin: 0,
  },
  imageContainer: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: '8px',
    overflow: 'hidden',
    backgroundColor: '#f8f9fa',
    maxHeight: '400px',
  },
  image: {
    maxWidth: '100%',
    maxHeight: '400px',
    width: 'auto',
    height: 'auto',
    display: 'block',
    objectFit: 'contain',
  },
  loadingContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '60px 20px',
  },
  spinner: {
    width: '40px',
    height: '40px',
    border: '4px solid #f3f3f3',
    borderTop: '4px solid #007bff',
    borderRadius: '50%',
    animation: 'spin 1s linear infinite',
  },
  loadingText: {
    marginTop: '20px',
    color: '#666',
    fontSize: '16px',
  },
};

// CSS animation for spinner
const styleSheet = document.createElement('style');
styleSheet.textContent = `
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;
document.head.appendChild(styleSheet);

