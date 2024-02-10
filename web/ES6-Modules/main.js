import {name, draw} from "./modules/square.js"
import {createCanvas} from "./modules/canvas.js"

window.addEventListener("DOMContentLoaded", ()=>{
    document.querySelector("#demo").innerText = name;
});