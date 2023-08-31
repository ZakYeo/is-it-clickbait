import React from 'react';
import './App.css';

function App() {
  const loginWithYouTube = () => {
    window.location.href = 'http://localhost:5000/login';
  };

  return (
    <div className="App">
      <header className="App-header">
        <button onClick={loginWithYouTube}>Login with YouTube</button>
      </header>
    </div>
  );
}

export default App;
