'use strict';

var map = L.map('map').setView([51.505, -0.09], 4);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 4, minZoom: 4,
  attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

async function gameStart() {
  const playerName = 'Testing';
  let playerCurrentLocation = '';
  let endPoint = '';
  const startPos = document.getElementById('StartPos');
  const endPos = document.getElementById('EndPos');
  try {
    const response = await fetch(
        `http://127.0.0.1:3000/gameStart/${playerName}`);
    const data = await response.json();
    playerCurrentLocation = data[2]['Icao'];
    endPoint = data[1]['Icao'];

    function gameStartPos(data) {
      const startLocation = document.createElement('li');
      startLocation.textContent = 'Name: ' + data[0]['Name'];
      const icao = document.createElement('li');
      icao.setAttribute('id', 'ICAO');
      icao.textContent = 'Icao: ' + data[0]['Icao'];
      startPos.append(startLocation);
      startPos.append(icao);
    }

    gameStartPos(data);

    function gameEndPos(data) {
      const startLocation = document.createElement('li');
      const endLocation = document.createElement('li');
      startLocation.textContent = 'Name: ' + data[1]['Name'];
      endLocation.textContent = 'Icao: ' + data[1]['Icao'];
      endPos.append(startLocation);
      endPos.append(endLocation);
    }

    gameEndPos(data);

  } catch (error) {
    console.log(error.message);
  }
  try {
    const response = await fetch(`http://127.0.0.1:3000/mapDrawer/`);
    const data = await response.json();
    const r = await fetch(`http://127.0.0.1:3000/connections/${playerCurrentLocation}`)
    const connections = await r.json();
    let conn = []
    connections.forEach(a=> {

      conn.push(a[0])
    })
    console.log(conn)
    data.forEach(i => {
      console.log(i.Icao)
      if (i.Icao === playerCurrentLocation){
        const marker = L.circle([i.Lat, i.Long], {
          color: 'green',
          fillColor: 'green',
          fillOpacity: 1,
          radius: 25000,
        }).addTo(map);
      } //End of first if statement
      else if (conn.includes(i.Icao)) {
        const marker = L.circle([i.Lat, i.Long], {
          color: 'yellow',
          fillColor: 'yellow',
          fillOpacity: 1,
          radius: 25000,
        }).addTo(map);
      }
      else if (i.Icao === endPoint) {
        const marker = L.circle([i.Lat, i.Long], {
          color: 'red',
          fillColor: 'red',
          fillOpacity: 1,
          radius: 25000,
        }).addTo(map);
      }
      else {
        const marker = L.circle([i.Lat, i.Long], {
          color: 'blue',
          fillColor: 'blue',
          fillOpacity: 1,
          radius: 25000,
        }).addTo(map);
      }


    });
    console.log(data);
  } catch (error) {
    console.log(error.message);
  }
} //This is the end of the function don't fuck with it

gameStart();