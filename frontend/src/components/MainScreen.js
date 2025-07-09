import React from 'react';

const MainScreen = ({ progress, stampedToday, gameAvailable, onStamp, onPlayGame }) => {
  return (
    <div className="screen">
      <h1 className="title">うがい習慣アプリ</h1>
      
      <div className={`status ${stampedToday ? 'success' : 'pending'}`}>
        {stampedToday ? '今日はうがいできました！ ⭐' : '今日のうがいはまだです'}
      </div>
      
      {progress && (
        <div className="stats">
          <p>連続日数: {progress.streak}日</p>
          <p>合計日数: {progress.total_days}日</p>
          <p>ゲーム回数: {progress.games_played}回</p>
        </div>
      )}
      
      <div className="buttons">
        {!stampedToday && (
          <button className="button primary" onClick={onStamp}>
            うがいしました（お母さんに押してもらう）
          </button>
        )}
        
        {gameAvailable && (
          <button className="button success" onClick={onPlayGame}>
            ゲームで遊ぶ
          </button>
        )}
      </div>
      
      <div className="instructions">
        <p>毎日うがいをしてスタンプをもらおう！</p>
        <p>スタンプをもらうとゲームで遊べます。</p>
      </div>
    </div>
  );
};

export default MainScreen;