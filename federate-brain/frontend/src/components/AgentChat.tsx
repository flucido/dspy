// components/AgentChat.tsx
'use client';

import { CopilotKit } from '@copilotkit/react-core';
import { CopilotPopup } from '@copilotkit/react-ui';
import '@copilotkit/react-ui/dist/styles.css';

export default function AgentChat() {
    return (
        <CopilotKit url="http://localhost:8000/api/copilot">
            <CopilotPopup
                instructions="Talk to the Federated Brain agent."
                defaultOpen={true}
                labels={{
                    title: "Federated Brain",
                    initial: "Hello! How can I help you today?",
                }}
            />
        </CopilotKit>
    );
}
