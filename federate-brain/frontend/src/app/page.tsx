import AgentChat from '@/components/AgentChat'
import CalendarView from '@/components/CalendarView'
import TaskList from '@/components/TaskList'
import DailyBriefing from '@/components/DailyBriefing'

export default function Home() {
  return (
    <main>
      <AgentChat />
      <CalendarView />
      <TaskList />
      <DailyBriefing />
    </main>
  )
}
