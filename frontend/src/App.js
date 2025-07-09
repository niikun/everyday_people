import React, { useState, useEffect } from 'react';
import axios from 'axios';
import MainScreen from './components/MainScreen';
import GameIntro from './components/GameIntro';
import CatchingGame from './components/CatchingGame';
import MemoryGame from './components/MemoryGame';
import DrawingGame from './components/DrawingGame';
import GameResult from './components/GameResult';
import './App.css';

function App() {
  const [screen, setScreen] = useState('main');
  const [progress, setProgress] = useState(null);
  const [stampedToday, setStampedToday] = useState(false);
  const [gameAvailable, setGameAvailable] = useState(false);
  const [selectedGame, setSelectedGame] = useState(null);
  const [gameScore, setGameScore] = useState(0);

  useEffect(() => {
    loadProgress();
  }, []);

  const loadProgress = async () => {
    try {
      const response = await axios.get('/api/progress');
      setProgress(response.data.progress);
      setStampedToday(response.data.stamped_today);
      setGameAvailable(response.data.stamped_today);
    } catch (error) {
      console.error('Error loading progress:', error);
    }
  };

  const giveStamp = async () => {
    try {
      const response = await axios.post('/api/stamp');
      if (response.data.success) {
        setStampedToday(true);
        setGameAvailable(true);
        await loadProgress();
        alert(response.data.message);
      } else {
        alert(response.data.message);
      }
    } catch (error) {
      console.error('Error giving stamp:', error);
    }
  };

  const selectGame = async () => {
    try {
      const response = await axios.post('/api/game/select');
      setSelectedGame(response.data.game);
      setGameAvailable(false);
      setScreen('game-intro');
    } catch (error) {
      console.error('Error selecting game:', error);
    }
  };

  const startGame = () => {
    setScreen('game');
  };

  const endGame = async (score) => {
    setGameScore(score);
    
    try {
      await axios.post('/api/game/result', {
        score: score,
        game_id: selectedGame.id
      });
    } catch (error) {
      console.error('Error saving game result:', error);
    }
    
    setScreen('game-result');
  };

  const backToMain = () => {
    setScreen('main');
    setGameAvailable(true);
  };

  const renderScreen = () => {
    switch (screen) {
      case 'main':
        return (
          <MainScreen
            progress={progress}
            stampedToday={stampedToday}
            gameAvailable={gameAvailable}
            onStamp={giveStamp}
            onPlayGame={selectGame}
          />
        );
      case 'game-intro':
        return (
          <GameIntro
            selectedGame={selectedGame}
            onStart={startGame}
            onBack={backToMain}
          />
        );
      case 'game':
        if (selectedGame.id === 'catching') {
          return <CatchingGame onEnd={endGame} />;
        } else if (selectedGame.id === 'memory') {
          return <MemoryGame onEnd={endGame} />;
        } else if (selectedGame.id === 'drawing') {
          return <DrawingGame onEnd={endGame} />;
        }
        break;
      case 'game-result':
        return (
          <GameResult
            score={gameScore}
            onBack={backToMain}
          />
        );
      default:
        return <MainScreen />;
    }
  };

  return (
    <div className="App">
      {renderScreen()}
    </div>
  );
}

export default App;