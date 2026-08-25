/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.html",
    "./src/**/*.js",
    "./templates/**/*.html",
    "./templates/**/**/*.html",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        dark: {
          DEFAULT: '#0a0e1a',
          surface: '#111827',
          elevated: '#1a2332',
          border: '#1e293b',
        },
        neon: {
          blue: '#00d4ff',
          green: '#00ff88',
          pink: '#ff0080',
          purple: '#a855f7',
          gold: '#ffd700',
          orange: '#ff6b35',
          cyan: '#06b6d4',
        },
        primary: '#0B2046',
        background: '#0a0e1a',
        surface: '#111827',
        text: {
          DEFAULT: '#e2e8f0',
          muted: '#64748b',
          dim: '#475569',
        },
        muted: '#1e293b',
        accent: '#D4AF37',
      },
      fontFamily: {
        heading: ['Outfit', 'sans-serif'],
        body: ['"Plus Jakarta Sans"', 'sans-serif'],
      },
      fontSize: {
        'heading-lg': ['48px', { fontWeight: 600 }],
        'heading-md': ['32px', { fontWeight: 600 }],
        'heading-sm': ['24px', { fontWeight: 600 }],
        'body-base': ['16px', { fontWeight: 400 }],
        'label': ['13px', { fontWeight: 500, letterSpacing: '1px', textTransform: 'uppercase' }],
        'btn': ['15px', { fontWeight: 500 }],
      },
      borderRadius: {
        'sm': '8px',
        'md': '16px',
        'lg': '24px',
      },
      boxShadow: {
        'soft': '0 8px 32px rgba(0, 0, 0, 0.3)',
        'gold': '0 4px 24px rgba(212, 175, 55, 0.15)',
        'neon-blue': '0 0 15px rgba(0, 212, 255, 0.3), 0 0 30px rgba(0, 212, 255, 0.1)',
        'neon-green': '0 0 15px rgba(0, 255, 136, 0.3), 0 0 30px rgba(0, 255, 136, 0.1)',
        'neon-pink': '0 0 15px rgba(255, 0, 128, 0.3), 0 0 30px rgba(255, 0, 128, 0.1)',
        'neon-purple': '0 0 15px rgba(168, 85, 247, 0.3), 0 0 30px rgba(168, 85, 247, 0.1)',
        'neon-gold': '0 0 15px rgba(255, 215, 0, 0.3), 0 0 30px rgba(255, 215, 0, 0.1)',
        'neon-pulse': '0 0 20px rgba(0, 212, 255, 0.4), 0 0 40px rgba(0, 212, 255, 0.2), 0 0 60px rgba(0, 212, 255, 0.1)',
        'glow-green': '0 0 20px rgba(0, 255, 136, 0.4)',
        'glow-pink': '0 0 20px rgba(255, 0, 128, 0.4)',
        'glow-purple': '0 0 20px rgba(168, 85, 247, 0.4)',
      },
      animation: {
        'pulse-neon': 'pulse-neon 2s ease-in-out infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'float': 'float 3s ease-in-out infinite',
        'shake': 'shake 0.4s ease-in-out',
        'slide-up': 'slide-up 0.3s ease-out',
        'slide-in-left': 'slide-in-left 0.3s ease-out',
        'slide-in-right': 'slide-in-right 0.3s ease-out',
        'confetti': 'confetti 1s ease-out forwards',
        'scanline': 'scanline 8s linear infinite',
        'combo-pop': 'combo-pop 0.5s ease-out',
        'boss-intro': 'boss-intro 0.8s ease-out',
      },
      keyframes: {
        'pulse-neon': {
          '0%, 100%': { boxShadow: '0 0 5px rgba(0, 212, 255, 0.2)' },
          '50%': { boxShadow: '0 0 20px rgba(0, 212, 255, 0.6), 0 0 40px rgba(0, 212, 255, 0.3)' },
        },
        'glow': {
          '0%': { boxShadow: '0 0 5px rgba(0, 212, 255, 0.2), inset 0 0 5px rgba(0, 212, 255, 0.1)' },
          '100%': { boxShadow: '0 0 20px rgba(0, 212, 255, 0.4), inset 0 0 10px rgba(0, 212, 255, 0.2)' },
        },
        'float': {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-6px)' },
        },
        'slide-up': {
          '0%': { opacity: '0', transform: 'translateY(16px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'slide-in-left': {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(0)' },
        },
        'slide-in-right': {
          '0%': { transform: 'translateX(100%)' },
          '100%': { transform: 'translateX(0)' },
        },
        'confetti': {
          '0%': { transform: 'scale(0) rotate(0deg)', opacity: '1' },
          '50%': { transform: 'scale(1.2) rotate(180deg)', opacity: '1' },
          '100%': { transform: 'scale(0) rotate(360deg)', opacity: '0' },
        },
        'scanline': {
          '0%': { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(100vh)' },
        },
        'combo-pop': {
          '0%': { transform: 'scale(0.5)', opacity: '0' },
          '50%': { transform: 'scale(1.3)' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        'boss-intro': {
          '0%': { transform: 'scale(0.8)', opacity: '0', filter: 'brightness(3)' },
          '50%': { filter: 'brightness(1.5)' },
          '100%': { transform: 'scale(1)', opacity: '1', filter: 'brightness(1)' },
        },
      },
    },
  },
  plugins: [],
}
