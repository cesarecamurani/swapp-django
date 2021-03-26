document.addEventListener('DOMContentLoaded', function() {
    let messages = document.querySelector('.messages')
    let forms_container = document.querySelector('.forms-container')
    let body_internal = document.querySelector('.body-internal')

    if (messages && messages.children && messages.children.length !== 0) {
        if (forms_container) {
            forms_container.style.marginTop = '10px';
        }
        if (body_internal) {
            body_internal.style.marginTop = '0px';
        }
    }

    displayClock()
})

function displayClock(){
    let date = new Date();
    let hours = date.getHours();
    let minutes = date.getMinutes();

    hours = (hours < 10) ? '0' + hours : hours;
    minutes = (minutes < 10) ? '0' + minutes : minutes;

    let time = hours + ':' + minutes;

    document.getElementById('clock-display').innerText = time;
    document.getElementById('clock-display').textContent = time;

    setTimeout(displayClock, 1000);
}
