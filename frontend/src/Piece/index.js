import React from "react";
import "./style.css";

function Piece({ color = "black" }) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="50px" height="50px">
      <circle cx="20" cy="20" r="20" fill={color} />
    </svg>
  );
}
export default Piece;
