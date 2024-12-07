(function() {

  //Ширина и высота снимка. Мы установим ширину на значение, 
  //но высота будет вычисляться на основе отношения потока.

  var width = 320;    // Мы будем масштабировать ширину фотографии до этого.
  var height = 0;     // Это будет вычисляться на основе входящего потока

  //|streaming| указывает, передаём ли мы видео из камеры. Очевидно, что мы начинаем с false.

  var streaming = false;

  //Различные элементы HTML, которые нам нужно настроить или контролировать.
  // Они будут установлены функцией startup().

  var video = null;
  var canvas = null;
  var photo = null;
  var startbutton = null;

  function startup() {
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    photo = document.getElementById('photo');
    startbutton = document.getElementById('startbutton');

    navigator.mediaDevices.getUserMedia({video: true, audio: false})
    .then(function(stream) {
      video.srcObject = stream;
      video.play();
    })
    .catch(function(err) {
      console.log("An error occurred: " + err);
    });

    video.addEventListener('canplay', function(ev){
      if (!streaming) {
        height = video.videoHeight / (video.videoWidth/width);
      
        // В Firefox в настоящее время есть ошибка, где высота не может быть прочитана из видео, 
        // так что мы будем делать предположения, если это произойдет.
      
        if (isNaN(height)) {
          height = width / (4/3);
        }
      
        video.setAttribute('width', width);
        video.setAttribute('height', height);
        canvas.setAttribute('width', width);
        canvas.setAttribute('height', height);
        streaming = true;
      }
    }, false);

    startbutton.addEventListener('click', function(ev){
      takepicture();
      ev.preventDefault();
    }, false);
    
    
    clearphoto();
  }

  // Заполнить фотографию с указанием того, что ни одного снимка не было сделано.

  function clearphoto() {
    var context = canvas.getContext('2d');
    context.fillStyle = "#AAA";
    context.fillRect(0, 0, canvas.width, canvas.height);

    var data = canvas.toDataURL('image/png');
    photo.setAttribute('src', data);
  }
  
  // Захватите фотографию, заберя текущее содержимое видео и нарисуя его на canvas, 
  // а затем преобразуя его в URL данных в формате PNG.
  // Рисуя его на оффшорном canvas и затем рисуя его на экран,
  // мы можем изменить его размер и/или применить другие изменения перед тем как нарисовать его.

  function takepicture() {
    var context = canvas.getContext('2d');
    if (width && height) {
      canvas.width = width;
      canvas.height = height;
      context.drawImage(video, 0, 0, width, height);
    
      var data = canvas.toDataURL('image/png');
      photo.setAttribute('src', data);
    } else {
      clearphoto();
    }
  }

  // Настроить event Listener для запуска процесса старта после завершения загрузки.
 window.addEventListener('load', startup, false);

 function uploadImage() {
  const imageFile = document.getElementById('imageInput').files[0]; // Получаем выбранный файл

  const formData = new FormData();
  formData.append('image', imageFile); // Добавляем файл в FormData

  fetch('https://httpbin.org/#/', { // Замените на ваш URL
      method: 'POST',
      body: formData // Отправляем FormData
  })
  .then(response => {
      if (!response.ok) {
          throw new Error('Ошибка сети');
      }
      return response.json(); // Обрабатываем ответ
  })
  .then(data => console.log('Успех:', data)) // Успешный ответ
  .catch(error => console.error('Ошибка:', error));
}

})();
