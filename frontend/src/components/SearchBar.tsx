/**
 * 검색 바 컴포넌트
 * 키워드와 날짜 범위를 입력받아 검색 실행
 */

import React, { useState } from 'react';

interface SearchBarProps {
  onSearch: (keyword: string, fromDate?: string, toDate?: string) => void;
  loading?: boolean;
}

export const SearchBar: React.FC<SearchBarProps> = ({ onSearch, loading }) => {
  const [keyword, setKeyword] = useState('');
  const [fromDate, setFromDate] = useState('');
  const [toDate, setToDate] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (keyword.trim()) {
      onSearch(keyword, fromDate || undefined, toDate || undefined);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={styles.form}>
      <div style={styles.container}>
        <input
          type="text"
          placeholder="검색 키워드 입력 (예: AI, 기술, 경제)"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          style={styles.input}
          required
          disabled={loading}
        />
        
        <div style={styles.dateContainer}>
          <label style={styles.dateLabel}>기간:</label>
          <input
            type="date"
            value={fromDate}
            onChange={(e) => setFromDate(e.target.value)}
            style={styles.dateInput}
            disabled={loading}
            placeholder="시작일"
          />
          <span style={styles.dateSeparator}>~</span>
          <input
            type="date"
            value={toDate}
            onChange={(e) => setToDate(e.target.value)}
            style={styles.dateInput}
            disabled={loading}
            placeholder="종료일"
          />
        </div>
        
        <button
          type="submit"
          style={{
            ...styles.button,
            ...(loading || !keyword.trim() ? styles.buttonDisabled : {}),
          }}
          disabled={loading || !keyword.trim()}
        >
          {loading ? '검색 중...' : '🔍 검색'}
        </button>
      </div>
    </form>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  form: {
    marginBottom: '30px',
    width: '100%',
  },
  container: {
    display: 'flex',
    gap: '12px',
    alignItems: 'center',
    flexWrap: 'wrap',
    width: '100%',
  },
  input: {
    flex: 1,
    minWidth: '300px',
    padding: '14px 18px',
    fontSize: '16px',
    border: '2px solid #e0e0e0',
    borderRadius: '10px',
    outline: 'none',
    transition: 'border-color 0.3s',
  },
  dateContainer: {
    display: 'flex',
    gap: '10px',
    alignItems: 'center',
    flexWrap: 'wrap',
  },
  dateLabel: {
    fontSize: '14px',
    color: '#666',
    fontWeight: 500,
  },
  dateInput: {
    padding: '12px 16px',
    fontSize: '14px',
    border: '2px solid #e0e0e0',
    borderRadius: '8px',
    outline: 'none',
  },
  dateSeparator: {
    color: '#999',
    fontSize: '14px',
  },
  button: {
    padding: '14px 32px',
    fontSize: '16px',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '10px',
    cursor: 'pointer',
    fontWeight: 600,
    transition: 'all 0.3s',
    boxShadow: '0 2px 8px rgba(0, 123, 255, 0.3)',
  },
  buttonDisabled: {
    backgroundColor: '#ccc',
    cursor: 'not-allowed',
    boxShadow: 'none',
  },
};


