import React from "react";
import "./style.css";
import Square from "../Square/index";

function Row({
  dim = 8,
  colorPalette = { accessible: "green", inaccessible: "yellow" },
  isOddRow = true,
}) {
  const range = [...Array(dim).keys()];
  let row = range.map((i) => {
    const color =
      i % 2 === Number(isOddRow)
        ? colorPalette.inaccessible
        : colorPalette.accessible;
    return <Square key={i} color={color}></Square>;
  });
  return <div className="board-row">{row}</div>;
}

function Board({
  dim = 8,
  colorPalette = { accessible: "green", inaccessible: "yellow" },
}) {
  const range = [...Array(dim).keys()];
  const board = range.map((i) => {
    const isOddRow = i % 2 === 1;
    return <Row dim={dim} colorPalette={colorPalette} isOddRow={isOddRow} />;
  });
  return board;
}

export default Board;
