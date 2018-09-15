let info = document.getElementById('info');
let score = document.getElementById('score');

// fetch('USERS_ENDPOINT').then((user) => {
// info.innerText = `${user.name ? `${user.name}:` : ''} ${user.score || 0}`;
chrome.storage.sync.get('sessionUser', (val) => {
  const { sessionUser } = val;
  info.innerText = `${sessionUser.name}`;
});
chrome.storage.sync.get('sessionCount', (val) => {
  score.innerText = val.sessionCount;
});

// });
