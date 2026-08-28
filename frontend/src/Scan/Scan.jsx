import React, { useRef, useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';
import {
    Leaf, ScanLine, LayoutDashboard, Trophy, BookOpen,
    Coffee, Settings, MapPin, Sprout, Package, CloudSnow,
    Lightbulb, Sparkles, BatteryWarning, Store, Building,
    Map, Trash2, CheckCircle, XCircle, Camera, CameraOff, ChevronRight, MessageCircle
} from 'lucide-react';

const styles = `
@keyframes pulse-border {
  0%   { border-color: rgba(22,163,74,0.4); }
  50%  { border-color: rgba(22,163,74,1); }
  100% { border-color: rgba(22,163,74,0.4); }
}
.scanner-focus { animation: pulse-border 2s infinite; }
`;

const MOCK_AI_RESULT = {
    label: 'Bouteille en Plastique',
    confidence: 62,
    instruction: 'Vider sans rincer, laisser le bouchon.',
    bin: 'BAC JAUNE',
    binColor: 'bg-yellow-400 text-yellow-900 border-yellow-500',
    points: 5,
};

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
                            <Link key={to} to={to} className={`flex items-center space-x-3 px-4 py-3 rounded-xl font-medium transition-colors ${active ? 'bg-green-50 text-ecoGreen' : navIdle}`}>
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
                    <div className="w-10 h-10 bg-ecoBrown rounded-full flex items-center justify-center text-white font-bold">K</div>
                    <div className="flex-1 min-w-0">
                        <p className={`text-sm font-medium ${profName} truncate`}>Katia</p>
                        <p className={`text-xs ${profSub} truncate`}>Profil &amp; Réglages</p>
                    </div>
                    <Settings className="w-4 h-4 text-gray-400" />
                </Link>
            </div>
        </aside>
    );
}

function CameraZone({ aiResult: defaultResult, onConfirm, onCorrect }) {
    const videoRef = useRef(null);
    const streamRef = useRef(null);
    const [cameraActive, setCameraActive] = useState(false);
    const [cameraError, setCameraError] = useState(null);
    const [showResult, setShowResult] = useState(false);
    const [currentResult, setCurrentResult] = useState(defaultResult);

    const mapApiToUI = (data) => {
        const binMap = {
            plastique: { bin: 'BAC JAUNE',  binColor: 'bg-yellow-400 text-yellow-900 border-yellow-500' },
            verre:     { bin: 'BAC VERT',   binColor: 'bg-green-500 text-white border-green-600' },
            papier:    { bin: 'BAC BLEU',   binColor: 'bg-blue-500 text-white border-blue-600' },
            carton:    { bin: 'BAC BLEU',   binColor: 'bg-blue-500 text-white border-blue-600' },
            metal:     { bin: 'BAC JAUNE',  binColor: 'bg-yellow-400 text-yellow-900 border-yellow-500' },
            organique: { bin: 'BAC MARRON', binColor: 'bg-amber-700 text-white border-amber-800' },
        };
        const label = data.waste_class || data.label || data.class_name || 'Objet inconnu';
        const confidence = Math.round((data.confidence || 0.5) * 100);
        const cat = Object.keys(binMap).find(k => label.toLowerCase().includes(k));
        const { bin, binColor } = binMap[cat] ?? { bin: 'ORDURES MÉNAGÈRES', binColor: 'bg-gray-500 text-white border-gray-600' };
        return { label, confidence, instruction: data.message || data.instruction || 'Vider sans rincer.', bin, binColor, points: data.points ?? 10 };
    };

    const detectFromCamera = async () => {
        try {
            if (!videoRef.current || videoRef.current.videoWidth === 0) return defaultResult;
            const canvas = document.createElement('canvas');
            canvas.width = videoRef.current.videoWidth;
            canvas.height = videoRef.current.videoHeight;
            canvas.getContext('2d').drawImage(videoRef.current, 0, 0);
            const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/jpeg', 0.85));
            const body = new FormData();
            body.append('file', blob, 'scan.jpg');
            const res = await fetch('/predict', { method: 'POST', body });
            if (!res.ok) throw new Error(`Erreur HTTP ${res.status}`);
            const data = await res.json();
            console.log('[ECO-TRI] Résultat IA :', data);
            return mapApiToUI(data);
        } catch (err) {
            console.warn('[ECO-TRI] Backend indisponible → mode démo :', err.message);
            return defaultResult;
        }
    };

    const startCamera = async () => {
        setCameraError(null);
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } },
                audio: false,
            });
            streamRef.current = stream;
            if (videoRef.current) {
                videoRef.current.srcObject = stream;
                await videoRef.current.play();
            }
            setCameraActive(true);
            setTimeout(async () => {
                const result = await detectFromCamera();
                setCurrentResult(result);
                setShowResult(true);
            }, 2500);
        } catch (err) {
            setCameraError("Impossible d'accéder à la caméra. Vérifiez les permissions.");
        }
    };

    const stopCamera = () => {
        streamRef.current?.getTracks().forEach(t => t.stop());
        streamRef.current = null;
        if (videoRef.current) videoRef.current.srcObject = null;
        setCameraActive(false);
        setShowResult(false);
        setCurrentResult(defaultResult);
    };

    useEffect(() => () => streamRef.current?.getTracks().forEach(t => t.stop()), []);

    return (
        <div className="bg-black rounded-2xl overflow-hidden relative aspect-video shadow-lg border-4 border-gray-800">
            <video ref={videoRef} className="w-full h-full object-cover opacity-90" playsInline muted />
            {!cameraActive && (
                <div className="absolute inset-0 flex flex-col items-center justify-center space-y-4 bg-gray-900">
                    {cameraError
                        ? <><CameraOff className="w-12 h-12 text-red-400" /><p className="text-red-300 text-sm px-8 text-center">{cameraError}</p></>
                        : <><Camera className="w-12 h-12 text-gray-400" /><p className="text-gray-400 text-sm">Caméra désactivée</p></>
                    }
                    <button onClick={startCamera} className="mt-2 flex items-center space-x-2 bg-ecoGreen hover:bg-green-700 text-white px-5 py-2.5 rounded-xl font-medium text-sm transition">
                        <Camera className="w-4 h-4" /><span>Activer la caméra</span>
                    </button>
                </div>
            )}
            {cameraActive && (
                <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                    <div className="w-64 h-80 border-2 border-dashed scanner-focus rounded-xl relative">
                        <div className="absolute top-0 left-0 w-4 h-4 border-t-4 border-l-4 border-ecoGreen rounded-tl-lg" />
                        <div className="absolute top-0 right-0 w-4 h-4 border-t-4 border-r-4 border-ecoGreen rounded-tr-lg" />
                        <div className="absolute bottom-0 left-0 w-4 h-4 border-b-4 border-l-4 border-ecoGreen rounded-bl-lg" />
                        <div className="absolute bottom-0 right-0 w-4 h-4 border-b-4 border-r-4 border-ecoGreen rounded-br-lg" />
                    </div>
                </div>
            )}
            {cameraActive && (
                <button onClick={stopCamera} className="absolute top-3 right-3 bg-black/50 hover:bg-black/70 text-white px-3 py-1.5 rounded-lg text-xs flex items-center space-x-1 transition">
                    <CameraOff className="w-3.5 h-3.5" /><span>Arrêter</span>
                </button>
            )}
            {showResult && cameraActive && (
                <div className="absolute bottom-6 left-1/2 transform -translate-x-1/2 w-11/12 max-w-md bg-white/95 backdrop-blur-sm p-4 rounded-xl shadow-2xl border border-gray-200">
                    <div className="flex items-start justify-between">
                        <div>
                            <p className="text-xs font-bold text-gray-500 uppercase">Détection IA : {currentResult.confidence}%</p>
                            <h3 className="text-xl font-black text-gray-800 mt-1">{currentResult.label}</h3>
                            <p className="text-sm text-gray-600 mt-1">Consigne : {currentResult.instruction}</p>
                        </div>
                        <div className={`${currentResult.binColor} px-4 py-2 rounded-lg font-bold shadow-sm border flex flex-col items-center`}>
                            <Trash2 className="w-6 h-6 mb-1" />{currentResult.bin}
                        </div>
                    </div>
                    <div className="mt-4 pt-3 border-t border-gray-200">
                        <p className="text-xs text-gray-500 mb-2 font-medium">L'IA hésite un peu. Confirmez-vous cet objet ?</p>
                        <div className="flex space-x-2">
                            <button onClick={onConfirm} className="flex-1 flex items-center justify-center space-x-1 bg-ecoGreen text-white py-2 rounded-lg font-medium text-sm hover:bg-green-700 transition shadow-sm">
                                <CheckCircle className="w-4 h-4" /><span>Oui, c'est ça ! (+{currentResult.points} pts)</span>
                            </button>
                            <button onClick={onCorrect} className="flex-1 flex items-center justify-center space-x-1 bg-gray-200 text-gray-700 py-2 rounded-lg font-medium text-sm hover:bg-gray-300 transition shadow-sm">
                                <XCircle className="w-4 h-4" /><span>Non, corriger</span>
                            </button>
                        </div>
                    </div>
                </div>
            )}
            {cameraActive && !showResult && (
                <div className="absolute bottom-6 left-1/2 -translate-x-1/2 bg-black/60 backdrop-blur-sm text-white px-4 py-2 rounded-full text-sm flex items-center space-x-2">
                    <span className="w-2 h-2 bg-ecoGreen rounded-full animate-pulse" />
                    <span>Analyse en cours…</span>
                </div>
            )}
        </div>
    );
}

export default function Scan() {
    const [points, setPoints] = useState(450);
    const [dechets, setDechets] = useState(142);
    const [locationLabel, setLocationLabel] = useState(null);
    const [locationError, setLocationError] = useState(false);

    useEffect(() => {
        if (!navigator.geolocation) { setLocationError(true); return; }
        navigator.geolocation.getCurrentPosition(
            async ({ coords }) => {
                try {
                    const res = await fetch(
                        `https://nominatim.openstreetmap.org/reverse?lat=${coords.latitude}&lon=${coords.longitude}&format=json`,
                        { headers: { 'Accept-Language': 'fr' } }
                    );
                    const data = await res.json();
                    const a = data.address || {};
                    const quartier = a.neighbourhood || a.city_district || a.suburb || a.quarter || '';
                    const ville = a.city || a.town || a.village || a.municipality || '';
                    setLocationLabel([quartier, ville].filter(Boolean).join(', ') || 'Position détectée');
                } catch { setLocationError(true); }
            },
            () => setLocationError(true),
            { enableHighAccuracy: true, timeout: 10000 }
        );
    }, []);

    const handleConfirm = () => { setPoints(p => p + 10); setDechets(d => d + 1); };
    const handleCorrect = () => alert('Fonctionnalité de correction à venir !');

    const { darkMode } = useTheme();
    const pageBg = darkMode ? 'bg-gray-950 text-gray-100' : 'bg-ecoLight text-gray-800';
    const headBg = darkMode ? 'bg-gray-900 border-gray-700' : 'bg-white border-gray-200';
    const headTxt = darkMode ? 'text-gray-100' : 'text-gray-800';
    const subTxt = darkMode ? 'text-gray-400' : 'text-gray-500';
    const cardBg = darkMode ? 'bg-gray-900 border-gray-700' : 'bg-white border-gray-100';
    const cardTxt = darkMode ? 'text-gray-100' : 'text-gray-800';
    const cardSub = darkMode ? 'text-gray-400' : 'text-gray-500';
    const rowBg = darkMode ? 'bg-gray-800' : 'bg-gray-50';
    const mapBtn = darkMode ? 'border-gray-700 text-gray-300 hover:bg-gray-800' : 'border-gray-200 text-gray-600 hover:bg-gray-50';

    return (
        <>
            <style>{styles}</style>
            <div className={`${pageBg} font-sans h-screen flex overflow-hidden transition-colors duration-300`}>
                <Sidebar />
                <main className="flex-1 flex flex-col h-screen overflow-y-auto relative">
                    <div className="pointer-events-none fixed inset-0 flex items-center justify-center opacity-[0.03] z-0">
                        <Leaf className="w-[500px] h-[500px] text-ecoGreen" />
                    </div>
                    <header className={`${headBg} px-8 py-5 border-b flex justify-between items-center sticky top-0 z-30 transition-colors duration-300`}>
                        <div>
                            <h2 className={`text-2xl font-bold ${headTxt}`}>Prêt à trier, Katia ? ♻️</h2>
                            <p className={`text-sm ${subTxt} mt-1 flex items-center`}>
                                <MapPin className="w-4 h-4 mr-1 text-ecoBrown" />
                                Localisation active :
                                {locationError ? (
                                    <span className="ml-1 text-red-500 font-medium">Permission refusée</span>
                                ) : locationLabel === null ? (
                                    <span className="ml-1 italic text-gray-400 animate-pulse">Détection en cours…</span>
                                ) : (
                                    <strong className={`ml-1 ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>{locationLabel}</strong>
                                )}
                            </p>
                        </div>
                        <div className="flex items-center space-x-4">
                            <div className="text-right">
                                <p className={`text-xs ${subTxt} uppercase font-bold tracking-wider`}>Niveau Actuel</p>
                                <p className="text-ecoGreen font-bold flex items-center justify-end">
                                    <Sprout className="w-4 h-4 mr-1" /> Apprenti Recycleur
                                </p>
                            </div>
                            <div className="w-12 h-12 bg-yellow-100 rounded-full flex items-center justify-center border-2 border-yellow-400">
                                <span className="font-bold text-yellow-600">{points}</span>
                            </div>
                        </div>
                    </header>
                    <div className="p-8 max-w-7xl mx-auto w-full grid grid-cols-1 lg:grid-cols-3 gap-8">
                        <div className="col-span-1 lg:col-span-2 space-y-6">
                            <CameraZone aiResult={MOCK_AI_RESULT} onConfirm={handleConfirm} onCorrect={handleCorrect} />
                            <div className="grid grid-cols-2 gap-4">
                                <div className={`${cardBg} p-5 rounded-2xl shadow-sm border flex items-center space-x-4 transition-colors duration-300`}>
                                    <div className="p-3 bg-blue-50 text-blue-600 rounded-xl"><Package className="w-6 h-6" /></div>
                                    <div>
                                        <p className={`text-sm ${cardSub} font-medium`}>Déchets triés</p>
                                        <p className={`text-2xl font-bold ${cardTxt}`}>{dechets}</p>
                                    </div>
                                </div>
                                <div className={`${cardBg} p-5 rounded-2xl shadow-sm border flex items-center space-x-4 transition-colors duration-300`}>
                                    <div className="p-3 bg-ecoGreen/10 text-ecoGreen rounded-xl"><CloudSnow className="w-6 h-6" /></div>
                                    <div>
                                        <p className={`text-sm ${cardSub} font-medium`}>CO2 Évité (est.)</p>
                                        <p className={`text-2xl font-bold ${cardTxt}`}>1.2 kg</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="space-y-6">
                            <div className="bg-ecoBrown text-white p-6 rounded-2xl shadow-md relative overflow-hidden">
                                <Lightbulb className="absolute -right-4 -bottom-4 w-32 h-32 opacity-10" />
                                <h3 className="text-lg font-bold mb-2 flex items-center">
                                    <Sparkles className="w-5 h-5 mr-2 text-yellow-400" /> Le Saviez-vous ?
                                </h3>
                                <p className="text-sm text-amber-50 leading-relaxed">
                                    Inutile de laver vos boîtes de conserve avant de les jeter ! Il suffit de bien les vider. Les laver gaspille de l'eau potable inutilement.
                                </p>
                            </div>
                            <div className={`${cardBg} rounded-2xl shadow-sm border p-6 transition-colors duration-300`}>
                                <h3 className={`${cardTxt} font-bold mb-4 flex items-center justify-between`}>
                                    <span>Top Recycleurs</span>
                                    <a href="#" className="text-ecoGreen text-sm font-medium hover:underline flex items-center">Voir tout <ChevronRight className="w-3 h-3 ml-0.5" /></a>
                                </h3>
                                <div className="space-y-3">
                                    <div className={`flex items-center justify-between p-2 rounded-lg ${rowBg}`}>
                                        <div className="flex items-center space-x-3">
                                            <span className="text-yellow-500 font-bold w-4">1</span>
                                            <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-xs font-bold text-blue-800">S</div>
                                            <span className={`text-sm font-medium ${cardTxt} italic text-gray-400`}>À connecter (BDD)</span>
                                        </div>
                                        <span className={`text-sm font-bold ${cardTxt} italic text-gray-400`}>— pts</span>
                                    </div>
                                    <div className="flex items-center justify-between p-2 rounded-lg border border-ecoGreen bg-green-50">
                                        <div className="flex items-center space-x-3">
                                            <span className="text-ecoGreen font-bold w-4">7</span>
                                            <div className="w-8 h-8 rounded-full bg-ecoBrown flex items-center justify-center text-xs font-bold text-white">K</div>
                                            <span className="text-sm font-bold text-ecoGreen">Katia (moi) 🌱</span>
                                        </div>
                                        <span className="text-sm font-bold text-ecoGreen">{points} pts</span>
                                    </div>
                                </div>
                            </div>
                            <div className={`${cardBg} rounded-2xl shadow-sm border p-6 transition-colors duration-300`}>
                                <h3 className={`${cardTxt} font-bold mb-3 flex items-center text-sm`}>
                                    <BatteryWarning className="w-4 h-4 mr-2 text-red-500" />Si vous scannez une pile :
                                </h3>
                                <p className={`text-xs ${cardSub} mb-3`}>Points de collecte près de vous :</p>
                                <ul className="space-y-2">
                                    <li className="flex items-start space-x-3 text-sm">
                                        <Store className="w-4 h-4 text-gray-400 mt-0.5" />
                                        <p className="font-medium italic text-gray-400 text-xs">À connecter (API)</p>
                                    </li>
                                </ul>
                                <button className={`w-full mt-4 py-2 border rounded-lg text-sm font-medium flex items-center justify-center transition ${mapBtn}`}>
                                    <Map className="w-4 h-4 mr-2" /> Ouvrir la carte
                                </button>
                            </div>
                        </div>
                    </div>
                </main>
            </div>
        </>
    );
}