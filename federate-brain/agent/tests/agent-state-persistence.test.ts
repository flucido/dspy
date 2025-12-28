import fs from 'fs/promises';
import path from 'path';

const mockAgentStatePath = path.join(process.cwd(), '.agent-state-test.json');
process.env.AGENT_STATE_PATH = mockAgentStatePath;

import { stateManager } from '../src/memory/stateManager';

describe('Agent State Persistence', () => {
    beforeEach(async () => {
        // Ensure the mock file is clean before each test
        try {
            await fs.unlink(mockAgentStatePath);
        } catch (error) {
            // Ignore if file does not exist
        }
    });

    afterAll(async () => {
        // Clean up mock file after all tests
        try {
            await fs.unlink(mockAgentStatePath);
        } catch (error) {
            // Ignore if file does not exist
        }
    });

    it('should save and load agent state', async () => {
        const testState = { counter: 1, message: 'hello' };
        await stateManager.saveState(testState);
        const loadedState = await stateManager.loadState();
        expect(loadedState).toEqual(testState);
    });

    it('should return null if no state is found', async () => {
        const loadedState = await stateManager.loadState();
        expect(loadedState).toBeNull();
    });

    it('should throw error if saveState fails', async () => {
        // Mock fs.mkdir to throw an error
        const mkdirSpy = jest.spyOn(fs, 'mkdir').mockRejectedValueOnce(new Error('Write error') as never);
        const testState = { counter: 1 };
        await expect(stateManager.saveState(testState)).rejects.toThrow('Write error');
        mkdirSpy.mockRestore();
    });

    it('should throw error if loadState fails for reasons other than file not found', async () => {
        // Mock fs.readFile to throw a generic error
        const readFileSpy = jest.spyOn(fs, 'readFile').mockRejectedValueOnce(new Error('Read error') as never);
        await expect(stateManager.loadState()).rejects.toThrow('Read error');
        readFileSpy.mockRestore();
    });
});
