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

async function gameLoading() {
  try {
    const response = await fetch('http://127.0.0.1:3000/savedGames/');
    const data = await response.json();
    const gamesTable = document.getElementById('savedGames');
    data.forEach(i => {
      const t = document.createElement('tr');
      const id = document.createElement('td');
      const playerName = document.createElement('td');
      const load = document.createElement('button');
      id.textContent = i.Id;
      playerName.textContent = i.Player;
      load.textContent = 'Lataa';
      load.setAttribute('id', i.Id);
      t.appendChild(id);
      t.appendChild(playerName);
      t.appendChild(load);
      gamesTable.appendChild(t);
      // This is a bad solution because if something gets deleted from the database it loads the wrong row or wont load at all
      // For demo purposes it does work
      load.addEventListener('click', function(evt) {
        const buttonId = this.id;
        const b = gamesTable.rows[buttonId].cells[1].textContent;
        console.log(b);
        gameLoader(buttonId, b);
      });
    });
  } catch (error) {
    console.log(error);
  }
}

async function gameLoader(buttonId, b) {
  try {
    const response = await fetch(
        `http://127.0.0.1:3000/loading/${buttonId}/${b}`);
    const data = await response.json();
    console.log(data)
    localStorage.setItem('FromLoading', "Yes")
    window.location.href = 'mainpage.html';
  } catch (error) {
    console.log(error);
  }
}

function playerNameSub() {
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
      localStorage.setItem('FromLoading', "No");
      window.location.href = 'mainpage.html';
    }
  });

}

function loadMenu() {
  const dialog = document.querySelector('dialog');
  const span = document.querySelector('span');
  const button = document.getElementById('loadMenu');
  button.addEventListener('click', function(evt) {
    gameLoading();
    dialog.showModal();
    span.addEventListener('click', function(evt) {
      dialog.close();
    });
  });
}

top5Games();
playerNameSub();
loadMenu();
//Creating players name to local storage
