import { jest } from '@jest/globals';

const mockListCalendarEvents = jest.fn<() => Promise<any[]>>().mockResolvedValue([{ summary: 'Mock Event' }]);
jest.mock('../src/tools/google-workspace/calendar', () => ({
    calendarTools: [
        {
            name: 'list_calendar_events',
            handler: mockListCalendarEvents,
        },
    ],
}));

import { CopilotRuntime } from '@copilotkit/runtime';
import { calendarTools } from '../src/tools/google-workspace/calendar';

describe('Agent Integration with Google Calendar Tools', () => {
    it('should initialize the CopilotRuntime with calendar tools without errors', () => {
        expect(() => {
            new CopilotRuntime({
                actions: calendarTools as any,
            });
        }).not.toThrow();
    });
});
