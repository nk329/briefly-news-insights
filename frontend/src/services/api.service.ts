/**
 * API 호출 서비스
 * 백엔드 FastAPI와 통신하는 함수들
 */

import axios from 'axios';
import { NewsSearchResponse } from '../types/news.types';
import {
  LoginRequest,
  SignupRequest,
  AuthResponse,
  User,
  SearchHistory,
  Category,
  CategoryCreate,
} from '../types/auth.types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Axios 인스턴스 생성
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Axios 인터셉터: Authorization 헤더 자동 추가 (토큰이 있을 때만)
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    console.log('[API] Request:', config.method?.toUpperCase(), config.url);
    console.log('[API] Token exists:', !!token);
    
    if (token) {
      config.headers = config.headers || {};
      config.headers['Authorization'] = `Bearer ${token}`;
      console.log('[API] Authorization header set');
    }
    return config;
  },
  (error) => {
    console.error('[API] Request error:', error);
    return Promise.reject(error);
  }
);

// Response 인터셉터: 에러 처리
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      console.error('[API] 401 Unauthorized - 토큰이 유효하지 않습니다');
      // 토큰 제거
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
    }
    return Promise.reject(error);
  }
);

// ==================== 인증 API ====================

/**
 * 회원가입
 */
export const signup = async (data: SignupRequest): Promise<User> => {
  try {
    const response = await apiClient.post<User>('/api/auth/signup', data);
    return response.data;
  } catch (error) {
    console.error('회원가입 실패:', error);
    throw error;
  }
};

/**
 * 로그인
 */
export const login = async (data: LoginRequest): Promise<AuthResponse> => {
  try {
    const response = await apiClient.post<AuthResponse>('/api/auth/login', data);
    // 토큰 저장
    localStorage.setItem('access_token', response.data.access_token);
    localStorage.setItem('user', JSON.stringify(response.data.user));
    return response.data;
  } catch (error) {
    console.error('로그인 실패:', error);
    throw error;
  }
};

/**
 * 로그아웃
 */
export const logout = (): void => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('user');
};

/**
 * 현재 로그인한 사용자 정보 조회
 */
export const getCurrentUser = async (): Promise<User> => {
  try {
    const response = await apiClient.get<User>('/api/auth/me');
    return response.data;
  } catch (error) {
    console.error('사용자 정보 조회 실패:', error);
    throw error;
  }
};

// ==================== 검색 히스토리 API ====================

/**
 * 검색 히스토리 목록 조회
 */
export const getSearchHistories = async (
  skip: number = 0,
  limit: number = 20
): Promise<SearchHistory[]> => {
  try {
    const response = await apiClient.get<SearchHistory[]>('/api/history/', {
      params: { skip, limit },
    });
    return response.data;
  } catch (error) {
    console.error('검색 히스토리 조회 실패:', error);
    throw error;
  }
};

/**
 * 검색 히스토리 저장
 */
export const createSearchHistory = async (
  keyword: string,
  fromDate?: string,
  toDate?: string,
  resultsCount: number = 0
): Promise<SearchHistory> => {
  try {
    const response = await apiClient.post<SearchHistory>('/api/history/', {
      keyword,
      from_date: fromDate,
      to_date: toDate,
      results_count: resultsCount,
    });
    return response.data;
  } catch (error) {
    console.error('검색 히스토리 저장 실패:', error);
    throw error;
  }
};

/**
 * 검색 히스토리 삭제
 */
export const deleteSearchHistory = async (historyId: number): Promise<void> => {
  try {
    await apiClient.delete(`/api/history/${historyId}`);
  } catch (error) {
    console.error('검색 히스토리 삭제 실패:', error);
    throw error;
  }
};

/**
 * 모든 검색 히스토리 삭제
 */
export const deleteAllSearchHistories = async (): Promise<void> => {
  try {
    await apiClient.delete('/api/history/');
  } catch (error) {
    console.error('검색 히스토리 전체 삭제 실패:', error);
    throw error;
  }
};

// ==================== 카테고리 API ====================

/**
 * 카테고리 목록 조회
 */
export const getCategories = async (): Promise<Category[]> => {
  try {
    const response = await apiClient.get<Category[]>('/api/categories/');
    return response.data;
  } catch (error) {
    console.error('카테고리 조회 실패:', error);
    throw error;
  }
};

/**
 * 카테고리 생성
 */
export const createCategory = async (data: CategoryCreate): Promise<Category> => {
  try {
    const response = await apiClient.post<Category>('/api/categories/', data);
    return response.data;
  } catch (error) {
    console.error('카테고리 생성 실패:', error);
    throw error;
  }
};

/**
 * 카테고리 수정
 */
export const updateCategory = async (
  categoryId: number,
  data: Partial<CategoryCreate>
): Promise<Category> => {
  try {
    const response = await apiClient.put<Category>(
      `/api/categories/${categoryId}`,
      data
    );
    return response.data;
  } catch (error) {
    console.error('카테고리 수정 실패:', error);
    throw error;
  }
};

/**
 * 카테고리 삭제
 */
export const deleteCategory = async (categoryId: number): Promise<void> => {
  try {
    await apiClient.delete(`/api/categories/${categoryId}`);
  } catch (error) {
    console.error('카테고리 삭제 실패:', error);
    throw error;
  }
};

// ==================== 뉴스 API ====================

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
    const response = await apiClient.get<NewsSearchResponse>(
      '/api/news/search',
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
    const response = await apiClient.post(
      '/api/analysis/articles/keywords',
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
    const response = await apiClient.post(
      '/api/analysis/articles/complete',
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
    const response = await apiClient.post(
      '/api/analysis/wordcloud',
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
    const response = await apiClient.get('/health');
    return response.data;
  } catch (error) {
    console.error('서버 상태 확인 실패:', error);
    throw error;
  }
};



