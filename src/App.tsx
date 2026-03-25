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
import { ArrowRight, ArrowLeft, Loader2 } from 'lucide-react';
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
      <div className="h-screen flex flex-col bg-slate-50 dark:bg-black font-sans text-slate-900 dark:text-slate-100 transition-colors duration-300">

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
// AUTHENTICATION SCREEN — CHATBOT STYLE
// =============================================

// AUTHENTICATION SCREEN — CHATBOT STYLE
// =============================================
const LoginScreen = ({ onAuthSuccess, onBack }: { onAuthSuccess: (p: Profile) => void, onBack: () => void }) => {
  const { theme, isDarkMode } = useTheme();
  const [isRegistering, setIsRegistering] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Chat state
  type ChatStep = 'name' | 'email' | 'password' | 'done';
  const [step, setStep] = useState<ChatStep>('email');
  const [chatInput, setChatInput] = useState('');
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [chatMessages, setChatMessages] = useState<{ role: 'bot' | 'user'; text: string }[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  const scrollRef = React.useRef<HTMLDivElement>(null);
  const inputRef = React.useRef<HTMLInputElement>(null);

  // Initialize first bot message
  useEffect(() => {
    setChatMessages([]);
    const timer = setTimeout(() => {
      if (isRegistering) {
        setChatMessages([{ role: 'bot', text: "Bienvenue ! 🎓 Créons votre compte.\nComment vous appelez-vous ?" }]);
        setStep('name');
      } else {
        setChatMessages([{ role: 'bot', text: "Bon retour ! 👋 Connectez-vous à YAFI.\nQuel est votre email ?" }]);
        setStep('email');
      }
    }, 400);
    return () => clearTimeout(timer);
  }, [isRegistering]);

  // Auto-scroll
  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatMessages, isTyping]);

  // Focus input when step changes
  useEffect(() => {
    inputRef.current?.focus();
  }, [step]);

  const addBotMessage = (text: string, delay = 600) => {
    setIsTyping(true);
    setTimeout(() => {
      setIsTyping(false);
      setChatMessages(prev => [...prev, { role: 'bot', text }]);
    }, delay);
  };

  const handleChatSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!chatInput.trim() || loading || isTyping) return;

    const userText = chatInput.trim();
    setChatInput('');

    if (step === 'name' && isRegistering) {
      setChatMessages(prev => [...prev, { role: 'user', text: userText }]);
      setFullName(userText);
      setStep('email');
      addBotMessage(`Enchanté ${userText} ! 😊\nMaintenant, quel est votre email ?`);
    } else if (step === 'email') {
      setChatMessages(prev => [...prev, { role: 'user', text: userText }]);
      setEmail(userText);
      setStep('password');
      addBotMessage("Parfait ! 🔒\nEntrez votre mot de passe :");
    } else if (step === 'password') {
      const pwd = userText;
      setChatMessages(prev => [...prev, { role: 'user', text: '•'.repeat(pwd.length) }]);
      setPassword(pwd);
      setStep('done');

      // Trigger auth
      setLoading(true);
      setError(null);
      addBotMessage("Vérification en cours... ⏳", 300);

      try {
        if (isRegistering) {
          const { data: existing, error: checkError } = await supabase.from('users').select('id').eq('email', email).single();
          if (checkError && checkError.code !== 'PGRST116') throw new Error("Erreur lors de la vérification.");
          if (existing) throw new Error("Cet email possède déjà un compte.");

          const { data, error: insertError } = await supabase.from('users').insert({
            full_name: fullName,
            email: email,
            password: pwd,
            role: 'user'
          }).select().single();

          if (insertError) throw new Error("Erreur : " + insertError.message);
          if (data) {
            addBotMessage(`Compte créé avec succès ! 🎉\nBienvenue ${data.full_name} !`, 800);
            setTimeout(() => {
              onAuthSuccess({
                id: data.id, name: data.full_name, email: data.email,
                role: data.role as 'user' | 'admin', joinedAt: data.created_at, is_premium: false
              });
            }, 1500);
          }
        } else {
          const { data, error: loginError } = await supabase
            .from('users').select('*').eq('email', email).eq('password', pwd).single();

          if (loginError) {
            if (loginError.code === 'PGRST116') throw new Error("Email ou mot de passe incorrect.");
            throw new Error("Erreur de connexion.");
          }
          if (!data) throw new Error("Compte introuvable.");

          addBotMessage(`Connexion réussie ! 🚀\nBon retour ${data.full_name} !`, 800);
          setTimeout(() => {
            onAuthSuccess({
              id: data.id, name: data.full_name, email: data.email,
              role: data.role as 'user' | 'admin', joinedAt: data.created_at, is_premium: data.is_premium
            });
          }, 1500);
        }
      } catch (err: any) {
        setError(err.message);
        setLoading(false);
        setStep('email');
        setEmail('');
        setPassword('');
        addBotMessage(`❌ ${err.message}\nRéessayons ! Quel est votre email ?`, 800);
      } finally {
        setLoading(false);
      }
    }
  };

  const switchMode = () => {
    setIsRegistering(!isRegistering);
    setError(null);
    setFullName('');
    setEmail('');
    setPassword('');
    setChatInput('');
  };

  return (
    <div className={clsx("min-h-screen flex flex-col items-center justify-center p-4 relative overflow-hidden transition-colors duration-300", isDarkMode ? "bg-black" : "bg-slate-50")}>
      
      {/* Background gradient orbs */}
      <div className={clsx("absolute top-[-10%] left-[-5%] w-[400px] h-[400px] rounded-full blur-[100px] opacity-20 animate-pulse", isDarkMode ? "bg-emerald-700" : "bg-emerald-300")} />
      <div className={clsx("absolute bottom-[-10%] right-[-5%] w-[500px] h-[500px] rounded-full blur-[100px] opacity-15 animate-pulse", isDarkMode ? "bg-blue-700" : "bg-blue-300")} style={{ animationDelay: '2s' }} />

      {/* Back button */}
      <button onClick={onBack} className={clsx("absolute top-6 left-6 flex items-center gap-2 text-sm font-medium transition-colors z-10", isDarkMode ? "text-zinc-500 hover:text-zinc-300" : "text-slate-400 hover:text-slate-600")}>
        <ArrowLeft size={18} /> Retour
      </button>

      {/* Chat Card */}
      <div className={clsx(
        "w-full max-w-lg rounded-3xl shadow-2xl overflow-hidden flex flex-col transition-all duration-300 relative z-10",
        isDarkMode ? "bg-zinc-900 border border-zinc-800" : "bg-white border border-slate-100"
      )}
        style={{ height: '520px' }}
      >
        {/* Chat Header */}
        <div className={clsx("px-6 py-4 flex items-center gap-3 border-b", isDarkMode ? "border-zinc-800 bg-zinc-900" : "border-slate-100 bg-white")}>
          <img src="/yafi.png" alt="YAFI" className="w-10 h-10 object-contain" />
          <div>
            <h2 className={clsx("font-bold text-base", isDarkMode ? "text-white" : "text-slate-800")}>YAFI</h2>
            <p className={clsx("text-xs", isDarkMode ? "text-emerald-400" : "text-emerald-600")}>
              {isRegistering ? "Inscription" : "Connexion"} • En ligne
            </p>
          </div>
          <div className="ml-auto w-2.5 h-2.5 bg-emerald-500 rounded-full animate-pulse" />
        </div>

        {/* Chat Messages */}
        <div className={clsx("flex-1 overflow-y-auto p-4 space-y-3", isDarkMode ? "bg-black/30" : "bg-slate-50/50")}>
          {chatMessages.map((msg, i) => (
            <div key={i} className={clsx("flex animate-fade-in", msg.role === 'user' ? "justify-end" : "justify-start")}>
              <div className={clsx(
                "max-w-[80%] px-4 py-3 text-sm leading-relaxed whitespace-pre-line",
                msg.role === 'user'
                  ? clsx("rounded-2xl rounded-br-sm text-white bg-gradient-to-r", theme.gradient)
                  : clsx("rounded-2xl rounded-bl-sm", isDarkMode ? "bg-zinc-800 text-zinc-200" : "bg-white text-slate-700 shadow-sm border border-slate-100")
              )}>
                {msg.text}
              </div>
            </div>
          ))}

          {/* Typing indicator */}
          {isTyping && (
            <div className="flex justify-start animate-fade-in">
              <div className={clsx("px-4 py-3 rounded-2xl rounded-bl-sm flex items-center gap-1.5", isDarkMode ? "bg-zinc-800" : "bg-white shadow-sm border border-slate-100")}>
                <span className={clsx("w-2 h-2 rounded-full animate-bounce", isDarkMode ? "bg-zinc-500" : "bg-slate-400")} style={{ animationDelay: '0ms' }} />
                <span className={clsx("w-2 h-2 rounded-full animate-bounce", isDarkMode ? "bg-zinc-500" : "bg-slate-400")} style={{ animationDelay: '150ms' }} />
                <span className={clsx("w-2 h-2 rounded-full animate-bounce", isDarkMode ? "bg-zinc-500" : "bg-slate-400")} style={{ animationDelay: '300ms' }} />

              </div>
            </div>
          )}


          <div ref={scrollRef} />
        </div>

        {/* Chat Input */}
        <div className={clsx("px-4 py-3 border-t", isDarkMode ? "border-zinc-800 bg-zinc-900" : "border-slate-100 bg-white")}>
          {step !== 'done' ? (
            <form onSubmit={handleChatSubmit} className="flex items-center gap-2">
              <input
                ref={inputRef}
                type={step === 'password' ? 'password' : (step === 'email' ? 'email' : 'text')}
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                placeholder={
                  step === 'name' ? "Votre nom complet..." :
                  step === 'email' ? "nom@exemple.com" :
                  step === 'password' ? "Mot de passe..." : ""
                }
                className={clsx(
                  "flex-1 px-4 py-3 rounded-xl border outline-none focus:ring-2 transition-all text-sm",
                  isDarkMode ? "bg-zinc-800 border-zinc-700 text-white focus:ring-emerald-500/50 placeholder-zinc-500" : "bg-slate-50 border-slate-200 text-slate-800 focus:ring-emerald-500/30 placeholder-slate-400"
                )}
                disabled={loading || isTyping}
                autoComplete={step === 'email' ? 'email' : step === 'password' ? 'current-password' : 'name'}
              />
              <button
                type="submit"
                disabled={!chatInput.trim() || loading || isTyping}
                className={clsx(
                  "p-3 rounded-xl text-white transition-all disabled:opacity-40 bg-gradient-to-r shadow-md hover:shadow-lg",
                  theme.gradient
                )}
              >
                <ArrowRight size={18} />
              </button>
            </form>
          ) : (
            <div className="flex items-center justify-center gap-2 py-2">
              <Loader2 size={18} className={clsx("animate-spin", isDarkMode ? "text-emerald-400" : "text-emerald-600")} />
              <span className={clsx("text-sm font-medium", isDarkMode ? "text-zinc-400" : "text-slate-500")}>Connexion en cours...</span>
            </div>
          )}

          {/* Toggle mode */}
          <button
            onClick={switchMode}
            className={clsx("w-full mt-2 text-xs text-center font-medium transition-colors py-1", isDarkMode ? "text-zinc-500 hover:text-zinc-300" : "text-slate-400 hover:text-slate-700")}
          >
            {isRegistering ? "Déjà un compte ? Se connecter" : "Pas de compte ? S'inscrire"}
          </button>
        </div>

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
  const [currentKeywords, setCurrentKeywords] = useState("");

  const [sidebarRefreshKey, setSidebarRefreshKey] = useState(0);
  const [isRightSidebarOpen, setIsRightSidebarOpen] = useState(true);

  useEffect(() => {
    if (!currentSessionId) {
      setMessages([]);
      return;
    }

    // CRITICAL: If we are CURRENTLY loading/streaming, do NOT reload from DB.
    // This prevents a new session creation in handleSendMessage from triggering a 
    // fetch that would overwrite the newly added optimistic message.
    if (isLoading) return;


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

        // --- DYNAMIC STATUS PREPARATION ---
        const kw = content.split(' ').filter(w => w.length > 3).slice(0, 2).join(' ') || "votre question";
        setCurrentKeywords(kw);
        
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
          if (minutesDiff >= 30) newCount = 1;
          const newTimestamp = now.toISOString();
          updateRequestState(newCount, newTimestamp);

          supabase.from('users').update({
            daily_requests_count: newCount,
            last_request_timestamp: newTimestamp
          }).eq('id', profile.id).then(res => {
            if (res.error) console.error("Error updating limit", res.error);
          });
        }
      }

      // --- STREAMING INITIATION ---
      const aiMsgId = crypto.randomUUID();
      const initialAiMsg: Message = {
        id: aiMsgId,
        session_id: sessionId!,
        role: 'assistant',
        content: '', // Start empty
        created_at: new Date().toISOString()
      };

      setMessages(prev => [...prev, initialAiMsg]);

      let accumulatedResponse = "";

      // --- NON-STREAMING FALLBACK FOR DIAGNOSTIC ---
      console.log("Sending non-streaming request for diagnostic...");
      const data = await apiService.sendMessage([...messages, tempUserMsg], content, profile.id);
      
      if (data && data.response) {
        accumulatedResponse = data.response;
        setMessages(prev => prev.map(m => 
          m.id === aiMsgId ? { ...m, content: accumulatedResponse } : m
        ));
        
        if (data.entities) setExtractedProfile(data.entities);
        
        if (sessionId) {
          await supabase.from('messages').insert({
            session_id: sessionId,
            role: 'assistant',
            content: accumulatedResponse
          });
        }
      } else {
        throw new Error("Empty response from server");
      }

    } catch (error: any) {
      console.error(error);

      const errorMsg: Message = {
        id: crypto.randomUUID(),
        session_id: currentSessionId || 'temp',
        role: 'system',
        content: "Désolé, je ne peux pas répondre pour le moment (Erreur de flux).",

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
        keywords={currentKeywords}

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
      <div className="flex-1 p-6 bg-slate-50 dark:bg-black overflow-hidden transition-colors">

        <SupportTicket profile={profile} />
      </div>
    </div>
  );
};
