export const cookies = Object.fromEntries(document.cookie.split('; ').map(x => x.split('=')));

export const fl_host = (process.env.REACT_APP_CUSTOM_PORT) ?
  `http://127.0.0.1:${process.env.REACT_APP_CUSTOM_PORT}` :
  window.origin;


export const AdTypes = {
  "": {display: "Any", payload: null},
  Selling: {display: "Selling", payload: "Selling"},
  Buying: {display: "Buying", payload: "Buying"},
  Trading: {display: "Trading", payload: "Trading"},
  Artisan: {display: "Artisan", payload: "Artisan"},
  Bulk: {display: "Bulk", payload: "Bulk"},
}

