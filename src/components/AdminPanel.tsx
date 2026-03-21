import { useState, useEffect } from 'react';
import { supabase } from '../lib/supabase';
import { FileText, Database, Users, Save, Trash, Plus, ArrowLeft, HelpCircle, Brain } from 'lucide-react';
import { clsx } from 'clsx';
import { useNavigate, Link } from 'react-router-dom';
import { useRef } from 'react';
import { LifeBuoy, Send } from 'lucide-react';

export const AdminPanel = () => {
    const [activeTab, setActiveTab] = useState<'knowledge' | 'members' | 'custom_qa' | 'tickets'>('members');

    const TabButton = ({ id, icon: Icon, label }: { id: any, icon: any, label: string }) => (
        <button
            onClick={() => setActiveTab(id)}
            className={clsx(
                "flex items-center gap-2 px-6 py-4 font-medium transition-all border-b-2 whitespace-nowrap",
                activeTab === id
                    ? "border-emerald-600 text-emerald-800 bg-emerald-50/50"
                    : "border-transparent text-slate-500 hover:text-slate-700 hover:bg-slate-50"
            )}
        >
            <Icon size={18} />
            {label}
        </button>
    );

    return (
        <div className="min-h-screen bg-slate-50 p-6 font-sans mt-16">
            <header className="mb-8 flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-slate-800">Admin Center</h1>
                    <p className="text-slate-500">YAFI Chatbot Configuration</p>
                </div>
                <Link
                    to="/"
                    className="flex items-center gap-2 px-4 py-2 bg-white text-slate-700 font-bold rounded-xl border border-slate-200 hover:bg-slate-50 hover:text-emerald-600 transition-all shadow-sm"
                >
                    <ArrowLeft size={18} />
                    Retour au Chat
                </Link>
            </header>

            <div className="bg-white rounded-3xl shadow-sm border border-slate-200 overflow-hidden w-full">
                <div className="flex border-b border-slate-200 overflow-x-auto">
                    <TabButton id="members" icon={Users} label="Membres" />
                    <TabButton id="custom_qa" icon={HelpCircle} label="Q&A Personnalisées" />
                    <TabButton id="tickets" icon={LifeBuoy} label="Tickets Support" />
                    <TabButton id="knowledge" icon={Database} label="Base Documentaire" />
                </div>

                <div className="p-8 h-[calc(100vh-220px)] overflow-y-auto">
                    {activeTab === 'knowledge' && <KnowledgeTab />}
                    {activeTab === 'custom_qa' && <CustomQATab />}
                    {activeTab === 'members' && <MembersTab />}
                    {activeTab === 'tickets' && <TicketsTab />}
                </div>
            </div>
        </div>
    );
};

const KnowledgeTab = () => {
    const [docs, setDocs] = useState<any[]>([]);
    const [newDocName, setNewDocName] = useState('');
    const [newDocContent, setNewDocContent] = useState('');

    useEffect(() => {
        const fetchDocs = async () => {
            const { data } = await supabase.from('knowledge_base').select('*');
            if (data) setDocs(data);
        };
        fetchDocs();
    }, []);

    const handleAdd = async () => {
        if (!newDocName || !newDocContent) return;
        const { data } = await supabase.from('knowledge_base').insert({
            name: newDocName,
            content: newDocContent,
            type: 'text/plain'
        }).select();

        if (data) {
            setDocs([...docs, data[0]]);
            setNewDocName('');
            setNewDocContent('');
        }
    };

    return (
        <div>
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-bold">Base de Connaissances (RAG)</h2>
            </div>

            {/* Add New */}
            <div className="bg-slate-50 p-6 rounded-2xl border border-slate-200 mb-8">
                <h3 className="font-bold text-slate-700 mb-4">Ajouter un document texte</h3>
                <div className="space-y-3">
                    <input
                        className="w-full p-3 rounded-lg border border-slate-300"
                        placeholder="Titre du document (ex: Guide YAFI 2024)"
                        value={newDocName}
                        onChange={e => setNewDocName(e.target.value)}
                    />
                    <textarea
                        className="w-full p-3 rounded-lg border border-slate-300 h-32"
                        placeholder="Contenu du document..."
                        value={newDocContent}
                        onChange={e => setNewDocContent(e.target.value)}
                    />
                    <button onClick={handleAdd} className="px-4 py-2 bg-slate-800 text-white rounded-lg text-sm font-semibold hover:bg-slate-900">
                        Publier dans la base
                    </button>
                </div>
            </div>

            {/* List */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {docs.length === 0 ? (
                    <div className="text-center py-8 text-slate-400 bg-white border border-dashed border-slate-200 rounded-xl">
                        <Database size={32} className="mx-auto mb-2 opacity-50" />
                        <p>Aucun document.</p>
                    </div>
                ) : docs.map(doc => (
                    <div key={doc.id} className="p-4 bg-white border border-slate-100 rounded-xl shadow-sm flex justify-between items-center group">
                        <div className="flex items-center gap-3">
                            <div className="p-2 bg-emerald-50 text-emerald-600 rounded-lg">
                                <FileText size={20} />
                            </div>
                            <div>
                                <p className="font-bold text-slate-800">{doc.name}</p>
                                <p className="text-xs text-slate-400">Ajouté le {new Date(doc.created_at).toLocaleDateString()}</p>
                            </div>
                        </div>
                        <button className="text-slate-300 hover:text-red-500 transition-colors p-2">
                            <Trash size={18} />
                        </button>
                    </div>
                ))}
            </div>
        </div>
    )
}

const MembersTab = () => {
    const [members, setMembers] = useState<any[]>([]);
    const [selectedMember, setSelectedMember] = useState<any | null>(null);
    const [memberSessions, setMemberSessions] = useState<any[]>([]);
    const [memberMessages, setMemberMessages] = useState<any[]>([]);

    useEffect(() => {
        const fetchMembers = async () => {
            // Fetch real users from our custom table
            const { data } = await supabase
                .from('users')
                .select('*')
                .order('created_at', { ascending: false });

            if (data) setMembers(data);
        };
        fetchMembers();
    }, []);

    // Load member sessions and messages when selected
    useEffect(() => {
        if (!selectedMember) {
            setMemberSessions([]);
            setMemberMessages([]);
            return;
        }

        const loadMemberData = async () => {
            // Fetch sessions
            const { data: sessions } = await supabase
                .from('sessions')
                .select('*')
                .eq('user_id', selectedMember.id)
                .order('created_at', { ascending: false });

            if (sessions) {
                setMemberSessions(sessions);

                // Fetch all messages from all sessions
                const sessionIds = sessions.map(s => s.id);
                if (sessionIds.length > 0) {
                    const { data: messages } = await supabase
                        .from('messages')
                        .select('*')
                        .in('session_id', sessionIds)
                        .order('created_at', { ascending: true });

                    if (messages) setMemberMessages(messages);
                }
            }
        };
        loadMemberData();
    }, [selectedMember]);

    const togglePremium = async (member: any) => {
        const newValue = !member.is_premium;
        const { error } = await supabase
            .from('users')
            .update({ is_premium: newValue })
            .eq('id', member.id);

        if (error) {
            console.error('Error updating premium status:', error);
            alert('Erreur: ' + error.message);
        } else {
            // Update local state
            setMembers(members.map(m => m.id === member.id ? { ...m, is_premium: newValue } : m));
            if (selectedMember && selectedMember.id === member.id) {
                setSelectedMember({ ...selectedMember, is_premium: newValue });
            }
        }
    };

    // Extract profile info from messages
    const extractProfileInfo = (messages: any[]) => {
        const userMessages = messages.filter(m => m.role === 'user').map(m => m.content.toLowerCase());
        const fullText = userMessages.join(' ');

        const info: { age?: string; bac?: string; moyenne?: string; ville?: string; objectif?: string } = {};

        // Extract age
        const ageMatch = fullText.match(/j'ai (\d+) ans|(\d+) ans|age (\d+)/);
        if (ageMatch) info.age = (ageMatch[1] || ageMatch[2] || ageMatch[3]) + ' ans';

        // Extract Bac type  
        if (fullText.includes('bac pc') || fullText.includes('pc')) info.bac = 'PC';
        else if (fullText.includes('bac sm') || fullText.includes('sm')) info.bac = 'SM';
        else if (fullText.includes('bac svt') || fullText.includes('svt')) info.bac = 'SVT';
        else if (fullText.includes('bac eco') || fullText.includes('eco')) info.bac = 'ECO';
        else if (fullText.includes('bac litt')) info.bac = 'Littéraire';

        // Extract moyenne
        const moyenneMatch = fullText.match(/moyenne (\d+\.?\d*)|(\d+\.?\d*) de moyenne|note (\d+\.?\d*)/);
        if (moyenneMatch) info.moyenne = (moyenneMatch[1] || moyenneMatch[2] || moyenneMatch[3]) + '/20';

        // Extract city
        const villes = ['casablanca', 'rabat', 'marrakech', 'fès', 'tanger', 'agadir', 'oujda', 'safi', 'kenitra'];
        for (const v of villes) {
            if (fullText.includes(v)) {
                info.ville = v.charAt(0).toUpperCase() + v.slice(1);
                break;
            }
        }

        // Extract objective
        if (fullText.includes('médecine') || fullText.includes('medecine')) info.objectif = 'Médecine';
        else if (fullText.includes('ingénieur') || fullText.includes('ingenieur') || fullText.includes('ensa')) info.objectif = 'Ingénierie';
        else if (fullText.includes('informatique') || fullText.includes('it') || fullText.includes('data')) info.objectif = 'Informatique';
        else if (fullText.includes('commerce') || fullText.includes('gestion')) info.objectif = 'Commerce/Gestion';

        return info;
    };

    const profileInfo = selectedMember ? extractProfileInfo(memberMessages) : {};

    return (
        <div>
            <h2 className="text-xl font-bold mb-6">Utilisateurs Enregistrés</h2>

            {/* Back button if member is selected */}
            {selectedMember && (
                <button
                    onClick={() => setSelectedMember(null)}
                    className="mb-4 px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-sm font-medium flex items-center gap-2"
                >
                    <ArrowLeft size={16} /> Retour à la liste
                </button>
            )}

            {/* Member detail view */}
            {selectedMember ? (
                <div className="space-y-6">
                    {/* Member header */}
                    <div className="bg-gradient-to-r from-emerald-50 to-slate-50 p-6 rounded-2xl border border-emerald-100">
                        <div className="flex items-center gap-4">
                            <div className={clsx(
                                "w-16 h-16 rounded-full flex items-center justify-center font-bold text-white text-2xl",
                                selectedMember.role === 'admin' ? "bg-emerald-600" : "bg-slate-500"
                            )}>
                                {selectedMember.full_name?.charAt(0).toUpperCase() || "?"}
                            </div>
                            <div>
                                <h3 className="text-2xl font-bold text-slate-800">{selectedMember.full_name}</h3>
                                <p className="text-slate-500">{selectedMember.email}</p>
                                <span className={clsx(
                                    "text-xs px-3 py-1 rounded-full font-medium mt-2 inline-block",
                                    selectedMember.role === 'admin' ? "bg-emerald-100 text-emerald-800" : "bg-slate-100 text-slate-600"
                                )}>
                                    {selectedMember.role === 'admin' ? 'Administrateur' : 'Utilisateur'}
                                </span>
                                {selectedMember.is_premium && (
                                    <span className="ml-2 text-xs px-3 py-1 rounded-full font-bold bg-amber-100 text-amber-700 inline-block border border-amber-200">
                                        👑 PREMIUM
                                    </span>
                                )}
                            </div>
                        </div>
                        <button
                            onClick={() => togglePremium(selectedMember)}
                            className={clsx(
                                "px-4 py-2 rounded-xl font-bold text-sm transition-all shadow-sm",
                                selectedMember.is_premium
                                    ? "bg-white text-slate-700 border border-slate-200 hover:bg-slate-50"
                                    : "bg-amber-400 text-white hover:bg-amber-500 shadow-amber-200"
                            )}
                        >
                            {selectedMember.is_premium ? 'Retirer Premium' : 'Donner Premium 👑'}
                        </button>
                    </div>

                    {/* Profile info extracted from conversations */}
                    <div className="bg-white p-6 rounded-2xl border border-slate-200">
                        <h4 className="font-bold text-slate-700 mb-4 flex items-center gap-2">
                            <Brain size={18} className="text-emerald-500" />
                            Profil Extrait des Conversations
                        </h4>
                        {Object.keys(profileInfo).length > 0 ? (
                            <div className="grid grid-cols-2 gap-4">
                                {profileInfo.age && (
                                    <div className="p-3 bg-slate-50 rounded-lg">
                                        <p className="text-xs text-slate-400 uppercase">Âge</p>
                                        <p className="font-bold text-slate-800">{profileInfo.age}</p>
                                    </div>
                                )}
                                {profileInfo.bac && (
                                    <div className="p-3 bg-slate-50 rounded-lg">
                                        <p className="text-xs text-slate-400 uppercase">Type de Bac</p>
                                        <p className="font-bold text-slate-800">Bac {profileInfo.bac}</p>
                                    </div>
                                )}
                                {profileInfo.moyenne && (
                                    <div className="p-3 bg-slate-50 rounded-lg">
                                        <p className="text-xs text-slate-400 uppercase">Moyenne</p>
                                        <p className="font-bold text-slate-800">{profileInfo.moyenne}</p>
                                    </div>
                                )}
                                {profileInfo.ville && (
                                    <div className="p-3 bg-slate-50 rounded-lg">
                                        <p className="text-xs text-slate-400 uppercase">Ville</p>
                                        <p className="font-bold text-slate-800">{profileInfo.ville}</p>
                                    </div>
                                )}
                                {profileInfo.objectif && (
                                    <div className="p-3 bg-emerald-50 rounded-lg col-span-2">
                                        <p className="text-xs text-emerald-600 uppercase">Objectif</p>
                                        <p className="font-bold text-emerald-800">{profileInfo.objectif}</p>
                                    </div>
                                )}
                            </div>
                        ) : (
                            <p className="text-slate-400 italic">Aucune information personnelle détectée dans les conversations.</p>
                        )}
                    </div>

                    {/* Sessions summary */}
                    <div className="bg-white p-6 rounded-2xl border border-slate-200">
                        <h4 className="font-bold text-slate-700 mb-4">Sessions ({memberSessions.length})</h4>
                        <div className="space-y-2 max-h-64 overflow-y-auto">
                            {memberSessions.map(s => (
                                <div key={s.id} className="p-3 bg-slate-50 rounded-lg flex justify-between items-center">
                                    <p className="font-medium text-slate-700 truncate">{s.title || 'Nouvelle conversation'}</p>
                                    <p className="text-xs text-slate-400">{new Date(s.created_at).toLocaleDateString()}</p>
                                </div>
                            ))}
                            {memberSessions.length === 0 && (
                                <p className="text-slate-400 italic">Aucune session.</p>
                            )}
                        </div>
                    </div>
                </div>
            ) : (
                /* Member list */
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {members.map((m) => (
                        <div
                            key={m.id}
                            onClick={() => setSelectedMember(m)}
                            className="p-4 bg-white border border-slate-200 rounded-xl flex items-center gap-4 hover:shadow-md hover:border-emerald-200 transition-all cursor-pointer"
                        >
                            <div className={clsx(
                                "w-12 h-12 rounded-full flex items-center justify-center font-bold text-white text-lg",
                                m.role === 'admin' ? "bg-emerald-600" : "bg-slate-400"
                            )}>
                                {m.full_name?.charAt(0).toUpperCase() || "?"}
                            </div>
                            <div className="flex-1">
                                <p className="font-bold text-slate-800">{m.full_name}</p>
                                <p className="text-sm text-slate-500">{m.email}</p>
                                <span className={clsx(
                                    "text-xs px-2 py-0.5 rounded-full font-medium mt-1 inline-block",
                                    m.role === 'admin' ? "bg-emerald-100 text-emerald-800" : "bg-slate-100 text-slate-600"
                                )}>
                                    {m.role === 'admin' ? 'Administrateur' : 'Utilisateur'}
                                </span>
                                {m.is_premium && (
                                    <span className="ml-2 text-[10px] px-2 py-0.5 rounded-full font-bold bg-amber-100 text-amber-700 inline-block border border-amber-200">
                                        👑 PREMIUM
                                    </span>
                                )}
                            </div>
                            <button
                                onClick={(e) => {
                                    e.stopPropagation();
                                    togglePremium(m);
                                }}
                                className={clsx(
                                    "p-2 rounded-lg transition-colors",
                                    m.is_premium ? "text-amber-500 hover:bg-amber-50" : "text-slate-300 hover:text-amber-400 hover:bg-slate-50"
                                )}
                                title={m.is_premium ? "Retirer Premium" : "Donner Premium"}
                            >
                                <Users size={18} className={m.is_premium ? "fill-amber-500" : ""} />
                            </button>
                            <ArrowLeft size={16} className="text-slate-300 rotate-180" />
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

const CustomQATab = () => {
    const [qaList, setQaList] = useState<any[]>([]);
    const [questions, setQuestions] = useState<string[]>(['']);
    const [answer, setAnswer] = useState('');
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        fetchQA();
    }, []);

    const fetchQA = async () => {
        const { data } = await supabase.from('custom_qa').select('*').order('created_at', { ascending: false });
        if (data) setQaList(data);
    };

    const handleAddQuestionField = () => {
        setQuestions([...questions, '']);
    };

    const handleRemoveQuestionField = (index: number) => {
        if (questions.length > 1) {
            const newQuestions = [...questions];
            newQuestions.splice(index, 1);
            setQuestions(newQuestions);
        }
    };

    const handleQuestionChange = (index: number, value: string) => {
        const newQuestions = [...questions];
        newQuestions[index] = value;
        setQuestions(newQuestions);
    };

    const handlePublish = async () => {
        const validQuestions = questions.filter(q => q.trim() !== '');
        if (validQuestions.length === 0 || !answer.trim()) {
            alert("Veuillez remplir au moins une question et une réponse.");
            return;
        }

        setLoading(true);
        const { data, error } = await supabase.from('custom_qa').insert({
            questions: validQuestions,
            answer: answer.trim()
        }).select();

        setLoading(false);

        if (error) {
            alert("Erreur lors de la publication: " + error.message);
        } else if (data) {
            setQaList([data[0], ...qaList]);
            setQuestions(['']);
            setAnswer('');
        }
    };

    const handleDelete = async (id: string) => {
        if (!confirm("Voulez-vous vraiment supprimer cette Q&A ?")) return;

        const { error } = await supabase.from('custom_qa').delete().eq('id', id);
        if (!error) {
            setQaList(qaList.filter(item => item.id !== id));
        } else {
            alert("Erreur lors de la suppression.");
        }
    };

    return (
        <div className="space-y-8">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-xl font-bold text-slate-800">Questions-Réponses Personnalisées</h2>
                    <p className="text-sm text-slate-500">Ajoutez des réponses spécifiques pour des questions attendues.</p>
                </div>
            </div>

            {/* Form */}
            <div className="bg-slate-50 p-6 rounded-2xl border border-slate-200">
                <div className="space-y-6">
                    <div>
                        <label className="block text-sm font-bold text-slate-700 mb-3">
                            Questions attendues (cliquez sur + pour ajouter des variantes)
                        </label>
                        <div className="space-y-3">
                            {questions.map((q, index) => (
                                <div key={index} className="flex gap-2">
                                    <input
                                        className="flex-1 p-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500"
                                        placeholder={`Question ${index + 1} (ex: Quels sont les frais ?)`}
                                        value={q}
                                        onChange={e => handleQuestionChange(index, e.target.value)}
                                    />
                                    {questions.length > 1 && (
                                        <button
                                            onClick={() => handleRemoveQuestionField(index)}
                                            className="p-3 text-slate-400 hover:text-red-500 transition-colors"
                                        >
                                            <Trash size={18} />
                                        </button>
                                    )}
                                </div>
                            ))}
                            <button
                                onClick={handleAddQuestionField}
                                className="flex items-center gap-2 text-sm font-bold text-emerald-600 hover:text-emerald-700 transition-colors px-1"
                            >
                                <Plus size={16} /> Ajouter une autre variante de question
                            </button>
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-bold text-slate-700 mb-2">Réponse à donner</label>
                        <textarea
                            className="w-full p-4 rounded-xl border border-slate-300 focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 h-32"
                            placeholder="Écrivez la réponse structurée ici..."
                            value={answer}
                            onChange={e => setAnswer(e.target.value)}
                        />
                    </div>

                    <button
                        onClick={handlePublish}
                        disabled={loading}
                        className={clsx(
                            "w-full py-4 rounded-xl font-bold text-white transition-all flex items-center justify-center gap-2 shadow-lg",
                            loading ? "bg-slate-400 cursor-not-allowed" : "bg-emerald-600 hover:bg-emerald-700 shadow-emerald-200"
                        )}
                    >
                        {loading ? "Publication..." : <><Save size={18} /> Publier la Q&A</>}
                    </button>
                </div>
            </div>

            {/* List */}
            <div className="space-y-4">
                <h3 className="font-bold text-slate-700 flex items-center gap-2">
                    <Database size={18} /> Liste des Q&A Personnalisées ({qaList.length})
                </h3>

                {qaList.length === 0 ? (
                    <div className="text-center py-12 bg-white rounded-2xl border border-dashed border-slate-200">
                        <HelpCircle size={48} className="mx-auto mb-3 text-slate-200" />
                        <p className="text-slate-400">Aucune Q&A personnalisée pour le moment.</p>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        {qaList.map((qa) => (
                            <div key={qa.id} className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm hover:border-emerald-200 transition-colors group">
                                <div className="flex justify-between items-start mb-4">
                                    <div className="space-y-1">
                                        {qa.questions.map((q: string, idx: number) => (
                                            <div key={idx} className="flex items-center gap-2 text-sm font-bold text-slate-800">
                                                <div className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                                                {q}
                                            </div>
                                        ))}
                                    </div>
                                    <button
                                        onClick={() => handleDelete(qa.id)}
                                        className="p-2 text-slate-300 hover:text-red-500 transition-colors"
                                    >
                                        <Trash size={18} />
                                    </button>
                                </div>
                                <div className="p-4 bg-slate-50 rounded-xl text-sm text-slate-600 leading-relaxed whitespace-pre-wrap">
                                    {qa.answer}
                                </div>
                                <div className="mt-3 flex justify-between items-center text-[10px] text-slate-400 uppercase font-bold tracking-wider">
                                    <span>{qa.questions.length} question(s) configurée(s)</span>
                                    <span>Ajouté le {new Date(qa.created_at).toLocaleDateString()}</span>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}
const TicketsTab = () => {
    const [tickets, setTickets] = useState<any[]>([]);
    const [selectedTickets, setSelectedTickets] = useState<string[]>([]);
    const [activeTicket, setActiveTicket] = useState<any | null>(null);
    const [messages, setMessages] = useState<any[]>([]);
    const [newMessage, setNewMessage] = useState('');
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        fetchTickets();

        // Subscribe to NEW tickets
        const ticketSub = supabase
            .channel('admin_tickets')
            .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'tickets' }, (payload) => {
                setTickets(prev => [payload.new, ...prev]);
            })
            .on('postgres_changes', { event: 'UPDATE', schema: 'public', table: 'tickets' }, (payload) => {
                setTickets(prev => prev.map(t => t.id === payload.new.id ? payload.new : t));
            })
            .subscribe();

        return () => { supabase.removeChannel(ticketSub); };
    }, []);

    useEffect(() => {
        if (activeTicket) {
            fetchMessages(activeTicket.id);
            const msgSub = supabase
                .channel(`admin_msg_${activeTicket.id}`)
                .on('postgres_changes', {
                    event: 'INSERT',
                    schema: 'public',
                    table: 'ticket_messages',
                    filter: `ticket_id=eq.${activeTicket.id}`
                }, (payload) => {
                    setMessages(prev => [...prev, payload.new]);
                })
                .subscribe();
            return () => { supabase.removeChannel(msgSub); };
        }
    }, [activeTicket]);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const fetchTickets = async () => {
        const { data } = await supabase.from('tickets').select('*, users(full_name, email)').order('created_at', { ascending: false });
        if (data) setTickets(data);
    };

    const fetchMessages = async (id: string) => {
        const { data } = await supabase.from('ticket_messages').select('*').eq('ticket_id', id).order('created_at', { ascending: true });
        if (data) setMessages(data);
    };

    const handleSendMessage = async () => {
        if (!newMessage.trim() || !activeTicket) return;
        const msg = newMessage;
        setNewMessage('');

        const { error } = await supabase.from('ticket_messages').insert({
            ticket_id: activeTicket.id,
            sender_id: 'admin_placeholder', // You should replace this with real admin ID check if possible
            content: msg
        });
        if (error) console.error(error);
    };

    const toggleSelect = (id: string) => {
        setSelectedTickets(prev => prev.includes(id) ? prev.filter(tid => tid !== id) : [...prev, id]);
    };

    const selectAll = () => {
        if (selectedTickets.length === tickets.length) setSelectedTickets([]);
        else setSelectedTickets(tickets.map(t => t.id));
    };

    const closeSelected = async () => {
        if (selectedTickets.length === 0) return;
        setLoading(true);
        const { error } = await supabase.from('tickets').update({ status: 'closed' }).in('id', selectedTickets);
        if (!error) {
            setTickets(tickets.map(t => selectedTickets.includes(t.id) ? { ...t, status: 'closed' } : t));
            setSelectedTickets([]);
        }
        setLoading(false);
    };

    return (
        <div>
            <h2 className="text-xl font-bold mb-6">Tickets Support</h2>

            {/* Back button if ticket is selected */}
            {activeTicket && (
                <button
                    onClick={() => setActiveTicket(null)}
                    className="mb-4 px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-sm font-medium flex items-center gap-2"
                >
                    <ArrowLeft size={16} /> Retour à la liste
                </button>
            )}

            {activeTicket ? (
                /* Ticket Detail View */
                <div className="bg-white rounded-3xl border border-slate-200 flex flex-col h-[600px] overflow-hidden">
                    <div className="p-6 border-b border-slate-100 bg-slate-50/50 flex justify-between items-center">
                        <div>
                            <h4 className="font-bold text-slate-800">{activeTicket.subject}</h4>
                            <p className="text-xs text-slate-500">Par {activeTicket.users?.full_name} ({activeTicket.users?.email})</p>
                        </div>
                        <button
                            onClick={() => {
                                supabase.from('tickets').update({ status: 'closed' }).eq('id', activeTicket.id).then(() => fetchTickets());
                                setActiveTicket({ ...activeTicket, status: 'closed' });
                            }}
                            className="px-4 py-2 bg-white border border-slate-200 rounded-xl text-xs font-bold hover:bg-slate-50"
                        >
                            Fermer le Ticket
                        </button>
                    </div>

                    <div className="flex-1 overflow-y-auto p-6 space-y-4">
                        {messages.map(m => (
                            <div key={m.id} className={clsx("flex flex-col max-w-[80%]", m.sender_id === activeTicket.user_id ? "items-start" : "ml-auto items-end")}>
                                <div className={clsx(
                                    "p-3 rounded-2xl text-sm",
                                    m.sender_id === activeTicket.user_id ? "bg-slate-100 text-slate-800 rounded-tl-none" : "bg-emerald-600 text-white rounded-tr-none"
                                )}>
                                    {m.content}
                                </div>
                                <span className="text-[10px] text-slate-400 mt-1">{new Date(m.created_at).toLocaleTimeString()}</span>
                            </div>
                        ))}
                        <div ref={messagesEndRef} />
                    </div>

                    <div className="p-4 border-t border-slate-100 flex gap-2">
                        <input
                            value={newMessage}
                            onChange={e => setNewMessage(e.target.value)}
                            onKeyDown={e => e.key === 'Enter' && handleSendMessage()}
                            placeholder="Répondre..."
                            className="flex-1 p-3 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-emerald-500/20 outline-none"
                        />
                        <button onClick={handleSendMessage} className="p-3 bg-emerald-600 text-white rounded-xl hover:bg-emerald-700">
                            <Send size={18} />
                        </button>
                    </div>
                </div>
            ) : (
                /* Ticket Grid List */
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {tickets.map(t => (
                        <div
                            key={t.id}
                            onClick={() => setActiveTicket(t)}
                            className={clsx(
                                "p-5 bg-white border border-slate-200 rounded-2xl hover:shadow-md hover:border-emerald-200 transition-all cursor-pointer group flex flex-col justify-between h-48"
                            )}
                        >
                            <div>
                                <div className="flex justify-between items-start mb-3">
                                    <span className={clsx(
                                        "text-[10px] px-2 py-1 rounded-full font-bold uppercase tracking-wide",
                                        t.status === 'open' ? "bg-emerald-100 text-emerald-700" : "bg-slate-100 text-slate-500"
                                    )}>
                                        {t.status === 'open' ? 'Ouvert' : 'Fermé'}
                                    </span>
                                    <span className="text-xs text-slate-400">{new Date(t.created_at).toLocaleDateString()}</span>
                                </div>
                                <h4 className="font-bold text-slate-800 mb-1 line-clamp-2">{t.subject}</h4>
                                <p className="text-sm text-slate-500 truncate">{t.users?.full_name}</p>
                            </div>

                            <div className="flex justify-end">
                                <span className="text-xs font-bold text-emerald-600 group-hover:underline flex items-center gap-1">
                                    Voir la discussion <ArrowLeft size={14} className="rotate-180" />
                                </span>
                            </div>
                        </div>
                    ))}
                    {tickets.length === 0 && (
                        <div className="col-span-full text-center py-12 text-slate-400 border border-dashed border-slate-200 rounded-2xl">
                            <LifeBuoy size={48} className="mx-auto mb-4 opacity-20" />
                            <p>Aucun ticket de support.</p>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};
