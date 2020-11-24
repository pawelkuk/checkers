import React from "react";
import "./style.css";
import Square from "../Square/index";

function Row({
  dim = 8,
  colorPalette = { accessible: "green", inaccessible: "yellow" },
  rowIdx = 0,
}) {
  const range = [...Array(dim).keys()];
  let row = range.map((colIdx) => {
    return (
      <Square
        key={colIdx}
        colorPalette={colorPalette}
        x={rowIdx}
        y={colIdx}
      ></Square>
    );
  });
  return <div className="board-row">{row}</div>;
}

function Board({
  dim = 8,
  colorPalette = { accessible: "green", inaccessible: "yellow" },
}) {
  const range = [...Array(dim).keys()];
  const board = range.map((i) => {
    return <Row dim={dim} colorPalette={colorPalette} rowIdx={i} />;
  });
  return board;
}

export default Board;
