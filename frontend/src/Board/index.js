import React from "react";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import "./style.css";
import Square from "../Square/index";
import Piece from "../Piece/index";

function renderPiece(x, y, positions) {
  const piece = x % 2 === 0 ? 4 * x + (y + 1) / 2 : 4 * x + y / 2 + 1;
  if (Number.isInteger(piece) && !!positions[piece])
    return <Piece color={positions[piece]} x={x} y={y} />;
}

function Row({
  dim = 8,
  colorPalette = { accessible: "green", inaccessible: "yellow" },
  rowIdx = 0,
  positions,
  onChange,
  perspective,
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
        {renderPiece(rowIdx, colIdx, positions)}
      </Square>
    );
  });
  row = perspective === "white" ? row : row.reverse();
  return <div className="board-row">{row}</div>;
}

function Board({
  dim = 8,
  colorPalette = { accessible: "green", inaccessible: "yellow" },
  perspective = "white" || "black",
  positions,
  onChange,
}) {
  const range = [...Array(dim).keys()];
  let board = range.map((i) => (
    <Row
      key={i}
      dim={dim}
      colorPalette={colorPalette}
      rowIdx={i}
      positions={positions}
      onChange={onChange}
      perspective={perspective}
    />
  ));
  board = perspective === "white" ? board : board.reverse();
  return <DndProvider backend={HTML5Backend}>{board}</DndProvider>;
}

export default Board;
