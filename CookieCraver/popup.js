let info = document.getElementById('info');
let score = document.getElementById('score');

// fetch('USERS_ENDPOINT').then((user) => {
// info.innerText = `${user.name ? `${user.name}:` : ''} ${user.score || 0}`;
chrome.storage.sync.get('sessionUser', (val) => {
  const { sessionUser } = val;
  info.innerHTML = '<img src="' + `${sessionUser.picture}` +'" class="avatar" />' + `${sessionUser.name}` + "'s cookies";
});
chrome.storage.sync.get('count', (val) => {
  const { count } = val;
  count
    .toString()
    .split('')
    .forEach(digit => score.innerHTML += `<span>${digit}</span>`);
});

// });
