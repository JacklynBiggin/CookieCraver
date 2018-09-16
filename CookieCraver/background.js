const USER_KEY = 'sessionUser';
const USER_URL = 'https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token=';
const DEBOUNCE_TIME = 300;
const API_URL = 'http://cookiecraver.eastus.cloudapp.azure.com';

chrome.runtime.onInstalled.addListener(() => {
  chrome.declarativeContent.onPageChanged.removeRules(undefined, () => {
    chrome.declarativeContent.onPageChanged.addRules([{
      conditions: [new chrome.declarativeContent.PageStateMatcher({
      })
      ],
      actions: [new chrome.declarativeContent.ShowPageAction()]
    }]);
  });
});

const initListeners = () => {
  let timeOutID;
  chrome.cookies.getAll({}, (cookies) => {
    chrome.storage.sync.set({ count: cookies.length });
  });
  chrome.cookies.onChanged.addListener(() => {
    window.clearTimeout(timeOutID);
    timeOutID = window.setTimeout(() => chrome.cookies.getAll({}, (cookies) => {
      const keys = {};
      cookies.forEach((c) => keys[c.domain] = keys[c.domain] ? keys[c.domain] + 1 : 1);
      let max = ['', 0];
      Object.entries(keys).forEach((kvp) => {
        if (kvp[1] > max[1]) {
          max = kvp;
        }
      });
      chrome.storage.sync.set({ commonDomain: max[0] }, () =>
        chrome.storage.sync.set({ count: cookies.length },
          () => chrome.storage.sync.get([USER_KEY], (val) => {
            const { sessionUser } = val;
            fetch(`${API_URL}/user/update`, {
              method: 'PUT',
              headers: {
                'Content-Type': 'application/json',
              },
              mode: 'cors',
              cache: 'default',
              body: JSON.stringify({
                uid: sessionUser.uid,
                new: cookies.length,
              }),
            });
          })));
    }), DEBOUNCE_TIME);
  });
}

chrome.identity.getAuthToken({
  interactive: true
}, (token) => {
  if (chrome.runtime.lastError) {
    alert(chrome.runtime.lastError.message);
    return;
  }
  const x = new XMLHttpRequest();
  x.open('GET', `${USER_URL}${token}`);
  x.onload = () => {
    const response = JSON.parse(x.response);
    const user = {
      uid: response.id,
      fname: response.given_name,
      sname: response.family_name,
      pic: response.picture,
    };
    fetch(`${API_URL}/user/cookies?uid=${user.uid}`)
      .then((r) => {
        if (!r.ok && r.status === 400) {
          throw new Error(r.statusText);
        }
        return r;
      })
      .then(() => {
        chrome.storage.sync.set({
          [USER_KEY]: user,
        }, () => initListeners());
      })
      .catch(() => {
        fetch(`${API_URL}/user`, {
          method: 'POST',
          body: JSON.stringify(user),
          headers: new Headers({ 'Content-Type': 'application/json' }),
        }).then(() => {
          chrome.storage.sync.set({ [USER_KEY]: user }, () => initListeners());
        })
      });
  };
  x.send();
});
