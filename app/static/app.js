let width = 320;
let height = 0;
let streaming = false;

const videoHtml = document.getElementById('video');
const canvasHtml = document.getElementById('canvas');
const recButtonHtml = document.getElementById('send_button');

const alertHtml = document.getElementById('alert_err');
const imageHtml = document.getElementById('res_img');
const nameHtml = document.getElementById('res_name');
const cardHtml = document.getElementById('res_card');
const clearCardHtml = document.getElementById('clear_card');

navigator
    .mediaDevices
    .getUserMedia({ video: true, audio: false })
    .then(stream => {
        videoHtml.srcObject = stream;
        videoHtml.play();
    })
    .catch(err => console.log("An error occurred: " + err));

recButtonHtml.onclick = sendImage;
clearCardHtml.onclick = clear;

videoHtml.addEventListener('canplay', function (ev) {
    if (!streaming) {
        height = window.innerHeight / 2.7
        width = videoHtml.videoWidth / (videoHtml.videoHeight / height)

        // В Firefox в настоящее время есть ошибка, где высота не может быть прочитана из видео, 
        // так что мы будем делать предположения, если это произойдет.

        if (isNaN(height)) {
            height = width / (4 / 3);
        }

        videoHtml.setAttribute('width', width);
        videoHtml.setAttribute('height', height);
        canvasHtml.setAttribute('width', width);
        canvasHtml.setAttribute('height', height);

        recButtonHtml.style.width = width + 'px';
        cardHtml.style.width = width + 'px';
        streaming = true;
    }
}, false);

function clear() {
    if (!cardHtml.classList.contains('d-none'))
        cardHtml.classList.add('d-none')

    if (!alertHtml.classList.contains('d-none'))
        alertHtml.classList.add('d-none')
}

async function getImagAsBlob() {
    canvasHtml
        .getContext('2d')
        .drawImage(videoHtml, 0, 0, width, height);

    return await new Promise(resolve => canvasHtml.toBlob(resolve, 'image/jpeg'));
}

async function sendImage() {
    clear();
    const imageBlob = await getImagAsBlob();

    let formData = new FormData();
    formData.append("file", imageBlob, "image.jpeg");

    let response = await fetch('/recognize', {
        method: 'POST',
        body: formData
    });

    let result = await response.json();
    if (result.success) {
        imageHtml.src = canvasHtml.toDataURL("image/jpeg");
        nameHtml.innerText = result.result;

        cardHtml.classList.remove('d-none')
    } else {
        alertHtml.classList.remove('d-none')
    }
}