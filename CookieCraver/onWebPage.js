const API_URL = 'http://cookiecraver.azurewebsites.net';
chrome.storage.sync.get('sessionUser', (val) => {
  const { sessionUser } = val;
  fetch(`${API_URL}/user/cookies?uid=${sessionUser.id}>`)
    .then(data => data.json())
    .then((data) => {
      const playerPic = document.getElementById('player-pic');
      const playerRank = document.getElementById('player-rank');
      const total = document.getElementById('total');
      const name = document.getElementById('name');
      const score = document.getElementById('score');
      playerPic.src = data.pic;
      playerRank.innerText = data.rank;
      total.innerText = data.total;
      name.innerText = `${data.fname} ${data.sname}`;
      score.innerHTML = data.score.toString().split('').map(digit => `<span>${digit}</span>`).join('');
    });
});
