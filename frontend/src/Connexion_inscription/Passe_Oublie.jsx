import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Leaf, Mail, ArrowRight, ArrowLeft, CheckCircle, KeyRound } from 'lucide-react';

export default function PasseOublie() {
    const [email, setEmail] = useState('');
    const [submitted, setSubmitted] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (email) setSubmitted(true);
    };

    return (
        <div className="bg-ecoLight text-gray-800 font-sans h-screen flex overflow-hidden">

            {/* Partie Gauche : Visuel */}
            <div className="hidden lg:flex lg:w-1/2 relative bg-ecoGreen items-center justify-center overflow-hidden">
                <img
                    src="https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80"
                    alt="Nature"
                    className="absolute inset-0 w-full h-full object-cover opacity-30 mix-blend-overlay"
                />

                <div className="relative z-10 p-12 max-w-lg text-white">
                    <div className="bg-white/20 backdrop-blur-md p-4 rounded-2xl inline-block mb-6 border border-white/30 shadow-lg">
                        <KeyRound className="w-12 h-12 text-white" />
                    </div>
                    <h1 className="text-4xl font-bold mb-4 leading-tight">Pas de panique, ça arrive à tout le monde.</h1>
                    <p className="text-green-50 text-lg leading-relaxed mb-8">
                        Entrez votre adresse e-mail et nous vous enverrons un lien pour réinitialiser votre mot de passe en toute sécurité.
                    </p>

                    <div className="bg-black/20 backdrop-blur-sm p-4 rounded-xl border-l-4 border-yellow-400">
                        <p className="text-sm italic text-green-50">"La sécurité de votre compte est notre priorité. Votre lien expirera dans 15 minutes."</p>
                        <p className="text-xs font-bold mt-2 text-white">— Équipe One-Two-Tri Vision</p>
                    </div>
                </div>
            </div>

            {/* Partie Droite */}
            <div className="w-full lg:w-1/2 flex items-center justify-center p-8 sm:p-12 overflow-y-auto">
                <div className="w-full max-w-md space-y-8">

                    {/* Logo */}
                    <div className="text-center lg:text-left">
                        <div className="flex items-center justify-center lg:justify-start space-x-3 mb-6">
                            <div className="bg-ecoGreen p-2 rounded-lg text-white shadow-sm">
                                <Leaf className="w-6 h-6" />
                            </div>
                            <h2 className="text-2xl font-black text-gray-800 tracking-tight">One-Two-Tri Vision</h2>
                        </div>

                        {!submitted ? (
                            <>
                                <h3 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-2">Mot de passe oublié 🔑</h3>
                                <p className="text-gray-500 text-sm">Saisissez l'adresse e-mail liée à votre compte. Nous vous enverrons un lien de réinitialisation.</p>
                            </>
                        ) : (
                            <>
                                <h3 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-2">E-mail envoyé ✅</h3>
                                <p className="text-gray-500 text-sm">Vérifiez votre boîte de réception et suivez le lien pour réinitialiser votre mot de passe.</p>
                            </>
                        )}
                    </div>

                    {!submitted ? (
                        /* Formulaire */
                        <form className="mt-8 space-y-5" onSubmit={handleSubmit}>

                            {/* Champ Email */}
                            <div>
                                <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                                    Adresse e-mail
                                </label>
                                <div className="relative">
                                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                        <Mail className="h-5 w-5 text-gray-400" />
                                    </div>
                                    <input
                                        id="email"
                                        name="email"
                                        type="email"
                                        required
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                        className="block w-full pl-10 pr-3 py-2.5 border border-gray-300 rounded-xl focus:ring-2 focus:ring-ecoGreen focus:border-ecoGreen outline-none transition text-sm bg-gray-50 focus:bg-white"
                                        placeholder="hello@exemple.com"
                                    />
                                </div>
                            </div>

                            {/* Bouton */}
                            <button
                                type="submit"
                                className="w-full flex justify-center items-center space-x-2 py-3 px-4 border border-transparent rounded-xl shadow-sm text-sm font-bold text-white bg-ecoGreen hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-ecoGreen transition"
                            >
                                <span>Envoyer le lien</span>
                                <ArrowRight className="w-4 h-4" />
                            </button>
                        </form>
                    ) : (
                        /* Message de confirmation */
                        <div className="mt-8 bg-green-50 border border-green-200 rounded-2xl p-6 text-center space-y-4">
                            <div className="flex justify-center">
                                <CheckCircle className="w-14 h-14 text-ecoGreen" />
                            </div>
                            <p className="text-sm text-gray-600">
                                Un e-mail de réinitialisation a été envoyé à <span className="font-bold text-gray-800">{email}</span>.<br />
                                Pensez à vérifier vos spams si vous ne le trouvez pas.
                            </p>
                            <button
                                type="button"
                                onClick={() => { setSubmitted(false); setEmail(''); }}
                                className="text-sm font-medium text-ecoGreen hover:text-green-700 transition underline underline-offset-2"
                            >
                                Utiliser une autre adresse
                            </button>
                        </div>
                    )}

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

                    {/* Retour à la connexion */}
                    <div className="mt-6 text-center">
                        <Link
                            to="/connexion"
                            className="inline-flex items-center justify-center space-x-2 text-sm font-bold text-gray-700 hover:text-gray-900 transition"
                        >
                            <ArrowLeft className="w-4 h-4" />
                            <span>Retour à la connexion</span>
                        </Link>
                    </div>

                </div>
            </div>
        </div>
    );
}
