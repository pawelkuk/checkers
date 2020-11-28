import { useState } from "react";
import Board from "../Board/index";

function idx2piece(idx) {
  if (0 < idx && idx <= 12) return "black";
  if (12 < idx && idx <= 20) return null;
  if (20 < idx && idx <= 32) return "white";
}

function App() {
  const allAccessibleFields = 33;
  const arr = Array.from({ length: allAccessibleFields }, (_, index) => [
    index,
    idx2piece(index),
  ]);
  const initBoard = Object.fromEntries(arr);
  const [piecePositions, setPiecePosition] = useState([0, 0]);
  const onChange = (position) => {
    setPiecePosition(position);
  };
  return (
    <div>
      <Board position={piecePositions} onChange={onChange} />
    </div>
  );
}

export default App;
