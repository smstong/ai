import {
    GestureRecognizer,
    FilesetResolver,
}from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision/vision_bundle.js";

window.addEventListener("DOMContentLoaded", (ev)=>{
    init();
});

async function init() {
    await initCam();
    const vision = await FilesetResolver.forVisionTasks("https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/wasm");
    const gestureRecognizer = await GestureRecognizer.createFromOptions(vision,
        {
            baseOptions: {
                modelAssetPath: "https://storage.googleapis.com/mediapipe-tasks/gesture_recognizer/gesture_recognizer.task"
            },
            runningMode: "video",
            numbHands: 1,
        }
    );

    let lastVideoTime = -1;
    function renderLoop() {
        const video = document.getElementById("webcam");
        if (video.currentTime !== lastVideoTime) {
            const R = gestureRecognizer.recognizeForVideo(video);
            console.log(R);
            lastVideoTime = video.currentTime;
        }
        requestAnimationFrame(()=>{
            renderLoop();
        });
    }
    renderLoop();
}

// initialize web camera
async function initCam() {
    let video = document.querySelector("#webcam");
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        video.srcObject = stream;
        video.play();
    } catch (e) {
        console.log(e);
    }
}