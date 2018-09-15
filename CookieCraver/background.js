const USER_KEY = 'sessionUser';
const USER_URL = 'https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token=';
const DEBOUNCE_TIME = 1000;

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
    const x = new XMLHttpRequest();
    x.open('GET', `${USER_URL}${token}`);
    x.onload = () => {
      chrome.storage.sync.set({ [USER_KEY]: JSON.parse(x.response) });
    };
    x.send();
  });

  chrome.storage.sync.set({
    [USER_KEY]: {
      email: "emailegmail.com",
      family_name: "user",
      gender: "",
      given_name: "test",
      id: "1234",
      link: "https://plus.google.com/1234",
      name: "Test User",
      picture: "https://lh3.googleusercontent.com/-XdUIqdMkCWA/AAAAAAAAAAI/AAAAAAAAAAA/4252rscbv5M/photo.jpg",
      verified_email: true,
    }
  });


  let timeOutID;
  chrome.storage.sync.set({ sessionCount: 0 });
  chrome.cookies.getAll({}, (cookies) => {
    allCookies = cookies;
  });
  chrome.cookies.onChanged.addListener((info) => {
    const {
      cause,
      cookie,
      removed
    } = info;
    window.clearTimeout(timeOutID)
    timeOutID = window.setTimeout(() => chrome.cookies.getAll({}, (cookies) => {
      console.log(cookies);
      chrome.storage.sync.set({ count: cookies.length });
    }), DEBOUNCE_TIME);

  });
});