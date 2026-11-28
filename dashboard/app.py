import json
import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "athena.db"

st.set_page_config(
    page_title="ATHENA | Fleet Intelligence",
    page_icon="A",
    layout="wide",
)


# -------------------- DESIGN SYSTEM --------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #0b0e11;
    --panel: #12171c;
    --panel2: #151b21;
    --border: #242c34;
    --text: #edf2f7;
    --muted: #8b98a5;
    --teal: #42e0c2;
    --red: #ff626e;
    --amber: #ffbe55;
}

html, body, [class*="css"] {
    font-family: 'Manrope', sans-serif;
}

.stApp {
    background: var(--bg);
    color: var(--text);
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: #0e1216;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] * {
    color: var(--text);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

h1, h2, h3 {
    font-family: 'Manrope', sans-serif !important;
    letter-spacing: -0.04em !important;
}

h1 {
    font-weight: 800 !important;
    font-size: 2.2rem !important;
}

h2 {
    font-size: 1.35rem !important;
    font-weight: 700 !important;
}

h3 {
    font-size: 1.05rem !important;
}

p, label {
    color: var(--muted);
}

[data-testid="stMetric"] {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px 20px;
}

[data-testid="stMetricLabel"] {
    color: var(--muted) !important;
    font-size: 0.78rem !important;
}

[data-testid="stMetricValue"] {
    color: var(--text) !important;
    font-weight: 800 !important;
}

[data-testid="stMetricDelta"] {
    font-family: 'DM Mono', monospace;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
}

[data-testid="stPlotlyChart"] {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 8px;
}

.stButton button {
    background: #17211f;
    border: 1px solid #29443f;
    border-radius: 8px;
    color: var(--teal);
    font-weight: 700;
    transition: 0.2s;
}

.stButton button:hover {
    background: #20332f;
    border-color: var(--teal);
    color: var(--teal);
}

.stSelectbox > div > div {
    background: var(--panel);
    border-radius: 8px;
}

hr {
    border-color: var(--border) !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px;
}

[data-testid="stCaptionContainer"] {
    color: var(--muted);
}

.athena-brand {
    font-size: 1.35rem;
    font-weight: 800;
    letter-spacing: 0.15em;
    color: var(--text);
}

.athena-sub {
    color: var(--muted);
    font-size: 0.72rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.section-label {
    font-size: 0.75rem;
    color: var(--muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-weight: 700;
    margin-bottom: 0.4rem;
}

.status-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-right: 7px;
}

.mono {
    font-family: 'DM Mono', monospace;
}

[data-testid="stTabs"] button {
    font-weight: 700;
}

[data-testid="stAlert"] {
    border-radius: 10px;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# -------------------- DATA --------------------

def load_data():
    con = sqlite3.connect(DB)

    latest = pd.read_sql_query("""
        SELECT *
        FROM vehicle_readings
        WHERE id IN (
            SELECT MAX(id)
            FROM vehicle_readings
            GROUP BY asset_id
        )
        ORDER BY asset_id
    """, con)

    history = pd.read_sql_query("""
        SELECT *
        FROM alert_history
        ORDER BY id DESC
        LIMIT 500
    """, con)

    trend = pd.read_sql_query("""
        SELECT asset_id, timestamp, health_score, status
        FROM vehicle_readings
        ORDER BY id DESC
        LIMIT 1500
    """, con)

    con.close()
    return latest, history, trend


def safe_json(value):
    try:
        return json.loads(value) if value else {}
    except (ValueError, TypeError):
        return {}


def severity_color(status):
    return {
        "HEALTHY": "#42e0c2",
        "WARNING": "#ffbe55",
        "CRITICAL": "#ff626e",
    }.get(status, "#8b98a5")


def style_plot(fig):
    fig.update_layout(
        paper_bgcolor="#12171c",
        plot_bgcolor="#12171c",
        font=dict(
            family="Manrope",
            color="#8b98a5",
        ),
        margin=dict(l=20, r=20, t=35, b=25),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#8b98a5"),
        ),
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        color="#8b98a5",
    )

    fig.update_yaxes(
        gridcolor="#242c34",
        zeroline=False,
        color="#8b98a5",
    )

    return fig


# -------------------- SIDEBAR --------------------

with st.sidebar:

    st.markdown(
        '<div class="athena-brand">ATHENA</div>'
        '<div class="athena-sub">Fleet Intelligence System</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown("### OVERVIEW")

    page = st.radio(
        "Navigation",
        ["Fleet Overview", "Vehicle Explorer", "Alert Center"],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown("### SYSTEM")

    st.markdown(
        """
        <span class="status-dot" style="background:#42e0c2"></span>
        <span style="color:#42e0c2">DATABASE CONNECTED</span>
        """,
        unsafe_allow_html=True,
    )

    st.caption("Local SQLite telemetry store")

    st.divider()

    if st.button("↻ Refresh telemetry", use_container_width=True):
        st.rerun()

    st.caption("ATHENA / CONFIGURE 2026")


# -------------------- LOAD --------------------

if not DB.exists():
    st.error("Athena database not found.")
    st.stop()

vehicles, alerts, trend = load_data()

if vehicles.empty:
    st.warning("Waiting for telemetry...")
    st.stop()

vehicles["issues"] = vehicles["active_issues_json"].apply(safe_json)
vehicles["telemetry"] = vehicles["telemetry_json"].apply(safe_json)

trend["timestamp"] = pd.to_datetime(
    trend["timestamp"], errors="coerce"
)

trend = trend.dropna(subset=["timestamp"]).sort_values("timestamp")

alerts["timestamp"] = pd.to_datetime(
    alerts["timestamp"], errors="coerce"
)

total = len(vehicles)
healthy = int((vehicles["status"] == "HEALTHY").sum())
warning = int((vehicles["status"] == "WARNING").sum())
critical = int((vehicles["status"] == "CRITICAL").sum())
avg_health = vehicles["health_score"].mean()


# -------------------- HEADER --------------------

st.markdown(
    '<div class="section-label">OPERATIONS / LIVE MONITORING</div>',
    unsafe_allow_html=True,
)

st.title("Fleet Overview" if page == "Fleet Overview" else page)

st.caption(
    "Monitor vehicle condition, detect anomalies and track fleet health."
)

st.divider()


# =========================================================
# FLEET OVERVIEW
# =========================================================

if page == "Fleet Overview":

    a, b, c, d = st.columns(4)

    a.metric("FLEET SIZE", f"{total:02d}")
    b.metric("HEALTHY", f"{healthy:02d}")
    c.metric("WARNING", f"{warning:02d}")
    d.metric("CRITICAL", f"{critical:02d}")

    st.write("")

    left, right = st.columns([1.15, 2])

    with left:

        st.markdown("### Fleet Health")

        status_df = pd.DataFrame({
            "Status": ["Healthy", "Warning", "Critical"],
            "Count": [healthy, warning, critical],
        })

        status_df = status_df[status_df["Count"] > 0]

        fig = px.pie(
            status_df,
            names="Status",
            values="Count",
            hole=0.72,
            color="Status",
            color_discrete_map={
                "Healthy": "#42e0c2",
                "Warning": "#ffbe55",
                "Critical": "#ff626e",
            },
        )

        fig.update_traces(
            textinfo="none",
            marker=dict(line=dict(color="#12171c", width=3)),
        )

        fig.update_layout(
            height=300,
            showlegend=True,
        )

        st.plotly_chart(
            style_plot(fig),
            use_container_width=True,
        )

        st.metric("AVERAGE FLEET HEALTH", f"{avg_health:.1f}/100")

    with right:

        st.markdown("### Vehicle Health")

        bar = px.bar(
            vehicles.sort_values("health_score"),
            x="asset_id",
            y="health_score",
            color="status",
            color_discrete_map={
                "HEALTHY": "#42e0c2",
                "WARNING": "#ffbe55",
                "CRITICAL": "#ff626e",
            },
        )

        bar.update_traces(
            marker_line_width=0,
            hovertemplate="%{x}<br>Health: %{y}/100<extra></extra>",
        )

        bar.update_layout(
            height=380,
            yaxis=dict(range=[0, 100]),
            xaxis_title=None,
            yaxis_title="Health score",
        )

        st.plotly_chart(
            style_plot(bar),
            use_container_width=True,
        )

    st.divider()

    st.markdown("### Fleet Registry")

    fleet = vehicles[
        ["asset_id", "health_score", "status", "timestamp"]
    ].copy()

    fleet.columns = [
        "VEHICLE",
        "HEALTH",
        "STATUS",
        "LAST TELEMETRY",
    ]

    st.dataframe(
        fleet,
        hide_index=True,
        use_container_width=True,
    )

    st.divider()

    st.markdown("### Active Faults")

    fault_rows = []

    for _, v in vehicles.iterrows():

        for issue_id, issue in v["issues"].items():

            fault_rows.append({
                "Vehicle": v["asset_id"],
                "Fault": issue_id.replace("_", " ").upper(),
                "Severity": issue.get("severity", "UNKNOWN"),
                "Details": issue.get("message", ""),
            })

    if fault_rows:

        st.dataframe(
            pd.DataFrame(fault_rows),
            hide_index=True,
            use_container_width=True,
        )

    else:

        st.success("No active faults.")


# =========================================================
# VEHICLE EXPLORER
# =========================================================

elif page == "Vehicle Explorer":

    selected = st.selectbox(
        "Select asset",
        vehicles["asset_id"].tolist(),
    )

    v = vehicles[vehicles["asset_id"] == selected].iloc[0]
    t = v["telemetry"]

    engine = t.get("engine") or {}
    electrical = t.get("electrical") or {}
    cooling = t.get("cooling") or {}
    brakes = t.get("brakes") or {}
    tyres = t.get("tyres") or {}
    vibration = t.get("vibration") or {}
    transmission = t.get("transmission") or {}

    st.markdown(f"## {selected}")

    x1, x2, x3, x4 = st.columns(4)

    x1.metric("HEALTH", f"{v['health_score']}/100")
    x2.metric("STATUS", v["status"])
    x3.metric("RPM", engine.get("engine_rpm", "N/A"))
    x4.metric("ENGINE TEMP", f"{engine.get('engine_temp_c', 'N/A')} °C")

    st.divider()

    st.markdown("### Powertrain & Electrical")

    p1, p2, p3, p4 = st.columns(4)

    p1.metric("Oil Pressure", f"{engine.get('oil_pressure_psi', 'N/A')} PSI")
    p2.metric("Oil Temperature", f"{engine.get('oil_temp_c', 'N/A')} °C")
    p3.metric("Battery", f"{electrical.get('battery_voltage', 'N/A')} V")
    p4.metric("Coolant Level", f"{cooling.get('coolant_level_pct', 'N/A')}%")

    st.markdown("### Vehicle Telemetry")

    p5, p6, p7, p8 = st.columns(4)

    p5.metric("Coolant Temp", f"{engine.get('coolant_temp_c', 'N/A')} °C")
    p6.metric("Transmission", f"{transmission.get('transmission_temp_c', 'N/A')} °C")
    p7.metric("Engine Load", f"{engine.get('engine_load_pct', 'N/A')}%")
    p8.metric("Odometer", f"{t.get('odometer_km', 'N/A')} km")

    with st.expander("Brake / Tyre / Vibration Details"):

        st.json({
            "brakes": brakes,
            "tyres": tyres,
            "vibration": vibration,
            "diagnostic_trouble_codes": t.get("diagnostic_trouble_codes", []),
        })

    st.divider()

    st.markdown("### Health History")

    history_trend = trend[
        trend["asset_id"] == selected
    ].copy()

    if not history_trend.empty:

        fig = px.line(
            history_trend,
            x="timestamp",
            y="health_score",
        )

        fig.update_traces(
            line=dict(color="#42e0c2", width=2),
        )

        fig.update_layout(
            yaxis=dict(range=[0, 100]),
            height=350,
            title=None,
        )

        st.plotly_chart(
            style_plot(fig),
            use_container_width=True,
        )

    st.markdown("### Current Faults")

    issues = v["issues"]

    if issues:

        for key, issue in issues.items():

            st.error(
                f"{issue.get('severity', 'UNKNOWN')}  |  "
                f"{key.replace('_', ' ').title()}  |  "
                f"{issue.get('message', '')}"
            )

    else:

        st.success("No active faults detected.")


# =========================================================
# ALERT CENTER
# =========================================================

elif page == "Alert Center":

    st.markdown("### Event Stream")

    if alerts.empty:

        st.info("No alert history available.")

    else:

        filters = st.columns(3)

        with filters[0]:

            event_filter = st.selectbox(
                "Event",
                ["ALL", "NEW", "RESOLVED"],
            )

        with filters[1]:

            severity_filter = st.selectbox(
                "Severity",
                ["ALL", "CRITICAL", "WARNING"],
            )

        with filters[2]:

            vehicle_filter = st.selectbox(
                "Vehicle",
                ["ALL"] + vehicles["asset_id"].tolist(),
            )

        filtered = alerts.copy()

        if event_filter != "ALL":
            filtered = filtered[
                filtered["event_type"] == event_filter
            ]

        if severity_filter != "ALL":
            filtered = filtered[
                filtered["severity"] == severity_filter
            ]

        if vehicle_filter != "ALL":
            filtered = filtered[
                filtered["asset_id"] == vehicle_filter
            ]

        st.caption(f"{len(filtered)} events")

        display = filtered[
            [
                "timestamp",
                "asset_id",
                "issue_id",
                "event_type",
                "severity",
                "message",
            ]
        ].copy()

        display.columns = [
            "TIMESTAMP",
            "VEHICLE",
            "ISSUE",
            "EVENT",
            "SEVERITY",
            "DETAIL",
        ]

        st.dataframe(
            display,
            hide_index=True,
            use_container_width=True,
        )


# -------------------- FOOTER --------------------

st.divider()

st.caption("ATHENA  /  CONFIGURE 2026  /  FLEET INTELLIGENCE")