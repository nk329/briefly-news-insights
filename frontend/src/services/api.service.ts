/**
 * API 호출 서비스
 * 백엔드 FastAPI와 통신하는 함수들
 */

import axios from 'axios';
import { NewsSearchResponse } from '../types/news.types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

/**
 * 뉴스 검색 API 호출
 * @param keyword 검색 키워드
 * @param fromDate 시작일 (YYYY-MM-DD)
 * @param toDate 종료일 (YYYY-MM-DD)
 * @param pageSize 결과 개수 (기본 10)
 * @returns 뉴스 검색 결과
 */
export const searchNews = async (
  keyword: string,
  fromDate?: string,
  toDate?: string,
  pageSize: number = 10
): Promise<NewsSearchResponse> => {
  try {
    const response = await axios.get<NewsSearchResponse>(
      `${API_BASE_URL}/api/news/search`,
      {
        params: {
          keyword,
          from_date: fromDate,
          to_date: toDate,
          page_size: pageSize,
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error('뉴스 검색 실패:', error);
    throw error;
  }
};

/**
 * 기사 키워드 분석
 * @param articles 뉴스 기사 배열
 * @param topN 추출할 키워드 개수
 * @returns 키워드 분석 결과
 */
export const analyzeArticlesKeywords = async (
  articles: any[],
  topN: number = 20
): Promise<any> => {
  try {
    const response = await axios.post(
      `${API_BASE_URL}/api/analysis/articles/keywords`,
      {
        articles,
        top_n: topN,
      }
    );
    return response.data;
  } catch (error) {
    console.error('키워드 분석 실패:', error);
    throw error;
  }
};

/**
 * 통합 분석 (키워드 + 워드클라우드)
 * @param articles 뉴스 기사 배열
 * @param topN 추출할 키워드 개수
 * @returns 키워드 분석 결과 + 워드클라우드 이미지 URL
 */
export const completeAnalysis = async (
  articles: any[],
  topN: number = 20
): Promise<any> => {
  try {
    const response = await axios.post(
      `${API_BASE_URL}/api/analysis/articles/complete`,
      {
        articles,
        top_n: topN,
      }
    );
    return response.data;
  } catch (error) {
    console.error('통합 분석 실패:', error);
    throw error;
  }
};

/**
 * 워드클라우드 생성
 * @param keywords 키워드 딕셔너리 {단어: 빈도수}
 * @param width 이미지 너비
 * @param height 이미지 높이
 * @returns 워드클라우드 이미지 URL
 */
export const generateWordCloud = async (
  keywords: { [key: string]: number },
  width: number = 600,
  height: number = 400
): Promise<any> => {
  try {
    const response = await axios.post(
      `${API_BASE_URL}/api/analysis/wordcloud`,
      {
        keywords,
        width,
        height,
      }
    );
    return response.data;
  } catch (error) {
    console.error('워드클라우드 생성 실패:', error);
    throw error;
  }
};

/**
 * API 서버 상태 확인
 * @returns 서버 상태
 */
export const healthCheck = async (): Promise<{ status: string }> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/health`);
    return response.data;
  } catch (error) {
    console.error('서버 상태 확인 실패:', error);
    throw error;
  }
};


