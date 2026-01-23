import { useState } from 'react'
import './SingleTF.css'

const COINS = [
  'ADA', 'AAVE', 'APE', 'ATOM', 'AVAX', 'AXS', 'BNB', 'BTC', 'DOGE', 'DOT',
  'ETH', 'FIL', 'LINK', 'LTC', 'MATIC', 'NEAR', 'SOL', 'XRP', 'UNI'
]

const TIMEFRAMES = ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w']

export default function SingleTF() {
  const [selectedCoins, setSelectedCoins] = useState(['BTC', 'ETH'])
  const [selectedTimeframe, setSelectedTimeframe] = useState('1h')
  const [sortBy, setSortBy] = useState('coin')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const toggleCoin = (coin) => {
    setSelectedCoins(prev =>
      prev.includes(coin)
        ? prev.filter(c => c !== coin)
        : [...prev, coin]
    )
  }

  const handleAnalyze = async () => {
    setLoading(true)
    setError(null)
    try {
      await new Promise(resolve => setTimeout(resolve, 1000))
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="single-tf">
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
          {loading ? 'Loading...' : 'Analyze'}
        </button>
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

      {error && <div className="error-message">{error}</div>}

      <div className="analysis-results">
        <div className="placeholder">
          <p>Select coins and click Analyze to view technical indicators</p>
          <p className="text-secondary">Indicators: RSI, Bollinger Bands, EMA, SMA, CCI, Price Change</p>
        </div>
      </div>
    </div>
  )
}
