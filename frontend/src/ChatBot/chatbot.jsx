import React, { useState, useRef, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';
import {
    Leaf, ScanLine, LayoutDashboard, Trophy, BookOpen, Coffee,
    Settings, Send, Bot, User, Sparkles, RotateCcw, ChevronDown,
    MessageCircle, Trash2
} from 'lucide-react';

/* ===================== Suggestions rapides ===================== */
const QUICK_SUGGESTIONS = [
    "Où jeter une bouteille en plastique ?",
    "Comment trier le verre ?",
    "Que faire avec une pile usagée ?",
    "Mon code postal pour les déchetteries ?",
    "Comment réduire mes déchets au quotidien ?",
    "Qu'est-ce que le compostage ?",
];

/* ===================== Réponses mock de l'IA ===================== */
const AI_RESPONSES = {
    default: [
        "Je suis **Éco-Assistant**, votre guide pour un tri parfait ! 🌱 Posez-moi vos questions sur le recyclage, les matières, ou les points de collecte près de chez vous.",
        "Bonne question ! Pour un tri optimal, pensez toujours à **vider** vos emballages avant de les jeter. Le nettoyage n'est pas nécessaire — les centres de tri s'en occupent !",
        "Je comprends votre question. En France, la règle générale est : **Bac Jaune** pour plastiques, métaux et papiers ; **Bac Vert** pour le verre ; **Ordures ménagères** pour le reste.",
        "Chaque geste compte ! En recyclant correctement, vous contribuez à réduire les émissions de CO₂ et à préserver nos ressources naturelles. 🌍",
    ],
    bouteille: "Une **bouteille en plastique** se jette dans le **Bac Jaune** ♻️\n\n✅ Videz-la complètement\n✅ Laissez le bouchon dessus (il se recycle aussi !)\n✅ Aplatissez-la dans la longueur pour gagner de la place\n\n❌ Inutile de la laver — les centres de tri s'en chargent.",
    verre: "Le **verre d'emballage** va dans le **Bac Vert** 🟢 ou la colonne à verre.\n\n✅ Bocaux, bouteilles de vin, pots de confiture\n✅ Enlevez les bouchons et capsules (→ Bac Jaune)\n\n❌ Verres à boire, vaisselle cassée, miroirs : poubelle grise car leur composition chimique est différente.",
    pile: "Les **piles et batteries** ne vont **jamais** à la poubelle ! ⚠️\n\nDéposez-les dans les bacs prévus :\n📍 Supermarchés (Carrefour, Leclerc…)\n📍 Magasins d'électronique\n📍 Pharmacies\n📍 Déchetteries communales\n\nScannez votre déchet dans l'app Eco-Tri pour trouver le point de dépôt le plus proche !",
    compost: "Le **compostage** est la meilleure solution pour les déchets organiques ! 🌱\n\nOn peut composter :\n✅ Épluchures de fruits et légumes\n✅ Marc de café, sachets de thé\n✅ Coquilles d'œufs\n✅ Feuilles mortes et tontes de gazon\n\n❌ Viande, poisson, produits laitiers (risque d'odeurs et de nuisibles)",
    plastique: "Tous les **plastiques** peuvent désormais aller dans le **Bac Jaune** depuis l'extension des consignes de tri ! ♻️\n\n✅ Bouteilles, flacons, barquettes, sacs plastiques\n✅ Films plastiques, blisters\n\nLaissez les emballages tels quels — juste vidés, pas lavés.",
};

function getAIResponse(message) {
    const lower = message.toLowerCase();
    if (lower.includes('bouteille') || lower.includes('plastique')) return AI_RESPONSES.bouteille;
    if (lower.includes('verre') || lower.includes('bocal')) return AI_RESPONSES.verre;
    if (lower.includes('pile') || lower.includes('batterie')) return AI_RESPONSES.pile;
    if (lower.includes('compost') || lower.includes('organique')) return AI_RESPONSES.compost;
    if (lower.includes('plastique') || lower.includes('emballage')) return AI_RESPONSES.plastique;
    // Réponse générique aléatoire
    return AI_RESPONSES.default[Math.floor(Math.random() * AI_RESPONSES.default.length)];
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

/* ===================== Bulle de message ===================== */
function MessageBubble({ msg, darkMode }) {
    const isUser = msg.role === 'user';

    /* Rendu Markdown basique (gras + sauts de ligne) */
    const renderText = (text) => {
        return text.split('\n').map((line, i) => {
            const parts = line.split(/\*\*(.*?)\*\*/g);
            return (
                <span key={i}>
                    {parts.map((part, j) =>
                        j % 2 === 1
                            ? <strong key={j}>{part}</strong>
                            : part
                    )}
                    {i < text.split('\n').length - 1 && <br />}
                </span>
            );
        });
    };

    return (
        <div className={`flex items-end gap-3 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
            {/* Avatar */}
            <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 shadow-sm
                ${isUser ? 'bg-ecoBrown text-white' : 'bg-ecoGreen text-white'}`}>
                {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
            </div>

            {/* Bulle */}
            <div className={`max-w-[75%] px-4 py-3 rounded-2xl text-sm leading-relaxed shadow-sm
                ${isUser
                    ? 'bg-ecoGreen text-white rounded-br-sm'
                    : darkMode
                        ? 'bg-gray-800 text-gray-100 rounded-bl-sm border border-gray-700'
                        : 'bg-white text-gray-800 rounded-bl-sm border border-gray-100'
                }`}>
                {msg.typing ? (
                    <span className="flex items-center gap-1.5">
                        <span className="w-2 h-2 bg-ecoGreen rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                        <span className="w-2 h-2 bg-ecoGreen rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                        <span className="w-2 h-2 bg-ecoGreen rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                    </span>
                ) : (
                    renderText(msg.text)
                )}
            </div>
        </div>
    );
}

/* ===================== Page ChatBot ===================== */
const WELCOME = {
    role: 'ai',
    text: "Bonjour ! Je suis **Éco-Assistant**, votre guide pour un recyclage parfait. 🌱\n\nPosez-moi vos questions sur le tri des déchets, les matières recyclables, ou les points de collecte près de chez vous !",
    id: 0,
};

export default function ChatBot() {
    const { darkMode } = useTheme();
    const [messages, setMessages] = useState([WELCOME]);
    const [input, setInput] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const [showScrollBtn, setShowScrollBtn] = useState(false);
    const bottomRef = useRef(null);
    const chatRef = useRef(null);
    const inputRef = useRef(null);

    /* Scroll automatique vers le bas */
    const scrollToBottom = () => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    /* Détection du scroll pour afficher le bouton */
    const handleScroll = () => {
        if (!chatRef.current) return;
        const { scrollTop, scrollHeight, clientHeight } = chatRef.current;
        setShowScrollBtn(scrollHeight - scrollTop - clientHeight > 100);
    };

    /* Envoi d'un message */
    const sendMessage = (text = input.trim()) => {
        if (!text || isTyping) return;
        setInput('');
        inputRef.current?.focus();

        const userMsg = { role: 'user', text, id: Date.now() };
        setMessages(prev => [...prev, userMsg]);

        // Indicateur "en train d'écrire"
        setIsTyping(true);
        const typingId = Date.now() + 1;
        setMessages(prev => [...prev, { role: 'ai', typing: true, id: typingId }]);

        // Simule un délai réseau (800–1600ms)
        const delay = 800 + Math.random() * 800;
        setTimeout(() => {
            const response = getAIResponse(text);
            setMessages(prev => prev.map(m =>
                m.id === typingId
                    ? { role: 'ai', text: response, id: typingId }
                    : m
            ));
            setIsTyping(false);
        }, delay);
    };

    const handleKey = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    const clearChat = () => {
        setMessages([WELCOME]);
        setIsTyping(false);
    };

    /* Couleurs thème */
    const pageBg = darkMode ? 'bg-gray-950' : 'bg-ecoLight';
    const headBg = darkMode ? 'bg-gray-900 border-gray-700' : 'bg-white border-gray-200';
    const headTxt = darkMode ? 'text-gray-100' : 'text-gray-800';
    const subTxt = darkMode ? 'text-gray-400' : 'text-gray-500';
    const chatBg = darkMode ? 'bg-gray-950' : 'bg-gray-50';
    const inputBg = darkMode ? 'bg-gray-900 border-gray-700' : 'bg-white border-gray-200';
    const fieldBg = darkMode ? 'bg-gray-800 border-gray-600 text-gray-100 placeholder-gray-500' : 'bg-gray-50 border-gray-200 text-gray-800 placeholder-gray-400';
    const suggBg = darkMode ? 'bg-gray-800 border-gray-700 text-gray-300 hover:bg-gray-700 hover:border-ecoGreen hover:text-ecoGreen' : 'bg-white border-gray-200 text-gray-600 hover:border-ecoGreen hover:text-ecoGreen hover:bg-green-50';

    return (
        <div className={`${pageBg} font-sans h-screen flex overflow-hidden transition-colors duration-300`}>
            <Sidebar />

            <div className="flex-1 flex flex-col h-screen overflow-hidden">

                {/* Header */}
                <header className={`${headBg} px-8 py-4 border-b flex justify-between items-center flex-shrink-0 transition-colors duration-300`}>
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 bg-ecoGreen rounded-xl flex items-center justify-center shadow-sm">
                            <Bot className="w-5 h-5 text-white" />
                        </div>
                        <div>
                            <h2 className={`text-lg font-bold ${headTxt} flex items-center gap-2`}>
                                Éco-Assistant IA
                                <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-green-100 text-ecoGreen text-xs font-bold rounded-full">
                                    <span className="w-1.5 h-1.5 bg-ecoGreen rounded-full animate-pulse" />
                                    En ligne
                                </span>
                            </h2>
                            <p className={`text-xs ${subTxt}`}>Posez vos questions sur le tri et le recyclage</p>
                        </div>
                    </div>
                    <button
                        onClick={clearChat}
                        title="Effacer la conversation"
                        className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition
                            ${darkMode ? 'text-gray-400 hover:bg-gray-800 hover:text-red-400' : 'text-gray-500 hover:bg-red-50 hover:text-red-500'}`}>
                        <Trash2 className="w-4 h-4" />
                        <span className="hidden sm:inline">Effacer</span>
                    </button>
                </header>

                {/* Zone de chat */}
                <div
                    ref={chatRef}
                    onScroll={handleScroll}
                    className={`flex-1 overflow-y-auto px-6 py-6 space-y-5 ${chatBg} transition-colors duration-300 relative`}
                >
                    {/* Filigrane */}
                    <div className="absolute inset-0 flex items-center justify-center pointer-events-none opacity-[0.03]">
                        <Leaf className="w-96 h-96 text-ecoGreen" />
                    </div>

                    {messages.map(msg => (
                        <MessageBubble key={msg.id} msg={msg} darkMode={darkMode} />
                    ))}
                    <div ref={bottomRef} />
                </div>

                {/* Bouton scroll to bottom */}
                {showScrollBtn && (
                    <button
                        onClick={scrollToBottom}
                        className="absolute bottom-28 right-8 w-9 h-9 bg-ecoGreen text-white rounded-full shadow-lg flex items-center justify-center hover:bg-green-700 transition z-10">
                        <ChevronDown className="w-5 h-5" />
                    </button>
                )}

                {/* Suggestions rapides */}
                <div className={`${inputBg} border-t px-6 pt-4 pb-2 flex-shrink-0 transition-colors duration-300`}>
                    <p className={`text-xs font-semibold ${subTxt} mb-2 flex items-center gap-1.5`}>
                        <Sparkles className="w-3.5 h-3.5 text-ecoGreen" /> Suggestions
                    </p>
                    <div className="flex gap-2 overflow-x-auto pb-1 scrollbar-hide">
                        {QUICK_SUGGESTIONS.map(s => (
                            <button
                                key={s}
                                onClick={() => sendMessage(s)}
                                disabled={isTyping}
                                className={`flex-shrink-0 px-3 py-1.5 rounded-full border text-xs font-medium transition whitespace-nowrap ${suggBg} disabled:opacity-40`}>
                                {s}
                            </button>
                        ))}
                    </div>
                </div>

                {/* Zone de saisie */}
                <div className={`${inputBg} px-6 py-4 border-t flex items-end gap-3 flex-shrink-0 transition-colors duration-300`}>
                    <textarea
                        ref={inputRef}
                        value={input}
                        onChange={e => setInput(e.target.value)}
                        onKeyDown={handleKey}
                        placeholder="Posez votre question sur le recyclage… (Entrée pour envoyer)"
                        rows={1}
                        disabled={isTyping}
                        className={`flex-1 resize-none rounded-xl border px-4 py-3 text-sm outline-none transition
                            focus:ring-2 focus:ring-ecoGreen focus:border-ecoGreen ${fieldBg}
                            max-h-32 disabled:opacity-50`}
                        style={{ overflowY: input.split('\n').length > 3 ? 'auto' : 'hidden' }}
                    />
                    <button
                        onClick={() => sendMessage()}
                        disabled={!input.trim() || isTyping}
                        className="w-11 h-11 bg-ecoGreen text-white rounded-xl flex items-center justify-center shadow-sm
                            hover:bg-green-700 transition disabled:opacity-40 disabled:cursor-not-allowed flex-shrink-0">
                        <Send className="w-4 h-4" />
                    </button>
                </div>

            </div>
        </div>
    );
}
