import fs from 'fs/promises';
import path from 'path';

const STATE_FILE_PATH = process.env.AGENT_STATE_PATH || '/app/state/agent-state.json';

export const stateManager = {
    /**
     * Saves the agent state to a JSON file.
     * @param state The state object to save.
     */
    async saveState(state: any): Promise<void> {
        const dir = path.dirname(STATE_FILE_PATH);
        try {
            await fs.mkdir(dir, { recursive: true });
            await fs.writeFile(STATE_FILE_PATH, JSON.stringify(state, null, 2), 'utf-8');
        } catch (error) {
            console.error('Error saving agent state:', error);
            throw error;
        }
    },

    /**
     * Loads the agent state from a JSON file.
     * @returns The parsed state object, or null if the file doesn't exist.
     */
    async loadState(): Promise<any | null> {
        try {
            const data = await fs.readFile(STATE_FILE_PATH, 'utf-8');
            return JSON.parse(data);
        } catch (error) {
            if ((error as any).code === 'ENOENT') {
                return null;
            }
            console.error('Error loading agent state:', error);
            throw error;
        }
    }
};
