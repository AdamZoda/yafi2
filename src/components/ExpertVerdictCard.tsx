import React from 'react';
import { motion } from 'framer-motion';
import { Award, CheckCircle, AlertTriangle, Info } from 'lucide-react';
import { clsx } from 'clsx';

interface ExpertVerdictCardProps {
  score: number;
  ecole?: string;
}

export const ExpertVerdictCard: React.FC<ExpertVerdictCardProps> = ({ score, ecole }) => {
  const getStatus = (s: number) => {
    if (s >= 75) return { label: 'Excellent', color: 'text-emerald-600', bg: 'bg-emerald-50', border: 'border-emerald-200', icon: <CheckCircle className="text-emerald-500" /> };
    if (s >= 60) return { label: 'Favorable', color: 'text-blue-600', bg: 'bg-blue-50', border: 'border-blue-200', icon: <Award className="text-blue-500" /> };
    if (s >= 45) return { label: 'Passable', color: 'text-amber-600', bg: 'bg-amber-50', border: 'border-amber-200', icon: <Info className="text-amber-500" /> };
    return { label: 'Difficile', color: 'text-slate-600', bg: 'bg-slate-50', border: 'border-slate-200', icon: <AlertTriangle className="text-slate-400" /> };
  };

  const status = getStatus(score);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      className={clsx(
        "mt-4 p-5 rounded-2xl border-2 shadow-sm flex flex-col items-center text-center",
        status.bg,
        status.border
      )}
    >
      <div className="flex items-center gap-2 mb-2">
        {status.icon}
        <span className={clsx("font-bold text-sm uppercase tracking-wider", status.color)}>
          Verdict Expert YAFI
        </span>
      </div>

      <h3 className="text-slate-800 font-bold text-lg mb-4">
        {ecole ? `Chance d'admission à l'${ecole}` : "Estimation d'admission"}
      </h3>

      <div className="relative w-32 h-32 mb-4">
        {/* SVG Gauge */}
        <svg className="w-full h-full" viewBox="0 0 100 100">
          <circle
            cx="50" cy="50" r="40"
            fill="transparent"
            stroke="#e2e8f0"
            strokeWidth="8"
          />
          <motion.circle
            cx="50" cy="50" r="40"
            fill="transparent"
            stroke={score >= 75 ? '#10b981' : score >= 60 ? '#3b82f6' : score >= 45 ? '#f59e0b' : '#94a3b8'}
            strokeWidth="8"
            strokeDasharray="251.2"
            initial={{ strokeDashoffset: 251.2 }}
            animate={{ strokeDashoffset: 251.2 - (251.2 * score) / 100 }}
            transition={{ duration: 1.5, ease: "easeOut" }}
            strokeLinecap="round"
            transform="rotate(-90 50 50)"
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-2xl font-black text-slate-800">{score}%</span>
          <span className="text-[10px] text-slate-500 uppercase font-medium">Probabilité</span>
        </div>
      </div>

      <div className={clsx("px-4 py-1 rounded-full font-bold text-sm", status.bg, status.color, "border", status.border)}>
        Profil {status.label}
      </div>
      
      <p className="mt-3 text-xs text-slate-500 italic">
        * Calculé via l'Expert System (Prolog) basé sur vos notes et critères d'admission.
      </p>
    </motion.div>
  );
};
