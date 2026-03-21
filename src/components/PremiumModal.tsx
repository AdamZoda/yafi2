import React, { useEffect, useState } from 'react';
import { X, Check, Star, Zap, Shield, Clock } from 'lucide-react';
import { clsx } from 'clsx';
import { useTheme } from '../contexts/ThemeContext';

interface PremiumModalProps {
    isOpen: boolean;
    onClose: () => void;
    userEmail?: string;
    lastRequestTime?: string | null;
}

export const PremiumModal: React.FC<PremiumModalProps> = ({ isOpen, onClose, userEmail, lastRequestTime }) => {
    const { theme } = useTheme();
    const [timeLeft, setTimeLeft] = useState<string>("");

    useEffect(() => {
        if (!isOpen || !lastRequestTime) {
            setTimeLeft("");
            return;
        }

        const interval = setInterval(() => {
            const now = new Date();
            const lastReq = new Date(lastRequestTime);
            // 30 minutes in ms = 30 * 60 * 1000 = 1,800,000
            const nextAvailable = new Date(lastReq.getTime() + 1800000);
            const diff = nextAvailable.getTime() - now.getTime();

            if (diff <= 0) {
                setTimeLeft("Maintenant !");
                clearInterval(interval);
            } else {
                const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
                const seconds = Math.floor((diff % (1000 * 60)) / 1000);
                setTimeLeft(`${minutes}m ${seconds}s`);
            }
        }, 1000);

        return () => clearInterval(interval);
    }, [isOpen, lastRequestTime]);

    if (!isOpen) return null;

    const paymentLink = "https://moufrij.gumroad.com/l/yoqenx"; // Placeholder

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fade-in">
            <div className="bg-white rounded-3xl shadow-2xl w-full max-w-lg overflow-hidden relative animate-scale-in">

                {/* Header with Gradient */}
                <div className={clsx("p-8 text-center relative overflow-hidden", theme.primary)}>
                    <div className="absolute top-0 left-0 w-full h-full bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10"></div>
                    <button
                        onClick={onClose}
                        className="absolute top-4 right-4 p-2 bg-white/20 hover:bg-white/30 rounded-full text-white transition-colors"
                    >
                        <X size={20} />
                    </button>

                    <div className="inline-flex items-center justify-center p-3 bg-white/20 rounded-2xl mb-4 backdrop-blur-md shadow-inner">
                        <Star className="text-yellow-300 fill-yellow-300" size={32} />
                    </div>
                    <h2 className="text-3xl font-bold text-white mb-2">Passez à YAFI PLUS</h2>
                    <p className="text-blue-50/90 font-medium">Débloquez tout le potentiel de votre assistant</p>
                </div>

                {/* Content */}
                <div className="p-8">
                    <div className="flex items-center justify-center mb-8">
                        <span className="text-5xl font-extrabold text-slate-800">30 <span className="text-2xl text-slate-500 font-semibold">DH</span></span>
                        <span className="ml-2 px-3 py-1 bg-green-100 text-green-700 text-xs font-bold uppercase tracking-wider rounded-full">Offre Unique</span>
                    </div>

                    {/* Timer Alert */}
                    {timeLeft && timeLeft !== "Maintenant !" && (
                        <div className="mb-6 p-4 bg-orange-50 border border-orange-200 rounded-xl flex items-center gap-3 animate-pulse">
                            <Clock className="text-orange-500" size={24} />
                            <div>
                                <p className="text-sm font-bold text-orange-800">Limite atteinte (5/5)</p>
                                <p className="text-xs text-orange-600">
                                    Prochaines questions gratuites dans : <span className="font-mono font-bold text-lg ml-1">{timeLeft}</span>
                                </p>
                            </div>
                        </div>
                    )}

                    <div className="space-y-4 mb-8">
                        <FeatureRow icon={<Zap className="text-yellow-500" />} text="Accès illimité (Questions sans limite)" />
                        <FeatureRow icon={<Shield className="text-green-500" />} text="Aucune publicité" />
                        <FeatureRow icon={<Star className="text-purple-500" />} text="Support prioritaire & Futures updates" />
                        <FeatureRow icon={<Check className="text-blue-500" />} text="Badge Membre Premium" />
                    </div>

                    <div className="space-y-3">
                        <a
                            href={paymentLink}
                            target="_blank"
                            rel="noopener noreferrer"
                            className={clsx(
                                "block w-full py-4 rounded-xl text-center font-bold text-lg text-white shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all",
                                theme.primary
                            )}
                        >
                            Obtenir l'accès maintenant
                        </a>
                        <p className="text-xs text-center text-slate-400 mt-4">
                            Paiement sécurisé. Aucun abonnement caché. <br />
                            Après paiement, contactez le support avec votre email : <span className="font-mono text-slate-600">{userEmail}</span>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

const FeatureRow = ({ icon, text }: { icon: React.ReactNode, text: string }) => (
    <div className="flex items-center gap-4 p-3 rounded-xl hover:bg-slate-50 transition-colors">
        <div className="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center shadow-sm">
            {icon}
        </div>
        <span className="text-slate-700 font-medium">{text}</span>
    </div>
);
