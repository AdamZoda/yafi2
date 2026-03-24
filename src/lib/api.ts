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
<<<<<<< HEAD
                    history: history // On envoie l'historique si on veut faire du contexte en Python
=======
                    history: history,
                    stream: false
>>>>>>> 3257fc1 (final)
                }),
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            const data = await response.json();
            return data;

        } catch (error) {
            console.error("Python API Error:", error);
<<<<<<< HEAD
            return "⚠️ Erreur de connexion au Cerveau (Python). Vérifiez que 'server.py' est lancé.";
=======
            return "⚠️ Erreur de connexion au Cerveau (Python).";
        }
    },

    async streamMessage(
        history: Message[], 
        newMessage: string, 
        userId: string, 
        onChunk: (chunk: string) => void,
        onComplete: (fullResponse: any) => void
    ) {
        let totalAccumulated = "";
        try {
            const response = await fetch(`${PYTHON_API_URL}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: newMessage,
                    userId: userId,
                    history: history,
                    stream: true
                }),
            });

            if (!response.ok) throw new Error(`Server error: ${response.status}`);

            const reader = response.body?.getReader();
            const decoder = new TextDecoder();
            if (!reader) throw new Error("No reader");

            let buffer = "";
            let isCompleted = false;

            const safeOnComplete = (data: any) => {
                if (!isCompleted) {
                    isCompleted = true;
                    onComplete(data);
                }
            };

            while (true) {
                const { done, value } = await reader.read();
                
                if (value) {
                    buffer += decoder.decode(value, { stream: true });
                    const lines = buffer.split('\n');
                    buffer = lines.pop() || "";

                    for (const line of lines) {
                        if (!line.trim()) continue;
                        try {
                            const data = JSON.parse(line);
                            if (data.token) {
                                totalAccumulated += data.token;
                                onChunk(data.token);
                            } else if (data.type === 'end') {
                                safeOnComplete(data);
                            } else if (data.response && data.done) {
                                totalAccumulated += data.response;
                                onChunk(data.response);
                                safeOnComplete(data);
                            }
                        } catch (e) {
                            console.warn("Error parsing stream line:", line, e);
                        }
                    }
                }

                if (done) {
                    // One last decode to flush
                    const lastValue = decoder.decode();
                    if (lastValue && lastValue.trim()) {
                         try {
                            const data = JSON.parse(lastValue);
                            if (data.response) {
                                totalAccumulated += data.response;
                                onChunk(data.response);
                            }
                            safeOnComplete(data);
                         } catch(e) {
                            // If we can't parse the last chunk, still complete with what we have
                            safeOnComplete({ response: totalAccumulated, done: true });
                         }
                    } else {
                        // Stream ended cleanly, call safeOnComplete with accumulated data
                        if (totalAccumulated) {
                            safeOnComplete({ response: totalAccumulated, done: true });
                        }
                    }
                    break;
                }
            }
        } catch (error) {
            console.error("Stream API Error:", error);
            // Only show error if we have NO content yet — preserve partial responses
            if (!totalAccumulated) {
                onChunk(" ⚠️ Erreur lors de la lecture du flux.");
            }
            // Always call onComplete to save whatever we got
            onComplete({ response: totalAccumulated, done: true });
>>>>>>> 3257fc1 (final)
        }
    }
};
