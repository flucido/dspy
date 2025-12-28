// placeholder for agent-state.test.ts
import { jest } from '@jest/globals';
import * as fs from 'fs/promises';

// Mock the fs/promises module
jest.mock('fs/promises', () => ({
    writeFile: jest.fn<() => Promise<void>>(),
    readFile: jest.fn<() => Promise<string>>(),
    access: jest.fn<() => Promise<void>>(),
}));

import { AgentState } from '../../src/memory/agent-state'; // Assuming your class is in memory/agent-state.ts

describe('AgentState', () => {
    const statePath = '/app/state';
    let agentState: AgentState;

    beforeEach(() => {
        agentState = new AgentState(statePath);
        jest.clearAllMocks();
    });

    describe('save', () => {
        it('should save the agent state to a file', async () => {
            const state = { conversationId: '123', history: [] };
            (fs.writeFile as jest.Mock).mockResolvedValue(undefined);

            await agentState.save('123', state);

            expect(fs.writeFile).toHaveBeenCalledWith(`${statePath}/123.json`, JSON.stringify(state), 'utf-8');
        });
    });

    describe('load', () => {
        it('should load the agent state from a file', async () => {
            const state = { conversationId: '123', history: [] };
            (fs.access as jest.Mock).mockResolvedValue(undefined);
            (fs.readFile as jest.Mock).mockResolvedValue(JSON.stringify(state));

            const result = await agentState.load('123');

            expect(fs.access).toHaveBeenCalledWith(`${statePath}/123.json`);
            expect(fs.readFile).toHaveBeenCalledWith(`${statePath}/123.json`, 'utf-8');
            expect(result).toEqual(state);
        });

        it('should return null if the state file does not exist', async () => {
            (fs.access as jest.Mock).mockRejectedValue({ code: 'ENOENT' });

            const result = await agentState.load('123');

            expect(result).toBeNull();
        });
    });
});
