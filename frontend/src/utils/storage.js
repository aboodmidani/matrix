const STORAGE_KEY = 'ms-url-history'

export function getUrlHistory() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : []
  } catch { return [] }
}

export function addUrlHistory(url) {
  const history = getUrlHistory().filter(h => h !== url)
  history.unshift(url)
  localStorage.setItem(STORAGE_KEY, JSON.stringify(history.slice(0, 10)))
}
