import React from "react";
import "./style.css";

function Square({ color }) {
  return (
    <div
      className="square"
      style={{
        backgroundColor: color,
      }}
    ></div>
  );
}

export default Square;
