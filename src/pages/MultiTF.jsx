import { useState } from 'react'
import './MultiTF.css'

const COINS = [
  'ADA', 'AAVE', 'APE', 'ATOM', 'AVAX', 'AXS', 'BNB', 'BTC', 'DOGE', 'DOT',
  'ETH', 'FIL', 'LINK', 'LTC', 'MATIC', 'NEAR', 'SOL', 'XRP', 'UNI'
]

const TIMEFRAMES = ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w']

const TABS = [
  { id: 'rsi', label: 'RSI' },
  { id: 'bb', label: 'Bollinger Bands' },
  { id: 'cci', label: 'CCI' },
  { id: 'change', label: 'Price Change %' },
  { id: 'ema', label: 'EMAs' },
  { id: 'sma', label: 'SMAs' }
]

export default function MultiTF() {
  const [selectedCoins, setSelectedCoins] = useState(['BTC', 'ETH'])
  const [selectedTimeframes, setSelectedTimeframes] = useState(['4h', '1d'])
  const [activeTab, setActiveTab] = useState('rsi')
  const [loading, setLoading] = useState(false)

  const toggleCoin = (coin) => {
    setSelectedCoins(prev =>
      prev.includes(coin)
        ? prev.filter(c => c !== coin)
        : [...prev, coin]
    )
  }

  const toggleTimeframe = (tf) => {
    setSelectedTimeframes(prev =>
      prev.includes(tf)
        ? prev.filter(t => t !== tf)
        : [...prev, tf]
    )
  }

  const handleAnalyze = async () => {
    setLoading(true)
    try {
      await new Promise(resolve => setTimeout(resolve, 1000))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="multi-tf">
      <div className="analysis-config">
        <button className="analyze-btn" onClick={handleAnalyze} disabled={loading || selectedCoins.length === 0 || selectedTimeframes.length === 0}>
          {loading ? 'Loading...' : 'Analyze'}
        </button>
      </div>

      <div className="selector-container">
        <div className="coin-selector">
          <h3>Coins</h3>
          <div className="coins-grid">
            {COINS.map(coin => (
              <button
                key={coin}
                className={`coin-btn ${selectedCoins.includes(coin) ? 'active' : ''}`}
                onClick={() => toggleCoin(coin)}
              >
                {coin}
              </button>
            ))}
          </div>
        </div>

        <div className="timeframe-selector">
          <h3>Time Frames</h3>
          <div className="timeframes-grid">
            {TIMEFRAMES.map(tf => (
              <button
                key={tf}
                className={`tf-btn ${selectedTimeframes.includes(tf) ? 'active' : ''}`}
                onClick={() => toggleTimeframe(tf)}
              >
                {tf}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="tabs-container">
        <div className="tabs">
          {TABS.map(tab => (
            <button
              key={tab.id}
              className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`}
              onClick={() => setActiveTab(tab.id)}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      <div className="heatmap-container">
        <div className="placeholder">
          <p>Select coins and timeframes to view multi-timeframe analysis</p>
          <p className="text-secondary">Heatmaps will display technical indicators across selected timeframes</p>
        </div>
      </div>
    </div>
  )
}
