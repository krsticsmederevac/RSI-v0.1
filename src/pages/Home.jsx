import './Home.css'

export default function Home() {
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
