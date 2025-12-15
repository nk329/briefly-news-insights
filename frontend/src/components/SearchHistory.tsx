/**
 * 검색 히스토리 컴포넌트
 */

import React, { useState, useEffect } from 'react';
import { SearchHistory as SearchHistoryType } from '../types/auth.types';
import {
  getSearchHistories,
  deleteSearchHistory,
  deleteAllSearchHistories,
} from '../services/api.service';
import '../styles/SearchHistory.css';

interface SearchHistoryProps {
  onSelectHistory: (keyword: string, fromDate?: string, toDate?: string) => void;
}

export const SearchHistory: React.FC<SearchHistoryProps> = ({ onSelectHistory }) => {
  const [histories, setHistories] = useState<SearchHistoryType[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadHistories();
  }, []);

  const loadHistories = async () => {
    try {
      setLoading(true);
      const data = await getSearchHistories(0, 10);
      setHistories(data);
    } catch (err) {
      setError('검색 히스토리를 불러올 수 없습니다');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (historyId: number, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await deleteSearchHistory(historyId);
      setHistories(histories.filter((h) => h.id !== historyId));
    } catch (err) {
      // 히스토리 삭제 실패는 콘솔 출력 없이 무시
    }
  };

  const handleDeleteAll = async () => {
    if (!window.confirm('모든 검색 히스토리를 삭제하시겠습니까?')) {
      return;
    }

    try {
      await deleteAllSearchHistories();
      setHistories([]);
    } catch (err) {
      // 전체 삭제 실패도 콘솔 출력 없이 무시
    }
  };

  const formatDate = (dateString: string) => {
    // 백엔드에서 받은 시간 문자열 파싱 (ISO 8601 형식, UTC 또는 타임존 포함)
    const date = new Date(dateString);
    
    // 유효하지 않은 날짜인 경우 처리
    if (isNaN(date.getTime())) {
      return '알 수 없음';
    }
    
    const now = new Date();
    
    // 밀리초 단위 시간 차이 계산 (UTC 기준으로 자동 변환됨)
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return '방금 전';
    if (diffMins < 60) return `${diffMins}분 전`;
    if (diffHours < 24) return `${diffHours}시간 전`;
    if (diffDays < 7) return `${diffDays}일 전`;
    return date.toLocaleDateString('ko-KR');
  };

  if (loading) {
    return <div className="history-loading">로딩 중...</div>;
  }

  if (error) {
    return <div className="history-error">{error}</div>;
  }

  return (
    <div className="history-container">
      <div className="history-header">
        <h3>최근 검색</h3>
        {histories.length > 0 && (
          <button className="btn-clear-all" onClick={handleDeleteAll}>
            전체 삭제
          </button>
        )}
      </div>

      {histories.length === 0 ? (
        <div className="history-empty">검색 히스토리가 없습니다</div>
      ) : (
        <div className="history-list">
          {histories.map((history) => (
            <div
              key={history.id}
              className="history-item"
              onClick={() =>
                onSelectHistory(history.keyword, history.from_date || undefined, history.to_date || undefined)
              }
            >
              <div className="history-item-content">
                <div className="history-keyword">{history.keyword}</div>
                <div className="history-meta">
                  <span className="history-time">{formatDate(history.searched_at)}</span>
                  <span className="history-count">결과 {history.results_count}개</span>
                </div>
              </div>
              <button
                className="btn-delete"
                onClick={(e) => handleDelete(history.id, e)}
                title="삭제"
              >
                ×
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};






