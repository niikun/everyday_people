import React, { useState, useEffect, useRef } from 'react';

const CatchingGame = ({ onEnd }) => {
  const [stars, setStars] = useState([]);
  const [score, setScore] = useState(0);
  const [timeLeft, setTimeLeft] = useState(30);
  const [gameRunning, setGameRunning] = useState(true);
  const gameAreaRef = useRef(null);

  useEffect(() => {
    const gameInterval = setInterval(() => {
      if (gameRunning) {
        // Add new star
        if (Math.random() < 0.3) {
          const newStar = {
            id: Date.now() + Math.random(),
            x: Math.random() * 700,
            y: 0,
            speed: 2 + Math.random() * 3
          };
          setStars(prev => [...prev, newStar]);
        }

        // Update star positions
        setStars(prev => 
          prev.map(star => ({ ...star, y: star.y + star.speed }))
            .filter(star => star.y < 400)
        );
      }
    }, 100);

    return () => clearInterval(gameInterval);
  }, [gameRunning]);

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 1) {
          setGameRunning(false);
          onEnd(score);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [score, onEnd]);

  const catchStar = (starId) => {
    setStars(prev => prev.filter(star => star.id !== starId));
    setScore(prev => prev + 10);
  };

  return (
    <div className="screen">
      <h1 className="game-title">星キャッチゲーム</h1>
      
      <div className="score-display">スコア: {score}</div>
      <div className="timer">残り時間: {timeLeft}秒</div>
      
      <div className="game-area" ref={gameAreaRef}>
        <div style={{ position: 'absolute', top: '10px', left: '10px', color: '#666' }}>
          星をクリックしてキャッチしよう！
        </div>
        
        {stars.map(star => (
          <button
            key={star.id}
            className="star"
            style={{
              left: `${star.x}px`,
              top: `${star.y}px`,
            }}
            onClick={() => catchStar(star.id)}
          >
            ⭐
          </button>
        ))}
      </div>
      
      <div className="instructions">
        <p>落ちてくる星をクリックしてキャッチしよう！</p>
        <p>制限時間: 30秒</p>
      </div>
    </div>
  );
};

export default CatchingGame;