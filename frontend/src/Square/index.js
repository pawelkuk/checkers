import React from "react";
import "./style.css";
import Piece from "../Piece/index";

function Square({ colorPalette, x, y }) {
  const ifAccessible = !(x % 2 === y % 2);
  const squareColor = ifAccessible
    ? colorPalette.accessible
    : colorPalette.inaccessible;
  const pieceColor = x < 3 ? "black" : "white";
  return (
    <div
      className="square"
      style={{
        backgroundColor: squareColor,
      }}
    >
      {ifAccessible ? <Piece color={pieceColor} /> : ""}
    </div>
  );
}

export default Square;
