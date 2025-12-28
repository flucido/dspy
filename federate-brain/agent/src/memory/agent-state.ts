// placeholder for agent-state.ts
import * as fs from 'fs/promises';

export class AgentState {
    constructor(private statePath: string) {}

    async save(conversationId: string, state: any): Promise<void> {
        const filePath = `${this.statePath}/${conversationId}.json`;
        await fs.writeFile(filePath, JSON.stringify(state), 'utf-8');
    }

    async load(conversationId: string): Promise<any | null> {
        const filePath = `${this.statePath}/${conversationId}.json`;
        try {
            await fs.access(filePath);
            const content = await fs.readFile(filePath, 'utf-8');
            return JSON.parse(content);
        } catch (error: any) {
            if (error.code === 'ENOENT') {
                return null;
            } else {
                throw error;
            }
        }
    }
}
