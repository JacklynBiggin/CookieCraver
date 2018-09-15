let info = document.getElementById('info');

// fetch('USERS_ENDPOINT').then((user) => {
// info.innerText = `${user.name ? `${user.name}:` : ''} ${user.score || 0}`;
chrome.storage.sync.get('sessionUser', (val) => {
  console.log(val.sessionUser);
  const { sessionUser } = val;
  info.innerText = `${sessionUser.name}`;
});
// });
