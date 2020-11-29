import React from "react";
import "./style.css";
import { useDrag } from "react-dnd";
import { ItemTypes } from "../Constants/index";
import "./style.css";

function Piece({ color = "black", x = -1, y = -1 }) {
  const [{ isDragging }, drag] = useDrag({
    item: { type: ItemTypes.PIECE, x: x, y: y, color: color },
    collect: (monitor) => ({
      isDragging: !!monitor.isDragging(),
    }),
  });
  return (
    <div
      className="drag-wrapper"
      ref={drag}
      style={{
        opacity: isDragging ? 0.5 : 1,
      }}
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
        <circle className="circle" fill={color} />
      </svg>
    </div>
  );
}
export default Piece;
