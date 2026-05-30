# Test Cases

Fabricated fact patterns used to validate the eviction-triage skill.

**Status:** To be built in the next session.

Each test case will include:
- A fabricated eviction notice (no real client data — all invented)
- Jurisdiction and tenancy facts
- Expected triage output (defects flagged, defenses identified)
- Pass/fail criteria

## Planned test cases

| ID | Jurisdiction | Scenario | Key defect to detect |
|----|-------------|----------|---------------------|
| TC-CA-01 | California / Los Angeles | Maria: 3-day notice, $1,850 rent + $200 late fees, 3-year tenancy | CA-DEFECT-01 (late fees in notice) |
| TC-CA-02 | California / San Francisco | 30-day notice served on 18-month tenant | CA-DEFECT-02 (should be 60-day) |
| TC-CA-03 | California / Oakland | AB 1482 covered unit, no-fault notice with no just cause stated | CA-DEFECT-04 (missing just cause) |
| TC-TX-01 | Texas / Houston | 3-day unconditional notice, tenant was current before this month | TX-DEFECT-01 (SB 38 violation) |
| TC-TX-02 | Texas / Dallas | Section 8 tenant, 3-day notice served | TX-DEFECT-05 (CARES Act — needs 30 days) |
| TC-NY-01 | New York / NYC | 3-day notice served (NY requires 14 days) | NY-DEFECT-01 (wrong notice period) |
| TC-NY-02 | New York / Buffalo | Rent increase above Good Cause threshold, nonpayment | NY-DEFECT-08 (Good Cause rent increase defense) |

All test cases use entirely fabricated names, addresses, and facts. No real client information.
