import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';
import {
    Leaf, ScanLine, LayoutDashboard, Trophy, BookOpen, Coffee,
    Settings, MapPin, Sprout, Package, Star, CloudSnow, Flame,
    Target, Medal, MessageCircle, ChevronRight, GlassWater,
    BatteryFull, FileText
} from 'lucide-react';

/* ── Valeur dynamique (bdd/api) ── */
function ApiValue({ children, className = '' }) {
    return (
        <span className={`text-gray-400 italic text-xs font-normal ${className}`}>
            {children || 'A recuperer via bdd/api'}
        </span>
    );
}

/* ===================== Sidebar ===================== */
function Sidebar() {
    const { pathname } = useLocation();
    const { darkMode } = useTheme();

    const navItems = [
        { to: '/scan', icon: <ScanLine className="w-5 h-5" />, label: 'Scanner (Live)' },
        { to: '/dashboard', icon: <LayoutDashboard className="w-5 h-5" />, label: 'Tableau de bord' },
        { to: '/classement', icon: <Trophy className="w-5 h-5" />, label: 'Classement' },
        { to: '/pratiques', icon: <BookOpen className="w-5 h-5" />, label: 'Bonnes Pratiques' },
        { to: '/chatbot', icon: <MessageCircle className="w-5 h-5" />, label: 'Eco-Assistant IA' },
    ];

    const asideBg = darkMode ? 'bg-gray-900 border-gray-700' : 'bg-white border-gray-200';
    const titleCl = darkMode ? 'text-gray-100' : 'text-gray-800';
    const navIdle = darkMode ? 'text-gray-400 hover:bg-gray-800' : 'text-gray-600 hover:bg-gray-50';
    const profBg = darkMode ? 'bg-gray-800 border-gray-700 hover:bg-gray-700' : 'bg-gray-50 border-gray-100 hover:bg-gray-100';
    const profName = darkMode ? 'text-gray-100' : 'text-gray-900';
    const profSub = darkMode ? 'text-gray-400' : 'text-gray-500';

    return (
        <aside className={`w-64 ${asideBg} border-r flex flex-col justify-between flex-shrink-0 overflow-hidden transition-colors duration-300`}>
            <div>
                <div className="p-6 flex items-center space-x-3">
                    <div className="bg-ecoGreen p-2 rounded-lg text-white">
                        <Leaf className="w-6 h-6" />
                    </div>
                    <h1 className={`text-xl font-bold ${titleCl} tracking-tight`}>One-Two-Tri Vision</h1>
                </div>
                <nav className="px-4 space-y-1">
                    {navItems.map(({ to, icon, label }) => {
                        const active = pathname === to;
                        return (
                            <Link key={to} to={to}
                                className={`flex items-center space-x-3 px-4 py-3 rounded-xl font-medium transition-colors
                                    ${active ? 'bg-green-50 text-ecoGreen' : navIdle}`}>
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
                <Link to="/profil" className={`flex items-center space-x-3 px-4 py-3 ${profBg} rounded-xl border mt-2 cursor-pointer transition`}>
                    <div className="w-10 h-10 bg-ecoBrown rounded-full flex items-center justify-center text-white font-bold">A</div>
                    <div className="flex-1 min-w-0">
                        <p className={`text-sm font-medium ${profName} truncate`}><ApiValue /></p>
                        <p className={`text-xs ${profSub} truncate`}>Profil &amp; Reglages</p>
                    </div>
                    <Settings className="w-4 h-4 text-gray-400" />
                </Link>
            </div>
        </aside>
    );
}

/* ── Jours du graphique (structure fixe) ── */
const DAYS = [
    { label: 'Lun', h: 'h-12', active: false },
    { label: 'Mar', h: 'h-24', active: false },
    { label: 'Mer', h: 'h-40', active: true },
    { label: 'Jeu', h: 'h-16', active: false },
    { label: 'Ven', h: 'h-4', active: false },
    { label: 'Sam', h: 'h-1', active: false },
    { label: 'Dim', h: 'h-1', active: false },
];

/* ── Items historique (3 slots, icones connues) ── */
const HISTORY = [
    { bg: 'bg-yellow-100', color: 'text-yellow-600', icon: <GlassWater className="w-5 h-5" /> },
    { bg: 'bg-red-100', color: 'text-red-600', icon: <BatteryFull className="w-5 h-5" /> },
    { bg: 'bg-blue-100', color: 'text-blue-600', icon: <FileText className="w-5 h-5" /> },
];

/* ===================== Page Dashboard ===================== */
export default function Dashboard() {
    const { darkMode } = useTheme();
    const [period, setPeriod] = useState('week');

    const pageBg = darkMode ? 'bg-gray-950 text-gray-100' : 'bg-ecoLight text-gray-800';
    const headBg = darkMode ? 'bg-gray-900 border-gray-700' : 'bg-white border-gray-200';
    const headTxt = darkMode ? 'text-gray-100' : 'text-gray-800';
    const subTxt = darkMode ? 'text-gray-400' : 'text-gray-500';
    const cardBg = darkMode ? 'bg-gray-900 border-gray-700' : 'bg-white border-gray-100';
    const cardTxt = darkMode ? 'text-gray-100' : 'text-gray-800';
    const cardSub = darkMode ? 'text-gray-400' : 'text-gray-500';
    const selectCl = darkMode ? 'bg-gray-800 border-gray-600 text-gray-300' : 'bg-gray-50 border-gray-200 text-gray-700';

    return (
        <div className={`${pageBg} font-sans h-screen flex overflow-hidden transition-colors duration-300`}>
            <Sidebar />

            <main className="flex-1 flex flex-col h-screen overflow-y-auto relative">

                {/* Filigrane */}
                <div className="pointer-events-none fixed inset-0 flex items-center justify-center opacity-[0.03] z-0">
                    <Leaf className="w-[500px] h-[500px] text-ecoGreen" />
                </div>

                {/* ── Header ── */}
                <header className={`${headBg} px-8 py-5 border-b flex justify-between items-center sticky top-0 z-30 transition-colors duration-300`}>
                    <div>
                        <h2 className={`text-2xl font-bold ${headTxt}`}>
                            Voici votre impact, <ApiValue className="text-lg" /> 🌍
                        </h2>
                        <p className={`text-sm ${subTxt} mt-1 flex items-center gap-1`}>
                            <MapPin className="w-4 h-4 text-ecoBrown" />
                            Localisation active :
                            <strong className={`ml-1 ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>
                                <ApiValue />
                            </strong>
                        </p>
                    </div>
                    <div className="flex items-center space-x-4">
                        <div className="text-right">
                            <p className={`text-xs ${subTxt} uppercase font-bold tracking-wider`}>Niveau Actuel</p>
                            <p className="text-ecoGreen font-bold flex items-center justify-end">
                                <Sprout className="w-4 h-4 mr-1" />
                                <ApiValue />
                            </p>
                        </div>
                        <div className="w-12 h-12 bg-yellow-100 rounded-full flex items-center justify-center border-2 border-yellow-400 shadow-sm">
                            <span className="text-yellow-600 text-[9px] font-bold text-center leading-tight">API</span>
                        </div>
                    </div>
                </header>

                {/* ── Contenu ── */}
                <div className="p-8 max-w-7xl mx-auto w-full space-y-8 relative z-10">

                    {/* Section 1 : KPIs */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">

                        <div className={`${cardBg} p-6 rounded-2xl shadow-sm border flex items-center space-x-4 transition-colors duration-300`}>
                            <div className="p-4 bg-blue-50 text-blue-600 rounded-xl flex-shrink-0">
                                <Package className="w-7 h-7" />
                            </div>
                            <div>
                                <p className={`text-sm ${cardSub} font-medium`}>Dechets tries</p>
                                <p className={`text-2xl font-bold ${cardTxt}`}><ApiValue /></p>
                            </div>
                        </div>

                        <div className={`${cardBg} p-6 rounded-2xl shadow-sm border flex items-center space-x-4 transition-colors duration-300`}>
                            <div className="p-4 bg-yellow-50 text-yellow-600 rounded-xl flex-shrink-0">
                                <Star className="w-7 h-7" />
                            </div>
                            <div>
                                <p className={`text-sm ${cardSub} font-medium`}>Score Total</p>
                                <p className={`text-2xl font-bold ${cardTxt}`}>
                                    <ApiValue /> <span className={`text-sm font-normal ${cardSub}`}>pts</span>
                                </p>
                            </div>
                        </div>

                        <div className={`${cardBg} p-6 rounded-2xl shadow-sm border flex items-center space-x-4 transition-colors duration-300`}>
                            <div className="p-4 bg-ecoGreen/10 text-ecoGreen rounded-xl flex-shrink-0">
                                <CloudSnow className="w-7 h-7" />
                            </div>
                            <div>
                                <p className={`text-sm ${cardSub} font-medium`}>CO2 Evite (est.)</p>
                                <p className={`text-2xl font-bold ${cardTxt}`}>
                                    <ApiValue /> <span className={`text-sm font-normal ${cardSub}`}>kg</span>
                                </p>
                            </div>
                        </div>

                        <div className={`${cardBg} p-6 rounded-2xl shadow-sm border flex items-center space-x-4 transition-colors duration-300`}>
                            <div className="p-4 bg-orange-50 text-orange-500 rounded-xl flex-shrink-0">
                                <Flame className="w-7 h-7" />
                            </div>
                            <div>
                                <p className={`text-sm ${cardSub} font-medium`}>Serie en cours</p>
                                <p className={`text-2xl font-bold ${cardTxt}`}>
                                    <ApiValue /> <span className={`text-sm font-normal ${cardSub}`}>jours</span>
                                </p>
                            </div>
                        </div>
                    </div>

                    {/* Section 2 : Graphique + Historique */}
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

                        {/* Graphique */}
                        <div className={`lg:col-span-2 ${cardBg} rounded-2xl shadow-sm border p-6 flex flex-col transition-colors duration-300`}>
                            <div className="flex justify-between items-center mb-6">
                                <div>
                                    <h3 className={`text-lg font-bold ${cardTxt}`}>Activite hebdomadaire</h3>
                                    <p className={`text-xs ${cardSub} mt-0.5`}>Dechets scannes par jour — <ApiValue /></p>
                                </div>
                                <select
                                    value={period}
                                    onChange={e => setPeriod(e.target.value)}
                                    className={`${selectCl} border text-sm rounded-lg px-3 py-1.5 outline-none transition-colors`}>
                                    <option value="week">Cette semaine</option>
                                    <option value="month">Ce mois-ci</option>
                                </select>
                            </div>

                            <div className="flex-1 flex items-end justify-between space-x-2 pt-10 pb-2 border-b border-gray-100">
                                {DAYS.map(({ label, h, active }) => (
                                    <div key={label} className="w-full flex flex-col items-center group relative">
                                        <div className={`w-10 rounded-t-md ${h} transition-all
                                            ${active
                                                ? 'bg-ecoGreen shadow-sm group-hover:bg-green-700'
                                                : darkMode
                                                    ? 'bg-gray-700 group-hover:bg-gray-600'
                                                    : 'bg-green-100 group-hover:bg-green-200'
                                            }`}
                                        />
                                        <span className={`text-xs mt-2 ${active ? `font-bold ${cardTxt}` : cardSub}`}>
                                            {label}
                                        </span>
                                    </div>
                                ))}
                            </div>
                            <p className={`text-[11px] ${cardSub} mt-3 italic`}>
                                * Hauteurs en demo. Valeurs reelles a recuperer via bdd/api.
                            </p>
                        </div>

                        {/* Historique */}
                        <div className={`${cardBg} rounded-2xl shadow-sm border p-6 flex flex-col transition-colors duration-300`}>
                            <div className="flex justify-between items-center mb-6">
                                <h3 className={`text-lg font-bold ${cardTxt}`}>Derniers scans</h3>
                                <a href="#" className="text-ecoGreen text-sm font-medium hover:underline flex items-center">
                                    Tout voir <ChevronRight className="w-3 h-3 ml-0.5" />
                                </a>
                            </div>

                            <div className="space-y-4 flex-1">
                                {HISTORY.map((item, i) => (
                                    <div key={i} className="flex items-start space-x-3">
                                        <div className={`w-10 h-10 rounded-full ${item.bg} ${item.color} flex items-center justify-center flex-shrink-0`}>
                                            {item.icon}
                                        </div>
                                        <div className="flex-1 min-w-0">
                                            <p className={`text-sm font-bold ${cardTxt} truncate`}><ApiValue /></p>
                                            <p className={`text-xs ${cardSub}`}><ApiValue /> - <ApiValue /></p>
                                        </div>
                                        <span className="text-xs font-bold text-ecoGreen bg-green-50 px-2 py-1 rounded-full flex-shrink-0">
                                            <ApiValue />
                                        </span>
                                    </div>
                                ))}
                            </div>

                            <Link to="/scan"
                                className="w-full mt-4 py-2 bg-ecoGreen text-white rounded-lg text-sm font-medium hover:bg-green-700 transition flex items-center justify-center">
                                <ScanLine className="w-4 h-4 mr-2" /> Lancer un nouveau scan
                            </Link>
                        </div>
                    </div>

                    {/* Section 3 : Progression */}
                    <div className="bg-ecoBrown text-white rounded-2xl shadow-sm p-6 relative overflow-hidden">
                        <Target className="absolute -right-10 -bottom-10 w-48 h-48 opacity-10" />
                        <div className="relative z-10 md:flex items-center justify-between gap-8">
                            <div className="mb-4 md:mb-0">
                                <h3 className="text-xl font-bold mb-1 flex items-center gap-2">
                                    Objectif : <ApiValue className="text-white text-base not-italic font-bold" />
                                    <Medal className="w-5 h-5 text-yellow-400" />
                                </h3>
                                <p className="text-sm text-amber-50">
                                    Plus que <ApiValue className="text-amber-200 font-bold not-italic" /> points pour passer au niveau superieur.
                                </p>
                            </div>
                            <div className="w-full md:w-1/2 flex-shrink-0">
                                <div className="flex justify-between text-xs font-medium mb-2 text-amber-100">
                                    <span><ApiValue className="text-amber-100 not-italic" /></span>
                                    <span><ApiValue className="text-amber-100 not-italic" /></span>
                                </div>
                                <div className="w-full bg-white/20 rounded-full h-3">
                                    <div className="bg-yellow-400 h-3 rounded-full" style={{ width: '0%' }} />
                                </div>
                                <p className="text-[10px] text-amber-200 italic mt-1">Progression a recuperer via bdd/api</p>
                            </div>
                        </div>
                    </div>

                </div>
            </main>
        </div>
    );
}
