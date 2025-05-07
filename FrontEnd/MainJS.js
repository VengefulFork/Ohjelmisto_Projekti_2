'use strict';

var map = L.map('map').setView([51.505, -0.09], 4);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 4, minZoom: 4,
  attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

async function mainProgram() {
  const playerName = localStorage.getItem('PlayerName')
  gameStart(playerName).then(i => {
    mapCreator();
    gameStatusUpdater();
    plane();

  });
  const planeChange = document.getElementById('change');
  planeChange.addEventListener('click', function() {
    planeSwitcher().then(i => {
      map.closePopup();
      if (i === 'Dash 8 Q400') {
        planeChange.textContent = 'Change plane to Boeing 737';
      } else {
        planeChange.textContent = 'Change plane to Dash 8 Q400';
      }
      plane();
    });
  });
}

async function gameStart(playerName) {
  // const playerName = 'Testing';
  const startPos = document.getElementById('StartPos');
  const endPos = document.getElementById('EndPos');
  try {
    const response = await fetch(
        `http://127.0.0.1:3000/gameStart/${playerName}`);
    const data = await response.json();
    console.log(data[2]);

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

} //End of function hands off

async function mapCreator() {
  try {
    const response = await fetch('http://127.0.0.1:3000/status/');
    const data = await response.json();
    //console.log(data)
    var playerCurrentLocation = data['Icao'];
    var endPoint = data['IcaoEnd'];
  } catch (error) {
    console.log(error.message);
  }
  try {
    const response = await fetch(`http://127.0.0.1:3000/mapDrawer/`);
    const data = await response.json();
    const r = await fetch(
        `http://127.0.0.1:3000/connections/${playerCurrentLocation}`);
    const connections = await r.json();
    let conn = [];
    connections.forEach(a => {
      conn.push(a[0]);
    });
    //console.log(conn);
    data.forEach(i => {
      //console.log(i.Icao);
      if (i.Icao === playerCurrentLocation) {
        const marker = L.circle([i.Lat, i.Long], {
          color: 'green',
          fillColor: 'green',
          fillOpacity: 1,
          radius: 25000,
        }).addTo(map);
        marker.bindPopup('You are here');
      } //End of first if statement
      else if (conn.includes(i.Icao) && i.Icao !== endPoint) {
        const marker = L.circle([i.Lat, i.Long], {
          color: 'yellow',
          fillColor: 'yellow',
          fillOpacity: 1,
          radius: 25000,
        }).addTo(map);
        const popupDiv = document.createElement('div');
        popupDiv.setAttribute('id', i.Icao);
        const h4 = document.createElement('h4');
        h4.textContent = 'You could fly here';
        popupDiv.appendChild(h4);
        const flyButton = document.createElement('button');
        flyButton.setAttribute('id', i.Icao);
        flyButton.type = 'button';
        flyButton.textContent = 'Fly here';
        const km = document.createElement('li');
        km.textContent = '';
        const flightInfo = document.createElement('ul');
        const time = document.createElement('li');
        const co2 = document.createElement('li');
        flightInfo.innerHTML = 'Info for flight with current plane';
        flightInfo.appendChild(time);
        flightInfo.appendChild(co2);

        popupDiv.appendChild(km);
        popupDiv.appendChild(flightInfo);
        popupDiv.appendChild(flyButton);
        marker.bindPopup(popupDiv);
        marker.on('click', onClick);

        function onClick() {
          const b = this._popup.getContent();
          const icao = b.id;
          distance(icao).then(i => {
            km.textContent = 'Distance ' + i['Distance'] + ' KM';
            co2.textContent = i['Co2'] + 'kg Co2 produced';
            time.textContent = i['Time'] + ' min';
          });
        }

        flyButton.addEventListener('click', function() {
          const icao = this.id;
          flying(icao).then(i => {
            mapCreator();
            gameStatusUpdater();
            marker.closePopup();

          });

        });

      } else if (i.Icao === endPoint && !conn.includes(i.Icao)) {
        const marker = L.circle([i.Lat, i.Long], {
          color: 'red',
          fillColor: 'red',
          fillOpacity: 1,
          radius: 25000,
        }).addTo(map);
      } else if (i.Icao === endPoint && conn.includes(i.Icao)) {
        const marker = L.circle([i.Lat, i.Long], {
          color: 'purple',
          fillColor: 'purple',
          fillOpacity: 1,
          radius: 25000,
        }).addTo(map);
        const popupDiv = document.createElement('div');
        popupDiv.setAttribute('id', i.Icao);
        const h4 = document.createElement('h4');
        h4.textContent = 'Fly here to win';
        popupDiv.appendChild(h4);
        const flyButton = document.createElement('button');
        flyButton.setAttribute('id', i.Icao);
        flyButton.type = 'button';
        flyButton.textContent = 'Fly here';
        const km = document.createElement('li');
        km.textContent = '';
        const flightInfo = document.createElement('ul');
        const time = document.createElement('li');
        const co2 = document.createElement('li');
        flightInfo.innerHTML = 'Info for flight with current plane';
        flightInfo.appendChild(time);
        flightInfo.appendChild(co2);

        popupDiv.appendChild(km);
        popupDiv.appendChild(flightInfo);
        popupDiv.appendChild(flyButton);
        marker.bindPopup(popupDiv);
        marker.on('click', onClick);

        function onClick() {
          const b = this._popup.getContent();
          const icao = b.id;
          distance(icao).then(i => {
            km.textContent = 'Distance ' + i['Distance'] + ' KM';
            co2.textContent = i['Co2'] + 'kg Co2 produced';
            time.textContent = i['Time'] + ' min';
          });
        }

        flyButton.addEventListener('click', function() {
          const icao = this.id;
          flying(icao).then(i => {
            mapCreator();
            gameStatusUpdater();
            marker.closePopup();

          });

        });
      } else {
        const marker = L.circle([i.Lat, i.Long], {
          color: 'blue',
          fillColor: 'blue',
          fillOpacity: 1,
          radius: 25000,
        }).addTo(map);
      }

    });
    //console.log(data);
  } catch (error) {
    console.log(error.message);
  }
  console.log(playerCurrentLocation);
} //mapCreator end hands off
// Calling flask for all the flying functionality
async function flying(icao) {
  const response = await fetch(`http://127.0.0.1:3000/flying/${icao}`);
  const data = await response.json();
  console.log(data);
} //End of function hands off
async function distance(icao) {
  let flight_data = '';
  try {
    const response = await fetch(`http://127.0.0.1:3000/distance/${icao}`);
    flight_data = await response.json();
    // console.log(flight_data);
  } catch (error) {
    console.log(error.message);
  }
  return flight_data;
}// End of function hands off
// Mostly for updating all the html elements that contain data for the current game
async function gameStatusUpdater() {

  try {
    const response = await fetch('http://127.0.0.1:3000/status/');
    const data = await response.json();
    const co2 = document.getElementById('Co2');
    co2.textContent = data['Co2'] + 'kg CO2';

    const km = document.getElementById('TotDist');
    km.textContent = data['Km'] + ' km';

    const time = document.getElementById('Time');
    time.textContent = data['Time'] + ' Mins';
    // If gameStatus is won then we load the victory screen
    if (data['GameStatus'] === 'WON') {
      // For reasons unknown this specific file refuses to load unless its this specific route
      window.location.href='http://localhost:63342/Ohjelmisto_Projekti_2/FrontEnd/victory.html';
    }
  } catch (error) {
    console.log(error.message);
  }
}//End of function hands off
// Function for populating the info for players current plane
async function plane() {
  try {
    const response = await fetch('http://127.0.0.1:3000/status/');
    const data = await response.json();
    const name = document.getElementById('PlaneName');
    const speed = document.getElementById('Speed');
    const co2PerKm = document.getElementById('Co2km');
    name.innerHTML = 'Name : ' + data['Plane']['malli'];
    speed.innerHTML = 'Speed of plane is : ' + data['Plane']['max_nopeus_kmh'] +
        ' kmh';
    co2PerKm.innerHTML = 'Co2 produced per km is around : ' +
        data['Plane']['hiilidioksidi_per_km'] + ' kg';
    console.log(data);
  } catch (error) {
    console.log(error);
  }

}//End of function hands off
//Function for calling the FLASK that switches players plane
async function planeSwitcher() {
  let newPlane = '';
  try {
    const response = await fetch('http://127.0.0.1:3000/plane/');
    const data = await response.json();
    newPlane = data['New Plane']['malli'];
    console.log(newPlane);
  } catch (error) {
    console.log(error);
  }
  return newPlane;
}

mainProgram();
