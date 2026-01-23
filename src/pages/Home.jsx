import './Home.css'

export default function Home() {
  const indicators = [
    {
      title: 'CryptoData Session Range',
      url: 'https://www.tradingview.com/script/AdS5zUeT-CryptoData-Session-Range-ic/'
    },
    {
      title: 'CryptoData Coin/BTC Quick Chart',
      url: 'https://www.tradingview.com/script/48BzLTIt-CryptoData-Coin-BTC-Quick-Chart-ic/'
    },
    {
      title: 'CryptoData EZ Bands & Levels',
      url: 'https://www.tradingview.com/script/zPyDN1gK-CryptoData-EZ-Bands-Levels-ic/'
    },
    {
      title: 'CryptoData Spot vs Futures',
      url: 'https://www.tradingview.com/script/EsVAnvc5-CryptoData-Spot-vs-Futurese-ic/'
    },
    {
      title: 'CryptoData Trend & ATH/ATL',
      url: 'https://www.tradingview.com/script/Tw8DmRpM-CryptoData-Trend-ATH-ATL-ic/'
    },
    {
      title: 'CryptoData Coin Volume Spot',
      url: 'https://www.tradingview.com/script/C706lqlR-CryptoData-Coin-Volume-Spot-ic/'
    },
    {
      title: 'CryptoData Bands & Lines',
      url: 'https://www.tradingview.com/script/1yvrKxza-CryptoData-Bands-Lines-ic/'
    },
    {
      title: 'CryptoData Bollinger, Keltner & RSI',
      url: 'https://www.tradingview.com/script/mobbjHHQ-CryptoData-Bollinger-Keltner-RSI-ic/'
    },
  ]

  return (
    <div className="home">
      <div className="home-intro">
        <h1>Crypto Technical Analysis</h1>
        <p>Real-time trading indicators and multi-timeframe analysis</p>
      </div>

      <div className="home-section">
        <h2>Available Tools</h2>
        <p className="section-description">
          Use the navigation above to explore different analysis tools
        </p>
        <ul className="tools-list">
          <li>
            <strong>Single TF:</strong> Analyze coins across a single timeframe with multiple indicators
          </li>
          <li>
            <strong>Multi TF:</strong> View RSI and other indicators across multiple timeframes simultaneously
          </li>
          <li>
            <strong>Filter RSI:</strong> Filter coins by RSI values to find trading opportunities
          </li>
        </ul>
      </div>

      <div className="home-section">
        <h2>TradingView Indicators</h2>
        <p className="section-description">
          Custom CryptoData indicators available on TradingView
        </p>
        <div className="indicators-grid">
          {indicators.map((indicator) => (
            <a
              key={indicator.url}
              href={indicator.url}
              target="_blank"
              rel="noopener noreferrer"
              className="indicator-card"
            >
              <span>{indicator.title}</span>
              <span className="external-icon">→</span>
            </a>
          ))}
        </div>
      </div>

      <div className="home-section tips-section">
        <h2>Support</h2>
        <p className="section-description">If you find this tool useful, feel free to leave a tip</p>
        <div className="tips-list">
          <div className="tip-item">
            <span className="tip-label">Ethereum:</span>
            <span className="tip-address">0xb77fcef5c13e1a54bdfff9a7e5268743e81325c4</span>
          </div>
          <div className="tip-item">
            <span className="tip-label">Tron:</span>
            <span className="tip-address">TVT4GcBP29NoiuHTttfa4QJA837rv9XZ7v</span>
          </div>
          <div className="tip-item">
            <span className="tip-label">Litecoin:</span>
            <span className="tip-address">LRb7sR5T3L3qqG8Tbvsp8GyvsTfydSmbU8</span>
          </div>
          <div className="tip-item">
            <span className="tip-label">Bitcoin:</span>
            <span className="tip-address">1GDi8CRH6QUFw6UiPVyt7ZtD9BjmsRNAWJ</span>
          </div>
        </div>
      </div>
    </div>
  )
}
