import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';
import {
    Leaf, ScanLine, LayoutDashboard, Trophy, BookOpen, Coffee,
    Settings, TreePine, Camera, Lock, Medal, User, Building2,
    Map, Crosshair, LogOut, Save, Sun, Moon, Info, Droplet,
    Flame, Bird, Flower2, Check, MessageCircle
} from 'lucide-react';

/* ===================== Avatars disponibles ===================== */
const AVATARS = [
    { id: 'tree', icon: <TreePine className="w-6 h-6" />, bg: 'bg-green-50', border: 'border-ecoGreen', text: 'text-ecoGreen' },
    { id: 'droplet', icon: <Droplet className="w-6 h-6" />, bg: 'bg-blue-50', border: 'border-blue-300', text: 'text-blue-500' },
    { id: 'flame', icon: <Flame className="w-6 h-6" />, bg: 'bg-orange-50', border: 'border-orange-300', text: 'text-orange-500' },
    { id: 'sun', icon: <Sun className="w-6 h-6" />, bg: 'bg-yellow-50', border: 'border-yellow-300', text: 'text-yellow-600' },
    { id: 'bird', icon: <Bird className="w-6 h-6" />, bg: 'bg-gray-50', border: 'border-gray-300', text: 'text-gray-600' },
    { id: 'leaf', icon: <Leaf className="w-6 h-6" />, bg: 'bg-green-50', border: 'border-green-300', text: 'text-ecoGreen' },
    { id: 'flower', icon: <Flower2 className="w-6 h-6" />, bg: 'bg-purple-50', border: 'border-purple-300', text: 'text-purple-500' },
    { id: 'letter', icon: <span className="font-bold text-lg">A</span>, bg: 'bg-ecoBrown', border: 'border-ecoBrown', text: 'text-white' },
];

/* Récupération de l'icône grande version pour l'avatar principal */
const BIG_ICONS = {
    tree: <TreePine className="w-16 h-16 text-white" />,
    droplet: <Droplet className="w-16 h-16 text-white" />,
    flame: <Flame className="w-16 h-16 text-white" />,
    sun: <Sun className="w-16 h-16 text-white" />,
    bird: <Bird className="w-16 h-16 text-white" />,
    leaf: <Leaf className="w-16 h-16 text-white" />,
    flower: <Flower2 className="w-16 h-16 text-white" />,
    letter: <span className="font-bold text-4xl text-white">A</span>,
};

/* ===================== Sidebar (partagée) ===================== */
function Sidebar({ darkMode }) {
    const { pathname } = useLocation();
    const navItems = [
        { to: '/scan', icon: <ScanLine className="w-5 h-5" />, label: 'Scanner (Live)' },
        { to: '/dashboard', icon: <LayoutDashboard className="w-5 h-5" />, label: 'Tableau de bord' },
        { to: '/classement', icon: <Trophy className="w-5 h-5" />, label: 'Classement' },
        { to: '/pratiques', icon: <BookOpen className="w-5 h-5" />, label: 'Bonnes Pratiques' },
        { to: '/chatbot', icon: <MessageCircle className="w-5 h-5" />, label: 'Éco-Assistant IA' },
    ];

    const bg = darkMode ? 'bg-gray-900 border-gray-700' : 'bg-white border-gray-200';
    const text = darkMode ? 'text-gray-100' : 'text-gray-800';
    const sub = darkMode ? 'text-gray-400' : 'text-gray-600';
    const hover = darkMode ? 'hover:bg-gray-800' : 'hover:bg-gray-50';

    return (
        <aside className={`w-64 ${bg} border-r flex flex-col justify-between flex-shrink-0 overflow-hidden`}>
            <div>
                <div className="p-6 flex items-center space-x-3">
                    <div className="bg-ecoGreen p-2 rounded-lg text-white">
                        <Leaf className="w-6 h-6" />
                    </div>
                    <h1 className={`text-xl font-bold ${text} tracking-tight`}>One-Two-Tri Vision</h1>
                </div>
                <nav className="px-4 space-y-1">
                    {navItems.map(({ to, icon, label }) => {
                        const active = pathname === to;
                        return (
                            <Link key={to} to={to}
                                className={`flex items-center space-x-3 px-4 py-3 rounded-xl font-medium transition-colors
                                    ${active ? 'bg-green-50 text-ecoGreen' : `${sub} ${hover}`}`}>
                                {icon}<span>{label}</span>
                            </Link>
                        );
                    })}
                </nav>
            </div>
            <div className="p-4 space-y-2">
                <button className="w-full flex items-center justify-center space-x-2 py-2 bg-amber-50 text-ecoBrown rounded-lg text-sm font-medium hover:bg-amber-100 transition">
                    <Coffee className="w-4 h-4" /><span>Soutenir le projet</span>
                </button>
                {/* Profil actif */}
                <Link to="/profil"
                    className="flex items-center space-x-3 px-4 py-3 bg-green-50 rounded-xl border border-green-200 mt-2 cursor-pointer">
                    <div className="w-10 h-10 bg-ecoBrown rounded-full flex items-center justify-center text-white font-bold">
                        <TreePine className="w-5 h-5" />
                    </div>
                    <div className="flex-1 min-w-0">
                        <p className="text-sm font-bold text-ecoGreen truncate">katia</p>
                        <p className="text-xs text-green-600 truncate">Mon Profil</p>
                    </div>
                    <Settings className="w-4 h-4 text-ecoGreen" />
                </Link>
            </div>
        </aside>
    );
}

/* ===================== Toggle Switch ===================== */
function ThemeToggle({ darkMode, onToggle }) {
    return (
        <button
            onClick={onToggle}
            className={`relative inline-flex items-center w-14 h-7 rounded-full transition-colors duration-300
                ${darkMode ? 'bg-gray-600' : 'bg-gray-200'}`}
        >
            <span className={`absolute left-1 top-1 w-5 h-5 rounded-full flex items-center justify-center shadow transition-transform duration-300
                ${darkMode ? 'translate-x-7 bg-gray-900' : 'translate-x-0 bg-white'}`}>
                {darkMode
                    ? <Moon className="w-3 h-3 text-yellow-300" />
                    : <Sun className="w-3 h-3 text-yellow-500" />}
            </span>
        </button>
    );
}

/* ===================== Page Profil ===================== */
export default function Profil() {
    const { darkMode, toggleDark } = useTheme();
    const [selectedAvatar, setSelectedAvatar] = useState('tree');
    const [pseudo, setPseudo] = useState('katia');
    const [ville, setVille] = useState('');
    const [quartier, setQuartier] = useState('');
    const [saved, setSaved] = useState(false);
    const [locLoading, setLocLoading] = useState(false);


    /* Géolocalisation "Mettre à jour la position" */
    const handleGeoloc = () => {
        if (!navigator.geolocation) return;
        setLocLoading(true);
        navigator.geolocation.getCurrentPosition(
            async ({ coords }) => {
                try {
                    const res = await fetch(
                        `https://nominatim.openstreetmap.org/reverse?lat=${coords.latitude}&lon=${coords.longitude}&format=json&accept-language=fr`
                    );
                    const data = await res.json();
                    const a = data.address || {};
                    setVille(a.city || a.town || a.village || a.municipality || '');
                    setQuartier(a.neighbourhood || a.city_district || a.suburb || a.quarter || '');
                } catch { /* silencieux */ }
                finally { setLocLoading(false); }
            },
            () => setLocLoading(false),
            { enableHighAccuracy: true, timeout: 10000 }
        );
    };

    /* Sauvegarde simulée */
    const handleSave = (e) => {
        e.preventDefault();
        setSaved(true);
        setTimeout(() => setSaved(false), 2500);
    };

    /* Couleurs thème */
    const bg = darkMode ? 'bg-gray-950' : 'bg-ecoLight';
    const cardBg = darkMode ? 'bg-gray-900 border-gray-700' : 'bg-white border-gray-100';
    const headBg = darkMode ? 'bg-gray-900 border-gray-700' : 'bg-white border-gray-200';
    const textMain = darkMode ? 'text-gray-100' : 'text-gray-800';
    const textSub = darkMode ? 'text-gray-400' : 'text-gray-500';
    const inputCl = darkMode
        ? 'bg-gray-800 border-gray-600 text-gray-100 focus:ring-ecoGreen focus:border-ecoGreen'
        : 'border-gray-300 text-gray-800 focus:ring-ecoGreen focus:border-ecoGreen';
    const disabledCl = darkMode
        ? 'bg-gray-800 border-gray-700 text-gray-500 cursor-not-allowed'
        : 'bg-gray-100 border-gray-200 text-gray-500 cursor-not-allowed';
    const labelCl = darkMode ? 'text-gray-300' : 'text-gray-700';
    const divider = darkMode ? 'border-gray-700' : 'border-gray-100';

    return (
        <div className={`${bg} ${textMain} font-sans h-screen flex overflow-hidden transition-colors duration-300`}>
            <Sidebar darkMode={darkMode} />

            <main className="flex-1 flex flex-col h-screen overflow-y-auto relative">
                {/* Filigrane */}
                <div className="pointer-events-none fixed inset-0 flex items-center justify-center opacity-[0.03] z-0">
                    <Leaf className="w-[500px] h-[500px] text-ecoGreen" />
                </div>
                {/* Header */}
                <header className={`${headBg} px-8 py-5 border-b flex justify-between items-center sticky top-0 z-30 transition-colors duration-300`}>
                    <div>
                        <h2 className={`text-2xl font-bold ${textMain}`}>Mon Profil 👤</h2>
                        <p className={`text-sm ${textSub} mt-1`}>Gérez vos informations et votre avatar.</p>
                    </div>
                    <div className="flex items-center space-x-4">
                        <div className="text-right">
                            <p className={`text-xs ${textSub} uppercase font-bold tracking-wider`}>Score Global</p>
                            <p className="text-ecoGreen font-bold italic text-xs">A rec. BDD/API pts</p>
                        </div>
                    </div>
                </header>

                {/* Contenu */}
                <div className="p-8 max-w-5xl mx-auto w-full">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">

                        {/* ── COLONNE GAUCHE : Avatar ── */}
                        <div className="md:col-span-1 space-y-6">
                            <div className={`${cardBg} rounded-2xl shadow-sm border p-6 text-center transition-colors duration-300`}>
                                {/* Avatar principal */}
                                <div className="relative inline-block mb-4">
                                    <div className="w-32 h-32 bg-ecoBrown rounded-full mx-auto flex items-center justify-center border-4 border-white shadow-lg">
                                        {BIG_ICONS[selectedAvatar]}
                                    </div>
                                    <button className={`absolute bottom-0 right-0 ${darkMode ? 'bg-gray-800 border-gray-600' : 'bg-white border-gray-200'} p-2 rounded-full border shadow-sm text-gray-600 hover:text-ecoGreen transition`}>
                                        <Camera className="w-4 h-4" />
                                    </button>
                                </div>
                                <h3 className={`text-xl font-bold ${textMain}`}>{pseudo}</h3>
                                <p className={`text-sm ${textSub} mb-6 italic text-gray-400 text-xs`}>Inscrit depuis le : A rec. BDD/API</p>

                                {/* Grille avatars */}
                                <div className={`border-t ${divider} pt-6`}>
                                    <p className={`text-xs font-bold ${textSub} uppercase tracking-wider mb-3`}>Changer d'avatar</p>
                                    <div className="grid grid-cols-4 gap-2">
                                        {AVATARS.map(av => (
                                            <button
                                                key={av.id}
                                                onClick={() => setSelectedAvatar(av.id)}
                                                className={`w-full aspect-square rounded-xl flex items-center justify-center border-2 transition hover:scale-105
                                                    ${selectedAvatar === av.id
                                                        ? `${av.bg} ${av.border} ${av.text}`
                                                        : `${darkMode ? 'bg-gray-800 border-gray-700' : `${av.bg} border-transparent`} ${av.text}`}`}
                                            >
                                                {av.icon}
                                            </button>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* ── COLONNE DROITE : Infos + Paramètres ── */}
                        <div className="md:col-span-2 space-y-6">
                            <form onSubmit={handleSave} className={`${cardBg} rounded-2xl shadow-sm border p-8 space-y-6 transition-colors duration-300`}>

                                {/* Informations non-modifiables */}
                                <div>
                                    <h4 className={`text-sm font-bold ${textMain} border-b ${divider} pb-2 mb-4`}>Informations du compte</h4>
                                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                        <div>
                                            <label className={`block text-sm font-medium ${darkMode ? 'text-gray-400' : 'text-gray-600'} mb-1`}>Adresse e-mail</label>
                                            <div className="relative">
                                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                                    <Lock className="h-4 w-4 text-gray-400" />
                                                </div>
                                                <input type="email" defaultValue="" placeholder="A rec. BDD/API" disabled
                                                    className={`block w-full pl-9 pr-3 py-2 border rounded-lg text-sm italic text-gray-400 ${disabledCl}`} />
                                            </div>
                                        </div>
                                        <div>
                                            <label className={`block text-sm font-medium ${darkMode ? 'text-gray-400' : 'text-gray-600'} mb-1`}>Niveau actuel</label>
                                            <div className="relative">
                                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                                    <Medal className="h-4 w-4 text-yellow-500" />
                                                </div>
                                                <input type="text" defaultValue="" placeholder="A rec. BDD/API" disabled
                                                    className={`block w-full pl-9 pr-3 py-2 border rounded-lg text-sm font-medium italic text-gray-400 ${disabledCl}`} />
                                            </div>
                                        </div>
                                    </div>
                                    <p className={`text-xs ${textSub} mt-2 flex items-center`}>
                                        <Info className="inline w-3 h-3 mr-1" />
                                        Ces informations ne peuvent pas être modifiées directement.
                                    </p>
                                </div>

                                {/* Informations modifiables */}
                                <div>
                                    <h4 className={`text-sm font-bold ${textMain} border-b ${divider} pb-2 mb-4 mt-8`}>Informations personnelles</h4>
                                    <div className="space-y-4">
                                        {/* Pseudo */}
                                        <div>
                                            <label htmlFor="pseudo" className={`block text-sm font-medium ${labelCl} mb-1`}>Pseudo</label>
                                            <div className="relative">
                                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                                    <User className="h-4 w-4 text-gray-400" />
                                                </div>
                                                <input id="pseudo" type="text" value={pseudo}
                                                    onChange={e => setPseudo(e.target.value)}
                                                    className={`block w-full pl-9 pr-3 py-2 border rounded-lg outline-none transition text-sm ${inputCl}`} />
                                            </div>
                                        </div>

                                        {/* Localisation */}
                                        <div className="pt-2">
                                            <div className="flex items-center justify-between mb-2">
                                                <label className={`block text-sm font-medium ${labelCl}`}>Votre secteur de tri</label>
                                                <button type="button" onClick={handleGeoloc}
                                                    className="flex items-center text-xs font-bold text-ecoGreen bg-green-50 hover:bg-green-100 px-3 py-1.5 rounded-lg transition border border-green-200 disabled:opacity-50"
                                                    disabled={locLoading}>
                                                    <Crosshair className="w-3.5 h-3.5 mr-1.5" />
                                                    {locLoading ? 'Détection…' : 'Mettre à jour la position'}
                                                </button>
                                            </div>
                                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                                <div className="relative">
                                                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                                        <Building2 className="h-4 w-4 text-gray-400" />
                                                    </div>
                                                    <input id="ville" type="text" value={ville}
                                                        onChange={e => setVille(e.target.value)}
                                                        placeholder="Ville"
                                                        className={`block w-full pl-9 pr-3 py-2 border rounded-lg outline-none transition text-sm ${inputCl}`} />
                                                </div>
                                                <div className="relative">
                                                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                                        <Map className="h-4 w-4 text-gray-400" />
                                                    </div>
                                                    <input id="quartier" type="text" value={quartier}
                                                        onChange={e => setQuartier(e.target.value)}
                                                        placeholder="Quartier"
                                                        className={`block w-full pl-9 pr-3 py-2 border rounded-lg outline-none transition text-sm ${inputCl}`} />
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                {/* ── Section Paramètres d'affichage ── */}
                                <div>
                                    <h4 className={`text-sm font-bold ${textMain} border-b ${divider} pb-2 mb-4 mt-8`}>Paramètres d'affichage</h4>
                                    <div className={`flex items-center justify-between p-4 rounded-xl ${darkMode ? 'bg-gray-800' : 'bg-gray-50'} transition-colors duration-300`}>
                                        <div className="flex items-center space-x-3">
                                            {darkMode
                                                ? <Moon className="w-5 h-5 text-yellow-300" />
                                                : <Sun className="w-5 h-5 text-yellow-500" />}
                                            <div>
                                                <p className={`text-sm font-semibold ${textMain}`}>
                                                    {darkMode ? 'Thème sombre activé' : 'Thème clair activé'}
                                                </p>
                                                <p className={`text-xs ${textSub}`}>
                                                    {darkMode ? 'Basculer vers le thème clair' : 'Basculer vers le thème sombre'}
                                                </p>
                                            </div>
                                        </div>
                                        <ThemeToggle darkMode={darkMode} onToggle={toggleDark} />
                                    </div>
                                </div>

                                {/* Boutons action */}
                                <div className={`pt-6 border-t ${divider} flex items-center justify-between`}>
                                    <Link to="/connexion"
                                        className="text-sm font-medium text-red-500 hover:text-red-700 flex items-center transition">
                                        <LogOut className="w-4 h-4 mr-1.5" /> Déconnexion
                                    </Link>
                                    <button type="submit"
                                        className={`flex items-center px-6 py-2.5 rounded-xl text-sm font-bold shadow-sm transition
                                            ${saved ? 'bg-green-600 text-white' : 'bg-ecoGreen hover:bg-green-700 text-white'}`}>
                                        {saved
                                            ? <><Check className="w-4 h-4 mr-2" /> Enregistré !</>
                                            : <><Save className="w-4 h-4 mr-2" /> Enregistrer les modifications</>}
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}
