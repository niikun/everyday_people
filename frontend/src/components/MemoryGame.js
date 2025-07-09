import React, { useState, useEffect } from 'react';

const MemoryGame = ({ onEnd }) => {
  const [cards, setCards] = useState([]);
  const [flippedCards, setFlippedCards] = useState([]);
  const [matchedCards, setMatchedCards] = useState([]);
  const [score, setScore] = useState(0);
  const [timeElapsed, setTimeElapsed] = useState(0);
  const [gameComplete, setGameComplete] = useState(false);

  const colors = ['#f44336', '#2196f3', '#4caf50', '#ff9800', '#9c27b0', '#00bcd4'];

  useEffect(() => {
    // Initialize cards
    const cardColors = [...colors, ...colors];
    const shuffledCards = cardColors.sort(() => Math.random() - 0.5);
    setCards(shuffledCards.map((color, index) => ({ id: index, color, flipped: false, matched: false })));
  }, []);

  useEffect(() => {
    const timer = setInterval(() => {
      if (!gameComplete) {
        setTimeElapsed(prev => prev + 1);
      }
    }, 1000);

    return () => clearInterval(timer);
  }, [gameComplete]);

  useEffect(() => {
    if (flippedCards.length === 2) {
      const [first, second] = flippedCards;
      if (cards[first].color === cards[second].color) {
        // Match found
        setMatchedCards(prev => [...prev, first, second]);
        setScore(prev => prev + 10);
        setFlippedCards([]);
        
        // Check if game is complete
        if (matchedCards.length + 2 === cards.length) {
          setGameComplete(true);
          setTimeout(() => {
            const finalScore = Math.max(0, 100 - timeElapsed);
            onEnd(finalScore);
          }, 1000);
        }
      } else {
        // No match - flip back after delay
        setTimeout(() => {
          setFlippedCards([]);
        }, 1000);
      }
    }
  }, [flippedCards, cards, matchedCards, timeElapsed, onEnd]);

  const flipCard = (index) => {
    if (flippedCards.length < 2 && !flippedCards.includes(index) && !matchedCards.includes(index)) {
      setFlippedCards(prev => [...prev, index]);
    }
  };

  const isCardFlipped = (index) => {
    return flippedCards.includes(index) || matchedCards.includes(index);
  };

  const isCardMatched = (index) => {
    return matchedCards.includes(index);
  };

  return (
    <div className="screen">
      <h1 className="game-title">メモリーマッチングゲーム</h1>
      
      <div className="score-display">スコア: {score}</div>
      <div className="timer">経過時間: {timeElapsed}秒</div>
      
      <div className="game-area">
        <div className="memory-board">
          {cards.map((card, index) => (
            <div
              key={card.id}
              className={`memory-card ${isCardFlipped(index) ? 'flipped' : ''} ${isCardMatched(index) ? 'matched' : ''}`}
              style={{
                backgroundColor: isCardFlipped(index) ? card.color : '#ddd',
              }}
              onClick={() => flipCard(index)}
            >
              {!isCardFlipped(index) && '?'}
            </div>
          ))}
        </div>
      </div>
      
      <div className="instructions">
        <p>同じ色のカードを2枚選んでマッチさせよう！</p>
        <p>マッチした組数: {matchedCards.length / 2} / 6</p>
      </div>
      
      <button className="button danger" onClick={() => onEnd(score)}>
        ゲーム終了
      </button>
    </div>
  );
};

export default MemoryGame;