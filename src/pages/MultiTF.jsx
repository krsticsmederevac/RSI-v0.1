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
  const [error, setError] = useState(null)
  const [results, setResults] = useState(null)

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

  const getHeatmapColor = (value, type) => {
    if (type === 'rsi') {
      if (value > 70) return '#ef4444'
      if (value < 30) return '#22c55e'
      return '#3b82f6'
    }
    if (type === 'change') {
      if (value > 2) return '#22c55e'
      if (value < -2) return '#ef4444'
      return '#3b82f6'
    }
    if (type === 'bb') {
      if (value > 1) return '#ef4444'
      if (value < -1) return '#22c55e'
      return '#3b82f6'
    }
    if (type === 'cci') {
      if (Math.abs(value) > 100) return '#ef4444'
      return '#3b82f6'
    }
    return '#3b82f6'
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
            timeframes: selectedTimeframes,
            type: 'multi',
          }),
        }
      )

      const data = await response.json()
      if (!data.success) {
        throw new Error(data.error || 'Analysis failed')
      }

      setResults(data.data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error occurred')
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

      {error && <div className="error-message">{error}</div>}

      <div className="heatmap-container">
        {!results ? (
          <div className="placeholder">
            <p>Select coins and timeframes to view multi-timeframe analysis</p>
            <p className="text-secondary">Heatmaps will display technical indicators across selected timeframes</p>
          </div>
        ) : (
          <div className="heatmap-grid">
            {selectedCoins.map(coin => (
              <div key={coin} className="heatmap-row">
                <div className="coin-label">{coin}</div>
                {selectedTimeframes.map(tf => {
                  const cellData = results.find(r => r.coin === coin && r.timeframe === tf)
                  if (!cellData) return null

                  let value, displayValue
                  if (activeTab === 'rsi') {
                    value = cellData.rsi
                    displayValue = value.toFixed(1)
                  } else if (activeTab === 'bb') {
                    value = cellData.bb_position
                    displayValue = value.toFixed(2)
                  } else if (activeTab === 'cci') {
                    value = cellData.cci
                    displayValue = value.toFixed(0)
                  } else if (activeTab === 'change') {
                    value = cellData.change
                    displayValue = value.toFixed(2)
                  } else if (activeTab === 'ema') {
                    value = ((cellData.ema50 - cellData.close) / cellData.close) * 100
                    displayValue = value.toFixed(1)
                  } else if (activeTab === 'sma') {
                    value = ((cellData.sma50 - cellData.close) / cellData.close) * 100
                    displayValue = value.toFixed(1)
                  }

                  const color = getHeatmapColor(value, activeTab)

                  return (
                    <div
                      key={`${coin}-${tf}`}
                      className="heatmap-cell"
                      style={{ backgroundColor: color }}
                      title={`${coin} ${tf}: ${displayValue}`}
                    >
                      <span className="cell-label">{tf}</span>
                      <span className="cell-value">{displayValue}</span>
                    </div>
                  )
                })}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
