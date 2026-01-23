import { useState } from 'react'
import Home from './pages/Home'
import SingleTF from './pages/SingleTF'
import MultiTF from './pages/MultiTF'
import FilterRSI from './pages/FilterRSI'
import './App.css'

export default function App() {
  const [currentPage, setCurrentPage] = useState('home')

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <h1 className="logo">Crypto TA</h1>
          <nav className="nav">
            <button
              className={`nav-btn ${currentPage === 'home' ? 'active' : ''}`}
              onClick={() => setCurrentPage('home')}
            >
              Home
            </button>
            <button
              className={`nav-btn ${currentPage === 'single-tf' ? 'active' : ''}`}
              onClick={() => setCurrentPage('single-tf')}
            >
              Single TF
            </button>
            <button
              className={`nav-btn ${currentPage === 'multi-tf' ? 'active' : ''}`}
              onClick={() => setCurrentPage('multi-tf')}
            >
              Multi TF
            </button>
            <button
              className={`nav-btn ${currentPage === 'filter-rsi' ? 'active' : ''}`}
              onClick={() => setCurrentPage('filter-rsi')}
            >
              Filter RSI
            </button>
          </nav>
        </div>
      </header>

      <main className="main-content">
        {currentPage === 'home' && <Home />}
        {currentPage === 'single-tf' && <SingleTF />}
        {currentPage === 'multi-tf' && <MultiTF />}
        {currentPage === 'filter-rsi' && <FilterRSI />}
      </main>

      <footer className="footer">
        <p>Tips: Eth: 0xb77fcef5c13e1a54bdfff9a7e5268743e81325c4</p>
      </footer>
    </div>
  )
}
