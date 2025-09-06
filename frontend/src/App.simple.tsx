import React from 'react';

function App() {
  return (
    <div style={{ padding: '20px', background: 'white', minHeight: '100vh' }}>
      <h1 style={{ color: 'black', fontSize: '32px' }}>Книги по Python</h1>
      <p style={{ color: 'gray', fontSize: '18px' }}>
        Это тестовая страница. Если вы это видите, React работает!
      </p>
      <div style={{ 
        background: '#f0f0f0', 
        padding: '20px', 
        margin: '20px 0',
        borderRadius: '8px'
      }}>
        <h2 style={{ color: 'blue' }}>Тест компонентов:</h2>
        <button 
          style={{ 
            background: 'blue', 
            color: 'white', 
            padding: '10px 20px',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
          onClick={() => alert('Кнопка работает!')}
        >
          Нажми меня
        </button>
      </div>
    </div>
  );
}

export default App;