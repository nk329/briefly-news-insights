/**
 * 사용자 프로필 헤더
 * 로그인 상태에 따라 로그인/로그아웃 버튼 표시
 */

import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Login } from './Login';
import { Signup } from './Signup';
import '../styles/UserHeader.css';

export const UserHeader: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const [showLogin, setShowLogin] = useState(false);
  const [showSignup, setShowSignup] = useState(false);

  const handleLogout = () => {
    logout();
  };

  return (
    <>
      <div className="user-header">
        {isAuthenticated && user ? (
          <div className="user-info">
            <span className="user-avatar">{user.username[0].toUpperCase()}</span>
            <span className="user-name">{user.username}</span>
            <button className="btn-logout" onClick={handleLogout}>
              로그아웃
            </button>
          </div>
        ) : (
          <div className="auth-buttons">
            <button className="btn-login" onClick={() => setShowLogin(true)}>
              로그인
            </button>
            <button className="btn-signup" onClick={() => setShowSignup(true)}>
              회원가입
            </button>
          </div>
        )}
      </div>

      {showLogin && (
        <Login
          onSwitchToSignup={() => {
            setShowLogin(false);
            setShowSignup(true);
          }}
          onClose={() => setShowLogin(false)}
        />
      )}

      {showSignup && (
        <Signup
          onSwitchToLogin={() => {
            setShowSignup(false);
            setShowLogin(true);
          }}
          onClose={() => setShowSignup(false)}
        />
      )}
    </>
  );
};



