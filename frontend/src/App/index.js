import { useState } from "react";
import Board from "../Board/index";

function App() {
  const [piecePosition, setPiecePosition] = useState([0, 0]);
  const onChange = (position) => {
    setPiecePosition(position);
  };
  return (
    <div>
      <Board position={piecePosition} onChange={onChange} />
    </div>
  );
}

export default App;
