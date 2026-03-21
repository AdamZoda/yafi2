import type { Message } from '../types';

const PYTHON_API_URL = import.meta.env.VITE_PYTHON_API_URL || '';

export const apiService = {
    async sendMessage(history: Message[], newMessage: string, userId: string) {
        try {
            const response = await fetch(`${PYTHON_API_URL}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: newMessage,
                    userId: userId,
                    history: history // On envoie l'historique si on veut faire du contexte en Python
                }),
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            const data = await response.json();
            return data;

        } catch (error) {
            console.error("Python API Error:", error);
            return "⚠️ Erreur de connexion au Cerveau (Python). Vérifiez que 'server.py' est lancé.";
        }
    }
};
