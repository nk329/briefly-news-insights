/**
 * 인증 관련 TypeScript 타입 정의
 */

export interface User {
  id: number;
  email: string;
  username: string;
  created_at: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface SignupRequest {
  email: string;
  username: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface SearchHistory {
  id: number;
  keyword: string;
  from_date: string | null;
  to_date: string | null;
  results_count: number;
  searched_at: string;
}

export interface Category {
  id: number;
  name: string;
  description: string | null;
  color: string;
  created_at: string;
}

export interface CategoryCreate {
  name: string;
  description?: string;
  color?: string;
}

