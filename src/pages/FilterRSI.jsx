import { useState } from 'react'
import './FilterRSI.css'

const COINS = [
  'ADA', 'AAVE', 'APE', 'ATOM', 'AVAX', 'AXS', 'BNB', 'BTC', 'DOGE', 'DOT',
  'ETH', 'FIL', 'LINK', 'LTC', 'MATIC', 'NEAR', 'SOL', 'XRP', 'UNI'
]

const TIMEFRAMES = ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w']

export default function FilterRSI() {
  const [selectedCoins, setSelectedCoins] = useState(['BTC', 'ETH'])
  const [selectedTimeframe, setSelectedTimeframe] = useState('1h')
  const [rsiMin, setRsiMin] = useState(30)
  const [rsiMax, setRsiMax] = useState(70)
  const [inverseRange, setInverseRange] = useState(true)
  const [sortBy, setSortBy] = useState('value')
  const [loading, setLoading] = useState(false)

  const toggleCoin = (coin) => {
    setSelectedCoins(prev =>
      prev.includes(coin)
        ? prev.filter(c => c !== coin)
        : [...prev, coin]
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

  const rangeDescription = inverseRange
    ? `RSI <= ${rsiMin} or RSI >= ${rsiMax}`
    : `${rsiMin} <= RSI <= ${rsiMax}`

  return (
    <div className="filter-rsi">
      <div className="analysis-config">
        <div className="config-section">
          <label>
            <strong>Time Frame</strong>
            <select value={selectedTimeframe} onChange={e => setSelectedTimeframe(e.target.value)}>
              {TIMEFRAMES.map(tf => (
                <option key={tf} value={tf}>{tf}</option>
              ))}
            </select>
          </label>
        </div>

        <div className="config-section">
          <label>
            <strong>Sort By</strong>
            <select value={sortBy} onChange={e => setSortBy(e.target.value)}>
              <option value="coin">Coin</option>
              <option value="value">Value</option>
            </select>
          </label>
        </div>

        <button className="analyze-btn" onClick={handleAnalyze} disabled={loading || selectedCoins.length === 0}>
          {loading ? 'Loading...' : 'Filter'}
        </button>
      </div>

      <div className="rsi-controls">
        <div className="rsi-section">
          <h3>RSI Range</h3>

          <div className="range-inputs">
            <div className="input-group">
              <label>Min RSI: {rsiMin}</label>
              <input
                type="range"
                min="0"
                max="100"
                value={rsiMin}
                onChange={e => setRsiMin(Number(e.target.value))}
                className="range-slider"
              />
            </div>

            <div className="input-group">
              <label>Max RSI: {rsiMax}</label>
              <input
                type="range"
                min="0"
                max="100"
                value={rsiMax}
                onChange={e => setRsiMax(Number(e.target.value))}
                className="range-slider"
              />
            </div>
          </div>

          <div className="checkbox-group">
            <input
              type="checkbox"
              id="inverse"
              checked={inverseRange}
              onChange={e => setInverseRange(e.target.checked)}
            />
            <label htmlFor="inverse">Inverse Range</label>
          </div>

          <div className="range-description">
            Filter: {rangeDescription}
          </div>
        </div>
      </div>

      <div className="coin-selector">
        <h3>Select Coins</h3>
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

      <div className="analysis-results">
        <div className="placeholder">
          <p>Results will appear here after filtering</p>
          <p className="text-secondary">Coins meeting the RSI criteria will be displayed</p>
        </div>
      </div>
    </div>
  )
}
