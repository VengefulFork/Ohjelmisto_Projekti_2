'use strict';

var map = L.map('map').setView([51.505, -0.09], 4);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 4, minZoom: 4,
  attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

async function fieldCreator() {
  let playerLocation = '';
  let endPoint = '';
  const startPos = document.getElementById('StartPos');
  const endPos = document.getElementById('EndPos');
  try {
    const response = await fetch(`http://127.0.0.1:3000/creator/`);
    const data = await response.json();
    playerLocation = data[0]['Icao'];
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
    const response = await fetch(`http://127.0.0.1:3000/search/`);
    const data = await response.json();
    console.log(typeof data);
    data.forEach(i => {
      if (i.Icao === playerLocation) {
        const marker = L.circle([i.Lat, i.Long], {
          color: 'green',
          fillColor: 'green',
          fillOpacity: 1,
          radius: 25000,

        }).addTo(map);
        const popupCont = document.createElement('div');
        const name = document.createElement('h4');
        popupCont.setAttribute('id', i.Icao);
        name.innerHTML = i.Name;
        popupCont.append(name);
        const uAreHere = document.createElement('h5');
        uAreHere.innerHTML = 'You are here';
        popupCont.append(uAreHere);
        const popupUl = document.createElement('ul');
        const icao = document.createElement('li');
        icao.textContent = 'ICAO: ' + i.Icao;
        const lat = document.createElement('li');
        lat.innerHTML = 'Lat: ' + i.Lat;
        const long = document.createElement('li');
        long.innerHTML = 'Long: ' + i.Long;
        popupUl.appendChild(icao);
        popupUl.appendChild(lat);
        popupUl.appendChild(long);
        popupCont.appendChild(popupUl);
        marker.bindPopup(popupCont);
        marker.on('click', onClick);

      } else if (i.Icao === endPoint) {
        const marker = L.circle([i.Lat, i.Long], {
          color: 'red',
          fillColor: 'red',
          fillOpacity: 1,
          radius: 25000,
        }).addTo(map);
        const popupCont = document.createElement('div');
        const name = document.createElement('h4');
        popupCont.setAttribute('id', i.Icao);
        name.innerHTML = i.Name;
        popupCont.append(name);
        const goal = document.createElement('h5');
        goal.innerHTML = 'This is your goal';
        popupCont.append(goal);
        const popupUl = document.createElement('ul');
        const icao = document.createElement('li');
        icao.textContent = 'ICAO: ' + i.Icao;
        const lat = document.createElement('li');
        lat.innerHTML = 'Lat: ' + i.Lat;
        const long = document.createElement('li');
        long.innerHTML = 'Long: ' + i.Long;
        popupUl.appendChild(icao);
        popupUl.appendChild(lat);
        popupUl.appendChild(long);
        popupCont.appendChild(popupUl);
        marker.bindPopup(popupCont);
        marker.on('click', onClick);
      } else {
        const marker = L.circle([i.Lat, i.Long], {
          color: 'blue',
          fillColor: 'blue',
          fillOpacity: 1,
          radius: 25000,
        }).addTo(map);
        const popupCont = document.createElement('div');
        const name = document.createElement('h4');
        popupCont.setAttribute('id', i.Icao);
        name.innerHTML = i.Name;
        popupCont.append(name);
        const popupUl = document.createElement('ul');
        const icao = document.createElement('li');
        icao.textContent = 'ICAO: ' + i.Icao;
        const lat = document.createElement('li');
        lat.innerHTML = 'Lat: ' + i.Lat;
        const long = document.createElement('li');
        long.innerHTML = 'Long: ' + i.Long;
        popupUl.appendChild(icao);
        popupUl.appendChild(lat);
        popupUl.appendChild(long);
        popupCont.appendChild(popupUl);
        marker.bindPopup(popupCont);
        marker.on('click', onClick);
      }
    });
  } catch (error) {
    console.log(error.message);
  }
  // let markers = document.querySelectorAll('.leaflet-interactive');
  // let id = 0;
  // for (let i of markers) {
  //   id++;
  //   i.setAttribute('id', id);
  // }
  //
  // console.log(markers);
  //
  // markers.forEach(i => {
  //   if (i.id === '2') {
  //     const a = i.getLatLng()
  //       console.log(a);
  //   }
  // });
  //
  // function onClick() {
  //   const a = this.options.color;
  //   const b = this._popup.getContent();
  //   const c = b.children;
  //   const e = document.getElementById(`${playerLocation}`);
  //   console.log(e)
  //   const d = this.getLatLng()
  //   console.log(a);
  //   console.log(d);
  //
  // }

}

fieldCreator();

// fieldCreator();

async function flying(toFlyIcao) {
  // await fieldCreator();
  let playerCurrentLocation = '';
  if (playerCurrentLocation === '') {
    playerCurrentLocation = document.getElementById('ICAO').innerText;
  }
  const a = playerCurrentLocation.split(':');
  playerCurrentLocation = a[1];
  const response = await fetch(
      `http://127.0.0.1:3000/flying/${playerCurrentLocation}/${toFlyIcao}`);
  const fields = await response.json();
  playerCurrentLocation = fields['Icao'];
  console.log(playerCurrentLocation);

}

function onClick() {
  const b = this._popup.getContent();
  const toFlyIcao = b.id;
  console.log(document.getElementById('EFKT'))
  // flying(toFlyIcao);
}