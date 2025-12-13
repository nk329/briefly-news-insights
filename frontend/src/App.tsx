/**
 * 메인 App 컴포넌트
 */

import React from 'react';
import { AuthProvider } from './contexts/AuthContext';
import { Dashboard } from './screens/Dashboard';
import './styles/global.css';

function App() {
  return (
    <AuthProvider>
      <div className="App">
        <Dashboard />
      </div>
    </AuthProvider>
  );
}

export default App;
