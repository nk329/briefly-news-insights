/**
 * 회원가입 컴포넌트
 */

import React, { useState } from 'react';
import { signup as apiSignup, login as apiLogin } from '../services/api.service';
import { useAuth } from '../contexts/AuthContext';
import '../styles/Auth.css';

interface SignupProps {
  onSwitchToLogin: () => void;
  onClose: () => void;
}

export const Signup: React.FC<SignupProps> = ({ onSwitchToLogin, onClose }) => {
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // 비밀번호 확인
    if (password !== confirmPassword) {
      setError('비밀번호가 일치하지 않습니다');
      return;
    }

    setIsLoading(true);

    try {
      // 회원가입
      await apiSignup({ email, username, password });

      // 자동 로그인
      const response = await apiLogin({ email, password });
      login(response.user, response.access_token);
      onClose();
    } catch (err: any) {
      console.error('회원가입 실패:', err);
      if (err.response?.status === 400) {
        setError(err.response.data.detail || '이미 등록된 이메일 또는 사용자명입니다');
      } else {
        setError('회원가입 중 오류가 발생했습니다');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>회원가입</h2>
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
            <label htmlFor="username">사용자명</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="사용자명 (3자 이상)"
              required
              minLength={3}
              maxLength={50}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">비밀번호</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="비밀번호 (6자 이상)"
              required
              minLength={6}
              maxLength={100}
            />
          </div>

          <div className="form-group">
            <label htmlFor="confirmPassword">비밀번호 확인</label>
            <input
              type="password"
              id="confirmPassword"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="비밀번호 재입력"
              required
              minLength={6}
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <button type="submit" className="btn-primary" disabled={isLoading}>
            {isLoading ? '가입 중...' : '회원가입'}
          </button>
        </form>

        <div className="auth-footer">
          <p>
            이미 계정이 있으신가요?{' '}
            <button type="button" className="link-button" onClick={onSwitchToLogin}>
              로그인
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




