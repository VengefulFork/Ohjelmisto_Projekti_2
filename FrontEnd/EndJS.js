'use strict';

async function gameEnd() {
  try {
    const response = await fetch('http://127.0.0.1:3000/status/');
    const data = await response.json();
    const victoryData = document.getElementById('victory');
    console.log(data);
    // Monstrosity below is for populating the game data table displayed after winning
    const t = document.createElement('tr');
    const tdName = document.createElement('td');
    const tdPoints = document.createElement('td');
    const tdStart = document.createElement('td');
    const tdGoal = document.createElement('td');
    const tdCo2 = document.createElement('td');
    const tdTime = document.createElement('td');
    const tdDistance = document.createElement('td');
    tdName.textContent = data['Name'];
    tdPoints.textContent = data['Points'];
    tdStart.textContent = data['Start'][0];
    tdGoal.textContent = data['End'][0];
    tdCo2.textContent = data['Co2'] + " kg";
    tdTime.textContent = data['Time']+ " min";
    tdDistance.textContent = data['Km'] + " km";
    t.appendChild(tdName);
    t.appendChild(tdStart);
    t.appendChild(tdGoal);
    t.appendChild(tdCo2);
    t.appendChild(tdTime);
    t.appendChild(tdDistance);
    t.appendChild(tdPoints);
    victoryData.appendChild(t);

  } catch (error) {
    console.log(error);
  }
}

gameEnd();