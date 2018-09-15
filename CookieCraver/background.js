const USER_KEY = 'sessionUser';

chrome.runtime.onInstalled.addListener(() => {
  chrome.declarativeContent.onPageChanged.removeRules(undefined, () => {
    chrome.declarativeContent.onPageChanged.addRules([{
      conditions: [new chrome.declarativeContent.PageStateMatcher({
      })
      ],
      actions: [new chrome.declarativeContent.ShowPageAction()]
    }]);
  });

  chrome.identity.getAuthToken({
    interactive: true
  }, (token) => {
    if (chrome.runtime.lastError) {
      alert(chrome.runtime.lastError.message);
      return;
    }
    var x = new XMLHttpRequest();
    x.open('GET', `https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token=${token}`);
    x.onload = () => {
      chrome.storage.sync.set({ [USER_KEY]: JSON.parse(x.response) });
    };
    x.send();
  });

  let collected = 0;
  chrome.cookies.onChanged.addListener((info) => {
    const {
      cause,
      cookie,
      removed
    } = info;
    if (cause === 'explicit' && !removed) {
      chrome.storage.sync.set({ sessionCount: collected += 1 });
    }
  });

});