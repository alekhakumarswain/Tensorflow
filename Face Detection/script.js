// Select video and canvas elements
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');

// Define square bracket dimensions
const bracketX = 160;  // Starting X coordinate
const bracketY = 120;  // Starting Y coordinate
const bracketWidth = 320;
const bracketHeight = 240;

// Load the camera feed
async function setupCamera() {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;

    return new Promise((resolve) => {
        video.onloadedmetadata = () => {
            resolve(video);
        };
    });
}

// Load the BlazeFace model and start detection
async function loadAndPredict() {
    const model = await blazeface.load();

    async function detect() {
        const predictions = await model.estimateFaces(video, false);

        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        drawBracket();

        if (predictions.length > 0) {
            predictions.forEach(prediction => {
                const start = prediction.topLeft;
                const end = prediction.bottomRight;

                const x = start[0];
                const y = start[1];
                const width = end[0] - start[0];
                const height = end[1] - start[1];

                const isInside = checkFaceInBracket(x, y, width, height);

                // Draw face bounding box
                context.beginPath();
                context.rect(x, y, width, height);
                context.lineWidth = isInside ? 3 : 1;
                context.strokeStyle = isInside ? 'green' : 'red';
                context.stroke();
            });
        }

        requestAnimationFrame(detect);
    }

    detect();
}

// Draw a square bracket on the canvas
function drawBracket() {
    context.beginPath();
    context.rect(bracketX, bracketY, bracketWidth, bracketHeight);
    context.lineWidth = 2;
    context.strokeStyle = 'blue';
    context.stroke();
}

// Check if the face is within the square bracket
function checkFaceInBracket(x, y, width, height) {
    return x >= bracketX && y >= bracketY && (x + width) <= (bracketX + bracketWidth) && (y + height) <= (bracketY + bracketHeight);
}

// Initialize the application
async function init() {
    await setupCamera();
    video.play();
    loadAndPredict();
}

init();
