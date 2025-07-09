import React from 'react';

const GameResult = ({ score, onBack }) => {
  const getMessage = (score) => {
    if (score >= 80) {
      return "すごい！上手にできました！";
    } else if (score >= 50) {
      return "よくできました！";
    } else {
      return "がんばりました！";
    }
  };

  return (
    <div className="screen">
      <div className="result-screen">
        <h1 className="title">ゲーム結果</h1>
        
        <div className="result-score">{score}</div>
        
        <div className="result-message">
          {getMessage(score)}
        </div>
        
        <button className="button primary" onClick={onBack}>
          メインに戻る
        </button>
      </div>
    </div>
  );
};

export default GameResult;