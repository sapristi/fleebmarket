import { atom } from 'recoil';


const storeSearchInput = ({setSelf, onSet}) => {
  const key = "searchInput_0.1";
  const savedValue = localStorage.getItem(key);
  if (savedValue != null) {
    setSelf({...JSON.parse(savedValue), terms: ""});
  }

  onSet(newValue => {
    localStorage.setItem(key, JSON.stringify(newValue));
  });
};


export const searchInputState = atom({
  key: 'searchInput',
  default: {
    terms: "",
    ad_type: "Selling",
    region: ""
  },
  effects_UNSTABLE: [
    storeSearchInput
  ]
});

export const searchResultsState = atom({
  key: 'searchResults',
  default: []
});

export const scrolledBottomTriggerState = atom({
  key: 'scrolledBottomTrigger',
  default: false
});

export const resultsEndState = atom({
  key: 'resultsEnd',
  default: false
});

const storePrefs = ({setSelf, onSet}) => {
  const key = "UIPrefs_0.1";
  const savedValue = localStorage.getItem(key);
  if (savedValue != null) {
    setSelf(JSON.parse(savedValue));
  }

  onSet(newValue => {
    localStorage.setItem(key, JSON.stringify(newValue));
  });
}

export const uiPrefsState = atom({
  key: "UIPrefs",
  default: {
    showImages: true
  },
  effects_UNSTABLE: [
    storePrefs
  ]
});

export const selectedCardState = atom({
  key: "selectedCard",
  default: null
})
