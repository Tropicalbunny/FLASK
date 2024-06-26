
/**sends the value of the specific button pressed part one, to handle the holding of the form. and when to send it*/
function sendValueEvent(event) {
    event.preventDefault();
    let buttonValue = event.target.value;
    sendValue(buttonValue).then(response => {
        if (response === 'success') {
            event.target.form.submit();
        } else {
            console.log('sendValue did not return success');
        }
    }).catch(error => {
        console.error('Error:', error);
    });
}


/** sends the value of the specific button pressed part two, sending response to python and wait for a return, if success then sends that to the 1st funtion*/
function sendValue(buttonValue) {
    return fetch('/button', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ value: buttonValue }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            return 'success';
        }else {
            console.error('Error processing guess:', data);
            throw new Error('Error processing guess');
        }
    })
}


fetch('/updateimage')
    .then(response => response.json())
    .then(data => {
        if (data == 6) {
            document.getElementById('hangman-image-inner').src = "/static/images/hang2.png";
    } else if (data == 5){
        document.getElementById('hangman-image-inner').src = "/static/images/hang3.png";
    } else if (data == 4){
        document.getElementById('hangman-image-inner').src = "/static/images/hang4.png";
    } else if (data == 3){
        document.getElementById('hangman-image-inner').src = "/static/images/hang5.png";
    } else if (data == 2){
        document.getElementById('hangman-image-inner').src = "/static/images/hang6.png";
    } else if (data == 1){
        document.getElementById('hangman-image-inner').src = "/static/images/hang7.png";
    } else if (data == 0){
        document.getElementById('hangman-image-inner').src = "/static/images/hang8.png";
    } else {
        document.getElementById('hangman-image-inner').src = "/static/images/hang1.png";
    }
});


fetch('/isGameOver')
    .then(response => response.json())
    .then(data => {
        if (data == 1) {
            window.location.href = '/fail';
    } else if (data == 2){
        window.location.href = '/pass';
    }
});


/** function to remove buttons after they are pressed */
function hideButton(buttonId) {
        var button = document.getElementById(buttonId);
        button.style.display = 'none'; 
    }
fetch('/updateButtons')
    .then(response => response.json())
    .then(data => {
    
    let buttonsArray = data.split('');

    buttonsArray.forEach(element => {
        hideButton(element);
    });
});


/** event listener to allow for get elements to work correctly */
document.addEventListener("DOMContentLoaded", (event) => {
    let infoOpen = document.getElementById('info-open');
    let infoContainer = document.getElementById('info-container');
    let infoClose = document.getElementById('info-close');
    infoOpen.addEventListener('click', function(){
        infoContainer.style.display = 'block';
    });
    
    infoClose.addEventListener('click', function(){
        infoContainer.style.display = 'none';
        
    });
    
});
