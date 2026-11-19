
# SOP-MOTOR-004: Equipment Motor Malfunction

Alarm Code: MOTOR_ERROR
Equipment Type: Automated Manufacturing Equipment
Severity: CRITICAL
Revision: 1.0
Document Status: SIMULATED / TRAINING ONLY

## Description
The equipment has detected a motor-related malfunction
that may prevent normal mechanical movement or operation.

This alarm may be associated with excessive motor current,
unexpected speed changes, positioning errors, or drive faults.

## Possible Causes
- Motor overload
- Motor drive malfunction
- Mechanical obstruction
- Bearing degradation
- Position feedback error
- Electrical power abnormality

## Investigation Procedure
1. Identify the affected motor and alarm timestamp.
2. Review motor current, speed, and position data.
3. Check equipment diagnostic logs for related drive alarms.
4. Compare motor performance with historical operating data.
5. Review recent maintenance and equipment fault history.
6. Request authorized maintenance inspection before
   equipment restart or mechanical intervention.

## Recommended Data Analysis
- Analyze motor current trends before downtime.
- Identify recurring MOTOR_ERROR alarms.
- Compare motor speed and position feedback.
- Review historical equipment failure patterns.
- Identify increases in downtime frequency or duration.

## Escalation Criteria
- Motor protection systems activate.
- Repeated motor faults occur after recovery.
- Unexpected mechanical movement is reported.
- Equipment cannot complete required motion sequences.

## Production Lot Handling
Identify production lots affected by interrupted
equipment movement or processing.

Keep affected lots on HOLD until authorized personnel
determine whether additional inspection is required.

## Safety
Follow approved equipment isolation and lockout/tagout
procedures where applicable.

Do not manually move equipment, reset protective devices,
or bypass safety interlocks without authorization.
