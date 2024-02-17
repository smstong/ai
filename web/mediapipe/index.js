import {
    GestureRecognizer,
    FilesetResolver,
}from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision/vision_bundle.js";

window.addEventListener("DOMContentLoaded", (ev)=>{
    init();
});

let gestureRecognizer = null;

async function init() {
    await initCam();
    const vision = await FilesetResolver.forVisionTasks("https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/wasm");
    gestureRecognizer = await GestureRecognizer.createFromOptions(vision,
        {
            baseOptions: {
                modelAssetPath: "https://storage.googleapis.com/mediapipe-tasks/gesture_recognizer/gesture_recognizer.task"
            },
            runningMode: "VIDEO",
            numbHands: 1,
        }
    );

}
let lastVideoTime = -1;

function renderLoop() {
    console.log("hello");
    const video = document.getElementById("webcam");
    if (video.currentTime !== lastVideoTime) {
        const R = gestureRecognizer.recognizeForVideo(video, Date.now());
        console.log(R);
        lastVideoTime = video.currentTime;
    }
    requestAnimationFrame(() => {
        renderLoop();
    });
}

// initialize web camera
async function initCam() {
    let video = document.querySelector("#webcam");
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        video.srcObject = stream;
        video.play();
        video.addEventListener("loadeddata", renderLoop);
    } catch (e) {
        console.log(e);
    }
}