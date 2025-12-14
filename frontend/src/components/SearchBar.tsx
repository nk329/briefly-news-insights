/**
 * 검색 바 컴포넌트
 * 키워드와 날짜 범위를 입력받아 검색 실행
 */

import React, { useState } from 'react';

interface SearchBarProps {
  onSearch: (
    keyword: string, 
    country: string,
    translateTo: string,
    fromDate?: string, 
    toDate?: string, 
    useGpt?: boolean
  ) => void;
  loading?: boolean;
}

export const SearchBar: React.FC<SearchBarProps> = ({ onSearch, loading }) => {
  const [keyword, setKeyword] = useState('');
  const [country, setCountry] = useState('kr');
  const [translateTo, setTranslateTo] = useState('ko');
  const [fromDate, setFromDate] = useState('');
  const [toDate, setToDate] = useState('');
  const [useGpt, setUseGpt] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(
      keyword || '',  // 키워드 없으면 빈 문자열
      country,
      translateTo,
      fromDate || undefined, 
      toDate || undefined, 
      useGpt
    );
  };

  const countries = [
    { value: 'kr', label: '🇰🇷 한국', name: '한국' },
    { value: 'us', label: '🇺🇸 미국', name: '미국' },
    { value: 'jp', label: '🇯🇵 일본', name: '일본' },
    { value: 'cn', label: '🇨🇳 중국', name: '중국' },
    { value: 'gb', label: '🇬🇧 영국', name: '영국' },
    { value: 'fr', label: '🇫🇷 프랑스', name: '프랑스' },
    { value: 'de', label: '🇩🇪 독일', name: '독일' },
    { value: 'au', label: '🇦🇺 호주', name: '호주' },
    { value: 'ca', label: '🇨🇦 캐나다', name: '캐나다' },
    { value: 'all', label: '🌍 전체', name: '전체' },
  ];

  const languages = [
    { value: 'ko', label: '🇰🇷 한국어', name: '한국어' },
    { value: 'en', label: '🇺🇸 영어', name: '영어' },
    { value: 'ja', label: '🇯🇵 일본어', name: '일본어' },
    { value: 'none', label: '❌ 번역 안 함', name: '번역 안 함' },
  ];

  return (
    <form onSubmit={handleSubmit} style={styles.form}>
      <div style={styles.container}>
        {/* 1. 국가 선택 체크박스 그룹 */}
        <div style={styles.checkboxGroup}>
          <label style={styles.groupLabel}>🌍 국가 선택</label>
          <div style={styles.checkboxContainer}>
            {countries.map((c) => (
              <label 
                key={c.value} 
                style={{
                  ...styles.checkboxLabel,
                  ...(country === c.value ? styles.checkboxLabelSelected : {}),
                }}
              >
                <input
                  type="radio"
                  name="country"
                  value={c.value}
                  checked={country === c.value}
                  onChange={(e) => setCountry(e.target.value)}
                  disabled={loading}
                  style={styles.radioInput}
                />
                <span style={styles.checkboxText}>{c.label}</span>
              </label>
            ))}
          </div>
        </div>

        {/* 2. 번역 언어 선택 + 날짜 범위 + GPT */}
        <div style={styles.translateRow}>
          {/* 번역 언어 선택 체크박스 그룹 */}
          <div style={styles.checkboxGroupInline}>
            <label style={styles.groupLabel}>🌐 번역 언어 선택</label>
            <div style={styles.checkboxContainer}>
              {languages.map((lang) => (
                <label 
                  key={lang.value} 
                  style={{
                    ...styles.checkboxLabel,
                    ...(translateTo === lang.value ? styles.checkboxLabelSelected : {}),
                  }}
                >
                  <input
                    type="radio"
                    name="translateTo"
                    value={lang.value}
                    checked={translateTo === lang.value}
                    onChange={(e) => setTranslateTo(e.target.value)}
                    disabled={loading}
                    style={styles.radioInput}
                  />
                  <span style={styles.checkboxText}>{lang.label}</span>
                </label>
              ))}
            </div>
          </div>

          {/* 날짜 범위 + GPT */}
          <div style={styles.optionsContainer}>
            <div style={styles.dateContainer}>
              <input
                type="date"
                value={fromDate}
                onChange={(e) => setFromDate(e.target.value)}
                style={styles.dateInput}
                disabled={loading || country !== 'all'}
                placeholder="연도-월-일"
              />
              <span style={styles.dateSeparator}>~</span>
              <input
                type="date"
                value={toDate}
                onChange={(e) => setToDate(e.target.value)}
                style={styles.dateInput}
                disabled={loading || country !== 'all'}
                placeholder="연도-월-일"
              />
            </div>
            
            <div style={styles.gptContainer}>
              <label style={styles.gptLabel}>
                <input
                  type="checkbox"
                  checked={useGpt}
                  onChange={(e) => setUseGpt(e.target.checked)}
                  disabled={loading}
                  style={styles.checkbox}
                />
                <span style={styles.gptText}>GPT-4 요약</span>
                <span style={styles.gptBadge}>고급</span>
              </label>
            </div>
          </div>
        </div>

        {/* 3. 키워드 입력 + 검색 버튼 */}
        <div style={styles.searchRow}>
          <input
            type="text"
            placeholder="키워드 입력 (선택, 없으면 해당 국가 헤드라인)"
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            style={styles.input}
            disabled={loading}
          />
          <button
            type="submit"
            style={{
              ...styles.button,
              ...(loading ? styles.buttonDisabled : {}),
            }}
            disabled={loading}
          >
            {loading ? '검색 중...' : '🔍 검색'}
          </button>
        </div>
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
    flexDirection: 'column',
    gap: '20px',
    width: '100%',
  },
  row: {
    display: 'flex',
    gap: '12px',
    alignItems: 'center',
    flexWrap: 'wrap',
    width: '100%',
  },
  checkboxGroup: {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
    padding: '15px',
    backgroundColor: '#f8f9fa',
    borderRadius: '10px',
    border: '1px solid #e0e0e0',
  },
  translateRow: {
    display: 'flex',
    gap: '20px',
    alignItems: 'center',
    flexWrap: 'wrap',
  },
  checkboxGroupInline: {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
    padding: '15px',
    backgroundColor: '#f8f9fa',
    borderRadius: '10px',
    border: '1px solid #e0e0e0',
    flex: 1,
    minWidth: '300px',
  },
  optionsContainer: {
    display: 'flex',
    gap: '15px',
    alignItems: 'center',
    flexWrap: 'wrap',
    padding: '15px',
  },
  searchRow: {
    display: 'flex',
    gap: '12px',
    alignItems: 'center',
    width: '100%',
  },
  groupLabel: {
    fontSize: '16px',
    fontWeight: 600,
    color: '#333',
    marginBottom: '8px',
  },
  checkboxContainer: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '12px',
    alignItems: 'center',
  },
  checkboxLabel: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    cursor: 'pointer',
    padding: '8px 12px',
    borderRadius: '8px',
    backgroundColor: 'white',
    border: '2px solid #e0e0e0',
    transition: 'all 0.3s',
    userSelect: 'none',
  },
  checkboxLabelSelected: {
    backgroundColor: '#e7f3ff',
    border: '2px solid #007bff',
    boxShadow: '0 2px 8px rgba(0, 123, 255, 0.2)',
  },
  radioInput: {
    width: '18px',
    height: '18px',
    cursor: 'pointer',
    accentColor: '#007bff',
  },
  checkboxText: {
    fontSize: '14px',
    fontWeight: 500,
    color: '#333',
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
    whiteSpace: 'nowrap',
  },
  buttonDisabled: {
    backgroundColor: '#ccc',
    cursor: 'not-allowed',
    boxShadow: 'none',
  },
  gptContainer: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
  },
  gptLabel: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    cursor: 'pointer',
    fontSize: '14px',
    userSelect: 'none',
  },
  checkbox: {
    width: '18px',
    height: '18px',
    cursor: 'pointer',
  },
  gptText: {
    color: '#333',
    fontWeight: 500,
  },
  gptBadge: {
    padding: '2px 8px',
    fontSize: '11px',
    backgroundColor: '#ff6b6b',
    color: 'white',
    borderRadius: '12px',
    fontWeight: 600,
  },
};





