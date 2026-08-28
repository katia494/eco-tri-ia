import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';
import {
    Leaf, ScanLine, LayoutDashboard, Trophy, BookOpen, Coffee,
    Settings, MapPin, Star, Sprout, Lock, Unlock, Check,
    BarChart2, Award, GlassWater, Recycle, Package,
    BatteryCharging, Flame, Shirt, MoreVertical, MessageCircle
} from 'lucide-react';

/* ── Animation CSS ── */
const STYLES = `
@keyframes pulse-glow {
    0%   { box-shadow: 0 0 0 0   rgba(250,204,21,0.5); }
    70%  { box-shadow: 0 0 0 18px rgba(250,204,21,0);   }
    100% { box-shadow: 0 0 0 0   rgba(250,204,21,0);   }
}
.current-level { animation: pulse-glow 2s infinite; }
`;

/* ── Placeholder valeur dynamique ── */
const D = ({ white = false }) => (
    <span className={`italic text-xs font-normal ${white ? 'text-green-200' : 'text-gray-400'}`}>
        A rec. BDD/API
    </span>
);

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
                        <p className={`text-sm font-medium ${profName} truncate italic text-gray-400`}>A rec. BDD/API</p>
                        <p className={`text-xs ${profSub} truncate`}>Profil &amp; Reglages</p>
                    </div>
                    <Settings className="w-4 h-4 text-gray-400" />
                </Link>
            </div>
        </aside>
    );
}

/* ── Niveaux du parcours (noms et seuils fixes) ── */
const LEVELS = [
    {
        label: 'Citoyen Modele',
        pts: '1000 pts',
        side: 'left',
        state: 'locked',
        dim: 'w-20 h-20',
        icon: <Lock className="w-8 h-8" />,
        style: 'border-gray-300 text-gray-400 bg-white',
        textColor: 'text-gray-600',
        ptColor: 'text-gray-400',
        opacity: 'opacity-60',
    },
    {
        label: 'Trieur Engage',
        pts: null,
        side: 'right',
        state: 'next',
        dim: 'w-20 h-20',
        icon: <Unlock className="w-8 h-8 opacity-50" />,
        style: 'border-dashed border-ecoGreen text-ecoGreen bg-green-50',
        textColor: 'text-gray-700',
        ptColor: 'text-ecoGreen',
        opacity: '',
    },
    {
        label: 'Apprenti Recycleur',
        pts: null,
        side: 'left',
        state: 'current',
        dim: 'w-24 h-24',
        icon: <Sprout className="w-12 h-12" />,
        style: 'bg-yellow-400 border-white text-white current-level',
        textColor: 'text-yellow-600',
        ptColor: 'text-gray-500',
        opacity: '',
    },
    {
        label: 'Graine de Trieur',
        pts: 'Termine (100 pts)',
        side: 'right',
        state: 'done',
        dim: 'w-16 h-16',
        icon: <Check className="w-8 h-8" />,
        style: 'bg-ecoGreen border-white text-white',
        textColor: 'text-gray-800',
        ptColor: 'text-gray-500',
        opacity: '',
    },
];

/* ── Badges ── */
const BADGES_UNLOCKED = [
    { icon: <GlassWater className="w-6 h-6 text-blue-500" />, bg: 'bg-blue-100 border-blue-200', label: 'Ami du Verre' },
    { icon: <Recycle className="w-6 h-6 text-yellow-600" />, bg: 'bg-yellow-100 border-yellow-200', label: '1er Tri' },
    { icon: <Package className="w-6 h-6 text-ecoBrown" />, bg: 'bg-amber-50 border-amber-100', label: 'Roi du Carton' },
];
const BADGES_LOCKED = [
    { icon: <BatteryCharging className="w-6 h-6 text-gray-400" />, label: 'Sauveur de Piles' },
    { icon: <Flame className="w-6 h-6 text-gray-400" />, label: 'Serie 7 Jours' },
    { icon: <Shirt className="w-6 h-6 text-gray-400" />, label: 'Mode Durable' },
];

/* ── Leaderboard (top 3 style fixe, données dynamiques) ── */
const LB_STYLES = [
    { rank: '1', bg: 'bg-yellow-50 border-yellow-100', rankCl: 'text-yellow-500', avatarBorder: 'border-yellow-400', scoreCl: 'text-yellow-600' },
    { rank: '2', bg: 'bg-gray-50 border-gray-200', rankCl: 'text-gray-400', avatarBorder: 'border-gray-300', scoreCl: 'text-gray-600' },
    { rank: '3', bg: 'bg-orange-50 border-orange-100', rankCl: 'text-orange-400', avatarBorder: 'border-orange-300', scoreCl: 'text-orange-600' },
];

/* ===================== Page Classement ===================== */
export default function LeGame() {
    const { darkMode } = useTheme();

    const pageBg = darkMode ? 'bg-gray-950 text-gray-100' : 'bg-ecoLight text-gray-800';
    const headBg = darkMode ? 'bg-gray-900 border-gray-700' : 'bg-white border-gray-200';
    const headTxt = darkMode ? 'text-gray-100' : 'text-gray-800';
    const subTxt = darkMode ? 'text-gray-400' : 'text-gray-500';
    const cardBg = darkMode ? 'bg-gray-900 border-gray-700' : 'bg-white border-gray-100';
    const cardTxt = darkMode ? 'text-gray-100' : 'text-gray-800';
    const pathLine = darkMode ? 'bg-gray-700' : 'bg-gray-100';

    return (
        <div className={`${pageBg} font-sans h-screen flex overflow-hidden transition-colors duration-300`}>
            <style>{STYLES}</style>
            <Sidebar />

            <main className="flex-1 flex flex-col h-screen overflow-y-auto relative">
                {/* Filigrane */}
                <div className="pointer-events-none fixed inset-0 flex items-center justify-center opacity-[0.03] z-0">
                    <Leaf className="w-[500px] h-[500px] text-ecoGreen" />
                </div>

                {/* Header */}
                <header className={`${headBg} px-8 py-5 border-b flex justify-between items-center sticky top-0 z-30 transition-colors duration-300`}>
                    <div>
                        <h2 className={`text-2xl font-bold ${headTxt}`}>Espace Competition 🏆</h2>
                        <p className={`text-sm ${subTxt} mt-1 flex items-center gap-1`}>
                            <MapPin className="w-4 h-4 text-ecoBrown" />
                            Classement local : <strong className={`ml-1 ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}><D /></strong>
                        </p>
                    </div>
                    <div className="flex items-center space-x-4">
                        <div className="text-right">
                            <p className={`text-xs ${subTxt} uppercase font-bold tracking-wider`}>Score Global</p>
                            <p className="text-ecoGreen font-bold flex items-center justify-end gap-1">
                                <Star className="w-4 h-4" /> <D />
                            </p>
                        </div>
                    </div>
                </header>

                {/* Grille */}
                <div className="p-8 max-w-7xl mx-auto w-full grid grid-cols-1 lg:grid-cols-3 gap-8 relative z-10">

                    {/* ── COLONNE GAUCHE+CENTRE : Parcours ── */}
                    <div className={`col-span-1 lg:col-span-2 ${cardBg} rounded-2xl shadow-sm border p-8 flex flex-col transition-colors duration-300`}>
                        <h3 className={`text-xl font-bold ${cardTxt} mb-2`}>Ton Parcours</h3>
                        <p className={`text-sm ${subTxt} mb-8`}>Continue de trier pour debloquer de nouveaux paliers et aider ta ville !</p>

                        {/* Chemin de progression */}
                        <div className="relative flex-1 flex flex-col items-center justify-center py-10 min-h-[420px]">
                            {/* Ligne de fond */}
                            <div className={`absolute top-10 bottom-10 left-1/2 w-3 ${pathLine} -translate-x-1/2 rounded-full`} />
                            {/* Ligne progression */}
                            <div className="absolute bottom-10 h-[45%] left-1/2 w-3 bg-ecoGreen -translate-x-1/2 rounded-full" />

                            {LEVELS.map((lv, i) => (
                                <div key={lv.label} className={`relative z-10 w-full flex justify-center ${i < LEVELS.length - 1 ? 'mb-16' : ''} ${lv.opacity}`}>
                                    {/* Label gauche */}
                                    {lv.side === 'left' && (
                                        <div className="absolute right-1/2 pr-16 top-1/2 -translate-y-1/2 text-right">
                                            <h4 className={`font-bold ${lv.textColor} ${lv.state === 'current' ? 'text-lg' : ''}`}>{lv.label}</h4>
                                            <p className={`text-xs ${lv.ptColor}`}>
                                                {lv.state === 'current' ? <><D /> pts</> : lv.pts}
                                            </p>
                                        </div>
                                    )}
                                    {/* Label droit */}
                                    {lv.side === 'right' && (
                                        <div className="absolute left-1/2 pl-16 top-1/2 -translate-y-1/2 text-left">
                                            <h4 className={`font-bold ${lv.textColor}`}>{lv.label}</h4>
                                            <p className={`text-xs ${lv.ptColor}`}>
                                                {lv.state === 'next' ? <span className="italic text-xs text-ecoGreen">Encore <D /> !</span> : lv.pts}
                                            </p>
                                        </div>
                                    )}
                                    {/* Cercle niveau */}
                                    <div className={`${lv.dim} ${lv.style} border-4 rounded-full flex items-center justify-center shadow-lg z-20`}>
                                        {lv.icon}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* ── COLONNE DROITE ── */}
                    <div className="space-y-6">

                        {/* Leaderboard */}
                        <div className={`${cardBg} rounded-2xl shadow-sm border p-6 transition-colors duration-300`}>
                            <div className="flex items-center justify-between mb-6">
                                <h3 className={`text-lg font-bold ${cardTxt} flex items-center`}>
                                    <BarChart2 className="w-5 h-5 mr-2 text-ecoGreen" /> Top <D />
                                </h3>
                                <span className={`text-xs font-medium px-2 py-1 rounded ${darkMode ? 'bg-gray-700 text-gray-300' : 'bg-gray-100 text-gray-600'}`}>Ce mois</span>
                            </div>

                            <div className="space-y-3">
                                {LB_STYLES.map(({ rank, bg, rankCl, avatarBorder, scoreCl }) => (
                                    <div key={rank} className={`flex items-center p-3 rounded-xl ${bg} border`}>
                                        <span className={`${rankCl} font-black text-lg w-6 text-center mr-3`}>{rank}</span>
                                        <div className={`w-10 h-10 rounded-full bg-white border-2 ${avatarBorder} flex items-center justify-center text-sm font-bold text-gray-700 mr-3 shadow-sm`}>
                                            <D />
                                        </div>
                                        <div className="flex-1 min-w-0">
                                            <p className={`text-sm font-bold ${darkMode ? 'text-gray-100' : 'text-gray-900'} truncate`}><D /></p>
                                            <p className={`text-xs ${subTxt} truncate`}><D /></p>
                                        </div>
                                        <span className={`font-bold ${scoreCl} ml-2`}><D /></span>
                                    </div>
                                ))}

                                {/* Separateur */}
                                <div className="flex justify-center py-1">
                                    <MoreVertical className="w-4 h-4 text-gray-300" />
                                </div>

                                {/* Utilisateur actuel */}
                                <div className="flex items-center p-3 rounded-xl bg-ecoGreen text-white shadow-md scale-105">
                                    <span className="font-black text-lg w-6 text-center mr-3 text-green-200"><D white /></span>
                                    <div className="w-10 h-10 rounded-full bg-white flex items-center justify-center text-sm font-bold text-ecoGreen mr-3">A</div>
                                    <div className="flex-1 min-w-0">
                                        <p className="text-sm font-bold text-white truncate"><D white /> (Toi)</p>
                                        <p className="text-xs text-green-100"><D white /></p>
                                    </div>
                                    <span className="font-bold text-white ml-2"><D white /></span>
                                </div>
                            </div>
                        </div>

                        {/* Badges */}
                        <div className={`${cardBg} rounded-2xl shadow-sm border p-6 transition-colors duration-300`}>
                            <div className="flex items-center justify-between mb-4">
                                <h3 className={`text-lg font-bold ${cardTxt} flex items-center`}>
                                    <Award className="w-5 h-5 mr-2 text-ecoBrown" /> Tes Badges
                                </h3>
                                <span className="text-xs font-bold text-ecoGreen bg-green-50 px-2 py-1 rounded-full">
                                    <D /> / 12
                                </span>
                            </div>

                            <div className="grid grid-cols-3 gap-3">
                                {/* Badges debloqués */}
                                {BADGES_UNLOCKED.map(b => (
                                    <div key={b.label} className="flex flex-col items-center p-2 group cursor-pointer">
                                        <div className={`w-14 h-14 rounded-2xl ${b.bg} border flex items-center justify-center mb-2 shadow-sm group-hover:scale-110 transition`}>
                                            {b.icon}
                                        </div>
                                        <span className={`text-[10px] font-bold text-center ${cardTxt} leading-tight`}>{b.label}</span>
                                    </div>
                                ))}
                                {/* Badges bloqués */}
                                {BADGES_LOCKED.map(b => (
                                    <div key={b.label} className="flex flex-col items-center p-2 opacity-40">
                                        <div className={`w-14 h-14 rounded-2xl border flex items-center justify-center mb-2 ${darkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-100 border-gray-200'}`}>
                                            {b.icon}
                                        </div>
                                        <span className={`text-[10px] font-medium text-center ${subTxt} leading-tight`}>{b.label}</span>
                                    </div>
                                ))}
                            </div>
                        </div>

                    </div>
                </div>
            </main>
        </div>
    );
}
