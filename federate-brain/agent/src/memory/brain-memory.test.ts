import { jest } from '@jest/globals';
import * as fs from 'fs/promises';

// Explicit mock functions
const mockReaddir = jest.fn<() => Promise<string[]>>();
const mockReadFile = jest.fn<() => Promise<string>>();
const mockAccess = jest.fn<() => Promise<void>>();

// Mock the fs/promises module
jest.mock('fs/promises', () => ({
    readdir: mockReaddir,
    readFile: mockReadFile,
    access: mockAccess,
}));

import { BrainMemory } from '../../src/memory/brain-memory';

describe('BrainMemory', () => {
    const knowledgePath = '/mnt/knowledge';
    let brainMemory: BrainMemory;

    beforeEach(() => {
        brainMemory = new BrainMemory(knowledgePath);
        jest.clearAllMocks();
    });

    describe('getCodeContext', () => {
        it('should read XML file for code context if it exists', async () => {
            const repoName = 'test-repo';
            const xmlContent = '<code/>';
            mockAccess.mockResolvedValue(undefined); // Simulate file exists
            mockReadFile.mockResolvedValue(xmlContent);

            const result = await brainMemory.getCodeContext(repoName);

            expect(mockAccess).toHaveBeenCalledWith(`${knowledgePath}/codebase/${repoName}.xml`);
            expect(mockReadFile).toHaveBeenCalledWith(`${knowledgePath}/codebase/${repoName}.xml`, 'utf-8');
            expect(result).toBe(xmlContent);
        });

        it('should return empty string if XML file does not exist', async () => {
            const repoName = 'non-existent-repo';
            mockAccess.mockRejectedValue({ code: 'ENOENT' }); // Simulate file does not exist

            const result = await brainMemory.getCodeContext(repoName);

            expect(mockAccess).toHaveBeenCalledWith(`${knowledgePath}/codebase/${repoName}.xml`);
            expect(mockReadFile).not.toHaveBeenCalled();
            expect(result).toBe('');
        });
    });

    describe('getLatestBriefing', () => {
        it('should read the latest markdown briefing for a given account', async () => {
            const account = 'personal';
            const mockFiles = ['daily-briefing-2025-12-27.md', 'daily-briefing-2025-12-28.md'];
            const latestBriefingContent = '# Daily Briefing for 2025-12-28\nSome content.';

            mockReaddir.mockResolvedValue(mockFiles);
            mockReadFile.mockResolvedValue(latestBriefingContent);

            const result = await brainMemory.getLatestBriefing(account);

            expect(mockReaddir).toHaveBeenCalledWith(`${knowledgePath}/life-ops/${account}`);
            expect(mockReadFile).toHaveBeenCalledWith(`${knowledgePath}/life-ops/${account}/${mockFiles[1]}`, 'utf-8');
            expect(result).toEqual({ title: 'Daily Briefing for 2025-12-28', content: latestBriefingContent });
        });

        it('should return undefined if no briefing files are found', async () => {
            const account = 'work';
            mockReaddir.mockResolvedValue([]);

            const result = await brainMemory.getLatestBriefing(account);

            expect(mockReaddir).toHaveBeenCalledWith(`${knowledgePath}/life-ops/${account}`);
            expect(mockReadFile).not.toHaveBeenCalled();
            expect(result).toBeUndefined();
        });

        it('should return undefined if the directory does not exist', async () => {
            const account = 'non-existent';
            mockReaddir.mockRejectedValue({ code: 'ENOENT' });

            const result = await brainMemory.getLatestBriefing(account);

            expect(mockReaddir).toHaveBeenCalledWith(`${knowledgePath}/life-ops/${account}`);
            expect(result).toBeUndefined();
        });

        it('should throw other errors from fs.readdir', async () => {
            const account = 'error-account';
            const mockError = new Error('Permission denied');
            mockReaddir.mockRejectedValue(mockError);

            await expect(brainMemory.getLatestBriefing(account)).rejects.toThrow(mockError);
        });
        it('should throw an error for unimplemented getChatHistory', async () => {
            const chatId = 'test-chat';
            // Expect an error because the mock implementation will return a string,
            // but we expect a more robust implementation.
            await expect(brainMemory.getChatHistory(chatId)).rejects.toThrow();
        });
    });
});
