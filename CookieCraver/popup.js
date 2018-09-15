let info = document.getElementById('info');
let score = document.getElementById('score');

chrome.storage.sync.get('sessionUser', (val) => {
  const { sessionUser } = val;
  info.innerHTML = `<img src=${sessionUser.picture} class="avatar" /> ${sessionUser.name}'s cookies`;
});
chrome.storage.sync.get('count', (val) => {
  const { count } = val;
  count
    .toString()
    .split('')
    .forEach(digit => score.innerHTML += `<span>${digit}</span>`);
});
