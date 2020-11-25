import React from "react";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import "./style.css";
import Square from "../Square/index";
import Piece from "../Piece/index";

function renderPiece(x, y, [pieceX, pieceY]) {
  if (x === pieceX && y === pieceY) {
    return <Piece />;
  }
}

function Row({
  dim = 8,
  colorPalette = { accessible: "green", inaccessible: "yellow" },
  rowIdx = 0,
  position,
  onChange,
}) {
  const range = [...Array(dim).keys()];
  let row = range.map((colIdx) => {
    return (
      <Square
        key={colIdx}
        colorPalette={colorPalette}
        x={rowIdx}
        y={colIdx}
        onChange={onChange}
      >
        {renderPiece(rowIdx, colIdx, position)}
      </Square>
    );
  });
  return <div className="board-row">{row}</div>;
}

function Board({
  dim = 8,
  colorPalette = { accessible: "green", inaccessible: "yellow" },
  position,
  onChange,
}) {
  const range = [...Array(dim).keys()];
  const board = range.map((i) => {
    return (
      <Row
        key={i}
        dim={dim}
        colorPalette={colorPalette}
        rowIdx={i}
        position={position}
        onChange={onChange}
      />
    );
  });
  return <DndProvider backend={HTML5Backend}>{board}</DndProvider>;
}

export default Board;
