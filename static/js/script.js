

function sendValue(buttonValue) {
    fetch('/button', {
        method: 'POST',
        body: JSON.stringify({value: buttonValue}),
        headers: {
            'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(data => console.log(data));
}
fetch('/update-image')
    .then(response => response.json())
    .then(data => {
        if (data == 6) {
            document.getElementById('hangman-image-inner').src = "/static/images/hang2.png"
    } else if (data == 5){
        document.getElementById('hangman-image-inner').src = "/static/images/hang3.png"
    } else if (data == 4){
        document.getElementById('hangman-image-inner').src = "/static/images/hang4.png"
    } else if (data == 3){
        document.getElementById('hangman-image-inner').src = "/static/images/hang5.png"
    } else if (data == 2){
        document.getElementById('hangman-image-inner').src = "/static/images/hang6.png"
    } else if (data == 1){
        document.getElementById('hangman-image-inner').src = "/static/images/hang7.png"
    } else if (data == 0){
        document.getElementById('hangman-image-inner').src = "/static/images/hang8.png"
    } else {
        document.getElementById('hangman-image-inner').src = "/static/images/hang1.png" 
    }
});
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
        console.log(element);
    });
});


document.addEventListener("DOMContentLoaded", (event) => {
    let infoOpen = document.getElementById('info-open');
    let infoContainer = document.getElementById('info-container');
    let infoClose = document.getElementById('info-close');
    infoOpen.addEventListener('click', function(){
        infoContainer.style.display = 'block';
    })
    
    infoClose.addEventListener('click', function(){
        infoContainer.style.display = 'none';
    })
});

