var popup = document.getElementById('simpleModal');
var modalBtn = document.getElementById('modalBtn');
var modalBtn1 = document.getElementById('modalBtn1');

var closeBtn = document.getElementsByClassName('closeBtn')[0];
var closeBtn1 = document.getElementsByClassName('welcome__button')[0];



modalBtn.addEventListener('click', OpenWindow);

modalBtn1.addEventListener('click', OpenWindow);

closeBtn.addEventListener('click', CloseWindow);

closeBtn1.addEventListener('click', CloseWindow);

window.addEventListener('click', outsideClick);

function OpenWindow() {
    popup.style.transform = 'scale(1)';
    //overlay.classList.add('active');
}

function CloseWindow() {
    popup.style.transform = 'scale(0)';
    //overlay.classList.remove('active');
}

function SaveWindow() {
    popup.style.transform = 'scale(0)';
}


function outsideClick(e) {
    if (e.target == popup) {
        popup.style.transform = 'scale(0)';
    }
}