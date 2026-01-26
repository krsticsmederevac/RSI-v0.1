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
  const [results, setResults] = useState(null)

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
    setResults(null)
    try {
      const response = await fetch(
        `${import.meta.env.VITE_SUPABASE_URL}/functions/v1/crypto-analysis`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${import.meta.env.VITE_SUPABASE_ANON_KEY}`,
          },
          body: JSON.stringify({
            coins: selectedCoins,
            timeframe: selectedTimeframe,
            type: 'single',
          }),
        }
      )

      const data = await response.json()
      if (!data.success) {
        throw new Error(data.error || 'Analysis failed')
      }

      let sortedData = [...data.data]
      if (sortBy === 'value') {
        sortedData.sort((a, b) => b.rsi - a.rsi)
      } else {
        sortedData.sort((a, b) => a.coin.localeCompare(b.coin))
      }

      setResults(sortedData)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error occurred')
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
        {!results ? (
          <div className="placeholder">
            <p>Select coins and click Analyze to view technical indicators</p>
            <p className="text-secondary">Indicators: RSI, Bollinger Bands, EMA, SMA, CCI, Price Change</p>
          </div>
        ) : (
          <table className="results-table">
            <thead>
              <tr>
                <th>Coin</th>
                <th>RSI</th>
                <th>Change %</th>
                <th>EMA20</th>
                <th>EMA50</th>
                <th>EMA100</th>
                <th>SMA20</th>
                <th>BB Position</th>
                <th>CCI</th>
              </tr>
            </thead>
            <tbody>
              {results.map((row) => (
                <tr key={row.coin}>
                  <td className="coin-name">{row.coin}</td>
                  <td className={row.rsi > 70 ? 'overbought' : row.rsi < 30 ? 'oversold' : ''}>
                    {row.rsi.toFixed(1)}
                  </td>
                  <td className={row.change > 0 ? 'positive' : 'negative'}>
                    {row.change.toFixed(2)}%
                  </td>
                  <td>{row.ema20.toFixed(2)}</td>
                  <td>{row.ema50.toFixed(2)}</td>
                  <td>{row.ema100.toFixed(2)}</td>
                  <td>{row.sma20.toFixed(2)}</td>
                  <td className={row.bb_position > 0 ? 'positive' : 'negative'}>
                    {row.bb_position.toFixed(2)}
                  </td>
                  <td className={Math.abs(row.cci) > 100 ? 'extreme' : ''}>
                    {row.cci.toFixed(1)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
