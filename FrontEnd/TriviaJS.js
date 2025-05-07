'use strict';

async function top5Games() {
  try {
    const gamesList = document.getElementById('topGames');
    const response = await fetch('http://127.0.0.1:3000/topFiveGames/');
    const data = await response.json();
    data.forEach(i=>{
      const t = document.createElement('tr');
      const td1 = document.createElement('td')
      const td2 = document.createElement('td')
      td1.textContent = i.Player;
      td2.textContent = i.Points;
      t.appendChild(td1);
      t.appendChild(td2);
      gamesList.appendChild(t);
    })
  } catch (error) {
    console.log(error);
  }
}
async function form(){

}
top5Games()