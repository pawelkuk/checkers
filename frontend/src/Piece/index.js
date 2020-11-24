import React from "react";
import "./style.css";

function Piece({ color = "black" }) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
      <circle cx="50%" cy="50%" r="35%" fill={color} />
    </svg>
  );
}
export default Piece;
