import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import Card from "./Card";

ReactDOM.render(
  <React.StrictMode>
    <div className="grid grid-cols-3 gap-4">
      <div></div>
      <div className="p-5">
        <Card />
      </div>
      <div></div>
      <div></div>
      <div className="p-5">
        <Card />
      </div>
    </div>
  </React.StrictMode>,
  document.getElementById("root")
);
