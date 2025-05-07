'use strict';
// Populating the top5Games table
async function top5Games() {
  try {
    const gamesList = document.getElementById('topGames');
    const response = await fetch('http://127.0.0.1:3000/topFiveGames/');
    const data = await response.json();
    data.forEach(i => {
      const t = document.createElement('tr');
      const td1 = document.createElement('td');
      const td2 = document.createElement('td');
      td1.textContent = i.Player;
      td2.textContent = i.Points;
      t.appendChild(td1);
      t.appendChild(td2);
      gamesList.appendChild(t);
    });
  } catch (error) {
    console.log(error);
  }
}

top5Games();
//Creating players name to local storage
const subButton = document.getElementById('submit');
subButton.addEventListener('click', function(evt) {
  evt.preventDefault();
  const playerName = document.getElementById('pName').value;
  // Just to check that the player actually inputs a name as to prevent empty names
  if (playerName === '') {
    alert('Enter a name');
  //   Once name is successfully given create it in localstorage and open the main game page
  } else {
    localStorage.setItem('PlayerName', playerName);
    window.location.href = 'mainpage.html';
  }

});
