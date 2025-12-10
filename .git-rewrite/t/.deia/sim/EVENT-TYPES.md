# RSE Event Types for Legislative Sim (v0.1)

Core
- bill_introduced {bill_id, chamber}
- committee_referral {bill_id, committee}
- committee_hearing {bill_id, committee}
- committee_markup {bill_id, committee}
- committee_report {bill_id, report_no}
- rule_adopted {bill_id, rule}
- floor_debate {bill_id, chamber}
- floor_vote {bill_id, chamber, yeas, nays, result}
- conference_committee {bill_id}
- enrolled {bill_id}
- signature {bill_id} | veto {bill_id}
- litigation_event {case_id, stage}

Coalitions & Parties
- whip_count_update {bill_id, chamber, counts}
- caucus_guidance {caucus, bill_id, guidance}
- coalition_offer {from, to, bill_id, terms}
- coalition_break {caucus|coalition, reason}

States & Executive
- governor_order {state, topic}
- intergovernmental_request {from, to, topic}
- emergency_declared {scope}

Media & Public
- narrative_drop {topic, lane, priority}
- fact_check {claim_id, verdict}
- poll_update {series, value}
- protest_event {location, size}

Safety & Control
- policy_guard {lock, path, mode}
- clock_tick {tick}
- priority_update {lane, reason}
- task_assign {assignee, ref}
- worker_ack {ref, status}

