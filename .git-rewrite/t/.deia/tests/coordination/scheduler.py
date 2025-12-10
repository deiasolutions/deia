#!/usr/bin/env python3
"""
Task Scheduler for Three-Task Coordination Test
Ensures fair time distribution with comprehensive telemetry
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

# Fix Windows console encoding
import sys
import io
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class TaskScheduler:
    """Manages time-balanced task scheduling with telemetry"""

    def __init__(self, test_id: str):
        self.test_id = test_id
        self.test_dir = Path(__file__).parent
        self.log_file = self.test_dir / f"test-{test_id}.jsonl"
        self.state_file = self.test_dir / f"state-{test_id}.json"

        self.tasks = {
            'A1': {
                'name': 'Federalist Fragment',
                'time_spent': 0.0,
                'turns': 0,
                'status': 'active',
                'agent': 'CLAUDE_CODE+CLAUDE_WEB_BEE_1'
            },
            'A2': {
                'name': 'Build Matrix Template',
                'time_spent': 0.0,
                'turns': 0,
                'status': 'active',
                'agent': 'CLAUDE_CODE+CLAUDE_WEB_BEE_2'
            },
            'B1': {
                'name': 'Filename Validator',
                'time_spent': 0.0,
                'turns': 0,
                'status': 'active',
                'agent': 'CLAUDE_CODE+DAVE+CHATGPT'
            }
        }

        self.turn_history = []
        self.start_time = time.time()

        # Initialize telemetry
        self._log_event('test_started', {
            'test_id': test_id,
            'tasks': list(self.tasks.keys()),
            'timestamp': datetime.now().isoformat()
        })

    def record_turn(self, task_id: str, agent: str, duration: float, output_file: str):
        """Record a turn with full telemetry"""
        turn_num = len(self.turn_history) + 1

        self.tasks[task_id]['time_spent'] += duration
        self.tasks[task_id]['turns'] += 1

        turn_data = {
            'turn': turn_num,
            'task': task_id,
            'task_name': self.tasks[task_id]['name'],
            'agent': agent,
            'start': time.time() - duration,
            'end': time.time(),
            'duration': duration,
            'output': output_file,
            'total_task_time': self.tasks[task_id]['time_spent'],
            'total_task_turns': self.tasks[task_id]['turns']
        }

        self.turn_history.append(turn_data)

        # Log to JSONL
        self._log_event('turn_completed', turn_data)

        # Update state file
        self._save_state()

        # Display dashboard
        self._display_dashboard()

    def get_next_task(self) -> Optional[str]:
        """Select next task (least time spent)"""
        active_tasks = {
            k: v for k, v in self.tasks.items()
            if v['status'] == 'active'
        }

        if not active_tasks:
            return None

        next_task = min(
            active_tasks.items(),
            key=lambda x: x[1]['time_spent']
        )[0]

        self._log_event('task_selected', {
            'next_task': next_task,
            'reason': 'least_time_spent',
            'current_times': {k: v['time_spent'] for k, v in active_tasks.items()}
        })

        return next_task

    def mark_complete(self, task_id: str):
        """Mark task as complete"""
        self.tasks[task_id]['status'] = 'complete'
        self._log_event('task_completed', {
            'task': task_id,
            'total_time': self.tasks[task_id]['time_spent'],
            'total_turns': self.tasks[task_id]['turns']
        })

    def get_time_balance(self) -> Dict:
        """Calculate time variance"""
        active_tasks = {
            k: v for k, v in self.tasks.items()
            if v['status'] == 'active'
        }

        if not active_tasks:
            return {'avg_time': 0, 'variance': 0, 'variance_pct': 0}

        times = [t['time_spent'] for t in active_tasks.values()]
        avg_time = sum(times) / len(times)
        variance = max(times) - min(times)
        variance_pct = (variance / avg_time * 100) if avg_time > 0 else 0

        return {
            'avg_time': avg_time,
            'variance': variance,
            'variance_pct': variance_pct,
            'max_time': max(times),
            'min_time': min(times)
        }

    def _display_dashboard(self):
        """Display real-time status"""
        elapsed = time.time() - self.start_time
        balance = self.get_time_balance()

        print("\n" + "═" * 60)
        print("  TASK COORDINATION TEST - LIVE STATUS")
        print("═" * 60)

        for task_id, task in self.tasks.items():
            status_emoji = "✅" if task['status'] == 'complete' else "🔄"
            print(f"{status_emoji} Task {task_id} ({task['name']})")
            print(f"   Turns: {task['turns']}/4    Time: {task['time_spent']:.1f}s    Status: {task['status'].title()}")

        print("─" * 60)
        variance_status = "✅ GOOD" if balance['variance_pct'] < 30 else "⚠️  HIGH"
        print(f"Time Balance: {balance['variance']:.1f}s variance ({balance['variance_pct']:.0f}% - {variance_status})")
        print(f"Total Elapsed: {elapsed:.0f}s")

        active_count = sum(1 for t in self.tasks.values() if t['status'] == 'active')
        if active_count > 0:
            est_remaining = (balance['avg_time'] * 4 - balance['avg_time']) / active_count
            print(f"Est. Completion: {elapsed + est_remaining:.0f}s")

        print("═" * 60 + "\n")

    def _log_event(self, event_type: str, data: Dict):
        """Log event to JSONL"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event': event_type,
            'data': data
        }

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')

    def _save_state(self):
        """Save current state to JSON"""
        balance = self.get_time_balance()

        state = {
            'test_id': self.test_id,
            'elapsed_time': time.time() - self.start_time,
            'total_turns': len(self.turn_history),
            'tasks': self.tasks,
            'time_balance': balance,
            'last_updated': datetime.now().isoformat()
        }

        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2)

    def generate_final_report(self):
        """Generate test completion report"""
        elapsed = time.time() - self.start_time
        balance = self.get_time_balance()

        report = {
            'test_id': self.test_id,
            'duration': elapsed,
            'total_turns': len(self.turn_history),
            'tasks': {
                task_id: {
                    'name': task['name'],
                    'turns': task['turns'],
                    'time': task['time_spent'],
                    'avg_turn_time': task['time_spent'] / task['turns'] if task['turns'] > 0 else 0
                }
                for task_id, task in self.tasks.items()
            },
            'time_balance': balance,
            'turn_sequence': [
                f"Turn {t['turn']}: {t['task']} ({t['duration']:.1f}s)"
                for t in self.turn_history
            ],
            'success_metrics': {
                'all_tasks_complete': all(t['status'] == 'complete' for t in self.tasks.values()),
                'time_variance_ok': balance['variance_pct'] < 30,
                'avg_turn_time': elapsed / len(self.turn_history) if self.turn_history else 0
            }
        }

        report_file = self.test_dir / f"report-{self.test_id}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)

        self._log_event('test_completed', report)

        # Display final summary
        print("\n" + "═" * 60)
        print("  TEST COMPLETED - FINAL SUMMARY")
        print("═" * 60)
        print(f"Duration: {elapsed:.1f}s")
        print(f"Total Turns: {len(self.turn_history)}")
        print(f"Time Variance: {balance['variance_pct']:.0f}%")
        print(f"All Complete: {'✅ YES' if report['success_metrics']['all_tasks_complete'] else '❌ NO'}")
        print("═" * 60 + "\n")

        return report


if __name__ == "__main__":
    # Test the scheduler
    test_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    scheduler = TaskScheduler(test_id)

    print("Scheduler initialized successfully!")
    print(f"Log file: {scheduler.log_file}")
    print(f"State file: {scheduler.state_file}")
