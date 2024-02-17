// this is a ES6 module js file

import {name, draw} from "./modules/square.js"
import {createCanvas} from "./modules/canvas.js"

window.addEventListener("DOMContentLoaded", ()=>{
    document.querySelector("#demo").innerText = name;
    createCanvas();
});

// this is undefined in a mdoule
console.log("main.js this is:", this);

// await is available at top level code
