import { ExternalLink } from 'lucide-react';

export const AdBanner = () => {
    // Simulate generic Google AdSense banner style
    return (
        <div className="w-full bg-slate-100 border-t border-slate-200 p-2 flex justify-center items-center relative">
            <div className="w-[728px] h-[90px] bg-white border border-slate-300 shadow-sm flex flex-col items-center justify-center relative overflow-hidden group cursor-pointer">
                {/* Ad Label */}
                <div className="absolute top-0 right-0 bg-slate-200 text-[10px] text-slate-500 px-1">
                    Annonce Google
                </div>

                {/* Simulated Content */}
                <div className="text-center p-2">
                    <p className="text-blue-600 font-bold text-lg hover:underline flex items-center gap-2 justify-center">
                        Study Abroad in Europe <ExternalLink size={14} />
                    </p>
                    <p className="text-slate-500 text-xs mt-1">
                        Master's degrees, PhDs, and Short courses. Apply now for 2026 intake.
                    </p>
                    <p className="text-emerald-600 text-[10px] mt-1 font-medium">www.study-europe.example.com</p>
                </div>

                {/* Hover Overlay to simulate click */}
                <div className="absolute inset-0 bg-blue-500/0 group-hover:bg-blue-500/5 transition-colors" />
            </div>
        </div>
    );
};
