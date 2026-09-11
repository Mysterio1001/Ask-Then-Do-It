import assert from 'node:assert/strict';
import { existsSync } from 'node:fs';
import test from 'node:test';
import { CatmullRomCurve3, Vector3 } from 'three';
import { createI18n, locales } from '../src/lib/i18n.js';
import { scrollProgress, stageForProgress } from '../src/lib/journey.js';
import { planets, routeProgress } from '../src/data/planets.js';
import { journeyStops, product } from '../src/data/product.js';

function replaceGlobal(t, name, descriptor) {
  const original = Object.getOwnPropertyDescriptor(globalThis, name);
  Object.defineProperty(globalThis, name, { configurable: true, ...descriptor });
  t.after(() => {
    if (original) Object.defineProperty(globalThis, name, original);
    else delete globalThis[name];
  });
}

function memoryStorage(initialValue = null) {
  const values = new Map(initialValue === null ? [] : [['ask-then-do-it.locale', initialValue]]);
  return {
    getItem(key) { return values.get(key) ?? null; },
    setItem(key, value) { values.set(key, String(value)); },
  };
}

// A narrow DOM fixture keeps translation behavior testable without a browser dependency.
function documentFixture() {
  function element(attributes = {}, children = []) {
    return {
      attributes: { ...attributes }, children, textContent: '', ownerDocument: null,
      hasAttribute(name) { return Object.hasOwn(this.attributes, name); },
      getAttribute(name) { return this.attributes[name] ?? null; },
      setAttribute(name, value) { this.attributes[name] = value; },
      matches() { return this.hasAttribute('data-i18n') || this.hasAttribute('data-i18n-aria'); },
      querySelectorAll() { return children.flatMap(child => [...(child.matches() ? [child] : []), ...child.querySelectorAll()]); },
    };
  }

  const title = element({ 'data-i18n': 'terminal.title' });
  const button = element({ 'data-i18n-aria': 'terminal.copy' });
  const nested = element({ 'data-i18n': 'stages.2.title' });
  const subtree = element({}, [nested]);
  const description = element({ name: 'description' });
  const nodes = [title, button, subtree];
  const document = {
    nodeType: 9, documentElement: { lang: '' }, title: '',
    querySelectorAll() { return nodes.flatMap(node => [...(node.matches() ? [node] : []), ...node.querySelectorAll()]); },
    querySelector(selector) { return selector === 'meta[name="description"]' ? description : null; },
  };
  [title, button, nested, subtree, description].forEach(node => { node.ownerDocument = document; });
  return { document, title, button, nested, subtree, description };
}

function translationPaths(value, prefix = '') {
  return Object.entries(value).flatMap(([key, entry]) => typeof entry === 'string'
    ? [`${prefix}${key}`]
    : translationPaths(entry, `${prefix}${key}.`));
}

test('every language supplies the same complete five-destination experience', () => {
  const requiredPaths = translationPaths(locales['zh-TW']).sort();
  assert.deepEqual(Object.keys(locales).sort(), ['en', 'ja', 'zh-TW']);
  for (const [locale, dictionary] of Object.entries(locales)) {
    assert.deepEqual(translationPaths(dictionary).sort(), requiredPaths, locale);
    assert.equal(dictionary.stages.length, 5, locale);
    assert.equal(dictionary.hero.line1 + dictionary.hero.line2, 'Ask-Then-Do-It.');
    assert.match(dictionary.meta.title, /Ask-Then-Do-It/);
    for (const path of requiredPaths) {
      const value = path.split('.').reduce((parent, key) => parent[key], dictionary);
      assert.ok(value.trim().length > 0, `${locale}: ${path} must not be blank`);
    }
  }
});

test('first visits use Traditional Chinese and returning visits restore a supported preference', t => {
  const storage = memoryStorage();
  replaceGlobal(t, 'localStorage', { value: storage });
  assert.equal(createI18n().locale, 'zh-TW');
  storage.setItem('ask-then-do-it.locale', 'en');
  assert.equal(createI18n().locale, 'en');
  storage.setItem('ask-then-do-it.locale', 'ja');
  assert.equal(createI18n().locale, 'ja');
  storage.setItem('ask-then-do-it.locale', 'invalid');
  assert.equal(createI18n().locale, 'zh-TW');
});

test('language switching updates visible text, accessibility labels, metadata, and future visits', t => {
  const storage = memoryStorage();
  const fixture = documentFixture();
  replaceGlobal(t, 'localStorage', { value: storage });
  replaceGlobal(t, 'document', { value: fixture.document });
  const changes = [];
  const i18n = createI18n({ onChange: locale => changes.push(locale) });
  assert.equal(fixture.title.textContent, locales['zh-TW'].terminal.title);
  assert.equal(i18n.setLocale('ja'), true);
  assert.equal(fixture.title.textContent, locales.ja.terminal.title);
  assert.equal(fixture.nested.textContent, locales.ja.stages[2].title);
  assert.equal(fixture.button.getAttribute('aria-label'), locales.ja.terminal.copy);
  assert.equal(fixture.document.documentElement.lang, 'ja');
  assert.equal(fixture.document.title, locales.ja.meta.title);
  assert.equal(fixture.description.getAttribute('content'), locales.ja.meta.description);
  assert.deepEqual(changes, ['ja']);
  assert.equal(createI18n().locale, 'ja');
  assert.equal(i18n.setLocale('fr'), false);
  assert.equal(i18n.locale, 'ja');
  assert.deepEqual(changes, ['ja']);
});

test('storage access denial never prevents rendering or language changes', t => {
  replaceGlobal(t, 'localStorage', { get() { throw new Error('Storage access denied'); } });
  const i18n = createI18n();
  assert.equal(i18n.locale, 'zh-TW');
  assert.equal(i18n.setLocale('en'), true);
  assert.equal(i18n.t('terminal.copy'), locales.en.terminal.copy);
});

test('a storage write failure leaves the selected language usable', t => {
  replaceGlobal(t, 'localStorage', { value: {
    getItem() { return 'en'; },
    setItem() { throw new Error('Storage quota exceeded'); },
  } });
  const i18n = createI18n();
  assert.equal(i18n.setLocale('ja'), true);
  assert.equal(i18n.locale, 'ja');
  assert.equal(i18n.t('stages.1.name'), 'AERIS');
});

test('missing translations fall back to Traditional Chinese and unknown keys stay diagnosable', t => {
  replaceGlobal(t, 'localStorage', { value: memoryStorage('en') });
  const original = locales.en.common.next;
  delete locales.en.common.next;
  t.after(() => { locales.en.common.next = original; });
  const i18n = createI18n();
  assert.equal(i18n.t('common.next'), locales['zh-TW'].common.next);
  assert.equal(i18n.t('not.a.translation'), 'not.a.translation');
});

test('newly inserted translated elements and subtrees can be localized independently', t => {
  replaceGlobal(t, 'localStorage', { value: memoryStorage('en') });
  const fixture = documentFixture();
  const i18n = createI18n();
  i18n.apply(fixture.title);
  assert.equal(fixture.title.textContent, locales.en.terminal.title);
  i18n.apply(fixture.subtree);
  assert.equal(fixture.nested.textContent, locales.en.stages[2].title);
  assert.equal(fixture.document.documentElement.lang, 'en');
  assert.doesNotThrow(() => i18n.apply(null));
});

test('scroll position reaches both journey endpoints and tolerates browser overscroll', () => {
  for (const [scrollY, height, viewport, expected] of [
    [0, 5000, 1000, 0], [1000, 5000, 1000, 0.25], [2000, 5000, 1000, 0.5],
    [4000, 5000, 1000, 1], [-100, 5000, 1000, 0], [4500, 5000, 1000, 1],
    [0, 800, 800, 0], [100, 600, 800, 0], [Number.NaN, 5000, 1000, 0],
  ]) {
    assert.equal(scrollProgress(scrollY, height, viewport), expected);
  }
});

test('the displayed destination changes at the halfway point between stops', () => {
  assert.equal(stageForProgress(-0.1), 0);
  assert.equal(stageForProgress(Number.NaN), 0);
  assert.equal(stageForProgress(1.1), 4);
  for (const [before, boundary, earlier, later] of [
    [0.12499, 0.125, 0, 1], [0.37499, 0.375, 1, 2],
    [0.62499, 0.625, 2, 3], [0.87499, 0.875, 3, 4],
  ]) {
    assert.equal(stageForProgress(before), earlier);
    assert.equal(stageForProgress(boundary), later);
  }
});

test('navigation, translations, and physical flight anchors identify the same destination', () => {
  assert.equal(product.repository, 'https://github.com/Mysterio1001/Ask-Then-Do-It');
  assert.equal(Object.hasOwn(product, 'zip'), false);
  assert.equal(planets.length, journeyStops.length);
  assert.equal(planets.length, locales['zh-TW'].stages.length);
  assert.equal(routeProgress[0], 0);
  assert.equal(routeProgress.at(-1), 1);
  const route = new CatmullRomCurve3(planets.map(planet => planet.position.clone()), false, 'catmullrom', 0.35);

  planets.forEach((planet, index) => {
    const stop = journeyStops[index];
    assert.equal(stop.progress, routeProgress[index]);
    assert.equal(stageForProgress(stop.progress, planets.length), index);
    if (index > 0) assert.equal(planet.id, stop.id);
    assert.ok(planet.position instanceof Vector3);
    assert.ok(planet.position.toArray().every(Number.isFinite));
    assert.ok(planet.radius > 0);
    assert.ok(route.getPoint(stop.progress).distanceTo(planet.position) < 1e-8, `${stop.id}: curve must reach its body`);
    if (index > 0) {
      const previous = planets[index - 1];
      assert.ok(planet.position.distanceTo(previous.position) > planet.radius + previous.radius, `${stop.id}: destinations must not overlap`);
    }
    if (planet.texture?.startsWith('/')) {
      assert.ok(existsSync(new URL(`../public${planet.texture}`, import.meta.url)), `${stop.id}: texture must be bundled locally`);
    }
    assert.notEqual(planet.texture, '/textures/moon.jpg');
  });
  assert.equal(planets.at(-1).type, 'station');
  assert.equal(existsSync(new URL('../public/textures/moon.jpg', import.meta.url)), false);
  assert.equal(planets.find(planet => planet.id === 'kronos')?.texture, 'rock');
});
