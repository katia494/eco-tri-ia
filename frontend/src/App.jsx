import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { ThemeProvider } from './context/ThemeContext'
import Connexion from './Connexion_inscription/Connexion'
import Inscription from './Connexion_inscription/Inscription'
import PasseOublie from './Connexion_inscription/Passe_Oublie'
import Scan from './Scan/Scan'
import BonnesPratiques from './Bonnes P/Bonnes_Pratiques'
import ChatBot from './ChatBot/chatbot'

function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Navigate to="/scan" replace />} />
          <Route path="/connexion" element={<Connexion />} />
          <Route path="/inscription" element={<Inscription />} />
          <Route path="/passe_oublie" element={<PasseOublie />} />

          <Route path="/scan" element={<Scan />} />
          <Route path="/pratiques" element={<BonnesPratiques />} />
          <Route path="/chatbot" element={<ChatBot />} />

          <Route path="/profil" element={<Navigate to="/scan" replace />} />
          <Route path="/dashboard" element={<Navigate to="/scan" replace />} />
          <Route path="/classement" element={<Navigate to="/scan" replace />} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  )
}

export default App