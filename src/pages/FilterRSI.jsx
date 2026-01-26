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
            type: 'filter-rsi',
            rsiMin,
            rsiMax,
            inverseRange,
          }),
        }
      )

      const data = await response.json()
      if (!data.success) {
        throw new Error(data.error || 'Filter failed')
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

      {error && <div className="error-message">{error}</div>}

      <div className="analysis-results">
        {!results ? (
          <div className="placeholder">
            <p>Results will appear here after filtering</p>
            <p className="text-secondary">Coins meeting the RSI criteria will be displayed</p>
          </div>
        ) : (
          <>
            {results.length === 0 ? (
              <div className="placeholder">
                <p>No coins match the selected RSI criteria</p>
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
          </>
        )}
      </div>
    </div>
  )
}
