import React, { useState, useRef, useEffect } from 'react';

const DrawingGame = ({ onEnd }) => {
  const canvasRef = useRef(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [currentColor, setCurrentColor] = useState('#000000');
  const [brushSize, setBrushSize] = useState(5);
  const [timeLeft, setTimeLeft] = useState(60);
  const [strokeCount, setStrokeCount] = useState(0);

  const colors = ['#000000', '#f44336', '#2196f3', '#4caf50', '#ff9800', '#9c27b0', '#00bcd4'];
  const brushSizes = [3, 5, 8, 12];

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    // Set canvas size
    canvas.width = 600;
    canvas.height = 400;
    
    // Set initial canvas background
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Set drawing properties
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
  }, []);

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 1) {
          const finalScore = 50 + Math.min(strokeCount * 2, 50);
          onEnd(finalScore);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [strokeCount, onEnd]);

  const startDrawing = (e) => {
    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    const ctx = canvas.getContext('2d');
    ctx.beginPath();
    ctx.moveTo(x, y);
    setIsDrawing(true);
    setStrokeCount(prev => prev + 1);
  };

  const draw = (e) => {
    if (!isDrawing) return;
    
    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    const ctx = canvas.getContext('2d');
    ctx.lineWidth = brushSize;
    ctx.strokeStyle = currentColor;
    ctx.lineTo(x, y);
    ctx.stroke();
  };

  const stopDrawing = () => {
    setIsDrawing(false);
  };

  const clearCanvas = () => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    setStrokeCount(0);
  };

  const finishDrawing = () => {
    const finalScore = 50 + Math.min(strokeCount * 2, 50);
    onEnd(finalScore);
  };

  return (
    <div className="screen">
      <h1 className="game-title">お絵かきゲーム</h1>
      
      <div className="score-display">ストローク数: {strokeCount}</div>
      <div className="timer">残り時間: {timeLeft}秒</div>
      
      <div className="game-area">
        <div className="canvas-container">
          <canvas
            ref={canvasRef}
            className="drawing-canvas"
            onMouseDown={startDrawing}
            onMouseMove={draw}
            onMouseUp={stopDrawing}
            onMouseLeave={stopDrawing}
          />
        </div>
        
        <div className="color-palette">
          {colors.map(color => (
            <button
              key={color}
              className={`color-button ${currentColor === color ? 'selected' : ''}`}
              style={{ backgroundColor: color }}
              onClick={() => setCurrentColor(color)}
            />
          ))}
        </div>
        
        <div className="brush-sizes">
          {brushSizes.map(size => (
            <button
              key={size}
              className={`brush-button ${brushSize === size ? 'selected' : ''}`}
              onClick={() => setBrushSize(size)}
            >
              <div
                className="brush-dot"
                style={{
                  width: `${size}px`,
                  height: `${size}px`,
                }}
              />
            </button>
          ))}
        </div>
        
        <div className="buttons">
          <button className="button warning" onClick={clearCanvas}>
            クリア
          </button>
          <button className="button success" onClick={finishDrawing}>
            完成！
          </button>
        </div>
      </div>
      
      <div className="instructions">
        <p>マウスでドラッグして自由にお絵かきしよう！</p>
        <p>色や筆のサイズを変えられます</p>
      </div>
    </div>
  );
};

export default DrawingGame;