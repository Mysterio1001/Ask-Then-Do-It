export const product = Object.freeze({
  name: 'Ask-Then-Do-It',
  repository: 'https://github.com/Mysterio1001/Ask-Then-Do-It',
  docs: {
    'zh-TW': 'https://github.com/Mysterio1001/Ask-Then-Do-It/blob/main/START-HERE.zh-TW.md',
    en: 'https://github.com/Mysterio1001/Ask-Then-Do-It/blob/main/START-HERE.en.md',
    ja: 'https://github.com/Mysterio1001/Ask-Then-Do-It/blob/main/START-HERE.ja.md',
  },
  commands: {
    codex: 'codex plugin marketplace add Mysterio1001/Ask-Then-Do-It\ncodex plugin add ask-then-do-it@ask-then-do-it',
    claude: '/plugin marketplace add Mysterio1001/Ask-Then-Do-It\n/plugin install ask-then-do-it@ask-then-do-it',
    clone: 'git clone https://github.com/Mysterio1001/Ask-Then-Do-It.git',
  },
});

export const journeyStops = [
  { id: 'origin', number: '00', name: 'DEEP SPACE', progress: 0 },
  { id: 'aeris', number: '01', name: 'AERIS', progress: 0.25 },
  { id: 'kronos', number: '02', name: 'KRONOS', progress: 0.5 },
  { id: 'solis', number: '03', name: 'SOLIS', progress: 0.75 },
  { id: 'aegis', number: '04', name: 'AEGIS STATION', progress: 1 },
];
