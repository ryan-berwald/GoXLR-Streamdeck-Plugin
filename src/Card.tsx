import { useState } from "react";

function Card() {
  const [key, setKey] = useState("Set key");

  return (
    <div>
<div></div>
      <div className="p-5">
    <div className="justify-center w-96 h-24 bg-gray-400 rounded-md filter drop-shadow-lg">
      <div className="grid grid-cols-3 gap-4 h-full">
      <div></div>
      <div></div>
      <div><button id="btnKp" onClick={() => keyPress(setKey)} className="w-full h-full bg-blue-300 rounded-r-md transform motion-safe:hover:scale-110">{key}</button></div>
      </div>
    </div>
    </div>
    <div></div>
</div>
  );
}

let keyPress = (k:any) => {
    document.addEventListener('keyup', (e) => {
      k(e.key);
    })
}

export default Card;
