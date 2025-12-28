// placeholder for tasks.ts
import { google } from 'googleapis';

export const tasksTools = [
    {
        name: "list_tasks",
        description: "Retrieve tasks from a task list",
        parameters: {
            type: "object",
            properties: {
                tasklist: { type: "string", description: "Task list ID or '@default'" },
                showCompleted: { type: "boolean" },
            },
            required: ["tasklist"],
        },
        handler: async (params: any) => {
            const tasks = google.tasks({ version: "v1" });
            const response = await tasks.tasks.list({
                tasklist: params.tasklist,
                showCompleted: params.showCompleted,
            });
            return response.data.items;
        },
    },
    {
        name: "create_task",
        description: "Create a new task",
        parameters: {
            type: "object",
            properties: {
                tasklist: { type: "string", description: "Task list ID or '@default'" },
                title: { type: "string" },
            },
            required: ["tasklist", "title"],
        },
        handler: async (params: any) => {
            const tasks = google.tasks({ version: "v1" });
            return await tasks.tasks.insert({
                tasklist: params.tasklist,
                requestBody: {
                    title: params.title,
                },
            });
        },
    },
    {
        name: "complete_task",
        description: "Mark a task as complete",
        parameters: {
            type: "object",
            properties: {
                tasklist: { type: "string", description: "Task list ID or '@default'" },
                task: { type: "string", description: "Task ID" },
            },
            required: ["tasklist", "task"],
        },
        handler: async (params: any) => {
            const tasks = google.tasks({ version: "v1" });
            return await tasks.tasks.update({
                tasklist: params.tasklist,
                task: params.task,
                requestBody: {
                    status: 'completed',
                },
            });
        },
    },
];
