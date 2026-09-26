import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Nassau Candy Shipping Analysis",
    page_icon="🍬",
    layout="wide"
)


# --------------------------------------------------
# DASHBOARD TITLE
# --------------------------------------------------

st.title("🍬 Nassau Candy Shipping Route Efficiency Dashboard")

st.write(
    "Interactive analysis of shipping routes, delivery performance, "
    "geographic bottlenecks, and ship mode performance."
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

DATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "processed"
    / "feature_engineered_data.csv"
)

df = pd.read_csv(DATA_PATH)


# --------------------------------------------------
# CONVERT DATE COLUMNS
# --------------------------------------------------

df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("Dashboard Filters")

# --------------------------------------------------
# RESET FILTERS
# --------------------------------------------------

if st.sidebar.button("🔄 Reset Filters"):
    st.rerun()

# Region
regions = sorted(
    df["Region"].dropna().unique()
)

selected_region = st.sidebar.multiselect(
    "Select Region",
    options=regions,
    default=regions
)


# State
states = sorted(
    df["State/Province"].dropna().unique()
)

selected_state = st.sidebar.multiselect(
    "Select State",
    options=states,
    default=states
)


# Ship Mode
ship_modes = sorted(
    df["Ship Mode"].dropna().unique()
)

selected_ship_mode = st.sidebar.multiselect(
    "Select Ship Mode",
    options=ship_modes,
    default=ship_modes
)


# --------------------------------------------------
# DATE RANGE FILTER
# --------------------------------------------------

min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

selected_date_range = st.sidebar.date_input(
    "Select Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(selected_date_range) == 2:

    start_date = selected_date_range[0]
    end_date = selected_date_range[1]

else:

    start_date = min_date
    end_date = max_date


# Lead-time filter
min_lead_time = int(
    df["Shipping Lead Time"].min()
)

max_lead_time = int(
    df["Shipping Lead Time"].max()
)

selected_lead_time = st.sidebar.slider(
    "Maximum Shipping Lead Time",
    min_value=min_lead_time,
    max_value=max_lead_time,
    value=max_lead_time
)


# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

filtered_df = df[
    (df["Region"].isin(selected_region))
    & (df["State/Province"].isin(selected_state))
    & (df["Ship Mode"].isin(selected_ship_mode))
    & (df["Order Date"].dt.date >= start_date)
    & (df["Order Date"].dt.date <= end_date)
    & (df["Shipping Lead Time"] <= selected_lead_time)
].copy()

# --------------------------------------------------
# FILTER STATUS
# --------------------------------------------------

st.caption(
    f"Showing {len(filtered_df):,} of {len(df):,} total shipments."
)


# --------------------------------------------------
# EMPTY FILTER CHECK
# --------------------------------------------------

if filtered_df.empty:

    st.warning(
        "⚠️ No shipments match the selected filters. "
        "Please change one or more filters."
    )

    st.stop()

# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------

total_shipments = len(filtered_df)

total_routes = filtered_df["Route"].nunique()

average_lead_time = filtered_df[
    "Shipping Lead Time"
].mean()

average_cost = filtered_df[
    "Cost"
].mean()

average_sales = filtered_df[
    "Sales"
].mean()


# --------------------------------------------------
# DELAY CALCULATION
# --------------------------------------------------

delay_threshold = df[
    "Shipping Lead Time"
].quantile(0.75)

delayed_shipments = (
    filtered_df["Shipping Lead Time"]
    > delay_threshold
).sum()


if total_shipments > 0:

    delay_frequency = (
        delayed_shipments
        / total_shipments
    ) * 100

else:

    delay_frequency = 0


# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

st.subheader("📊 Key Performance Indicators")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Shipments",
        f"{total_shipments:,}"
    )


with col2:

    st.metric(
        "Total Routes",
        f"{total_routes:,}"
    )


with col3:

    st.metric(
        "Average Lead Time",
        f"{average_lead_time:.2f} days"
        if total_shipments > 0
        else "N/A"
    )


with col4:

    st.metric(
        "Delay Frequency",
        f"{delay_frequency:.2f}%"
    )


# --------------------------------------------------
# SECOND KPI ROW
# --------------------------------------------------

col5, col6 = st.columns(2)


with col5:

    st.metric(
        "Average Cost",
        f"{average_cost:,.2f}"
        if total_shipments > 0
        else "N/A"
    )


with col6:

    st.metric(
        "Average Sales",
        f"{average_sales:,.2f}"
        if total_shipments > 0
        else "N/A"
    )


# --------------------------------------------------
# SHIPMENT DISTRIBUTION BY SHIP MODE
# --------------------------------------------------

st.subheader("🚚 Shipments by Ship Mode")


if total_shipments > 0:

    ship_mode_counts = (
        filtered_df["Ship Mode"]
        .value_counts()
        .reset_index()
    )

    ship_mode_counts.columns = [
        "Ship Mode",
        "Shipment Volume"
    ]

    fig = px.bar(
        ship_mode_counts,
        x="Ship Mode",
        y="Shipment Volume",
        title="Shipment Volume by Ship Mode"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

else:

    st.warning(
        "No shipments match the selected filters."
    )



# --------------------------------------------------
# ROUTE EFFICIENCY OVERVIEW
# --------------------------------------------------

st.subheader("🛣️ Route Efficiency Overview")


# Load route efficiency analysis
ROUTE_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "processed"
    / "final_route_efficiency_analysis.csv"
)

route_analysis = pd.read_csv(
    ROUTE_PATH,
    index_col=0
)

# --------------------------------------------------
# APPLY DASHBOARD FILTERS TO ROUTE DATA
# --------------------------------------------------

# Keep only routes that belong to the selected states
# and selected regions.

filtered_routes = route_analysis.copy()

selected_states_set = set(selected_state)

filtered_routes = filtered_routes[
    filtered_routes.index.str.split(" → ").str[-1].isin(
        selected_states_set
    )
]


# --------------------------------------------------
# ROUTE EFFICIENCY CHART
# --------------------------------------------------

if len(filtered_routes) > 0:

    route_chart_data = (
        filtered_routes
        .sort_values(
            "Efficiency_Score",
            ascending=False
        )
        .head(15)
        .reset_index()
    )

    route_chart_data = route_chart_data.rename(
        columns={
            "index": "Route"
        }
    )

    fig_route = px.bar(
        route_chart_data,
        x="Efficiency_Score",
        y="Route",
        orientation="h",
        title="Top 15 Routes by Efficiency Score",
        hover_data=[
            "Shipment_Volume",
            "Average_Lead_Time",
            "Delay_Frequency"
        ]
    )

    fig_route.update_layout(
        yaxis={
            "categoryorder": "total ascending"
        }
    )

    st.plotly_chart(
        fig_route,
        width="stretch"
    )

else:

    st.warning(
        "No route data matches the selected states."
    )


# --------------------------------------------------
# ROUTE PERFORMANCE TABLE
# --------------------------------------------------

st.subheader("📋 Route Performance Details")


if len(filtered_routes) > 0:

    route_table = (
        filtered_routes
        .reset_index()
        .rename(
            columns={
                "index": "Route"
            }
        )
    )

    route_table = route_table[
        [
            "Route",
            "Shipment_Volume",
            "Average_Lead_Time",
            "Delay_Frequency",
            "Efficiency_Score",
            "Route_Classification"
        ]
    ]

    route_table = route_table.sort_values(
        "Efficiency_Score",
        ascending=False
    )

    st.dataframe(
        route_table,
        width="stretch"
    )

else:

    st.warning(
        "No route performance data available."
    )


# --------------------------------------------------
# GEOGRAPHIC SHIPPING MAP
# --------------------------------------------------

st.subheader("🗺️ Geographic Shipping Analysis")


# Calculate state-level geographic performance
state_map_data = (
    filtered_df
    .groupby("State/Province")
    .agg(
        Shipment_Volume=("State/Province", "size"),
        Average_Lead_Time=("Shipping Lead Time", "mean")
    )
    .reset_index()
)


# Round average lead time
state_map_data["Average_Lead_Time"] = (
    state_map_data["Average_Lead_Time"].round(2)
)


# --------------------------------------------------
# US STATE NAME → STATE CODE
# --------------------------------------------------

state_codes = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC"
}


state_map_data["State_Code"] = (
    state_map_data["State/Province"]
    .map(state_codes)
)


# --------------------------------------------------
# REMOVE UNMATCHED STATES
# --------------------------------------------------

state_map_data = state_map_data.dropna(
    subset=["State_Code"]
)


# --------------------------------------------------
# CREATE GEOGRAPHIC MAP
# --------------------------------------------------

if len(state_map_data) > 0:

    fig_map = px.choropleth(
        state_map_data,
        locations="State_Code",
        locationmode="USA-states",
        color="Average_Lead_Time",
        scope="usa",
        hover_name="State/Province",
        hover_data={
            "State_Code": False,
            "Shipment_Volume": True,
            "Average_Lead_Time": True
        },
        title="Average Shipping Lead Time by Customer State"
    )

    fig_map.update_layout(
        height=600
    )

    st.plotly_chart(
        fig_map,
        width="stretch"
    )

else:

    st.warning(
        "No geographic data available for the selected filters."
    )


# --------------------------------------------------
# GEOGRAPHIC PERFORMANCE TABLE
# --------------------------------------------------

st.subheader("📍 State-Level Shipping Performance")


if len(state_map_data) > 0:

    geographic_table = (
        state_map_data
        .sort_values(
            "Average_Lead_Time",
            ascending=False
        )
    )

    st.dataframe(
        geographic_table[
            [
                "State/Province",
                "Shipment_Volume",
                "Average_Lead_Time"
            ]
        ],
        width="stretch"
    )

else:

    st.warning(
        "No state-level performance data available."
    )


# --------------------------------------------------
# SHIP MODE PERFORMANCE COMPARISON
# --------------------------------------------------

st.subheader("🚚 Ship Mode Performance Comparison")


# Calculate ship mode performance
ship_mode_dashboard = (
    filtered_df
    .groupby("Ship Mode")
    .agg(
        Shipment_Volume=("Ship Mode", "size"),
        Average_Lead_Time=("Shipping Lead Time", "mean"),
        Average_Cost=("Cost", "mean"),
        Average_Sales=("Sales", "mean")
    )
    .reset_index()
)


# Calculate delayed shipments using
# the same 75th-percentile benchmark
ship_mode_dashboard["Delayed_Shipments"] = (
    filtered_df
    .groupby("Ship Mode")["Shipping Lead Time"]
    .apply(
        lambda x: (x > delay_threshold).sum()
    )
    .values
)


# Calculate delay frequency
ship_mode_dashboard["Delay_Frequency"] = (
    ship_mode_dashboard["Delayed_Shipments"]
    / ship_mode_dashboard["Shipment_Volume"]
    * 100
)


# Round numerical values
ship_mode_dashboard["Average_Lead_Time"] = (
    ship_mode_dashboard["Average_Lead_Time"].round(2)
)

ship_mode_dashboard["Average_Cost"] = (
    ship_mode_dashboard["Average_Cost"].round(2)
)

ship_mode_dashboard["Average_Sales"] = (
    ship_mode_dashboard["Average_Sales"].round(2)
)

ship_mode_dashboard["Delay_Frequency"] = (
    ship_mode_dashboard["Delay_Frequency"].round(2)
)


# --------------------------------------------------
# LEAD TIME COMPARISON
# --------------------------------------------------

if len(ship_mode_dashboard) > 0:

    fig_ship_time = px.bar(
        ship_mode_dashboard,
        x="Ship Mode",
        y="Average_Lead_Time",
        title="Average Shipping Lead Time by Ship Mode",
        hover_data=[
            "Shipment_Volume",
            "Delay_Frequency"
        ]
    )

    st.plotly_chart(
        fig_ship_time,
        width="stretch"
    )


# --------------------------------------------------
# DELAY FREQUENCY COMPARISON
# --------------------------------------------------

if len(ship_mode_dashboard) > 0:

    fig_ship_delay = px.bar(
        ship_mode_dashboard,
        x="Ship Mode",
        y="Delay_Frequency",
        title="Delay Frequency by Ship Mode",
        hover_data=[
            "Shipment_Volume",
            "Average_Lead_Time"
        ]
    )

    st.plotly_chart(
        fig_ship_delay,
        width="stretch"
    )


# --------------------------------------------------
# SHIP MODE PERFORMANCE TABLE
# --------------------------------------------------

st.subheader("📋 Ship Mode Performance Details")


if len(ship_mode_dashboard) > 0:

    st.dataframe(
        ship_mode_dashboard[
            [
                "Ship Mode",
                "Shipment_Volume",
                "Average_Lead_Time",
                "Delay_Frequency",
                "Average_Cost",
                "Average_Sales"
            ]
        ],
        width="stretch"
    )

else:

    st.warning(
        "No ship mode data matches the selected filters."
    )

# --------------------------------------------------
# ROUTE DRILL-DOWN
# --------------------------------------------------

st.subheader("🔎 Route Drill-Down")


# Get available routes
available_routes = sorted(
    filtered_routes.index.unique()
)


if len(available_routes) > 0:

    selected_route = st.selectbox(
        "Select a Route",
        options=available_routes
    )


    # Get selected route details
    selected_route_data = (
        filtered_routes
        .loc[selected_route]
    )


    # --------------------------------------------------
    # ROUTE KPI CARDS
    # --------------------------------------------------

    route_col1, route_col2, route_col3, route_col4 = st.columns(4)


    with route_col1:

        st.metric(
            "Shipment Volume",
            f"{int(selected_route_data['Shipment_Volume']):,}"
        )


    with route_col2:

        st.metric(
            "Average Lead Time",
            f"{selected_route_data['Average_Lead_Time']:.2f} days"
        )


    with route_col3:

        st.metric(
            "Delay Frequency",
            f"{selected_route_data['Delay_Frequency']:.2f}%"
        )


    with route_col4:

        st.metric(
            "Efficiency Score",
            f"{selected_route_data['Efficiency_Score']:.2f}"
        )


    # --------------------------------------------------
    # ROUTE DETAILS
    # --------------------------------------------------

    st.write("### Route Details")


    route_details = pd.DataFrame({
        "Metric": [
            "Route",
            "Shipment Volume",
            "Minimum Lead Time",
            "Average Lead Time",
            "Maximum Lead Time",
            "Delayed Shipments",
            "Delay Frequency",
            "Efficiency Score",
            "Route Classification"
        ],

        "Value": [
            selected_route,
            int(selected_route_data["Shipment_Volume"]),
            f"{selected_route_data['Minimum_Lead_Time']:.0f} days",
            f"{selected_route_data['Average_Lead_Time']:.2f} days",
            f"{selected_route_data['Maximum_Lead_Time']:.0f} days",
            int(selected_route_data["Delayed_Shipments"]),
            f"{selected_route_data['Delay_Frequency']:.2f}%",
            f"{selected_route_data['Efficiency_Score']:.2f}",
            selected_route_data["Route_Classification"]
        ]
    })


    st.dataframe(
        route_details,
        width="stretch",
        hide_index=True
    )


else:

    st.warning(
        "No routes are available for the selected filters."
    )


# --------------------------------------------------
# GEOGRAPHIC BOTTLENECK HIGHLIGHTING
# --------------------------------------------------

st.subheader("⚠️ Potential Geographic Bottlenecks")


# Calculate state-level performance
bottleneck_data = (
    filtered_df
    .groupby("State/Province")
    .agg(
        Shipment_Volume=("State/Province", "size"),
        Average_Lead_Time=("Shipping Lead Time", "mean")
    )
    .reset_index()
)


# Calculate state delay frequency
state_delay_values = (
    filtered_df
    .groupby("State/Province")["Shipping Lead Time"]
    .apply(
        lambda x: (x > delay_threshold).mean() * 100
    )
    .reset_index(name="Delay_Frequency")
)


# Merge delay frequency
bottleneck_data = bottleneck_data.merge(
    state_delay_values,
    on="State/Province",
    how="left"
)


# Calculate medians for relative benchmarking
if len(bottleneck_data) > 0:

    volume_benchmark = (
        bottleneck_data["Shipment_Volume"].median()
    )

    lead_benchmark = (
        bottleneck_data["Average_Lead_Time"].median()
    )

    delay_benchmark = (
        bottleneck_data["Delay_Frequency"].median()
    )


    # Identify potential bottlenecks
    bottleneck_data["Potential_Bottleneck"] = (
        (bottleneck_data["Shipment_Volume"] >= volume_benchmark)
        &
        (bottleneck_data["Average_Lead_Time"] >= lead_benchmark)
        &
        (bottleneck_data["Delay_Frequency"] >= delay_benchmark)
    )


    bottlenecks = (
        bottleneck_data[
            bottleneck_data["Potential_Bottleneck"]
        ]
        .sort_values(
            ["Shipment_Volume", "Average_Lead_Time"],
            ascending=[False, False]
        )
    )


    if len(bottlenecks) > 0:

        st.warning(
            f"{len(bottlenecks)} state(s) meet the "
            "relative potential-bottleneck criteria."
        )


        st.dataframe(
            bottlenecks[
                [
                    "State/Province",
                    "Shipment_Volume",
                    "Average_Lead_Time",
                    "Delay_Frequency"
                ]
            ],
            width="stretch",
            hide_index=True
        )

    else:

        st.info(
            "No states meet all three relative "
            "potential-bottleneck criteria."
        )

else:

    st.info(
        "No geographic data is available for the selected filters."
    )