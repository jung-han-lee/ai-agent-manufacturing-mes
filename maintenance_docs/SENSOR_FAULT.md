
# SOP-SENSOR-002: Equipment Sensor Fault

Alarm Code: SENSOR_FAULT
Equipment Type: Manufacturing Process Equipment
Severity: MEDIUM
Revision: 1.0
Document Status: SIMULATED / TRAINING ONLY

## Description
An equipment sensor has reported an abnormal, missing,
or inconsistent signal. Sensor faults can reduce process
monitoring accuracy and may interrupt automated operations.

## Possible Causes
- Sensor malfunction or calibration drift
- Loose electrical connections
- Communication interruption
- Electrical interference
- Sensor signal outside the expected operating range
- Data acquisition system malfunction

## Investigation Procedure
1. Identify the affected sensor and alarm timestamp.
2. Review recent sensor readings and signal trends.
3. Compare the affected sensor with redundant sensors,
   if available.
4. Check equipment communication and diagnostic logs.
5. Review the sensor's maintenance and calibration history.
6. Request authorized maintenance inspection if the
   abnormal signal persists.

## Recommended Data Analysis
- Identify missing or abnormal sensor readings.
- Compare sensor signals before and after downtime.
- Analyze the frequency of SENSOR_FAULT alarms.
- Identify equipment with repeated sensor failures.
- Compare sensor behavior across similar equipment.

## Escalation Criteria
- Critical process measurements become unavailable.
- Multiple sensors fail simultaneously.
- Sensor values remain inconsistent after recovery.
- Equipment operation cannot be safely verified.

## Production Lot Handling
Review affected production lots to determine whether
required process measurements were captured correctly.

Keep potentially affected lots on HOLD until authorized
quality personnel complete their review.

## Safety
Do not disable alarms or substitute unverified sensor
values to continue production.
