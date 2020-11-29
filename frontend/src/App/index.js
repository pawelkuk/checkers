import { useState } from "react";
import Board from "../Board/index";

function idx2piece(idx) {
  if (0 < idx && idx <= 12) return "black";
  if (12 < idx && idx <= 20) return null;
  if (20 < idx && idx <= 32) return "white";
}

function coordsToCheckersNotation(x, y) {
  return x % 2 === 0 ? 4 * x + (y + 1) / 2 : 4 * x + y / 2 + 1;
}

function App() {
  const initBoard = {};
  for (let i = 1; i <= 32; i++) initBoard[i] = idx2piece(i);
  const [piecePositions, setPiecePosition] = useState(initBoard);
  const onChange = (from, to, color) => {
    const piece = coordsToCheckersNotation(...to);
    if (Number.isInteger(piece) && piecePositions[piece] === null) {
      piecePositions[piece] = color;
      const toNull = coordsToCheckersNotation(...from);
      piecePositions[toNull] = null;
      const copy = Object.assign({}, piecePositions);
      setPiecePosition(copy);
    }
  };
  return (
    <div>
      <Board
        positions={piecePositions}
        onChange={onChange}
        perspective="white"
      />
    </div>
  );
}

export default App;
