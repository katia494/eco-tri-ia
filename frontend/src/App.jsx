import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { ThemeProvider } from './context/ThemeContext'
import Connexion from './Connexion_inscription/Connexion'
import Inscription from './Connexion_inscription/Inscription'
import PasseOublie from './Connexion_inscription/Passe_Oublie'
import Scan from './Scan/Scan'
import Profil from './Profil/Profil'
import BonnesPratiques from './Bonnes P/Bonnes_Pratiques'
import ChatBot from './ChatBot/chatbot'
import Dashboard from './Dashboard/dashboard'
import LeGame from './Classement/Le game'

function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Navigate to="/connexion" replace />} />
          <Route path="/connexion" element={<Connexion />} />
          <Route path="/inscription" element={<Inscription />} />
          <Route path="/passe-oublie" element={<PasseOublie />} />
          <Route path="/scan" element={<Scan />} />
          <Route path="/profil" element={<Profil />} />
          <Route path="/pratiques" element={<BonnesPratiques />} />
          <Route path="/chatbot" element={<ChatBot />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/classement" element={<LeGame />} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  )
}

export default App
