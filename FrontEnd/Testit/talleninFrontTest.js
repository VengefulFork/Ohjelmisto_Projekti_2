'use strict';

const searchForm = document.getElementById('target');
const list = document.getElementById('list');

searchForm.addEventListener('submit', async function(evt) {
  evt.preventDefault();
  const searchParam = document.querySelector('input[name=name]').value;
  try {
    const response = await fetch(`http://127.0.0.1:3000/lataus/${searchParam}`);
    const jsonData = await response.json();
    console.log(jsonData);

    Object.keys(jsonData).forEach(key => {
      const value = jsonData[key];
      console.log(`${key}: ${value}`);
      const a = document.createElement('li')
      a.textContent = (`${key}: ${value}`)
      list.appendChild(a)
    })

  } catch (error) {
    console.log(error.message);
  }
});