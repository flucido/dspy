import { jest } from '@jest/globals';

// Mock the Google APIs library
const mockEventsList = jest.fn<() => Promise<any>>();
const mockEventsInsert = jest.fn<() => Promise<any>>();
const mockCalendar = {
    events: {
        list: mockEventsList,
        insert: mockEventsInsert,
    },
};

jest.mock('googleapis', () => ({
    google: {
        calendar: jest.fn(() => mockCalendar),
    },
}));

import { calendarTools } from './calendar'; // Assuming your functions are in 'calendar.ts'

describe('Google Calendar Tools', () => {
    beforeEach(() => {
        // Clear mock history before each test
        mockEventsList.mockClear();
        mockEventsInsert.mockClear();
        (require('googleapis').google.calendar as jest.Mock).mockClear();
    });

    describe('list_calendar_events', () => {
        it('should call the calendar.events.list with correct parameters', async () => {
            const listEventsTool = calendarTools.find(tool => tool.name === 'list_calendar_events');
            if (!listEventsTool) {
                throw new Error('list_calendar_events tool not found');
            }
            
            const params = {
                timeMin: '2025-12-28T10:00:00Z',
                timeMax: '2025-12-28T17:00:00Z',
                calendarId: 'primary',
            };

            // Simulate a successful API response
            const mockResponse = { data: { items: [{ summary: 'Test Event' }] } };
            mockEventsList.mockResolvedValue(mockResponse);

            await listEventsTool.handler(params);

            // Expect the google.calendar API to be called
            expect(require('googleapis').google.calendar).toHaveBeenCalledWith({ version: 'v3', auth: undefined });
            
            // Expect the events.list method to be called with the correct parameters
            expect(mockEventsList).toHaveBeenCalledWith({
                calendarId: params.calendarId,
                timeMin: params.timeMin,
                timeMax: params.timeMax,
                singleEvents: true,
                orderBy: 'startTime',
            });
        });

        it('should return the list of events from the API call', async () => {
            const listEventsTool = calendarTools.find(tool => tool.name === 'list_calendar_events');
            if (!listEventsTool) {
                throw new Error('list_calendar_events tool not found');
            }
            
            const params = {
                timeMin: '2025-12-28T10:00:00Z',
                timeMax: '2025-12-28T17:00:00Z',
            };
            const mockItems = [{ summary: 'Test Event 1' }, { summary: 'Test Event 2' }];
            const mockResponse = { data: { items: mockItems } };
            mockEventsList.mockResolvedValue(mockResponse);
            
            const result = await listEventsTool.handler(params);
            
            expect(result).toEqual(mockItems);
        });

        it('should fail gracefully if the API call fails', async () => {
            const listEventsTool = calendarTools.find(tool => tool.name === 'list_calendar_events');
            if (!listEventsTool) {
                throw new Error('list_calendar_events tool not found');
            }
            
            const params = {
                timeMin: '2025-12-28T10:00:00Z',
                timeMax: '2025-12-28T17:00:00Z',
            };
            const errorMessage = 'API Error';
            mockEventsList.mockRejectedValue(new Error(errorMessage));
            
            await expect(listEventsTool.handler(params)).rejects.toThrow(errorMessage);
        });
    });

    describe('create_calendar_event', () => {
        it('should call calendar.events.insert with correct parameters', async () => {
            const createEventTool = calendarTools.find(tool => tool.name === 'create_calendar_event');
            if (!createEventTool) {
                throw new Error('create_calendar_event tool not found');
            }

            const params = {
                summary: 'New Event',
                start: { dateTime: '2025-12-29T10:00:00Z' },
                end: { dateTime: '2025-12-29T11:00:00Z' },
                attendees: ['test@example.com'],
            };
            
            await createEventTool.handler(params);

            expect(mockEventsInsert).toHaveBeenCalledWith({
                calendarId: 'primary',
                requestBody: {
                    summary: params.summary,
                    start: params.start,
                    end: params.end,
                    attendees: params.attendees.map(email => ({ email })),
                },
            });
        });
    });

    describe('detect_calendar_conflicts', () => {
        it('should check for conflicts by calling list_calendar_events for each calendar', async () => {
            const detectConflictsTool = calendarTools.find(tool => tool.name === 'detect_calendar_conflicts');
            if (!detectConflictsTool) {
                throw new Error('detect_calendar_conflicts tool not found');
            }

            const params = {
                calendarIds: ['primary', 'secondary'],
                proposedEvent: {
                    start: '2025-12-30T14:00:00Z',
                    end: '2025-12-30T15:00:00Z',
                },
            };
            
            // Mock that the first calendar has a conflict, the second does not
            mockEventsList
                .mockResolvedValueOnce({ data: { items: [{ summary: 'Existing Event' }] } })
                .mockResolvedValueOnce({ data: { items: [] } });

            const conflicts = await detectConflictsTool.handler(params);
            
            expect(mockEventsList).toHaveBeenCalledTimes(2);
            expect(mockEventsList).toHaveBeenCalledWith(expect.objectContaining({ calendarId: 'primary' }));
            expect(mockEventsList).toHaveBeenCalledWith(expect.objectContaining({ calendarId: 'secondary' }));
            expect(conflicts).toEqual([{ calendarId: 'primary', conflicts: [{ summary: 'Existing Event' }] }]);
        });

        it('should return an empty array if there are no conflicts', async () => {
            const detectConflictsTool = calendarTools.find(tool => tool.name === 'detect_calendar_conflicts');
            if (!detectConflictsTool) {
                throw new Error('detect_calendar_conflicts tool not found');
            }

            const params = {
                calendarIds: ['primary'],
                proposedEvent: {
                    start: '2025-12-30T14:00:00Z',
                    end: '2025-12-30T15:00:00Z',
                },
            };
            
            mockEventsList.mockResolvedValue({ data: { items: [] } });
            
            const conflicts = await detectConflictsTool.handler(params);

            expect(conflicts).toEqual([]);
        });
    });
});
