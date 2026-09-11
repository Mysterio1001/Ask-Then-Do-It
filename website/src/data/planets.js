import { Vector3 } from 'three';

// Each route anchor owns its physical appearance; editorial copy lives in i18n.
export const planets = [
  {
    id: 'chaos',
    position: new Vector3(0, 0, 0),
    radius: 3.2,
    color: '#e0e4e5',
    atmosphereColor: '#b6d6e7',
    rotationSpeed: 0.021,
    texture: 'gas',
    roughness: 0.98,
    rings: { inner: 1.3, outer: 2.05, tilt: 1.28, rotation: 0.35, color: '#e1ded0' },
    camera: { distance: 4.8, horizontal: 0.45, vertical: -0.11 },
  },
  {
    id: 'aeris',
    position: new Vector3(-15, 4, -36),
    radius: 3.05,
    color: '#c4d7d9',
    atmosphereColor: '#7bc3c9',
    rotationSpeed: 0.032,
    texture: '/textures/earth.jpg',
    roughness: 0.86,
    clouds: true,
    rings: null,
    camera: { distance: 4.8, horizontal: 0.45, vertical: -0.11 },
  },
  {
    id: 'kronos',
    position: new Vector3(10, -2, -74),
    radius: 3.05,
    color: '#b3aca2',
    atmosphereColor: '#b3c2c9',
    rotationSpeed: 0.017,
    texture: 'rock',
    roughness: 1,
    rings: { inner: 1.45, outer: 1.95, tilt: 1.31, rotation: 0.28, color: '#a9b7bf' },
    satellites: true,
    camera: { distance: 4.8, horizontal: 0.45, vertical: -0.11 },
  },
  {
    id: 'solis',
    position: new Vector3(-12, 4, -113),
    radius: 3.25,
    color: '#e0b283',
    atmosphereColor: '#f5c67f',
    rotationSpeed: 0.028,
    texture: 'solar',
    roughness: 0.92,
    rings: null,
    camera: { distance: 4.8, horizontal: 0.45, vertical: -0.11 },
  },
  {
    id: 'aegis',
    position: new Vector3(4, 0, -153),
    radius: 3.3,
    color: '#c8cdd0',
    atmosphereColor: '#83cfcc',
    rotationSpeed: 0.028,
    type: 'station',
    rings: null,
    camera: { distance: 5.9, horizontal: 0.45, vertical: -0.11 },
  },
];

export const routeProgress = planets.map((_, index) => index / (planets.length - 1));

export const cruiseOffsets = planets.slice(0, -1).map(() => new Vector3(0, 9, 0));

export const universeSettings = {
  fieldOfView: 42,
  desktopPixelRatio: 1.6,
  mobilePixelRatio: 1.4,
  desktopStars: 2600,
  mobileStars: 1400,
  background: '#030608',
  lightColor: '#f7ecdb',
};
