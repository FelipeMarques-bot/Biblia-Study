/* ============================================
   BÍBLIA STUDY — SOUND ENGINE (Web Audio API + MP3)
   3-state: 'all' (music+effects), 'effects' (no music), 'none' (off)
   State persisted in localStorage('sound_state')
   ============================================ */

const SoundEngine = (() => {
  let ctx = null
  let musicGain = null
  let musicOscillators = []
  let musicPlaying = false
  let masterVolume = 0.3
  let musicVolume = 0.08
  let enabled = true
  let musicEnabled = true

  // ── MP3 audio elements ──
  const mp3 = {
    correct: null,
    wrong: null,
    background: null,
  }

  function initMp3() {
    try {
      mp3.correct = new Audio('/static/audio/acertou-pergunta.mp3')
      mp3.correct.volume = 0.7
      mp3.wrong = new Audio('/static/audio/errou-pergunta.mp3')
      mp3.wrong.volume = 0.7
      mp3.background = new Audio('/static/audio/fundo.mp3')
      mp3.background.loop = true
      mp3.background.volume = 0.15
    } catch (e) { /* MP3 files may not exist yet */ }
  }

  function getCtx() {
    if (!ctx) {
      ctx = new (window.AudioContext || window.webkitAudioContext)()
      musicGain = ctx.createGain()
      musicGain.gain.value = musicVolume
      musicGain.connect(ctx.destination)
    }
    if (ctx.state === 'suspended') ctx.resume()
    return ctx
  }

  function playTone(freq, duration, type = 'sine', vol = 0.15, detune = 0) {
    if (!enabled) return
    const c = getCtx()
    const osc = c.createOscillator()
    const gain = c.createGain()
    osc.type = type
    osc.frequency.value = freq
    osc.detune.value = detune
    gain.gain.setValueAtTime(vol * masterVolume, c.currentTime)
    gain.gain.exponentialRampToValueAtTime(0.001, c.currentTime + duration)
    osc.connect(gain)
    gain.connect(c.destination)
    osc.start(c.currentTime)
    osc.stop(c.currentTime + duration)
  }

  function playChord(freqs, duration, type = 'sine', vol = 0.1) {
    freqs.forEach((f, i) => {
      setTimeout(() => playTone(f, duration, type, vol), i * 40)
    })
  }

  // ── State persistence ──
  function loadState() {
    const s = localStorage.getItem('sound_state') || 'all'
    if (s === 'none') { enabled = false; musicEnabled = false }
    else if (s === 'effects') { enabled = true; musicEnabled = false }
    else { enabled = true; musicEnabled = true }
  }

  function saveState() {
    let s = 'all'
    if (!enabled && !musicEnabled) s = 'none'
    else if (enabled && !musicEnabled) s = 'effects'
    else if (!enabled && musicEnabled) s = 'all' // shouldn't happen, fallback
    localStorage.setItem('sound_state', s)
  }

  // Load state on init
  loadState()

  return {
    init() {
      document.addEventListener('click', () => getCtx(), { once: true })
      document.addEventListener('touchstart', () => getCtx(), { once: true })
      initMp3()
      loadState()
    },

    // ── 3-state toggle: all → effects → none → all ──
    cycleState() {
      const s = localStorage.getItem('sound_state') || 'all'
      if (s === 'all') {
        enabled = true; musicEnabled = false
        localStorage.setItem('sound_state', 'effects')
        if (musicPlaying) this.fadeOutMusic()
      } else if (s === 'effects') {
        enabled = false; musicEnabled = false
        localStorage.setItem('sound_state', 'none')
      } else {
        enabled = true; musicEnabled = true
        localStorage.setItem('sound_state', 'all')
      }
      return localStorage.getItem('sound_state')
    },
    getState() { return localStorage.getItem('sound_state') || 'all' },
    isEnabled() { return enabled },
    isMusicEnabled() { return musicEnabled },
    setMasterVolume(v) { masterVolume = v },
    setMusicVolume(v) { musicVolume = v; if (musicGain) musicGain.gain.value = v },

    /* === UI SOUNDS === */
    click() {
      if (!enabled) return
      playTone(800, 0.08, 'sine', 0.12)
      playTone(1200, 0.05, 'sine', 0.06)
    },
    hover() { if (!enabled) return; playTone(600, 0.04, 'sine', 0.04) },
    menuOpen() {
      if (!enabled) return
      playTone(400, 0.12, 'sine', 0.1)
      setTimeout(() => playTone(600, 0.1, 'sine', 0.08), 60)
    },
    menuClose() {
      if (!enabled) return
      playTone(600, 0.1, 'sine', 0.1)
      setTimeout(() => playTone(400, 0.08, 'sine', 0.06), 50)
    },
    back() {
      if (!enabled) return
      playTone(500, 0.08, 'triangle', 0.1)
      playTone(350, 0.1, 'triangle', 0.07)
    },

    /* === GAME SOUNDS === */
    correct() {
      if (!enabled) return
      if (mp3.correct) { mp3.correct.currentTime = 0; mp3.correct.play().catch(() => {}) }
      else {
        playTone(523, 0.12, 'sine', 0.18)
        setTimeout(() => playTone(659, 0.12, 'sine', 0.15), 80)
        setTimeout(() => playTone(784, 0.2, 'sine', 0.12), 160)
      }
    },
    wrong() {
      if (!enabled) return
      if (mp3.wrong) { mp3.wrong.currentTime = 0; mp3.wrong.play().catch(() => {}) }
      else {
        playTone(300, 0.15, 'sawtooth', 0.08)
        setTimeout(() => playTone(220, 0.25, 'sawtooth', 0.06), 100)
      }
    },
    combo(count) {
      if (!enabled) return
      const baseFreq = 523 + (count * 50)
      playTone(baseFreq, 0.08, 'sine', 0.15)
      setTimeout(() => playTone(baseFreq * 1.25, 0.08, 'sine', 0.12), 50)
      setTimeout(() => playTone(baseFreq * 1.5, 0.15, 'sine', 0.1), 100)
      if (count >= 3) setTimeout(() => playTone(baseFreq * 2, 0.2, 'sine', 0.08), 150)
    },
    levelUp() {
      if (!enabled) return
      const notes = [523, 659, 784, 1047]
      notes.forEach((f, i) => setTimeout(() => playTone(f, 0.2, 'sine', 0.12), i * 100))
      setTimeout(() => playChord([523, 659, 784], 0.5, 'sine', 0.06), 400)
    },
    xpGain() {
      if (!enabled) return
      playTone(880, 0.08, 'sine', 0.1)
      setTimeout(() => playTone(1100, 0.12, 'sine', 0.08), 60)
    },
    chestShake() {
      if (!enabled) return
      for (let i = 0; i < 4; i++) setTimeout(() => playTone(200 + Math.random() * 100, 0.06, 'triangle', 0.08), i * 80)
    },
    chestOpen() {
      if (!enabled) return
      playChord([261, 329, 392, 523], 0.6, 'sine', 0.1)
      setTimeout(() => playChord([523, 659, 784, 1047], 0.8, 'sine', 0.08), 300)
      setTimeout(() => playTone(1047, 0.4, 'sine', 0.06), 500)
    },
    reward() {
      if (!enabled) return
      const melody = [784, 880, 988, 1047, 1175, 1318]
      melody.forEach((f, i) => setTimeout(() => playTone(f, 0.15, 'sine', 0.1), i * 80))
    },
    achievement() {
      if (!enabled) return
      playChord([523, 659], 0.3, 'sine', 0.1)
      setTimeout(() => playChord([659, 784], 0.3, 'sine', 0.1), 200)
      setTimeout(() => playChord([784, 1047], 0.5, 'sine', 0.1), 400)
    },
    select() { if (!enabled) return; playTone(700, 0.06, 'sine', 0.08) },
    deselect() { if (!enabled) return; playTone(400, 0.06, 'sine', 0.06) },
    submit() {
      if (!enabled) return
      playTone(600, 0.08, 'sine', 0.1)
      setTimeout(() => playTone(900, 0.12, 'sine', 0.08), 80)
    },
    error() {
      if (!enabled) return
      playTone(200, 0.2, 'square', 0.06)
      playTone(150, 0.3, 'square', 0.04)
    },

    /* === BACKGROUND MUSIC === */
    startMusic() {
      if (musicPlaying || !musicEnabled) return
      if (mp3.background) {
        mp3.background.currentTime = 0
        mp3.background.play().catch(() => {})
        musicPlaying = true
        return
      }
      // Fallback: Web Audio procedural music
      const c = getCtx()
      musicPlaying = true
      function createDrone(freq, vol = 0.04) {
        const osc = c.createOscillator()
        const gain = c.createGain()
        const lfo = c.createOscillator()
        const lfoGain = c.createGain()
        osc.type = 'sine'; osc.frequency.value = freq
        lfo.type = 'sine'; lfo.frequency.value = 0.1 + Math.random() * 0.15
        lfoGain.gain.value = 2
        lfo.connect(lfoGain); lfoGain.connect(osc.frequency)
        gain.gain.value = vol; osc.connect(gain); gain.connect(musicGain)
        osc.start(); lfo.start()
        musicOscillators.push(osc, lfo)
      }
      createDrone(130.81, 0.05); createDrone(196.00, 0.03)
      createDrone(261.63, 0.02); createDrone(98.00, 0.04)
      function playMelodyNote() {
        if (!musicPlaying || !musicEnabled) return
        const scale = [261.63, 293.66, 329.63, 392.00, 440.00, 523.25, 587.33, 659.25]
        const note = scale[Math.floor(Math.random() * scale.length)]
        const dur = 1.5 + Math.random() * 2
        const osc = c.createOscillator()
        const gain = c.createGain()
        osc.type = 'sine'; osc.frequency.value = note
        gain.gain.setValueAtTime(0, c.currentTime)
        gain.gain.linearRampToValueAtTime(0.03 * masterVolume, c.currentTime + 0.3)
        gain.gain.linearRampToValueAtTime(0, c.currentTime + dur)
        osc.connect(gain); gain.connect(c.destination)
        osc.start(c.currentTime); osc.stop(c.currentTime + dur)
        setTimeout(playMelodyNote, 2000 + Math.random() * 4000)
      }
      setTimeout(playMelodyNote, 1000)
    },
    stopMusic() {
      musicPlaying = false
      if (mp3.background) { mp3.background.pause(); mp3.background.currentTime = 0 }
      musicOscillators.forEach(o => { try { o.stop() } catch (e) {} })
      musicOscillators = []
    },
    isMusicPlaying() { return musicPlaying },
    fadeInMusic() {
      if (!musicEnabled) return
      if (mp3.background) {
        mp3.background.volume = 0
        mp3.background.play().catch(() => {})
        let vol = 0
        const fade = setInterval(() => {
          vol = Math.min(vol + 0.02, 0.15)
          mp3.background.volume = vol
          if (vol >= 0.15) clearInterval(fade)
        }, 100)
        musicPlaying = true
        return
      }
      if (!musicGain) getCtx()
      musicGain.gain.setValueAtTime(0, ctx.currentTime)
      musicGain.gain.linearRampToValueAtTime(musicVolume, ctx.currentTime + 2)
      this.startMusic()
    },
    fadeOutMusic() {
      if (mp3.background) {
        let vol = mp3.background.volume
        const fade = setInterval(() => {
          vol = Math.max(vol - 0.02, 0)
          mp3.background.volume = vol
          if (vol <= 0) { clearInterval(fade); mp3.background.pause(); mp3.background.currentTime = 0 }
        }, 100)
        musicPlaying = false
        return
      }
      if (!musicGain) return
      musicGain.gain.linearRampToValueAtTime(0, ctx.currentTime + 1.5)
      setTimeout(() => this.stopMusic(), 1600)
    }
  }
})()

SoundEngine.init()
