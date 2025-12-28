// Placeholder for calendar.ts
import { google } from 'googleapis';

async function listEvents(calendarId: string, timeMin: string, timeMax: string) {
    const calendar = google.calendar({ version: 'v3' });
    const response = await calendar.events.list({
        calendarId: calendarId,
        timeMin: timeMin,
        timeMax: timeMax,
        singleEvents: true,
        orderBy: 'startTime',
    });
    return response.data.items;
}

export const calendarTools = [
    {
        name: "list_calendar_events",
        description: "Retrieve calendar events within a date range",
        parameters: {
            type: "object",
            properties: {
                calendarId: { type: "string", description: "Calendar ID or 'primary'" },
                timeMin: { type: "string", format: "date-time" },
                timeMax: { type: "string", format: "date-time" },
            },
            required: ["timeMin", "timeMax"],
        },
        handler: async (params: any) => {
            const calendar = google.calendar({ version: "v3" });
            const response = await calendar.events.list({
                calendarId: params.calendarId || "primary",
                timeMin: params.timeMin,
                timeMax: params.timeMax,
                singleEvents: true,
                orderBy: "startTime",
            });
            return response.data.items;
        },
    },
    {
        name: "create_calendar_event",
        description: "Create a new calendar event",
        parameters: {
            type: "object",
            properties: {
                calendarId: { type: "string" },
                summary: { type: "string" },
                start: { type: "object" },
                end: { type: "object" },
                attendees: { type: "array", items: { type: "string" } },
            },
            required: ["summary", "start", "end"],
        },
        handler: async (params: any) => {
            const calendar = google.calendar({ version: "v3" });
            return await calendar.events.insert({
                calendarId: params.calendarId || "primary",
                requestBody: {
                    summary: params.summary,
                    start: params.start,
                    end: params.end,
                    attendees: params.attendees?.map((email: string) => ({ email })),
                },
            });
        },
    },
    {
        name: "detect_calendar_conflicts",
        description: "Check for scheduling conflicts across multiple calendars",
        parameters: {
            type: "object",
            properties: {
                calendarIds: { type: "array", items: { type: "string" } },
                proposedEvent: { type: "object" },
            },
            required: ["calendarIds", "proposedEvent"],
        },
        handler: async (params: any) => {
            const conflicts = [];
            for (const calendarId of params.calendarIds) {
                const events = await listEvents(
                    calendarId,
                    params.proposedEvent.start,
                    params.proposedEvent.end
                );
                if (events && events.length > 0) {
                    conflicts.push({ calendarId, conflicts: events });
                }
            }
            return conflicts;
        },
    },
];
