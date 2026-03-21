export interface Profile {
    id: string;
    name: string;
    email: string;
    role: 'user' | 'admin';
    joinedAt: string;
    is_premium?: boolean;
}

export interface Session {
    id: string;
    user_id: string;
    title: string;
    created_at: string;
}

export interface Message {
    id: string;
    session_id: string;
    role: 'user' | 'assistant' | 'system';
    content: string;
    created_at: string;
    metadata?: {
        score?: number;
        ecole?: string;
        source?: string;
        response_time_ms?: number;
    };
}
