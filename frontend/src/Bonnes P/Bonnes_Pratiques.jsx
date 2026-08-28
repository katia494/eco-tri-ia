import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';
import {
    Leaf, ScanLine, LayoutDashboard, Trophy, BookOpen, Coffee,
    Settings, Sprout, Lightbulb, Layers, Package, GlassWater,
    FileText, BatteryWarning, CheckCircle2, Info, XCircle,
    AlertTriangle, MapPin, Ghost, Droplets, Thermometer,
    Receipt, Pizza, MessageCircle
} from 'lucide-react';

/* ===================== Sidebar ===================== */
function Sidebar() {
    const { pathname } = useLocation();
    const { darkMode } = useTheme();

    const navItems = [
        { to: '/scan', icon: <ScanLine className="w-5 h-5" />, label: 'Scanner (Live)' },
        { to: '/dashboard', icon: <LayoutDashboard className="w-5 h-5" />, label: 'Tableau de bord' },
        { to: '/classement', icon: <Trophy className="w-5 h-5" />, label: 'Classement' },
        { to: '/pratiques', icon: <BookOpen className="w-5 h-5" />, label: 'Bonnes Pratiques' },
        { to: '/chatbot', icon: <MessageCircle className="w-5 h-5" />, label: 'Éco-Assistant IA' },
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
                        <p className={`text-xs ${profSub} truncate`}>Profil &amp; Réglages</p>
                    </div>
                    <Settings className="w-4 h-4 text-gray-400" />
                </Link>
            </div>
        </aside>
    );
}

/* ===================== Données des cartes matières ===================== */
const MATIERES = [
    {
        title: 'Plastiques & Métaux',
        sub: 'Bac Jaune',
        headerBg: 'bg-yellow-100 border-yellow-200',
        iconBg: 'bg-yellow-400 text-yellow-900',
        icon: <Package className="w-6 h-6" />,
        oui: "Bouteilles, flacons, boîtes de conserve, canettes, barquettes, capsules de café.",
        conseil: "Laissez les bouchons sur les bouteilles plastiques, ils se recyclent avec ! Aplatissez les bouteilles dans la longueur.",
        non: "N'imbriquez pas les emballages les uns dans les autres, cela empêche les machines de les reconnaître.",
    },
    {
        title: 'Emballages en Verre',
        sub: 'Bac Vert / Colonne à verre',
        headerBg: 'bg-green-100 border-green-200',
        iconBg: 'bg-ecoGreen text-white',
        icon: <GlassWater className="w-6 h-6" />,
        oui: "Bouteilles de vin/jus, pots de confiture, bocaux de sauces.",
        conseil: "Enlevez impérativement les bouchons et couvercles (à jeter dans le bac jaune !).",
        non: "Vaisselle cassée, verres à boire, miroirs ou ampoules. Leur composition chimique est différente du verre d'emballage.",
    },
    {
        title: 'Papiers & Cartons',
        sub: 'Bac Jaune (ou Bleu selon les villes)',
        headerBg: 'bg-blue-50 border-blue-100',
        iconBg: 'bg-blue-500 text-white',
        icon: <FileText className="w-6 h-6" />,
        oui: "Boîtes de céréales, journaux, magazines, enveloppes (même avec fenêtre), courriers.",
        conseil: "Aplatissez bien les gros cartons de livraison pour gagner de la place dans la poubelle.",
        non: "Mouchoirs en papier, essuie-tout (compost ou ordures ménagères). Papiers très gras ou salis.",
    },
    {
        title: 'Déchets Spéciaux',
        sub: 'Points de collecte spécifiques',
        headerBg: 'bg-red-50 border-red-100',
        iconBg: 'bg-red-500 text-white',
        icon: <BatteryWarning className="w-6 h-6" />,
        attn: "Piles, batteries, ampoules, médicaments, vêtements et petits électroménagers ne vont jamais à la poubelle.",
        solution: "Utilisez l'outil \"Scanner\" de l'application Eco-Tri, nous vous indiquerons le point de dépôt le plus proche !",
    },
];

/* Carte matière */
function CarteMatiere({ m, cardBg, cardTxt, cardSub }) {
    return (
        <div className={`${cardBg} rounded-2xl border shadow-sm overflow-hidden hover:shadow-md transition`}>
            <div className={`${m.headerBg} p-4 border-b flex items-center space-x-3`}>
                <div className={`p-2 ${m.iconBg} rounded-lg`}>{m.icon}</div>
                <div>
                    <h4 className={`font-bold ${cardTxt}`}>{m.title}</h4>
                    <p className={`text-xs font-medium ${cardSub}`}>{m.sub}</p>
                </div>
            </div>
            <div className="p-5 space-y-3">
                {m.oui && (
                    <div className="flex items-start space-x-3">
                        <CheckCircle2 className="w-5 h-5 text-ecoGreen shrink-0 mt-0.5" />
                        <p className={`text-sm ${cardSub}`}><strong className={cardTxt}>Oui :</strong> {m.oui}</p>
                    </div>
                )}
                {m.conseil && (
                    <div className="flex items-start space-x-3">
                        <Info className="w-5 h-5 text-blue-500 shrink-0 mt-0.5" />
                        <p className={`text-sm ${cardSub}`}><strong className={cardTxt}>Conseil :</strong> {m.conseil}</p>
                    </div>
                )}
                {m.non && (
                    <div className="flex items-start space-x-3">
                        <XCircle className="w-5 h-5 text-red-500 shrink-0 mt-0.5" />
                        <p className={`text-sm ${cardSub}`}><strong className={cardTxt}>Non :</strong> {m.non}</p>
                    </div>
                )}
                {m.attn && (
                    <div className="flex items-start space-x-3">
                        <AlertTriangle className="w-5 h-5 text-orange-500 shrink-0 mt-0.5" />
                        <p className={`text-sm ${cardSub}`}><strong className={cardTxt}>Attention :</strong> {m.attn}</p>
                    </div>
                )}
                {m.solution && (
                    <div className="flex items-start space-x-3">
                        <MapPin className="w-5 h-5 text-ecoGreen shrink-0 mt-0.5" />
                        <p className={`text-sm ${cardSub}`}><strong className={cardTxt}>Solution :</strong> {m.solution}</p>
                    </div>
                )}
            </div>
        </div>
    );
}

/* ===================== Faux-amis ===================== */
const FAUX_AMIS = [
    { icon: <GlassWater className="w-6 h-6" />, label: 'Verre à boire', desc: "Poubelle grise (ne fond pas à la même température que le verre d'emballage)" },
    { icon: <Thermometer className="w-6 h-6" />, label: 'Médicaments', desc: 'À rapporter en pharmacie (Cyclamed)' },
    { icon: <Receipt className="w-6 h-6" />, label: 'Tickets de caisse', desc: 'Poubelle grise (trop chimiques pour être recyclés avec le papier)' },
    { icon: <Pizza className="w-6 h-6" />, label: 'Boîte à pizza', desc: 'Bac jaune si propre. Si très grasse : poubelle grise.' },
];

/* ===================== Page principale ===================== */
export default function BonnesPratiques() {
    const { darkMode } = useTheme();

    const pageBg = darkMode ? 'bg-gray-950 text-gray-100' : 'bg-ecoLight text-gray-800';
    const headBg = darkMode ? 'bg-gray-900 border-gray-700' : 'bg-white border-gray-200';
    const headTxt = darkMode ? 'text-gray-100' : 'text-gray-800';
    const subTxt = darkMode ? 'text-gray-400' : 'text-gray-500';
    const cardBg = darkMode ? 'bg-gray-900 border-gray-700' : 'bg-white border-gray-100';
    const cardTxt = darkMode ? 'text-gray-100' : 'text-gray-800';
    const cardSub = darkMode ? 'text-gray-400' : 'text-gray-600';
    const fauxBg = darkMode ? 'bg-gray-800 border-gray-700' : 'bg-gray-50 border-gray-100';
    const fauxIcon = darkMode ? 'bg-gray-700 text-gray-300' : 'bg-white text-gray-500';
    const sectionBg = darkMode ? 'bg-gray-900 border-gray-700' : 'bg-white border-gray-200';

    return (
        <div className={`${pageBg} font-sans h-screen flex overflow-hidden transition-colors duration-300`}>
            <Sidebar />

            <main className="flex-1 flex flex-col h-screen overflow-y-auto relative">
                {/* Filigrane */}
                <div className="pointer-events-none fixed inset-0 flex items-center justify-center opacity-[0.03] z-0">
                    <Leaf className="w-[500px] h-[500px] text-ecoGreen" />
                </div>

                {/* Header */}
                <header className={`${headBg} px-8 py-5 border-b flex justify-between items-center sticky top-0 z-30 transition-colors duration-300`}>
                    <div>
                        <h2 className={`text-2xl font-bold ${headTxt}`}>Le Guide du Bon Trieur 📖</h2>
                        <p className={`text-sm ${subTxt} mt-1`}>Apprenez les bons gestes pour un recyclage parfait.</p>
                    </div>
                    <div className="text-right">
                        <p className={`text-xs ${subTxt} uppercase font-bold tracking-wider`}>Niveau Actuel</p>
                        <p className="text-ecoGreen font-bold flex items-center justify-end">
                            <Sprout className="w-4 h-4 mr-1" /> Apprenti Recycleur
                        </p>
                    </div>
                </header>

                {/* Contenu */}
                <div className="p-8 max-w-6xl mx-auto w-full space-y-8">

                    {/* ── Section 1 : Astuce de la semaine ── */}
                    <div className="bg-ecoGreen text-white rounded-2xl shadow-sm p-8 relative overflow-hidden flex items-center">
                        <Lightbulb className="absolute -right-10 -bottom-10 w-64 h-64 text-green-700 opacity-20" />
                        <div className="relative z-10 md:w-2/3">
                            <span className="inline-block px-3 py-1 bg-white text-ecoGreen text-xs font-bold rounded-full mb-4 uppercase tracking-wider">
                                Astuce de la semaine
                            </span>
                            <h3 className="text-2xl font-bold mb-3">Faut-il laver ses emballages ?</h3>
                            <p className="text-green-50 text-lg leading-relaxed">
                                <strong>Non !</strong> C'est une erreur très courante. Il suffit de bien les vider.
                                Laver vos boîtes de conserve ou vos pots de yaourt gaspille de l'eau potable inutilement.
                                Les centres de tri s'occupent du nettoyage !
                            </p>
                        </div>
                        <div className="hidden md:flex relative z-10 w-1/3 justify-center">
                            <div className="w-32 h-32 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center border-4 border-white/30">
                                <Droplets className="w-16 h-16 text-white" />
                            </div>
                        </div>
                    </div>

                    {/* ── Section 2 : Guide par matière ── */}
                    <div>
                        <h3 className={`text-xl font-bold ${headTxt} mb-6 flex items-center`}>
                            <Layers className="w-6 h-6 mr-2 text-ecoBrown" />
                            Les règles par type de déchet
                        </h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            {MATIERES.map(m => (
                                <CarteMatiere
                                    key={m.title}
                                    m={m}
                                    cardBg={cardBg}
                                    cardTxt={cardTxt}
                                    cardSub={cardSub}
                                />
                            ))}
                        </div>
                    </div>

                    {/* ── Section 3 : Les Faux-Amis ── */}
                    <div className={`${sectionBg} rounded-2xl shadow-sm border p-8 transition-colors duration-300`}>
                        <h3 className={`text-xl font-bold ${headTxt} mb-6 flex items-center`}>
                            <Ghost className="w-6 h-6 mr-2 text-gray-400" />
                            Les &quot;Faux-Amis&quot; du tri
                        </h3>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                            {FAUX_AMIS.map(fa => (
                                <div key={fa.label} className={`text-center p-4 rounded-xl ${fauxBg} border transition-colors duration-300`}>
                                    <div className={`w-12 h-12 ${fauxIcon} rounded-full flex items-center justify-center mx-auto mb-3 shadow-sm`}>
                                        {fa.icon}
                                    </div>
                                    <p className={`font-bold text-sm ${cardTxt}`}>{fa.label}</p>
                                    <p className={`text-xs ${subTxt} mt-1`}>{fa.desc}</p>
                                </div>
                            ))}
                        </div>
                    </div>

                </div>
            </main>
        </div>
    );
}
