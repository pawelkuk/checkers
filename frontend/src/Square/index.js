import React from "react";
import { useDrop } from "react-dnd";
import "./style.css";
import { ItemTypes } from "../Constants/index";

function Square({ colorPalette, x, y, children, onChange }) {
  const ifAccessible = !(x % 2 === y % 2);
  const squareColor = ifAccessible
    ? colorPalette.accessible
    : colorPalette.inaccessible;
  const [{ isOver }, drop] = useDrop({
    accept: ItemTypes.PIECE,
    drop: () => onChange([x, y]),
    collect: (monitor) => ({
      isOver: !!monitor.isOver(),
    }),
  });
  return (
    <div
      ref={drop}
      className="square"
      style={{
        backgroundColor: squareColor,
      }}
    >
      {children}
      {isOver && (
        <div
          style={{
            position: "inherit",
            top: 0,
            left: 0,
            height: "50px",
            width: "50px",
            zIndex: 1,
            opacity: 0.5,
            backgroundColor: "yellow",
          }}
        />
      )}
    </div>
  );
}

export default Square;
