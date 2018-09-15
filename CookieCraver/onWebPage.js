const API_URL = '';

chrome.storage.sync.get('sessionUser', (val) => {
  const { sessionUser } = val;
  fetch(`${API_URL}/user/cookies?uid=${sessionUser.id}>`)
    .then(data => data.json())
    .then((data) => {
      const el1 = document.getElementById();
    });
});
