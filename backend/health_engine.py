import math


def evaluate_vehicle(data, previous_state=None):
    """
    Evaluate vehicle telemetry.

    Returns:
        result: Health score, status, active alerts and data quality.
        current_state: State retained for the next reading.
    """

    previous_state = previous_state or {}
    asset_id = data.get("asset_id", "UNKNOWN")

    engine = data.get("engine")
    electrical = data.get("electrical")
    cooling = data.get("cooling")

    # Safely convert sensor readings to finite numbers.
    def number(value):
        try:
            result = float(value) if value is not None else None
            return result if result is not None and math.isfinite(result) else None
        except (TypeError, ValueError):
            return None

    temperature = number(engine.get("engine_temp_c")) if isinstance(engine, dict) else None
    oil_pressure = number(engine.get("oil_pressure_psi")) if isinstance(engine, dict) else None
    battery_voltage = number(electrical.get("battery_voltage")) if isinstance(electrical, dict) else None
    coolant_level = number(cooling.get("coolant_level_pct")) if isinstance(cooling, dict) else None

    # Validate the minimum telemetry contract.
    data_quality_issues = []

    required_readings = {
        "engine_temp_c": temperature,
        "oil_pressure_psi": oil_pressure,
        "battery_voltage": battery_voltage,
        "coolant_level_pct": coolant_level
    }

    for sensor, value in required_readings.items():
        if value is None:
            data_quality_issues.append(f"Missing or invalid sensor: {sensor}")

    # Invalid telemetry must not falsely resolve previous mechanical alerts.
    if data_quality_issues:
        previous_issues = previous_state.get("issues", {})

        result = {
            "asset_id": asset_id,
            "health_score": None,
            "status": "DATA_INVALID",
            "active_issues": previous_issues,
            "new_alerts": {},
            "ongoing_alerts": previous_issues,
            "resolved_alerts": {},
            "data_quality_issues": data_quality_issues
        }

        current_state = {
            "issues": previous_issues
        }

        return result, current_state

    diagnostics = data.get("diagnostic_trouble_codes") or []

    # Active mechanical issues are stored by unique ID.
    issues = {}

    def add_issue(issue_id, severity, message):
        issues[issue_id] = {
            "severity": severity,
            "message": message
        }

    # 1. Engine overheating
    if temperature > 110:
        add_issue(
            "engine_overheat",
            "CRITICAL",
            f"Engine overheating: {temperature} C"
        )

    # 2. Low engine oil pressure
    if oil_pressure < 10:
        add_issue(
            "low_oil_pressure",
            "CRITICAL",
            f"Low oil pressure: {oil_pressure} PSI"
        )

    # 3. Low battery voltage
    if battery_voltage < 11.5:
        add_issue(
            "low_battery_voltage",
            "WARNING",
            f"Low battery voltage: {battery_voltage} V"
        )

    # 4. Low coolant level
    if coolant_level < 20:
        add_issue(
            "low_coolant",
            "WARNING",
            f"Low coolant level: {coolant_level}%"
        )

    # 5. Diagnostic trouble codes
    code_mapping = {
        "P0217": "engine_overheat",
        "P0524": "low_oil_pressure",
        "P0562": "low_battery_voltage"
    }

    descriptions = {
        "P0217": ("CRITICAL", "Engine over-temperature (P0217)"),
        "P0524": ("CRITICAL", "Low engine oil pressure (P0524)"),
        "P0562": ("WARNING", "System voltage too low (P0562)")
    }

    for code in diagnostics:
        issue_id = code_mapping.get(code)

        if issue_id and issue_id in issues:
            continue

        if issue_id:
            severity, message = descriptions[code]
            add_issue(issue_id, severity, message)
        else:
            add_issue(
                f"unknown_dtc_{code}",
                "WARNING",
                f"Unclassified diagnostic code: {code}"
            )

    # Compare current issues with previous reading.
    previous_issues = previous_state.get("issues", {})

    new_alerts = {
        key: value for key, value in issues.items()
        if key not in previous_issues
    }

    ongoing_alerts = {
        key: value for key, value in issues.items()
        if key in previous_issues
    }

    resolved_alerts = {
        key: value for key, value in previous_issues.items()
        if key not in issues
    }

    # Calculate health score.
    deductions = sum(
        40 if issue["severity"] == "CRITICAL" else 20
        for issue in issues.values()
    )

    health_score = max(0, 100 - deductions)

    if any(issue["severity"] == "CRITICAL" for issue in issues.values()):
        status = "CRITICAL"
    elif issues:
        status = "WARNING"
    else:
        status = "HEALTHY"

    result = {
        "asset_id": asset_id,
        "health_score": health_score,
        "status": status,
        "active_issues": issues,
        "new_alerts": new_alerts,
        "ongoing_alerts": ongoing_alerts,
        "resolved_alerts": resolved_alerts,
        "data_quality_issues": []
    }

    current_state = {
        "issues": issues
    }

    return result, current_state