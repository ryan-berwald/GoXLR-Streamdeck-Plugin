import { useState } from "react";

const fs = require("fs"); //read file sys

function Card() {
  const [key, setKey] = useState("Set key");
  const files = fs.readdir(
    "C:\\Users\\Ryan\\Documents\\goxlr\\profiles",
    (err: Error, files: String[]) => {
      if (err) console.log(err);
      else {
        files.forEach((file) => {
          console.log(file);
        });
        return files;
      }
    }
  );
  return (
    <div>
      <div></div>
      <div className="p-5">
        <div className="justify-center w-96 h-24 bg-gray-400 rounded-md filter drop-shadow-lg">
          <div className="grid grid-cols-3 gap-4 h-full">
            <div>
              <select
                className="mt-8 ml-8 w-24 h-8 bg-blue-400 rounded-md"
                name="profiles"
                id="profiles"
              >
                <option value="volvo">Volvo</option>
              </select>
            </div>
            <div></div>
            <div>
              <button
                id="btnKp"
                onClick={() => keyPress(setKey)}
                className="w-full h-full bg-blue-300 rounded-r-md transform motion-safe:hover:scale-110"
              >
                {key}
              </button>
            </div>
          </div>
        </div>
      </div>
      <div></div>
    </div>
  );
}

let keyPress = (k: any) => {
  document.addEventListener("keyup", (e) => {
    k(e.key);
  });
};

export default Card;
