/**
 * 로그인 컴포넌트
 */

import React, { useState } from 'react';
import { login as apiLogin } from '../services/api.service';
import { useAuth } from '../contexts/AuthContext';
import '../styles/Auth.css';

interface LoginProps {
  onSwitchToSignup: () => void;
  onClose: () => void;
}

export const Login: React.FC<LoginProps> = ({ onSwitchToSignup, onClose }) => {
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const response = await apiLogin({ email, password });
      login(response.user, response.access_token);
      onClose();
    } catch (err: any) {
      console.error('로그인 실패:', err);
      if (err.response?.status === 401) {
        setError('이메일 또는 비밀번호가 올바르지 않습니다');
      } else {
        setError('로그인 중 오류가 발생했습니다');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>로그인</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">이메일</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="example@email.com"
              required
              autoFocus
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">비밀번호</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="비밀번호 입력"
              required
              minLength={6}
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <button type="submit" className="btn-primary" disabled={isLoading}>
            {isLoading ? '로그인 중...' : '로그인'}
          </button>
        </form>

        <div className="auth-footer">
          <p>
            계정이 없으신가요?{' '}
            <button type="button" className="link-button" onClick={onSwitchToSignup}>
              회원가입
            </button>
          </p>
        </div>

        <button className="btn-close" onClick={onClose}>
          ✕
        </button>
      </div>
    </div>
  );
};




