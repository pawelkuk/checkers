import React from "react";
import { useDrop } from "react-dnd";
import "./style.css";
import { ItemTypes } from "../Constants/index";

function Square({ colorPalette, x, y, children, onChange }) {
  const ifAccessible = x % 2 !== y % 2;
  const squareColor = ifAccessible
    ? colorPalette.accessible
    : colorPalette.inaccessible;
  const [{ isOver }, drop] = useDrop({
    accept: ItemTypes.PIECE,
    drop: (item) => onChange(item.from, [x, y], item.color),
    collect: (monitor) => ({
      isOver: !!monitor.isOver(),
    }),
  });
  return (
    <div
      ref={ifAccessible ? drop : null}
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
