
# SOP-PRESSURE-003: Low Process Pressure

Alarm Code: PRESSURE_LOW
Equipment Type: Manufacturing Process Equipment
Severity: HIGH
Revision: 1.0
Document Status: SIMULATED / TRAINING ONLY

## Description
The equipment has detected process pressure below its
configured operating threshold.

Low pressure may indicate a problem with process gas,
vacuum, pneumatic, or fluid delivery systems, depending
on the equipment configuration.

## Possible Causes
- Insufficient supply pressure
- Pressure regulator malfunction
- Process line leakage
- Valve malfunction
- Pump performance degradation
- Pressure sensor failure

## Investigation Procedure
1. Identify the affected pressure measurement.
2. Review pressure trends before the alarm occurred.
3. Compare actual pressure with the approved process range.
4. Review related pump, valve, and supply-system alarms.
5. Check equipment diagnostic information for abnormalities.
6. Escalate suspected leaks or supply-system failures
   to authorized maintenance personnel.

## Recommended Data Analysis
- Compare pressure trends across recent production cycles.
- Identify repeated PRESSURE_LOW alarms.
- Analyze pressure changes immediately before downtime.
- Compare downtime frequency across similar equipment.
- Review relationships between pressure alarms and
  production interruptions.

## Escalation Criteria
- Pressure remains below the approved operating range.
- Multiple related pressure alarms occur.
- A leak or supply-system failure is suspected.
- Equipment cannot maintain stable process conditions.

## Production Lot Handling
Identify production lots processed during the pressure
abnormality.

Affected lots must remain on HOLD pending an authorized
process engineering and quality assessment.

## Safety
Do not adjust pressure regulators, open process lines,
or bypass protective controls without approved procedures
and authorization.
