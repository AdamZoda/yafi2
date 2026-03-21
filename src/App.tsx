import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Header } from './components/Header';
import { Sidebar } from './components/Sidebar';
import { ChatArea } from './components/ChatArea';
import { AdminPanel } from './components/AdminPanel';
import { LandingPage } from './components/LandingPage';
import { ProfileModal } from './components/ProfileModal';
import { SuggestionsSidebar } from './components/SuggestionsSidebar';
import { apiService } from './lib/api';
import { supabase } from './lib/supabase';
import { ThemeProvider, useTheme } from './contexts/ThemeContext';
import type { Message, Profile } from './types';
import { ArrowRight, User, Lock, GraduationCap, ArrowLeft, Loader2, AlertCircle, Mail } from 'lucide-react';
import { clsx } from 'clsx';
import { PremiumModal } from './components/PremiumModal';
import { SupportTicket } from './components/SupportTicket';

function AppContent() {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [showLanding, setShowLanding] = useState(true);
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const [isPremiumModalOpen, setIsPremiumModalOpen] = useState(false);
  const [requestCount, setRequestCount] = useState(0);
  const [lastRequestTime, setLastRequestTime] = useState<string | null>(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [extractedProfile, setExtractedProfile] = useState<any>(null);

  // 1. Initialization
  useEffect(() => {
    const savedUser = localStorage.getItem('est_safi_user_v2');
    if (savedUser) {
      const parsedUser = JSON.parse(savedUser);
      setProfile(parsedUser);
      setShowLanding(false);

      // RE-VERIFY & REFRESH DATA FROM DB
      if (parsedUser.email) {
        supabase.from('users').select('*').eq('email', parsedUser.email).single().then(({ data, error }) => {
          if (data) {
            console.log("Profile refreshed from DB:", data);
            const updatedProfile = {
              id: data.id,
              name: data.full_name,
              email: data.email,
              role: data.role as 'user' | 'admin',
              joinedAt: data.created_at,
              is_premium: data.is_premium
            };
            setRequestCount(data.daily_requests_count || 0);
            setLastRequestTime(data.last_request_timestamp);
            setProfile(updatedProfile);
            localStorage.setItem('est_safi_user_v2', JSON.stringify(updatedProfile));
          } else if (error) {
            console.error("Error refreshing profile:", error);
          }
        });
      }
    }
  }, []);

  const handleAuthSuccess = (profile: Profile) => {
    localStorage.setItem('est_safi_user_v2', JSON.stringify(profile));
    setProfile(profile);
    setShowLanding(false);
  };

  const handleLogout = () => {
    localStorage.removeItem('est_safi_user_v2');
    setProfile(null);
    setShowLanding(true);
  };

  const handleUpdateProfile = (updatedProfile: Profile) => {
    setProfile(updatedProfile);
    localStorage.setItem('est_safi_user_v2', JSON.stringify(updatedProfile));
  };

  if (showLanding && !profile) {
    return <LandingPage onStart={() => setShowLanding(false)} />;
  }

  if (!profile) {
    return <LoginScreen onAuthSuccess={handleAuthSuccess} onBack={() => setShowLanding(true)} />;
  }

  return (
    <BrowserRouter>
      <div className="h-screen flex flex-col bg-slate-50 font-sans text-slate-900">
        <Header
          profile={profile}
          onOpenProfile={() => setIsProfileOpen(true)}
          onUpgrade={() => setIsPremiumModalOpen(true)}
          onToggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)}
        />
        <PremiumModal
          isOpen={isPremiumModalOpen}
          onClose={() => setIsPremiumModalOpen(false)}
          userEmail={profile.email}
          lastRequestTime={lastRequestTime}
        />
        <ProfileModal
          isOpen={isProfileOpen}
          onClose={() => setIsProfileOpen(false)}
          profile={profile}
          onLogout={handleLogout}
          onUpdateProfile={handleUpdateProfile}
        />
        <div className="flex flex-1 overflow-hidden">
          <Routes>
            <Route path="/" element={<ChatLayout
              profile={profile}
              onLimitReached={() => setIsPremiumModalOpen(true)}
              updateRequestState={(count, time) => {
                setRequestCount(count);
                setLastRequestTime(time);
              }}
              requestCount={requestCount}
              lastRequestTime={lastRequestTime}
              isSidebarOpen={isSidebarOpen}
              setIsSidebarOpen={setIsSidebarOpen}
              setExtractedProfile={setExtractedProfile}
              extractedProfile={extractedProfile}
            />} />

            {/* Alias for main client if used by user */}
            <Route path="/client" element={<Navigate to="/" replace />} />
            
            <Route path="/admin" element={
              profile.role === 'admin' ? <AdminPanel /> : <Navigate to="/" />
            } />
            
            <Route path="/support" element={
              profile.is_premium ? <SupportChatLayout 
                profile={profile} 
                isSidebarOpen={isSidebarOpen} 
                setIsSidebarOpen={setIsSidebarOpen}
                extractedProfile={extractedProfile}
              /> : <Navigate to="/" />
            } />

            {/* Catch-all redirect to prevent blank pages on 404 */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default function App() {
  return (
    <ThemeProvider>
      <AppContent />
    </ThemeProvider>
  );
}

// =============================================
// AUTHENTICATION SCREEN (EMAIL & PASSWORD)
// =============================================
const LoginScreen = ({ onAuthSuccess, onBack }: { onAuthSuccess: (p: Profile) => void, onBack: () => void }) => {
  const { theme } = useTheme();
  const [isRegistering, setIsRegistering] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      if (isRegistering) {
        // --- INSCRIPTION ---
        const { data: existing, error: checkError } = await supabase.from('users').select('id').eq('email', email).single();

        if (checkError && checkError.code !== 'PGRST116') {
          console.error("Check Error:", checkError);
          throw new Error("Erreur lors de la vérification de l'email.");
        }

        if (existing) throw new Error("Cet email possède déjà un compte.");

        const { data, error: insertError } = await supabase.from('users').insert({
          full_name: fullName,
          email: email,
          password: password,
          role: 'user'
        }).select().single();

        if (insertError) {
          console.error("Insert Error:", insertError);
          throw new Error("Erreur lors de la création du compte: " + insertError.message);
        }

        if (data) {
          onAuthSuccess({
            id: data.id,
            name: data.full_name,
            email: data.email,
            role: data.role as 'user' | 'admin',
            joinedAt: data.created_at,
            is_premium: false
          });
        }

      } else {
        // --- CONNEXION ---
        console.log("Attempting login for:", email);

        const { data, error } = await supabase
          .from('users')
          .select('*')
          .eq('email', email)
          .eq('password', password)
          .single();

        if (error) {
          console.error("Login Error:", error);
          if (error.code === 'PGRST116') {
            throw new Error("Email ou mot de passe incorrect.");
          }
          throw new Error("Erreur de connexion base de données.");
        }

        if (!data) {
          throw new Error("Compte introuvable.");
        }

        console.log("Login successful:", data.id);

        onAuthSuccess({
          id: data.id,
          name: data.full_name,
          email: data.email,
          role: data.role as 'user' | 'admin',
          joinedAt: data.created_at,
          is_premium: data.is_premium
        });
        // We set dailyCount in the main component after auth callback usually, 
        // but for now the useEffect refresh will handle it.
      }
    } catch (err: any) {
      console.error(err);
      setError(err.message || "Une erreur technique est survenue.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col items-center justify-center p-4">
      <button onClick={onBack} className="absolute top-8 left-8 flex items-center gap-2 text-slate-400 hover:text-slate-600 transition-colors">
        <ArrowLeft size={20} /> Retour
      </button>

      <div className="bg-white p-8 rounded-3xl shadow-xl w-full max-w-md animate-fade-in border border-slate-100">
        <div className="text-center mb-8">
          <div className={clsx("w-16 h-16 rounded-2xl flex items-center justify-center text-white mb-4 mx-auto shadow-lg", theme.primary, theme.shadow)}>
            <GraduationCap size={40} />
          </div>
          <h1 className="text-2xl font-bold text-slate-800">{isRegistering ? 'Nouveau Compte' : 'Bon retour !'}</h1>
          <p className="text-slate-500">Connectez-vous pour accéder au Chatbot YAFI.</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">

          {isRegistering && (
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Nom Complet</label>
              <div className="relative">
                <User className="absolute left-3 top-3.5 text-slate-400" size={18} />
                <input
                  type="text"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="Ex: Ahmed Etudiant"
                  className={clsx("w-full pl-10 pr-4 py-3 rounded-xl border border-slate-200 focus:ring-2 outline-none", `focus:ring-${theme.primary.split('-')[1]}-500`)}
                  style={{ '--tw-ring-color': theme.primary.replace('bg-', 'var(--tw-colors-') } as React.CSSProperties}
                  required
                />
              </div>
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Email</label>
            <div className="relative">
              <Mail className="absolute left-3 top-3.5 text-slate-400" size={18} />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="nom@exemple.com"
                className="w-full pl-10 pr-4 py-3 rounded-xl border border-slate-200 focus:ring-2 outline-none"
                style={{ '--tw-ring-color': theme.primary.replace('bg-', 'var(--tw-colors-') } as React.CSSProperties}
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Mot de passe</label>
            <div className="relative">
              <Lock className="absolute left-3 top-3.5 text-slate-400" size={18} />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full pl-10 pr-4 py-3 rounded-xl border border-slate-200 focus:ring-2 outline-none"
                style={{ '--tw-ring-color': theme.primary.replace('bg-', 'var(--tw-colors-') } as React.CSSProperties}
                required
              />
            </div>
          </div>

          {error && (
            <div className="p-3 bg-red-50 text-red-600 text-sm rounded-lg flex items-center gap-2 animate-shake">
              <AlertCircle size={16} />
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className={clsx("w-full flex items-center justify-center gap-2 group disabled:opacity-70 disabled:cursor-not-allowed py-3 rounded-xl font-bold text-white transition-all", theme.primary, theme.shadow)}
          >
            {loading ? <Loader2 className="animate-spin" /> : (
              <>
                {isRegistering ? "S'inscrire" : "Se connecter"}
                <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
              </>
            )}
          </button>
        </form>

        <button
          onClick={() => { setIsRegistering(!isRegistering); setError(null); }}
          className={clsx("w-full mt-6 text-sm text-center font-medium transition-colors text-slate-500 hover:text-slate-800")}
        >
          {isRegistering ? "J'ai déjà un compte ? Me connecter" : "Pas encore de compte ? M'inscrire"}
        </button>
      </div>
    </div>
  );
};

// =============================================
// CHAT LAYOUT LOGIC
// =============================================

const ChatLayout = ({
  profile,
  onLimitReached,
  updateRequestState,
  requestCount,
  lastRequestTime,
  isSidebarOpen,
  setIsSidebarOpen,
  setExtractedProfile,
  extractedProfile
}: {
  profile: Profile,
  onLimitReached: () => void,
  updateRequestState: (c: number, t: string) => void,
  requestCount: number,
  lastRequestTime: string | null,
  isSidebarOpen: boolean,
  setIsSidebarOpen: (open: boolean) => void,
  setExtractedProfile: (p: any) => void,
  extractedProfile: any
}) => {
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sidebarRefreshKey, setSidebarRefreshKey] = useState(0);
  const [isRightSidebarOpen, setIsRightSidebarOpen] = useState(true);

  useEffect(() => {
    if (!currentSessionId) {
      setMessages([]);
      return;
    }
    const loadMessages = async () => {
      const { data } = await supabase
        .from('messages')
        .select('*')
        .eq('session_id', currentSessionId)
        .order('created_at', { ascending: true });
      if (data) setMessages(data as Message[]);
    };
    loadMessages();
  }, [currentSessionId]);

  const handleNewChat = () => {
    setCurrentSessionId(null);
    setMessages([]);
  };

  const handleSendMessage = async (content: string) => {
    // --- LIMIT CHECK (5 messages per 30 mins) ---
    if (!profile.is_premium) {
      const now = new Date();
      const lastReq = lastRequestTime ? new Date(lastRequestTime) : new Date(0);
      const timeDiff = now.getTime() - lastReq.getTime(); // diff in ms
      const minutesDiff = timeDiff / (1000 * 60);

      if (minutesDiff >= 30) {
        // It's been more than 30 mins, reset counter
        // Actually, we do this reset *after* sending successfully usually, 
        // but for the check we can say: if > 30 mins, he is safe.
        // We will set count to 1 after send.
      } else {
        // Less than 30 mins passed
        if (requestCount >= 5) {
          onLimitReached();
          return;
        }
      }
    }

    const tempUserMsg: Message = {
      id: crypto.randomUUID(),
      session_id: currentSessionId || 'temp',
      role: 'user',
      content,
      created_at: new Date().toISOString(),
    };

    setMessages(prev => [...prev, tempUserMsg]);
    setIsLoading(true);

    try {
      let sessionId = currentSessionId;
      if (!sessionId) {
        const { data: sessionData } = await supabase
          .from('sessions')
          .insert({
            title: content.slice(0, 30) + '...',
            user_id: profile.id
          })
          .select()
          .single();

        if (sessionData) {
          sessionId = sessionData.id;
          setCurrentSessionId(sessionId);
          setSidebarRefreshKey(prev => prev + 1);
          console.log('New session created:', sessionId);
        } else {
          sessionId = crypto.randomUUID();
          setCurrentSessionId(sessionId);
        }
      }

      if (sessionId) {
        const { error: saveError } = await supabase.from('messages').insert({
          session_id: sessionId,
          role: 'user',
          content
        });
        if (saveError) console.error('Error saving user message:', saveError);

        // Increment count or reset if interval passed
        if (!profile.is_premium) {
          const now = new Date();
          const lastReq = lastRequestTime ? new Date(lastRequestTime) : new Date(0);
          const timeDiff = now.getTime() - lastReq.getTime();
          const minutesDiff = timeDiff / (1000 * 60);

          let newCount = requestCount + 1;

          if (minutesDiff >= 30) {
            newCount = 1; // Reset to 1 (this is the first new message of the block)
          }

          const newTimestamp = now.toISOString();

          // Update State
          updateRequestState(newCount, newTimestamp);

          // Update DB
          supabase.from('users').update({
            daily_requests_count: newCount,
            last_request_timestamp: newTimestamp
          }).eq('id', profile.id).then(res => {
            if (res.error) console.error("Error updating limit", res.error);
          });
        }
      }

      const responseData = await apiService.sendMessage(messages, content, profile.id);
      
      // Update extracted profile if backend sent it
      if (typeof responseData === 'object' && responseData.entities) {
        setExtractedProfile(responseData.entities);
      }
      
      // Handle both old string responses and new structured objects
      const responseText = typeof responseData === 'object' ? responseData.response : responseData;
      const metadata = typeof responseData === 'object' ? {
        score: responseData.score,
        ecole: responseData.ecole,
        source: responseData.source,
        response_time_ms: responseData.response_time_ms
      } : undefined;

      const aiMsg: Message = {
        id: crypto.randomUUID(),
        session_id: sessionId!,
        role: 'assistant',
        content: responseText,
        created_at: new Date().toISOString(),
        metadata: metadata
      };

      setMessages(prev => [...prev, aiMsg]);

      if (sessionId) {
        const { error: aiSaveError } = await supabase.from('messages').insert({
          session_id: sessionId,
          role: 'assistant',
          content: responseText
        });
        if (aiSaveError) console.error('Error saving AI message:', aiSaveError);
      }

    } catch (error: any) {
      console.error(error);
      let errorText = "Désolé, je ne peux pas répondre pour le moment.";

      if (error.message?.includes('429') || error.status === 429) {
        errorText = "⚠️ Limite de quota atteinte. Le modèle est surchargé, veuillez patienter une minute avant de réessayer.";
      }

      const errorMsg: Message = {
        id: crypto.randomUUID(),
        session_id: currentSessionId || 'temp',
        role: 'system',
        content: errorText,
        created_at: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-1 relative">
      <Sidebar
        currentSessionId={currentSessionId}
        onSelectSession={setCurrentSessionId}
        onNewChat={handleNewChat}
        profile={profile}
        refreshKey={sidebarRefreshKey}
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
        extractedProfile={extractedProfile}
      />
      <ChatArea
        messages={messages}
        isLoading={isLoading}
        onSendMessage={handleSendMessage}
        userName={profile.name}
      />
      <SuggestionsSidebar
        isOpen={isRightSidebarOpen}
        onToggle={() => setIsRightSidebarOpen(!isRightSidebarOpen)}
        onSendMessage={handleSendMessage}
      />
    </div>
  );
};

const SupportChatLayout = ({
  profile,
  isSidebarOpen,
  setIsSidebarOpen,
  extractedProfile
}: {
  profile: Profile,
  isSidebarOpen: boolean,
  setIsSidebarOpen: (open: boolean) => void,
  extractedProfile: any
}) => {
  return (
    <div className="flex flex-1 relative">
      <Sidebar
        currentSessionId={null}
        onSelectSession={() => { }}
        onNewChat={() => { }}
        profile={profile}
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
        extractedProfile={extractedProfile}
      />
      <div className="flex-1 p-6 bg-slate-50 overflow-hidden">
        <SupportTicket profile={profile} />
      </div>
    </div>
  );
};
