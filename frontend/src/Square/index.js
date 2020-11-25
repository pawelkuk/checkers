import React from "react";
import "./style.css";
import Piece from "../Piece/index";

function Square({ colorPalette, x, y, children }) {
  const ifAccessible = !(x % 2 === y % 2);
  const squareColor = ifAccessible
    ? colorPalette.accessible
    : colorPalette.inaccessible;
  return (
    <div
      className="square"
      style={{
        backgroundColor: squareColor,
      }}
    >
      {children}
    </div>
  );
}

export default Square;
