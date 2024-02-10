window.addEventListener("DOMContentLoaded", init);

function init() {
    initCam();
    // after opencv.js is loaded, it's WASM code is not compiled yet.
    // So, cv is only available in cv['onRuntimeInitialized'] function.
    cv['onRuntimeInitialized'] = () => {
        document.querySelector("#status").innerHTML = "opencv is ready.";
        startApp();
    };
}

// initialize web camera
async function initCam() {
    let video = document.querySelector("#videoInput");
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        video.srcObject = stream;
        video.play();
    } catch (e) {
        console.log(e);
    }
}

// main app
function startApp() {
    let video = document.querySelector("#videoInput");
    let src = new cv.Mat(video.height, video.width, cv.CV_8UC4);
    let dst = new cv.Mat(video.height, video.width, cv.CV_8UC1);
    let cap = new cv.VideoCapture(video);

    const FPS = 30;
    function processVideo() {
        let begin = Date.now();
        cap.read(src);
        cv.cvtColor(src, dst, cv.COLOR_RGB2GRAY);
        cv.rectangle(dst, {x:0,y:0}, {x:100,y:100}, [255,0,0,1], 1);
        cv.imshow("canvasOutput", dst);

        let delay = 1000 / FPS - (Date.now() - begin);
        setTimeout(processVideo, delay);
    }

    setTimeout(processVideo, 0);
}
