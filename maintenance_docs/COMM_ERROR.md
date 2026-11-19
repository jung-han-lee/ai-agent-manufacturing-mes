
# SOP-COMM-005: Equipment Communication Failure

Alarm Code: COMM_ERROR
Equipment Type: Automated Manufacturing Equipment
Severity: MEDIUM
Revision: 1.0
Document Status: SIMULATED / TRAINING ONLY

## Description
Communication between manufacturing equipment and
a connected system has been interrupted or degraded.

Affected systems may include PLCs, equipment controllers,
MES interfaces, data acquisition services, or industrial
network components.

## Possible Causes
- Network connectivity interruption
- PLC or controller communication failure
- Equipment interface service failure
- Communication timeout
- Network configuration mismatch
- Data acquisition system interruption

## Investigation Procedure
1. Identify the affected equipment and communication interface.
2. Review the communication failure timestamp.
3. Check available controller and interface status indicators.
4. Review network and application communication logs.
5. Identify whether other equipment experienced similar errors.
6. Check whether MES data updates stopped during the incident.
7. Escalate persistent failures to manufacturing IT
   or automation engineering.

## Recommended Data Analysis
- Identify missing equipment data during the incident.
- Compare MES timestamps with equipment event timestamps.
- Analyze communication timeout frequency.
- Identify simultaneous failures across multiple machines.
- Review historical network and interface error patterns.

## Escalation Criteria
- Communication cannot be restored through approved procedures.
- Multiple equipment interfaces fail simultaneously.
- MES production tracking becomes unavailable.
- Equipment state cannot be reliably verified.

## Production Lot Handling
Verify that production transactions and lot tracking
records are complete and consistent.

If lot traceability cannot be confirmed, affected lots
must remain on HOLD until authorized personnel reconcile
the production records.

## Safety
Do not assume equipment is stopped solely because
communication with MES has been lost.

Follow approved equipment-state verification procedures.
