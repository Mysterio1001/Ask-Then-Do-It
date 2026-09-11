import * as THREE from "three";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { planets, cruiseOffsets, universeSettings } from "../data/planets.js";

function randomGenerator(seed) {
  return () => {
    seed = (seed * 1664525 + 1013904223) >>> 0;
    return seed / 4294967296;
  };
}

function cruisePoints(anchors) {
  return anchors.flatMap((anchor, index) =>
    index === anchors.length - 1
      ? [anchor]
      : [
          anchor,
          anchor
            .clone()
            .lerp(anchors[index + 1], 0.5)
            .add(cruiseOffsets[index]),
        ],
  );
}

const hash = (x, y) => {
  const value = Math.sin(x * 127.1 + y * 311.7) * 43758.5453;
  return value - Math.floor(value);
};

function noise(x, y) {
  const ix = Math.floor(x);
  const iy = Math.floor(y);
  const fx = x - ix;
  const fy = y - iy;
  const sx = fx * fx * (3 - 2 * fx);
  const sy = fy * fy * (3 - 2 * fy);
  return THREE.MathUtils.lerp(
    THREE.MathUtils.lerp(hash(ix, iy), hash(ix + 1, iy), sx),
    THREE.MathUtils.lerp(hash(ix, iy + 1), hash(ix + 1, iy + 1), sx),
    sy,
  );
}

function textureFromPixels(width, height, getPixel) {
  const canvas = document.createElement("canvas");
  canvas.width = width;
  canvas.height = height;
  const context = canvas.getContext("2d");
  const data = context.createImageData(width, height);
  for (let y = 0; y < height; y += 1) {
    for (let x = 0; x < width; x += 1) {
      const color = getPixel(x / width, y / height, x, y);
      const index = (y * width + x) * 4;
      data.data[index] = color[0];
      data.data[index + 1] = color[1];
      data.data[index + 2] = color[2];
      data.data[index + 3] = color[3] ?? 255;
    }
  }
  context.putImageData(data, 0, 0);
  const texture = new THREE.CanvasTexture(canvas);
  texture.colorSpace = THREE.SRGBColorSpace;
  return texture;
}

function surfaceTexture(type, mobile) {
  const width = mobile ? 512 : 1024;
  const texture = textureFromPixels(width, width / 2, (u, v) => {
    const longitude = u * Math.PI * 2;
    const base = noise(
      Math.cos(longitude) * 3 + 4,
      Math.sin(longitude) * 3 + v * 28,
    );
    const fine = noise(
      Math.cos(longitude) * 20 + 24,
      Math.sin(longitude) * 20 + v * 170,
    );
    const turbulence = noise(
      Math.cos(longitude) * 1.2 + base * 1.6 + 4,
      Math.sin(longitude) * 1.2 + v * 13,
    );
    if (type === "solar") {
      const streak = Math.sin(v * 97 + turbulence * 6 + base * 2);
      const terrain = noise(
        Math.cos(longitude) * 6 + turbulence * 4 + 8,
        Math.sin(longitude) * 6 + v * 54,
      );
      const bright = 0.57 + terrain * 0.43 + streak * 0.055;
      return [
        191 * bright + fine * 10,
        143 * bright + fine * 9,
        98 * bright + fine * 8,
      ];
    }
    if (type === "rock") {
      const ridge = noise(
        Math.cos(longitude) * 8 + fine * 2,
        Math.sin(longitude) * 8 + v * 63,
      );
      const crater = Math.pow(Math.max(0, noise(u * 54, v * 31) - 0.68), 1.7);
      const mineral =
        0.54 + base * 0.2 + ridge * 0.2 + fine * 0.08 - crater * 1.5;
      return [170 * mineral, 164 * mineral, 156 * mineral];
    }
    const band = Math.sin(v * 85 + turbulence * 4.4 + base * 1.2);
    const detail = 0.65 + turbulence * 0.25 + band * 0.072 + fine * 0.052;
    const ochre = Math.max(0, Math.sin(v * 20 + turbulence)) * 6;
    return [130 * detail + ochre, 143 * detail + ochre * 0.6, 155 * detail];
  });
  texture.wrapS = THREE.RepeatWrapping;
  return texture;
}

function ringTexture() {
  return textureFromPixels(512, 8, (u) => {
    const thinBands = Math.sin(u * 980) * 0.11 + Math.sin(u * 284) * 0.14;
    const broadBands = 0.5 + noise(u * 38, 3) * 0.45;
    const gap = u > 0.66 && u < 0.7 ? 0.08 : 1;
    const edge = Math.min(u * 28, (1 - u) * 18, 1);
    const brightness = 155 + broadBands * 85;
    return [
      brightness,
      brightness - 3,
      brightness - 10,
      (broadBands + thinBands) * gap * edge * 230,
    ];
  });
}

function atmosphere(radius, color, segments) {
  const material = new THREE.ShaderMaterial({
    uniforms: { glowColor: { value: new THREE.Color(color) } },
    vertexShader: `
      varying vec3 vNormal;
      varying vec3 vView;
      void main() {
        vec4 positionView = modelViewMatrix * vec4(position, 1.0);
        vNormal = normalize(normalMatrix * normal);
        vView = normalize(-positionView.xyz);
        gl_Position = projectionMatrix * positionView;
      }
    `,
    fragmentShader: `
      uniform vec3 glowColor;
      varying vec3 vNormal;
      varying vec3 vView;
      void main() {
        float rim = pow(1.0 - abs(dot(normalize(vNormal), normalize(vView))), 3.5);
        float sun = max(dot(normalize(vNormal), normalize(vec3(-0.8, 0.5, 0.3))), 0.0);
        gl_FragColor = vec4(glowColor, rim * (0.06 + sun * 0.31));
      }
    `,
    side: THREE.BackSide,
    blending: THREE.AdditiveBlending,
    transparent: true,
    depthWrite: false,
  });
  return new THREE.Mesh(
    new THREE.SphereGeometry(radius * 1.014, segments, segments / 2),
    material,
  );
}

function addRings(config, radius, texture, segments) {
  const geometry = new THREE.RingGeometry(
    radius * config.inner,
    radius * config.outer,
    segments,
  );
  const uv = geometry.attributes.uv;
  const position = geometry.attributes.position;
  const vertex = new THREE.Vector3();
  // RingGeometry uses planar UVs; radial UVs preserve narrow concentric bands.
  for (let index = 0; index < position.count; index += 1) {
    vertex.fromBufferAttribute(position, index);
    uv.setXY(
      index,
      (vertex.length() / radius - config.inner) / (config.outer - config.inner),
      0.5,
    );
  }
  const ring = new THREE.Mesh(
    geometry,
    new THREE.MeshStandardMaterial({
      map: texture,
      color: config.color,
      emissiveMap: texture,
      emissive: "#9d9a88",
      emissiveIntensity: 0.8,
      roughness: 0.96,
      metalness: 0.04,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.82,
      alphaTest: 0.015,
      depthWrite: false,
    }),
  );
  ring.rotation.set(config.tilt, 0.11, config.rotation, "ZXY");
  ring.receiveShadow = false;
  return ring;
}

function solarPanelTexture() {
  const canvas = document.createElement("canvas");
  canvas.width = 256;
  canvas.height = 512;
  const context = canvas.getContext("2d");
  context.fillStyle = "#10202c";
  context.fillRect(0, 0, 256, 512);
  for (let x = 4; x < 252; x += 31) {
    for (let y = 4; y < 508; y += 31) {
      context.fillStyle = (x + y) % 3 === 0 ? "#315365" : "#244553";
      context.fillRect(x, y, 27, 27);
      context.fillStyle = "#54727b";
      context.fillRect(x, y + 7, 27, 1);
      context.fillRect(x, y + 18, 27, 1);
    }
  }
  const texture = new THREE.CanvasTexture(canvas);
  texture.colorSpace = THREE.SRGBColorSpace;
  return texture;
}

function buildStation(panelTexture, mobile) {
  const station = new THREE.Group();
  const metal = new THREE.MeshStandardMaterial({
    color: "#a5afb4",
    roughness: 0.4,
    metalness: 0.75,
  });
  const darkMetal = new THREE.MeshStandardMaterial({
    color: "#273239",
    roughness: 0.6,
    metalness: 0.7,
  });
  const white = new THREE.MeshStandardMaterial({
    color: "#d7d6ce",
    roughness: 0.7,
    metalness: 0.25,
  });
  const panelMaterial = new THREE.MeshStandardMaterial({
    map: panelTexture,
    metalness: 0.6,
    roughness: 0.35,
    side: THREE.DoubleSide,
  });
  const glass = new THREE.MeshStandardMaterial({
    color: "#133333",
    emissive: "#77ccc5",
    emissiveIntensity: 1.6,
    metalness: 0.4,
    roughness: 0.25,
  });
  const orange = new THREE.MeshStandardMaterial({
    color: "#bd763c",
    emissive: "#ad5723",
    emissiveIntensity: 0.3,
    roughness: 0.75,
  });
  const segments = mobile ? 48 : 96;
  const addMesh = (geometry, material, position = [0, 0, 0]) => {
    const mesh = new THREE.Mesh(geometry, material);
    mesh.position.set(...position);
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    station.add(mesh);
    return mesh;
  };

  const hub = addMesh(new THREE.CylinderGeometry(0.68, 0.78, 3.1, 24), white);
  hub.rotation.x = Math.PI / 2;
  const docking = addMesh(
    new THREE.TorusGeometry(0.72, 0.13, 12, 48),
    darkMetal,
    [0, 0, 1.62],
  );
  docking.rotation.z = Math.PI / 8;
  addMesh(new THREE.CircleGeometry(0.58, 32), darkMetal, [0, 0, 1.62]);
  addMesh(new THREE.TorusGeometry(0.51, 0.022, 8, 48), glass, [0, 0, 1.65]);
  addMesh(new THREE.TorusGeometry(2.4, 0.19, 12, segments), metal);
  addMesh(
    new THREE.TorusGeometry(2.4, 0.038, 8, segments),
    glass,
    [0, 0, 0.18],
  );
  addMesh(
    new THREE.TorusGeometry(2.4, 0.048, 8, segments),
    darkMetal,
    [0, 0, -0.2],
  );

  for (let index = 0; index < 8; index += 1) {
    const angle = (index / 8) * Math.PI * 2;
    const spoke = addMesh(new THREE.BoxGeometry(0.09, 1.8, 0.11), metal, [
      Math.sin(angle) * 1.4,
      Math.cos(angle) * 1.4,
      0,
    ]);
    spoke.rotation.z = -angle;
    const habitat = addMesh(new THREE.BoxGeometry(0.42, 0.8, 0.46), white, [
      Math.sin(angle) * 2.4,
      Math.cos(angle) * 2.4,
      0,
    ]);
    habitat.rotation.z = -angle;
    const window = addMesh(new THREE.BoxGeometry(0.27, 0.32, 0.025), glass, [
      Math.sin(angle) * 2.4,
      Math.cos(angle) * 2.4,
      0.245,
    ]);
    window.rotation.z = -angle;
  }

  for (const sign of [-1, 1]) {
    addMesh(new THREE.BoxGeometry(3.8, 0.13, 0.15), metal, [
      sign * 2.5,
      0,
      -0.65,
    ]);
    for (const offset of [-1, 1]) {
      const frame = addMesh(new THREE.BoxGeometry(1.38, 2.25, 0.08), metal, [
        sign * 3.65,
        offset * 1.28,
        -0.65,
      ]);
      const panel = addMesh(
        new THREE.PlaneGeometry(1.29, 2.15),
        panelMaterial,
        [sign * 3.65, offset * 1.28, -0.598],
      );
      frame.rotation.y = sign * 0.1;
      panel.rotation.y = sign * 0.1;
    }
    const cargo = addMesh(
      new THREE.CylinderGeometry(0.34, 0.34, 1.1, 12),
      orange,
      [sign * 0.75, 0, -1.0],
    );
    cargo.rotation.x = Math.PI / 2;
  }
  const mast = addMesh(
    new THREE.CylinderGeometry(0.025, 0.025, 1.9, 8),
    metal,
    [0, 1.2, -0.8],
  );
  mast.rotation.z = -0.18;
  const dish = addMesh(
    new THREE.SphereGeometry(0.38, 24, 12, 0, Math.PI * 2, 0, Math.PI / 2),
    white,
    [0.17, 2.14, -0.8],
  );
  dish.rotation.z = -0.18;
  station.rotation.set(0.32, -0.43, -0.21);
  return station;
}

function createStars(count) {
  const random = randomGenerator(8042);
  const positions = new Float32Array(count * 3);
  const colors = new Float32Array(count * 3);
  const sizes = new Float32Array(count);
  const phases = new Float32Array(count);
  const color = new THREE.Color();
  for (let index = 0; index < count; index += 1) {
    const theta = random() * Math.PI * 2;
    const cosPhi = random() * 2 - 1;
    const radius = 95 + random() * 200;
    positions[index * 3] =
      radius * Math.sqrt(1 - cosPhi * cosPhi) * Math.cos(theta);
    positions[index * 3 + 1] =
      radius * Math.sqrt(1 - cosPhi * cosPhi) * Math.sin(theta);
    positions[index * 3 + 2] = radius * cosPhi - 70;
    color.setHSL(
      random() > 0.76 ? 0.1 : 0.56,
      random() * 0.2,
      0.62 + random() * 0.34,
    );
    color.toArray(colors, index * 3);
    sizes[index] = random() > 0.97 ? 3.2 + random() * 1.8 : 1 + random() * 1.5;
    phases[index] = random() * Math.PI * 2;
  }
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));
  geometry.setAttribute("color", new THREE.BufferAttribute(colors, 3));
  geometry.setAttribute("starSize", new THREE.BufferAttribute(sizes, 1));
  geometry.setAttribute("phase", new THREE.BufferAttribute(phases, 1));
  const material = new THREE.ShaderMaterial({
    uniforms: { time: { value: 0 }, pixelRatio: { value: 1 } },
    vertexShader: `
      uniform float time;
      uniform float pixelRatio;
      attribute vec3 color;
      attribute float starSize;
      attribute float phase;
      varying vec3 vColor;
      varying float vBrightness;
      void main() {
        vec4 viewPosition = modelViewMatrix * vec4(position, 1.0);
        vColor = color;
        vBrightness = 0.90 + sin(time * 0.7 + phase) * 0.15;
        gl_PointSize = starSize * pixelRatio * clamp(150.0 / -viewPosition.z, 0.85, 1.7);
        gl_Position = projectionMatrix * viewPosition;
      }
    `,
    fragmentShader: `
      varying vec3 vColor;
      varying float vBrightness;
      void main() {
        float distanceToCenter = length(gl_PointCoord - 0.5) * 2.0;
        float alpha = smoothstep(1.0, 0.15, distanceToCenter);
        gl_FragColor = vec4(vColor * vBrightness * 2.1, alpha);
      }
    `,
    transparent: true,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
  });
  const points = new THREE.Points(geometry, material);
  points.frustumCulled = false;
  return points;
}

function createNebulae() {
  const texture = textureFromPixels(512, 256, (u, v) => {
    const turbulence = noise(u * 8, v * 7);
    const filaments = noise(u * 28 + turbulence * 6, v * 22 + turbulence * 3);
    const density = Math.pow(
      Math.max(0, filaments * 0.5 + turbulence * 0.5 - 0.28),
      2,
    );
    const edge = Math.pow(Math.sin(u * Math.PI) * Math.sin(v * Math.PI), 1.8);
    const diagonal = Math.exp(-Math.pow((v - u * 0.35 - 0.32) * 3.6, 2));
    return [105, 126, 136, density * edge * diagonal * 180];
  });
  const group = new THREE.Group();
  const placements = [
    {
      position: [30, 17, -75],
      scale: [180, 84],
      rotation: -0.35,
      color: "#6f8690",
      opacity: 0.11,
    },
    {
      position: [-28, -20, -185],
      scale: [210, 90],
      rotation: 0.2,
      color: "#877e76",
      opacity: 0.12,
    },
    {
      position: [52, 9, -245],
      scale: [180, 100],
      rotation: -0.5,
      color: "#719393",
      opacity: 0.12,
    },
  ];
  placements.forEach(({ position, scale, rotation, color, opacity }) => {
    const material = new THREE.SpriteMaterial({
      map: texture,
      color,
      opacity,
      transparent: true,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
    });
    material.rotation = rotation;
    const sprite = new THREE.Sprite(material);
    sprite.position.set(...position);
    sprite.scale.set(...scale, 1);
    group.add(sprite);
  });
  return group;
}

export function createUniverse({
  canvas,
  onReady,
  onError,
  reducedMotion = false,
}) {
  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({
      canvas,
      alpha: false,
      antialias: false,
      powerPreference: "high-performance",
    });
  } catch (error) {
    onError?.(error);
    return {
      setProgress() {},
      setPointer() {},
      resize() {},
      dispose() {},
      setPaused() {},
    };
  }

  const mobileAtStart = window.innerWidth < 760;
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(universeSettings.background);
  const camera = new THREE.PerspectiveCamera(
    universeSettings.fieldOfView,
    1,
    0.1,
    600,
  );
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.28;
  renderer.shadowMap.enabled = !mobileAtStart;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.info.autoReset = false;

  const composer = new EffectComposer(renderer);
  const renderPass = new RenderPass(scene, camera);
  const bloom = new UnrealBloomPass(new THREE.Vector2(1, 1), 0.34, 0.52, 0.89);
  const outputPass = new OutputPass();
  composer.addPass(renderPass);
  composer.addPass(bloom);
  composer.addPass(outputPass);

  scene.add(new THREE.HemisphereLight("#859cab", "#29251f", 0.25));
  const sun = new THREE.DirectionalLight(universeSettings.lightColor, 4.3);
  sun.castShadow = !mobileAtStart;
  sun.shadow.mapSize.set(1024, 1024);
  sun.shadow.camera.left = -10;
  sun.shadow.camera.right = 10;
  sun.shadow.camera.top = 10;
  sun.shadow.camera.bottom = -10;
  sun.shadow.camera.near = 0.1;
  sun.shadow.camera.far = 55;
  sun.shadow.normalBias = 0.018;
  sun.shadow.bias = -0.0003;
  scene.add(sun, sun.target);
  const fill = new THREE.DirectionalLight("#78949e", 0.13);
  fill.position.set(15, -3, 10);
  scene.add(fill);

  const textureLoader = new THREE.TextureLoader();
  const generatedTextures = new Set();
  const surfaceMaps = new Map();
  const ringMap = ringTexture();
  const panelMap = solarPanelTexture();
  generatedTextures.add(ringMap);
  generatedTextures.add(panelMap);
  const segments = mobileAtStart ? 64 : 112;
  const bodies = planets.map((config) => {
    const group = new THREE.Group();
    group.name = config.id;
    group.position.copy(config.position);
    let sphere;
    let cloud;
    let station;
    if (config.type === "station") {
      station = buildStation(panelMap, mobileAtStart);
      group.add(station);
    } else {
      const surfaceType = ["gas", "rock", "solar"].includes(config.texture)
        ? config.texture
        : "gas";
      if (!surfaceMaps.has(surfaceType)) {
        const surfaceMap = surfaceTexture(surfaceType, mobileAtStart);
        surfaceMaps.set(surfaceType, surfaceMap);
        generatedTextures.add(surfaceMap);
      }
      const fallback = surfaceMaps.get(surfaceType);
      const material = new THREE.MeshStandardMaterial({
        map: fallback,
        color: config.color,
        roughness: config.roughness,
        metalness: 0.015,
        bumpMap: config.texture === "gas" ? null : fallback,
        bumpScale:
          config.texture === "solar"
            ? 0.05
            : config.texture === "rock"
              ? 0.075
              : 0.015,
      });
      if (config.texture.startsWith("/")) {
        textureLoader.load(
          `${import.meta.env.BASE_URL}${config.texture.slice(1)}`,
          (texture) => {
            if (disposed) {
              texture.dispose();
              return;
            }
            texture.colorSpace = THREE.SRGBColorSpace;
            texture.anisotropy = Math.min(
              renderer.capabilities.getMaxAnisotropy(),
              4,
            );
            material.map = texture;
            material.bumpMap = texture;
            material.bumpScale = config.id === "kronos" ? 0.065 : 0.018;
            material.needsUpdate = true;
            generatedTextures.add(texture);
            canvas.dataset[`${config.id}Texture`] = "loaded";
            dirty = true;
          },
          undefined,
          () => {
            canvas.dataset[`${config.id}Texture`] = "fallback";
          },
        );
      }
      sphere = new THREE.Mesh(
        new THREE.SphereGeometry(config.radius, segments, segments / 2),
        material,
      );
      sphere.rotation.z =
        config.id === "aeris" ? -0.12 : (config.rings?.rotation ?? 0.13);
      sphere.rotation.y = config.id === "aeris" ? 2.4 : 0.5;
      sphere.castShadow = true;
      sphere.receiveShadow = false;
      group.add(
        sphere,
        atmosphere(config.radius, config.atmosphereColor, segments),
      );
      if (config.rings)
        group.add(
          addRings(
            config.rings,
            config.radius,
            ringMap,
            mobileAtStart ? 144 : 224,
          ),
        );
      if (config.clouds) {
        const cloudMap = textureFromPixels(512, 256, (u, v) => {
          const base = noise(u * 23, v * 19);
          const cloudDensity = Math.max(
            0,
            noise(u * 41 + base * 5, v * 34) * 0.6 + base * 0.4 - 0.59,
          );
          return [221, 227, 224, cloudDensity * 450];
        });
        generatedTextures.add(cloudMap);
        cloud = new THREE.Mesh(
          new THREE.SphereGeometry(
            config.radius * 1.007,
            segments,
            segments / 2,
          ),
          new THREE.MeshStandardMaterial({
            map: cloudMap,
            transparent: true,
            opacity: 0.42,
            roughness: 1,
            depthWrite: false,
          }),
        );
        group.add(cloud);
      }
      if (config.satellites) {
        const satellite = new THREE.Mesh(
          new THREE.SphereGeometry(0.34, 24, 16),
          new THREE.MeshStandardMaterial({
            map: fallback,
            color: "#8c9194",
            roughness: 1,
          }),
        );
        satellite.position.set(-5.6, 2.8, -2);
        satellite.castShadow = true;
        group.add(satellite);
      }
    }
    scene.add(group);
    return { config, group, sphere, cloud, station };
  });

  const stars = createStars(
    mobileAtStart
      ? universeSettings.mobileStars
      : universeSettings.desktopStars,
  );
  scene.add(stars, createNebulae());
  let positionCurve;
  let targetCurve;
  let scrollProgress = 0;
  let renderedProgress = 0;
  let elapsed = 0;
  let previousTime = 0;
  let frameId;
  let disposed = false;
  let paused = reducedMotion;
  let dirty = true;
  let ready = false;
  const pointer = new THREE.Vector2();
  const smoothPointer = new THREE.Vector2();
  const lookTarget = new THREE.Vector3();
  const lightTarget = new THREE.Vector3();
  const lightOffset = new THREE.Vector3(-15, 8, 5);
  const fillOffset = new THREE.Vector3(14, -4, 8);
  const worldPath = new THREE.CatmullRomCurve3(
    cruisePoints(planets.map(({ position }) => position.clone())),
    false,
    "catmullrom",
    0.3,
  );

  function resize() {
    if (disposed) return;
    const width = canvas.clientWidth || window.innerWidth;
    const height = canvas.clientHeight || window.innerHeight;
    const aspect = width / height;
    const mobile = width <= 700;
    const pixelRatio = Math.min(
      window.devicePixelRatio || 1,
      mobile
        ? universeSettings.mobilePixelRatio
        : universeSettings.desktopPixelRatio,
    );
    renderer.setPixelRatio(pixelRatio);
    renderer.setSize(width, height, false);
    composer.setPixelRatio(pixelRatio);
    composer.setSize(width, height);
    stars.material.uniforms.pixelRatio.value = pixelRatio;
    camera.aspect = aspect;
    camera.updateProjectionMatrix();
    const positions = [];
    const targets = [];
    const tangent = Math.tan(
      THREE.MathUtils.degToRad(universeSettings.fieldOfView / 2),
    );
    planets.forEach((config) => {
      const stationFraming = mobile && config.type === "station" ? 1.45 : 1;
      const distance =
        config.radius *
        (mobile ? Math.max(4.5, 3.5 / aspect) : config.camera.distance) *
        stationFraming;
      const halfHeight = distance * tangent;
      const offsetX =
        -halfHeight * aspect * (mobile ? 0.25 : config.camera.horizontal);
      const offsetY = halfHeight * (mobile ? -0.56 : config.camera.vertical);
      const target = config.position
        .clone()
        .add(new THREE.Vector3(offsetX, offsetY, 0));
      targets.push(target);
      positions.push(target.clone().add(new THREE.Vector3(0, 0, distance)));
    });
    positionCurve = new THREE.CatmullRomCurve3(
      cruisePoints(positions),
      false,
      "catmullrom",
      0.3,
    );
    targetCurve = new THREE.CatmullRomCurve3(
      cruisePoints(targets),
      false,
      "catmullrom",
      0.3,
    );
    dirty = true;
  }

  function render(time) {
    if (disposed) return;
    frameId = requestAnimationFrame(render);
    if (document.hidden) {
      previousTime = time;
      return;
    }
    const delta = Math.min((time - previousTime) / 1000 || 0, 0.05);
    previousTime = time;
    const oldProgress = renderedProgress;
    renderedProgress = reducedMotion
      ? scrollProgress
      : THREE.MathUtils.lerp(
          renderedProgress,
          scrollProgress,
          1 - Math.exp(-delta * 6),
        );
    if (Math.abs(renderedProgress - scrollProgress) < 0.00001)
      renderedProgress = scrollProgress;
    smoothPointer.lerp(pointer, 1 - Math.exp(-delta * 3));
    const moving =
      Math.abs(oldProgress - renderedProgress) > 0.000001 ||
      smoothPointer.distanceToSquared(pointer) > 0.00001;
    if (paused && !moving && !dirty) return;
    if (!paused) elapsed += delta;

    camera.position.copy(positionCurve.getPoint(renderedProgress));
    targetCurve.getPoint(renderedProgress, lookTarget);
    if (!reducedMotion) {
      camera.position.x += smoothPointer.x * 0.17;
      camera.position.y += smoothPointer.y * 0.11;
      lookTarget.x += smoothPointer.x * 0.025;
      lookTarget.y += smoothPointer.y * 0.025;
    }
    camera.lookAt(lookTarget);
    worldPath.getPoint(renderedProgress, lightTarget);
    sun.position.copy(lightTarget).add(lightOffset);
    sun.target.position.copy(lightTarget);
    fill.position.copy(lightTarget).add(fillOffset);
    fill.target.position.copy(lightTarget);
    fill.target.updateMatrixWorld();
    bodies.forEach(({ config, group, sphere, cloud, station }, index) => {
      group.visible =
        Math.abs(index / (planets.length - 1) - renderedProgress) < 0.18;
      if (sphere)
        sphere.rotation.y =
          (config.id === "aeris" ? 2.4 : 0.5) + elapsed * config.rotationSpeed;
      if (cloud) cloud.rotation.y = elapsed * config.rotationSpeed * 1.18;
      if (station)
        station.rotation.y =
          -0.43 + Math.sin(elapsed * config.rotationSpeed) * 0.15;
    });
    stars.material.uniforms.time.value = elapsed;
    renderer.info.reset();
    composer.render(delta);
    dirty = false;
    canvas.dataset.sceneProgress = renderedProgress.toFixed(4);
    canvas.dataset.activeBody =
      planets[Math.round(renderedProgress * (planets.length - 1))].id;
    canvas.dataset.renderCalls = String(renderer.info.render.calls);
    canvas.dataset.renderTriangles = String(renderer.info.render.triangles);
    if (!ready) {
      ready = true;
      canvas.dataset.sceneReady = "true";
      onReady?.();
    }
  }

  const onContextLost = (event) => {
    event.preventDefault();
    cancelAnimationFrame(frameId);
    onError?.(new Error("WebGL context lost"));
  };
  const onContextRestored = () => {
    previousTime = performance.now();
    dirty = true;
    frameId = requestAnimationFrame(render);
    onReady?.();
  };
  canvas.addEventListener("webglcontextlost", onContextLost);
  canvas.addEventListener("webglcontextrestored", onContextRestored);
  resize();
  frameId = requestAnimationFrame(render);

  return {
    setProgress(value) {
      scrollProgress = THREE.MathUtils.clamp(
        Number.isFinite(value) ? value : 0,
        0,
        1,
      );
      dirty = true;
    },
    setPointer(x, y) {
      pointer.set(
        THREE.MathUtils.clamp(x, -1, 1),
        THREE.MathUtils.clamp(y, -1, 1),
      );
      dirty = true;
    },
    setPaused(value) {
      paused = Boolean(value);
      dirty = true;
    },
    setReducedMotion(value) {
      reducedMotion = Boolean(value);
      dirty = true;
    },
    resize,
    dispose() {
      if (disposed) return;
      disposed = true;
      cancelAnimationFrame(frameId);
      canvas.removeEventListener("webglcontextlost", onContextLost);
      canvas.removeEventListener("webglcontextrestored", onContextRestored);
      const materials = new Set();
      const geometries = new Set();
      scene.traverse((object) => {
        if (object.geometry) geometries.add(object.geometry);
        if (object.material) {
          const list = Array.isArray(object.material)
            ? object.material
            : [object.material];
          list.forEach((material) => {
            materials.add(material);
            if (material.map) generatedTextures.add(material.map);
          });
        }
      });
      geometries.forEach((geometry) => geometry.dispose());
      materials.forEach((material) => material.dispose());
      generatedTextures.forEach((texture) => texture.dispose());
      sun.shadow.map?.dispose();
      bloom.dispose();
      outputPass.dispose();
      composer.dispose();
      renderer.dispose();
    },
  };
}
