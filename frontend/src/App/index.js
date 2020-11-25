import { useState } from "react";
import Board from "../Board/index";

function App() {
  const [piecePosition, setPiecePosition] = useState([0, 0]);
  return (
    <div>
      <Board position={piecePosition} onChange={setPiecePosition} />
    </div>
  );
}

export default App;
