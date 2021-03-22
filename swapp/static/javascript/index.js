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
})
