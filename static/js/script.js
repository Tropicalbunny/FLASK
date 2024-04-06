
/**sends the value of the specific button pressed */
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
fetch('/updateimage')
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
fetch('/isGameOver')
    .then(response => response.json())
    .then(data => {
        console.log(data)
        if (data == 1) {
            window.location.href = '/fail'
    } else if (data == 2){
        window.location.href = '/pass'
    }
})
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
        console.log(element);
    });
});
/**function used to transition to game page */
function goToGameboard() {
    window.location.href = '/gameboard';
}

/** event listener to allow for get elements to work correctly */
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

