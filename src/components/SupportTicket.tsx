import React, { useState, useEffect, useRef } from 'react';
import { supabase } from '../lib/supabase';
import { Send, MessageSquare, History, X, Clock, AlertCircle, CheckCircle } from 'lucide-react';
import { clsx } from 'clsx';
import { useTheme } from '../contexts/ThemeContext';
import type { Profile } from '../types';

interface Ticket {
    id: string;
    subject: string;
    status: 'open' | 'closed';
    created_at: string;
}

interface TicketMessage {
    id: string;
    sender_id: string;
    content: string;
    created_at: string;
}

interface SupportTicketProps {
    profile: Profile;
}

export const SupportTicket: React.FC<SupportTicketProps> = ({ profile }) => {
    const { theme } = useTheme();
    const [tickets, setTickets] = useState<Ticket[]>([]);
    const [activeTicket, setActiveTicket] = useState<Ticket | null>(null);
    const [messages, setMessages] = useState<TicketMessage[]>([]);
    const [newMessage, setNewMessage] = useState('');
    const [newSubject, setNewSubject] = useState('');
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        fetchTickets();
    }, []);

    useEffect(() => {
        if (activeTicket) {
            fetchMessages(activeTicket.id);

            // Subscribe to real-time messages
            const subscription = supabase
                .channel(`ticket_${activeTicket.id}`)
                .on('postgres_changes', {
                    event: 'INSERT',
                    schema: 'public',
                    table: 'ticket_messages',
                    filter: `ticket_id=eq.${activeTicket.id}`
                }, (payload) => {
                    setMessages(prev => [...prev, payload.new as TicketMessage]);
                })
                .subscribe();

            return () => {
                supabase.removeChannel(subscription);
            };
        }
    }, [activeTicket]);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const fetchTickets = async () => {
        const { data } = await supabase
            .from('tickets')
            .select('*')
            .eq('user_id', profile.id)
            .order('created_at', { ascending: false });
        if (data) setTickets(data);
    };

    const fetchMessages = async (ticketId: string) => {
        const { data } = await supabase
            .from('ticket_messages')
            .select('*')
            .eq('ticket_id', ticketId)
            .order('created_at', { ascending: true });
        if (data) setMessages(data);
    };

    const handleOpenTicket = async () => {
        if (!newSubject.trim()) return;
        setLoading(true);
        setError(null);

        // --- 24H RATE LIMIT CHECK ---
        const { data: recentTickets } = await supabase
            .from('tickets')
            .select('created_at')
            .eq('user_id', profile.id)
            .order('created_at', { ascending: false })
            .limit(1);

        if (recentTickets && recentTickets.length > 0) {
            const lastTicketDate = new Date(recentTickets[0].created_at);
            const now = new Date();
            const diffHours = (now.getTime() - lastTicketDate.getTime()) / (1000 * 60 * 60);

            if (diffHours < 24) {
                setError(`Vous avez déjà ouvert un ticket récemment. Prochain ticket dans ${Math.ceil(24 - diffHours)} heures.`);
                setLoading(false);
                return;
            }
        }

        const { data, error: insertError } = await supabase
            .from('tickets')
            .insert({
                user_id: profile.id,
                subject: newSubject,
                status: 'open'
            })
            .select()
            .single();

        if (insertError) {
            setError(`Erreur: ${insertError.message || insertError.details || "Inconnue"}`);
            console.error("Supabase Error:", insertError);
        } else if (data) {
            setTickets([data, ...tickets]);
            setActiveTicket(data);
            setNewSubject('');
        }
        setLoading(false);
    };

    const handleSendMessage = async () => {
        if (!newMessage.trim() || !activeTicket || activeTicket.status === 'closed') return;

        const content = newMessage;
        setNewMessage('');

        const { error } = await supabase
            .from('ticket_messages')
            .insert({
                ticket_id: activeTicket.id,
                sender_id: profile.id,
                content: content
            });

        if (error) {
            console.error("Error sending message:", error);
            setError("Échec de l'envoi.");
        }
    };

    const closeTicket = async (ticketId: string) => {
        const { error } = await supabase
            .from('tickets')
            .update({ status: 'closed' })
            .eq('id', ticketId);

        if (!error) {
            setTickets(tickets.map(t => t.id === ticketId ? { ...t, status: 'closed' } : t));
            if (activeTicket?.id === ticketId) {
                setActiveTicket(prev => prev ? { ...prev, status: 'closed' } : null);
            }
        }
    };

    return (
        <div className="flex h-full bg-white rounded-3xl overflow-hidden shadow-xl border border-slate-100">
            {/* Ticket List / Sidebar */}
            <div className="w-80 border-r border-slate-100 flex flex-col bg-slate-50">
                <div className="p-6 border-b border-slate-100 bg-white">
                    <h2 className="text-xl font-bold text-slate-800 flex items-center gap-2">
                        <MessageSquare className="text-emerald-500" size={24} />
                        Support Client
                    </h2>
                    <p className="text-xs text-slate-500 mt-1 uppercase font-bold tracking-wider">Premium Assistance</p>
                </div>

                <div className="flex-1 overflow-y-auto p-4 space-y-3">
                    {/* Open New Ticket Form */}
                    <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm mb-4">
                        <h3 className="text-sm font-bold text-slate-700 mb-2">Nouveau Ticket</h3>
                        <input
                            value={newSubject}
                            onChange={(e) => setNewSubject(e.target.value)}
                            placeholder="Sujet de votre demande..."
                            className="w-full p-2 text-sm border border-slate-200 rounded-lg mb-2 focus:ring-2 focus:ring-emerald-500/20 outline-none"
                        />
                        <button
                            onClick={handleOpenTicket}
                            disabled={loading || !newSubject.trim()}
                            className="w-full py-2 bg-emerald-600 text-white rounded-lg text-xs font-bold hover:bg-emerald-700 transition-colors disabled:opacity-50"
                        >
                            {loading ? "Chargement..." : "Ouvrir un ticket"}
                        </button>
                    </div>

                    <div className="px-2 py-2 text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-2">
                        <History size={12} /> Vos Tickets
                    </div>

                    {tickets.map(ticket => (
                        <button
                            key={ticket.id}
                            onClick={() => setActiveTicket(ticket)}
                            className={clsx(
                                "w-full text-left p-4 rounded-2xl transition-all border",
                                activeTicket?.id === ticket.id
                                    ? "bg-white border-emerald-500 shadow-md ring-1 ring-emerald-500"
                                    : "bg-white border-slate-100 hover:border-slate-300 shadow-sm"
                            )}
                        >
                            <div className="flex justify-between items-start mb-1">
                                <span className={clsx(
                                    "text-[10px] px-2 py-0.5 rounded-full font-bold uppercase",
                                    ticket.status === 'open' ? "bg-emerald-100 text-emerald-700" : "bg-slate-100 text-slate-500"
                                )}>
                                    {ticket.status === 'open' ? 'En cours' : 'Fermé'}
                                </span>
                                <span className="text-[10px] text-slate-400">
                                    {new Date(ticket.created_at).toLocaleDateString()}
                                </span>
                            </div>
                            <p className="text-sm font-bold text-slate-800 truncate">{ticket.subject}</p>
                        </button>
                    ))}
                </div>
            </div>

            {/* Chat Area */}
            <div className="flex-1 flex flex-col bg-white">
                {activeTicket ? (
                    <>
                        {/* Header Chat */}
                        <div className="p-6 border-b border-slate-100 flex justify-between items-center shadow-sm">
                            <div>
                                <h3 className="text-lg font-bold text-slate-800">{activeTicket.subject}</h3>
                                <div className="flex items-center gap-2 text-xs text-slate-500">
                                    <Clock size={12} /> Ouvert le {new Date(activeTicket.created_at).toLocaleString()}
                                </div>
                            </div>
                            <div className="flex items-center gap-3">
                                {activeTicket.status === 'open' && (
                                    <button
                                        onClick={() => closeTicket(activeTicket.id)}
                                        className="px-4 py-2 border border-slate-200 text-slate-500 rounded-xl text-sm font-bold hover:bg-slate-50 transition-all flex items-center gap-2"
                                    >
                                        <X size={16} /> Fermer
                                    </button>
                                )}
                                <span className={clsx(
                                    "px-4 py-2 rounded-xl text-sm font-bold border",
                                    activeTicket.status === 'open' ? "bg-emerald-50 border-emerald-100 text-emerald-700" : "bg-slate-50 border-slate-100 text-slate-500"
                                )}>
                                    {activeTicket.status === 'open' ? '✓ Ouvert' : '✕ Fermé'}
                                </span>
                            </div>
                        </div>

                        {/* Messages */}
                        <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-slate-50/30">
                            {messages.map(msg => (
                                <div key={msg.id} className={clsx(
                                    "flex flex-col max-w-[80%]",
                                    msg.sender_id === profile.id ? "ml-auto items-end" : "items-start"
                                )}>
                                    <div className={clsx(
                                        "p-4 rounded-2xl shadow-sm",
                                        msg.sender_id === profile.id
                                            ? "bg-emerald-600 text-white rounded-tr-none"
                                            : "bg-white border border-slate-100 text-slate-800 rounded-tl-none"
                                    )}>
                                        <p className="text-sm leading-relaxed">{msg.content}</p>
                                    </div>
                                    <span className="text-[10px] text-slate-400 mt-1 px-1">
                                        {new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                    </span>
                                </div>
                            ))}
                            <div ref={messagesEndRef} />
                        </div>

                        {/* Input Area */}
                        {activeTicket.status === 'open' ? (
                            <div className="p-6 bg-white border-t border-slate-100">
                                <div className="relative flex items-center gap-3">
                                    <input
                                        value={newMessage}
                                        onChange={(e) => setNewMessage(e.target.value)}
                                        onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
                                        placeholder="Votre message ici..."
                                        className="flex-1 p-4 pr-16 border border-slate-200 rounded-2xl focus:ring-4 focus:ring-emerald-500/10 focus:border-emerald-500 outline-none transition-all shadow-sm"
                                    />
                                    <button
                                        onClick={handleSendMessage}
                                        disabled={!newMessage.trim()}
                                        className="absolute right-2 p-3 bg-emerald-600 text-white rounded-xl hover:bg-emerald-700 transition-all disabled:opacity-50 shadow-lg shadow-emerald-200 active:scale-90"
                                    >
                                        <Send size={20} />
                                    </button>
                                </div>
                            </div>
                        ) : (
                            <div className="p-10 bg-slate-50 text-center border-t border-slate-100">
                                <div className="bg-white p-6 rounded-3xl border border-slate-200 inline-block">
                                    <CheckCircle size={48} className="mx-auto mb-4 text-emerald-500" />
                                    <h4 className="font-bold text-slate-800">Ticket Résolu</h4>
                                    <p className="text-sm text-slate-500 max-w-xs mx-auto mt-2">
                                        Cette conversation est close. Vous pouvez ouvrir un nouveau ticket dans 24h si besoin.
                                    </p>
                                </div>
                            </div>
                        )}
                    </>
                ) : (
                    <div className="flex-1 flex flex-col items-center justify-center p-12 text-center text-slate-400">
                        <div className="w-20 h-20 bg-emerald-50 rounded-full flex items-center justify-center mb-6">
                            <MessageSquare size={40} className="text-emerald-500" />
                        </div>
                        <h3 className="text-xl font-bold text-slate-800 mb-2">Centre de Support Premium</h3>
                        <p className="max-w-md text-slate-500">
                            Sélectionnez un ticket dans la liste à gauche pour voir les messages ou ouvrez un nouveau ticket pour discuter avec un admin.
                        </p>

                        {error && (
                            <div className="mt-8 p-4 bg-red-50 text-red-600 rounded-2xl flex items-center gap-3 border border-red-100 animate-shake">
                                <AlertCircle size={20} />
                                <span className="text-sm font-bold">{error}</span>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
};
