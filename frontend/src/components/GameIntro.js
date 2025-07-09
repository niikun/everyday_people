import React from 'react';

const GameIntro = ({ selectedGame, onStart, onBack }) => {
  return (
    <div className="screen">
      <h1 className="title">今日のゲーム</h1>
      
      {selectedGame && (
        <div className="game-intro">
          <h2 className="game-title">{selectedGame.name}</h2>
          <p className="game-description">{selectedGame.description}</p>
          
          <div className="buttons">
            <button className="button success" onClick={onStart}>
              ゲームスタート！
            </button>
            <button className="button danger" onClick={onBack}>
              戻る
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default GameIntro;