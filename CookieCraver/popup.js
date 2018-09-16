let info = document.getElementById('info');
let score = document.getElementById('score');
let commonDomain = document.getElementById('common-domain');

chrome.storage.sync.get('sessionUser', (val) => {
  const { sessionUser } = val;
  info.innerHTML = `<img src=${sessionUser.pic} class="avatar" /> ${sessionUser.fname}'s cookies`;
});
chrome.storage.sync.get('count', (val) => {
  const { count } = val;
  count
    .toString()
    .split('')
    .forEach(digit => score.innerHTML += `<span>${digit}</span>`);
});
chrome.storage.sync.get('commonDomain', (val) => {
  if (val && val.commonDomain) {
    commonDomain.innerHTML = `Most common Cookie Giver: ${val.commonDomain}`;
  }
});
