import { debounce } from 'lodash'

export function asyncDebounce(func, wait) {
  const debounced = debounce((resolve, reject, args) => {
    func(...args).then(resolve).catch(reject);
  }, wait);
  return (...args) =>
  new Promise((resolve, reject) => {
    debounced(resolve, reject, args);
  });
}
