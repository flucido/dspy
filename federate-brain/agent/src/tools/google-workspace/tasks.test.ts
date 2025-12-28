// placeholder for tasks.test.ts
import { jest } from '@jest/globals';

const mockTasksList = jest.fn<() => Promise<any>>();
const mockTasksInsert = jest.fn<() => Promise<any>>();
const mockTasksUpdate = jest.fn<() => Promise<any>>();

const mockTasks = {
    list: mockTasksList,
    insert: mockTasksInsert,
    update: mockTasksUpdate,
};

const mockTasksApi = {
    tasks: mockTasks,
};

jest.mock('googleapis', () => ({
    google: {
        tasks: jest.fn(() => mockTasksApi),
    },
}));

import { tasksTools } from './tasks';

describe('Google Tasks Tools', () => {
    beforeEach(() => {
        mockTasksList.mockClear();
        mockTasksInsert.mockClear();
        mockTasksUpdate.mockClear();
        (require('googleapis').google.tasks as jest.Mock).mockClear();
    });

    describe('list_tasks', () => {
        it('should call the tasks.list with correct parameters', async () => {
            const listTasksTool = tasksTools.find(tool => tool.name === 'list_tasks');
            if (!listTasksTool) {
                throw new Error('list_tasks tool not found');
            }

            const params = {
                tasklist: '@default',
                showCompleted: false,
            };

            const mockResponse = { data: { items: [{ title: 'Test Task' }] } };
            mockTasksList.mockResolvedValue(mockResponse);

            await listTasksTool.handler(params);

            expect(require('googleapis').google.tasks).toHaveBeenCalledWith({ version: 'v1', auth: undefined });

            expect(mockTasksList).toHaveBeenCalledWith({
                tasklist: params.tasklist,
                showCompleted: params.showCompleted,
            });
        });
    });

    describe('create_task', () => {
        it('should call tasks.insert with correct parameters', async () => {
            const createTaskTool = tasksTools.find(tool => tool.name === 'create_task');
            if (!createTaskTool) {
                throw new Error('create_task tool not found');
            }

            const params = {
                tasklist: '@default',
                title: 'New Task',
            };

            await createTaskTool.handler(params);

            expect(mockTasksInsert).toHaveBeenCalledWith({
                tasklist: params.tasklist,
                requestBody: {
                    title: params.title,
                },
            });
        });
    });

    describe('complete_task', () => {
        it('should call tasks.update with correct parameters', async () => {
            const completeTaskTool = tasksTools.find(tool => tool.name === 'complete_task');
            if (!completeTaskTool) {
                throw new Error('complete_task tool not found');
            }

            const params = {
                tasklist: '@default',
                task: 'test-task-id',
            };

            await completeTaskTool.handler(params);

            expect(mockTasksUpdate).toHaveBeenCalledWith({
                tasklist: params.tasklist,
                task: params.task,
                requestBody: {
                    status: 'completed',
                },
            });
        });
    });
});
