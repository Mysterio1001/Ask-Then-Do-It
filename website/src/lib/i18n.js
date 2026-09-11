import { defaultLocale, locales } from '../data/i18n/index.js';

export { locales };

const STORAGE_KEY = 'ask-then-do-it.locale';
const isSupported = (locale) => Object.hasOwn(locales, locale);

export function createI18n({ onChange } = {}) {
  let locale = defaultLocale;

  try {
    const savedLocale = globalThis.localStorage?.getItem(STORAGE_KEY);
    if (isSupported(savedLocale)) locale = savedLocale;
  } catch {
    // Private browsing and restrictive storage policies must not block rendering.
  }

  function t(path) {
    const resolve = (dictionary) => path.split('.').reduce((value, key) => value?.[key], dictionary);
    const value = resolve(locales[locale]) ?? resolve(locales[defaultLocale]);
    return typeof value === 'string' ? value : path;
  }

  function apply(root = globalThis.document) {
    if (!root?.querySelectorAll) return;

    const update = (element) => {
      if (element.hasAttribute('data-i18n')) element.textContent = t(element.getAttribute('data-i18n'));
      if (element.hasAttribute('data-i18n-aria')) element.setAttribute('aria-label', t(element.getAttribute('data-i18n-aria')));
    };

    if (root.matches?.('[data-i18n], [data-i18n-aria]')) update(root);
    root.querySelectorAll('[data-i18n], [data-i18n-aria]').forEach(update);

    const document = root.nodeType === 9 ? root : root.ownerDocument;
    if (document) {
      document.documentElement.lang = locale;
      document.title = t('meta.title');
      document.querySelector('meta[name="description"]')?.setAttribute('content', t('meta.description'));
    }
  }

  function setLocale(nextLocale) {
    if (!isSupported(nextLocale)) return false;
    locale = nextLocale;
    try {
      globalThis.localStorage?.setItem(STORAGE_KEY, locale);
    } catch {
      // The selected language remains usable when persistence is unavailable.
    }
    apply();
    onChange?.(locale);
    return true;
  }

  apply();

  return { get locale() { return locale; }, t, setLocale, apply };
}
