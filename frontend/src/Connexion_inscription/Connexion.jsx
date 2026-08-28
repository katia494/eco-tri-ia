import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { ScanEye, Leaf, User, Lock, Eye, EyeOff, ArrowRight } from 'lucide-react';

const LoginPage = () => {
    // État pour gérer l'affichage du mot de passe
    const [showPassword, setShowPassword] = useState(false);

    return (
        <div className="bg-ecoLight text-gray-800 font-sans h-screen flex overflow-hidden">

            {/* Partie Gauche : Visuel / Mission (Cachée sur petit écran) */}
            <div className="hidden lg:flex lg:w-1/2 relative bg-ecoGreen items-center justify-center overflow-hidden">
                {/* Image de fond (Unsplash - Nature/Forêt) */}
                <img
                    src="https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80"
                    alt="Nature"
                    className="absolute inset-0 w-full h-full object-cover opacity-30 mix-blend-overlay"
                />

                {/* Contenu superposé */}
                <div className="relative z-10 p-12 max-w-lg text-white">
                    <div className="bg-white/20 backdrop-blur-md p-4 rounded-2xl inline-block mb-6 border border-white/30 shadow-lg">
                        <ScanEye className="w-12 h-12 text-white" />
                    </div>
                    <h1 className="text-4xl font-bold mb-4 leading-tight">Apprenons à mieux trier, ensemble.</h1>
                    <p className="text-green-50 text-lg leading-relaxed mb-8">
                        Un simple scan pour faire le bon geste. Rejoignez la communauté One-Two-Tri Vision et progressez à votre rythme pour réduire votre impact au quotidien.
                    </p>

                    {/* Petit feedback utilisateur en citation */}
                    <div className="bg-black/20 backdrop-blur-sm p-4 rounded-xl border-l-4 border-yellow-400">
                        <p className="text-sm italic text-green-50">"Grâce à l'application, je ne me trompe plus sur la poubelle jaune !"</p>
                        <p className="text-xs font-bold mt-2 text-white">— Un apprenti recycleur</p>
                    </div>
                </div>
            </div>

            {/* Partie Droite : Formulaire de Connexion */}
            <div className="w-full lg:w-1/2 flex items-center justify-center p-8 sm:p-12 overflow-y-auto">
                <div className="w-full max-w-md space-y-8">

                    {/* Logo & En-tête */}
                    <div className="text-center lg:text-left">
                        <div className="flex items-center justify-center lg:justify-start space-x-3 mb-6">
                            <div className="bg-ecoGreen p-2 rounded-lg text-white shadow-sm">
                                <Leaf className="w-6 h-6" />
                            </div>
                            <h2 className="text-2xl font-black text-gray-800 tracking-tight">One-Two-Tri Vision</h2>
                        </div>
                        <h3 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-2">Heureux de vous revoir 👋</h3>
                        <p className="text-gray-500 text-sm">Connectez-vous pour continuer votre parcours.</p>
                    </div>

                    {/* Formulaire */}
                    <form className="mt-8 space-y-5" action="#" method="POST" onSubmit={(e) => e.preventDefault()}>

                        {/* Champ Pseudo / Email */}
                        <div>
                            <label htmlFor="identifiant" className="block text-sm font-medium text-gray-700 mb-1">Pseudo ou Adresse e-mail</label>
                            <div className="relative">
                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <User className="h-5 w-5 text-gray-400" />
                                </div>
                                <input
                                    id="identifiant"
                                    name="identifiant"
                                    type="text"
                                    required
                                    className="block w-full pl-10 pr-3 py-2.5 border border-gray-300 rounded-xl focus:ring-2 focus:ring-ecoGreen focus:border-ecoGreen outline-none transition text-sm bg-gray-50 focus:bg-white"
                                    placeholder="ex: katia92"
                                />
                            </div>
                        </div>

                        {/* Champ Mot de passe */}
                        <div>
                            <div className="flex items-center justify-between mb-1">
                                <label htmlFor="password" className="block text-sm font-medium text-gray-700">Mot de passe</label>
                                <Link to="/passe-oublie" className="text-sm font-medium text-ecoGreen hover:text-green-700 transition">Mot de passe oublié ?</Link>
                            </div>
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

                        {/* Se souvenir de moi */}
                        <div className="flex items-center">
                            <input
                                id="remember-me"
                                name="remember-me"
                                type="checkbox"
                                className="h-4 w-4 text-ecoGreen focus:ring-ecoGreen border-gray-300 rounded cursor-pointer"
                            />
                            <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-600 cursor-pointer">
                                Se souvenir de moi
                            </label>
                        </div>

                        {/* Bouton de soumission */}
                        <button
                            type="submit"
                            className="w-full flex justify-center items-center space-x-2 py-3 px-4 border border-transparent rounded-xl shadow-sm text-sm font-bold text-white bg-ecoGreen hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-ecoGreen transition"
                        >
                            <span>Se connecter</span>
                            <ArrowRight className="w-4 h-4" />
                        </button>
                    </form>

                    {/* Séparateur */}
                    <div className="mt-6">
                        <div className="relative">
                            <div className="absolute inset-0 flex items-center">
                                <div className="w-full border-t border-gray-200"></div>
                            </div>
                            <div className="relative flex justify-center text-sm">
                                <span className="px-2 bg-ecoLight text-gray-500">Ou</span>
                            </div>
                        </div>
                    </div>

                    {/* Inscription */}
                    <div className="mt-6 text-center">
                        <p className="text-sm text-gray-600">
                            Nouveau ici ?{' '}
                            <Link to="/inscription" className="font-bold text-ecoBrown hover:text-orange-800 transition">Créer un compte</Link>
                        </p>
                    </div>

                </div>
            </div>
        </div>
    );
};

export default LoginPage;