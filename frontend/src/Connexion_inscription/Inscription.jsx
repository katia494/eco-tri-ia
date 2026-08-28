import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import {
    Sprout,
    Leaf,
    User,
    Mail,
    Lock,
    Eye,
    EyeOff,
    Crosshair,
    Building2,
    Map,
    UserPlus
} from 'lucide-react';

export default function Inscription() {
    const [showPassword, setShowPassword] = useState(false);

    return (
        <div className="bg-ecoLight text-gray-800 font-sans h-screen flex overflow-hidden">

            {/* Partie Gauche : Visuel / Mission (Cachée sur petit écran) */}
            <div className="hidden lg:flex lg:w-1/2 relative bg-ecoBrown items-center justify-center overflow-hidden">
                {/* Image de fond */}
                <img
                    src="https://images.unsplash.com/photo-1518173946687-a4c8892bbd9f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80"
                    alt="Nature"
                    className="absolute inset-0 w-full h-full object-cover opacity-30 mix-blend-overlay"
                />

                {/* Contenu superposé */}
                <div className="relative z-10 p-12 max-w-lg text-white">
                    <div className="bg-white/20 backdrop-blur-md p-4 rounded-2xl inline-block mb-6 border border-white/30 shadow-lg">
                        <Sprout className="w-12 h-12 text-white" />
                    </div>
                    <h1 className="text-4xl font-bold mb-4 leading-tight">Rejoignez le mouvement.</h1>
                    <p className="text-orange-50 text-lg leading-relaxed mb-8">
                        Devenez acteur de votre environnement. Créez votre profil, cumulez des points à chaque bon tri, et découvrez les points de collecte proches de chez vous.
                    </p>

                    {/* Petit feedback utilisateur en citation */}
                    <div className="bg-black/20 backdrop-blur-sm p-4 rounded-xl border-l-4 border-ecoGreen">
                        <p className="text-sm italic text-orange-50">"Une application simple, sans prise de tête, qui m'aide au quotidien."</p>
                        <p className="text-xs font-bold mt-2 text-white">— Une graine de trieur</p>
                    </div>
                </div>
            </div>

            {/* Partie Droite : Formulaire d'Inscription */}
            <div className="w-full lg:w-1/2 flex items-center justify-center p-8 sm:p-12 overflow-y-auto">
                <div className="w-full max-w-md space-y-6 my-auto">

                    {/* Logo & En-tête */}
                    <div className="text-center lg:text-left">
                        <div className="flex items-center justify-center lg:justify-start space-x-3 mb-4">
                            <div className="bg-ecoGreen p-2 rounded-lg text-white shadow-sm">
                                <Leaf className="w-6 h-6" />
                            </div>
                            <h2 className="text-xl font-black text-gray-800 tracking-tight">One-Two-Tri Vision</h2>
                        </div>
                        <h3 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-2">Créer un compte 🌱</h3>
                        <p className="text-gray-500 text-sm">Commencez votre aventure écologique en quelques secondes.</p>
                    </div>

                    {/* Formulaire */}
                    <form className="mt-6 space-y-4" action="#" method="POST" onSubmit={(e) => e.preventDefault()}>

                        {/* Champ Pseudo */}
                        <div>
                            <label htmlFor="pseudo" className="block text-sm font-medium text-gray-700 mb-1">Pseudo</label>
                            <div className="relative">
                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <User className="h-5 w-5 text-gray-400" />
                                </div>
                                <input
                                    id="pseudo"
                                    name="pseudo"
                                    type="text"
                                    required
                                    className="block w-full pl-10 pr-3 py-2.5 border border-gray-300 rounded-xl focus:ring-2 focus:ring-ecoGreen focus:border-ecoGreen outline-none transition text-sm bg-gray-50 focus:bg-white"
                                    placeholder="ex: katia92"
                                />
                            </div>
                        </div>

                        {/* Champ Email */}
                        <div>
                            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">Adresse e-mail</label>
                            <div className="relative">
                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <Mail className="h-5 w-5 text-gray-400" />
                                </div>
                                <input
                                    id="email"
                                    name="email"
                                    type="email"
                                    required
                                    className="block w-full pl-10 pr-3 py-2.5 border border-gray-300 rounded-xl focus:ring-2 focus:ring-ecoGreen focus:border-ecoGreen outline-none transition text-sm bg-gray-50 focus:bg-white"
                                    placeholder="hello@exemple.com"
                                />
                            </div>
                        </div>

                        {/* Champ Mot de passe */}
                        <div>
                            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">Mot de passe</label>
                            <div className="relative">
                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <Lock className="h-5 w-5 text-gray-400" />
                                </div>
                                <input
                                    id="password"
                                    name="password"
                                    type={showPassword ? "text" : "password"}
                                    required
                                    className="block w-full pl-10 pr-10 py-2.5 border border-gray-300 rounded-xl focus:ring-2 focus:ring-ecoGreen focus:border-ecoGreen outline-none transition text-sm bg-gray-50 focus:bg-white"
                                    placeholder="••••••••"
                                />
                                <button
                                    type="button"
                                    onClick={() => setShowPassword(!showPassword)}
                                    className="absolute inset-y-0 right-0 pr-3 flex items-center cursor-pointer text-gray-400 hover:text-gray-600 focus:outline-none"
                                >
                                    {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                                </button>
                            </div>
                        </div>

                        {/* Zone Localisation */}
                        <div className="pt-2">
                            <div className="flex items-center justify-between mb-2">
                                <label className="block text-sm font-medium text-gray-700">Votre secteur de tri</label>
                                <button
                                    type="button"
                                    className="flex items-center text-xs font-bold text-ecoGreen bg-green-50 hover:bg-green-100 px-3 py-1.5 rounded-lg transition border border-green-200"
                                >
                                    <Crosshair className="w-3.5 h-3.5 mr-1.5" /> Me localiser
                                </button>
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                {/* Champ Ville */}
                                <div className="relative">
                                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                        <Building2 className="h-4 w-4 text-gray-400" />
                                    </div>
                                    <input
                                        id="ville"
                                        name="ville"
                                        type="text"
                                        required
                                        className="block w-full pl-9 pr-3 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-ecoGreen focus:border-ecoGreen outline-none transition text-sm bg-gray-50 focus:bg-white"
                                        placeholder="Ville"
                                    />
                                </div>
                                {/* Champ Quartier */}
                                <div className="relative">
                                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                        <Map className="h-4 w-4 text-gray-400" />
                                    </div>
                                    <input
                                        id="quartier"
                                        name="quartier"
                                        type="text"
                                        required
                                        className="block w-full pl-9 pr-3 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-ecoGreen focus:border-ecoGreen outline-none transition text-sm bg-gray-50 focus:bg-white"
                                        placeholder="Quartier"
                                    />
                                </div>
                            </div>
                            <p className="text-xs text-gray-500 mt-1.5">Nécessaire pour vous donner les bonnes consignes de tri locales.</p>
                        </div>

                        {/* Bouton de soumission */}
                        <button
                            type="submit"
                            className="w-full mt-4 flex justify-center items-center space-x-2 py-3 px-4 border border-transparent rounded-xl shadow-sm text-sm font-bold text-white bg-ecoGreen hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-ecoGreen transition"
                        >
                            <span>Créer mon compte</span>
                            <UserPlus className="w-4 h-4" />
                        </button>
                    </form>

                    {/* Séparateur */}
                    <div className="mt-6">
                        <div className="relative">
                            <div className="absolute inset-0 flex items-center">
                                <div className="w-full border-t border-gray-200"></div>
                            </div>
                            <div className="relative flex justify-center text-sm">
                                <span className="px-2 bg-ecoLight text-gray-500">Déjà membre ?</span>
                            </div>
                        </div>
                    </div>

                    {/* Lien vers Connexion */}
                    <div className="mt-6 text-center">
                        <Link
                            to="/connexion"
                            className="inline-flex items-center justify-center w-full py-2.5 px-4 border-2 border-gray-200 rounded-xl shadow-sm text-sm font-bold text-gray-700 bg-white hover:bg-gray-50 hover:border-gray-300 transition"
                        >
                            Se connecter à mon compte
                        </Link>
                    </div>

                </div>
            </div>
        </div>
    );
}