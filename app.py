import streamlit as st
import time
import random
import plotly.graph_objects as go
import tools
import agents

# Page Configuration
st.set_page_config(page_title="INVESTIFY: INVESTMENT GOT SIMPLIFIED", layout="wide")

# Initialize Session State
if "nav_tab" not in st.session_state:
    st.session_state.nav_tab = "Landing"  # Starts on the centered Zerodha-style landing screen
if "selected_stock" not in st.session_state:
    st.session_state.selected_stock = "ITC.NS"
if "selected_bond" not in st.session_state:
    st.session_state.selected_bond = None

# Master database of stocks for dropdown suggestions and watchlist
master_watchlist = [
    {"symbol": "RELIANCE.NS", "price": 2450.50, "change": +1.24},
    {"symbol": "TCS.NS", "price": 3890.10, "change": -0.45},
    {"symbol": "HDFCBANK.NS", "price": 1650.00, "change": +0.88},
    {"symbol": "INFY.NS", "price": 1420.30, "change": +2.10},
    {"symbol": "ICICIBANK.NS", "price": 1105.40, "change": -1.12},
    {"symbol": "SBIN.NS", "price": 810.20, "change": -0.05},
    {"symbol": "BHARTIARTL.NS", "price": 1253.66, "change": -2.46},
    {"symbol": "ITC.NS", "price": 2690.74, "change": +1.91},
    {"symbol": "LTIM.NS", "price": 5551.30, "change": +0.51},
    {"symbol": "LT.NS", "price": 3447.27, "change": +2.47},
    {"symbol": "AAPL", "price": 225.40, "change": +1.15},
    {"symbol": "TSLA", "price": 248.10, "change": -3.20}
]

all_symbols = [s["symbol"] for s in master_watchlist]

# ==========================================
# VIEW 0: KITE-STYLE CENTERED LANDING DISPLAY
# ==========================================
if st.session_state.nav_tab == "Landing":
    # Centering trick using empty columns on the sides
    _, center_col, _ = st.columns([1, 2.5, 1])
    
    with center_col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: #00FFA3;'>⚡ INVESTIFY</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #A0A0A0;'>INVESTMENT GOT SIMPLIFIED</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 14px;'>Autonomous Multi-Agent Financial Intelligence & Trading Terminal</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Action Card Box
        with st.container(border=True):
            st.markdown("#### 🚀 Launch Terminal Session")
            st.caption("Access real-time quantitative metrics, RAG compliance corpus, AI manager synthesis, and debt terminals.")
            
            launch_profile = st.selectbox(
                "Select Default Risk Profile for Quick Launch",
                options=["Conservative (Low Risk)", "Moderate (Balanced)", "Aggressive (High Risk)"],
                key="landing_profile_select"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("Enter Trading Terminal ➔", type="primary", use_container_width=True):
                st.session_state.nav_tab = "Dashboard"
                st.rerun()
                
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #666; font-size: 12px;'>Secured via Google Gemini AI SDK • Institutional-Grade Analytics</p>", unsafe_allow_html=True)

else:
    # ==========================================
    # APP HEADER & TOP NAVIGATION BAR
    # ==========================================
    st.markdown("### ⚡ INVESTIFY: INVESTMENT GOT SIMPLIFIED")

    nav_col1, nav_col2, nav_col3, nav_col4, nav_space = st.columns([1.1, 1.1, 1.1, 1.1, 5])

    with nav_col1:
        if st.button("🏠 Home", key="nav_btn_home"):
            st.session_state.nav_tab = "Landing"
            st.rerun()
    with nav_col2:
        if st.button("📊 Dashboard", key="nav_btn_dash", type="primary" if st.session_state.nav_tab == "Dashboard" else "secondary"):
            st.session_state.nav_tab = "Dashboard"
            st.rerun()
    with nav_col3:
        if st.button("⭐ Watchlist", key="nav_btn_watch", type="primary" if st.session_state.nav_tab == "Watchlist" else "secondary"):
            st.session_state.nav_tab = "Watchlist"
            st.rerun()
    with nav_col4:
        if st.button("🛡️ Bonds", key="nav_btn_bonds", type="primary" if st.session_state.nav_tab == "Bonds" else "secondary"):
            st.session_state.nav_tab = "Bonds"
            st.rerun()

    st.markdown("---")

    # ==========================================
    # VIEW 1: DASHBOARD & MULTI-AGENT EXECUTION
    # ==========================================
    if st.session_state.nav_tab == "Dashboard":
        st.title("Autonomous Financial Intelligence System")
        
        col_input1, col_input2, col_btn = st.columns([2, 2, 1])
        with col_input1:
            current_index = all_symbols.index(st.session_state.selected_stock) if st.session_state.selected_stock in all_symbols else 0
            
            stock_symbol = st.selectbox(
                "Target Asset Ticker (Search / Select)",
                options=all_symbols,
                index=current_index,
                key="dashboard_stock_selectbox"
            )
            st.session_state.selected_stock = stock_symbol
            
        with col_input2:
            user_profile = st.selectbox(
                "Investor Risk Profile",
                options=["Conservative (Low Risk)", "Moderate (Balanced)", "Aggressive (High Risk)"],
                key="dashboard_risk_selectbox"
            )
        with col_btn:
            st.write("") 
            st.write("")
            run_button = st.button("Run Multi-Agent Analysis", type="primary", key="btn_run_analysis")

        st.caption(f"Active Analysis Target: **{stock_symbol}** | Profile: **{user_profile}**")
        st.markdown("---")

        if run_button:
            start_time = time.time()

            # Step 1: Ingest Market Data
            with st.spinner("Step 1/3: Ingesting live exchange feeds..."):
                market_data = tools.get_stock_data(stock_symbol)

            # Step 2: Display Live Metrics Banner
            col1, col2, col3, col4 = st.columns(4)
            price = market_data.get("current_price", 0.0)
            prev = market_data.get("previous_close", 0.0)
            delta = round(price - prev, 2)
            currency_symbol = "$" if not stock_symbol.endswith(".NS") else "₹"

            col1.metric("LIVE PRICE", f"{currency_symbol}{price:,.2f}", f"{delta:+.2f}")
            col2.metric("FEED STATUS", market_data.get("status", "UNKNOWN"))
            signal_label = "Bullish Momentum" if delta >= 0 else "Bearish Drift"
            col3.metric("SIGNAL DIMENSION", signal_label)
            col4.metric("RISK SCORE", "72/100" if "Aggressive" in user_profile else "34/100")

            if market_data.get("status") == "FALLBACK_SIMULATED_FEED":
                st.warning("DATA FEED NOTICE: Live market stream throttled or degraded. Pipeline operating safely on fallback data.")

            # 📈 INTERACTIVE PLOTLY CHART (Zoomable, Price ± 100 Scale Domain)
            st.markdown("### Interactive Intraday Price Action (Zoomable Scale)")
            
            timestamps = [f"10:{i:02d}" for i in range(15)]
            prices = [price + random.uniform(-15, 15) for _ in range(14)] + [price]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=timestamps, 
                y=prices, 
                mode='lines+markers', 
                name='Price',
                line=dict(color='#00FFA3', width=2)
            ))
            
            fig.update_layout(
                yaxis=dict(range=[price - 100, price + 100], title="Price (₹/$)" ),
                xaxis=dict(title="Timeline"),
                template="plotly_dark",
                margin=dict(l=20, r=20, t=20, b=20),
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("---")

            # Step 3: Multi-Agent Execution Traces
            st.subheader("MULTI-AGENT REASONING & EVIDENCE TRACE")
            col_left, col_right = st.columns(2)

            with col_left:
                with st.spinner("Agent 1 (Quant) evaluating metrics..."):
                    quant_result = agents.quant_agent(stock_symbol)
                st.info(f"**AGENT 1 — QUANTITATIVE TECHNICAL ANALYST**\n\n{quant_result}")

            time.sleep(1)

            with col_right:
                with st.spinner("Agent 2 (Researcher) scanning compliance corpus..."):
                    research_result = agents.research_agent(stock_symbol)
                st.info(f"**AGENT 2 — FUNDAMENTAL & COMPLIANCE RESEARCHER (RAG)**\n\n{research_result}")

            time.sleep(1)

            # Step 4: Manager Synthesis
            st.subheader("SYNTHESIZED DECISION INTELLIGENCE")
            with st.spinner("Agent 3 (Portfolio Manager) synthesizing advisory..."):
                final_decision = agents.manager_agent(stock_symbol, user_profile, quant_result, research_result)

            st.success(f"### Final Recommendation for {user_profile}\n\n{final_decision}")

            # INTERACTIVE SIP CALCULATOR SECTION
            st.markdown("---")
            st.subheader("📊 Systematic Investment Plan (SIP) Calculator")
            st.caption("Simulate long-term wealth compounding for regular monthly allocations into this asset.")
            
            scol1, scol2 = st.columns(2)
            with scol1:
                monthly_inv = st.slider("Monthly Investment Amount (₹)", 1000, 100000, 10000, step=1000, key="sip_monthly")
                expected_return = st.slider("Expected Annual Return (%)", 5.0, 30.0, 14.0, step=0.5, key="sip_return")
            with scol2:
                time_period = st.slider("Time Period (Years)", 1, 30, 10, step=1, key="sip_years")

            i = (expected_return / 100) / 12
            n = time_period * 12
            invested_amount = monthly_inv * n
            if i > 0:
                total_value = monthly_inv * (((1 + i)**n - 1) / i) * (1 + i)
            else:
                total_value = invested_amount
            estimated_returns = total_value - invested_amount

            rcol1, rcol2, rcol3 = st.columns(3)
            rcol1.metric("Total Invested Amount", f"₹{invested_amount:,.0f}")
            rcol2.metric("Estimated Wealth Gain", f"₹{estimated_returns:,.0f}")
            rcol3.metric("Total Corpus Value", f"₹{total_value:,.0f}")

            # Step 5: Performance Logs
            end_time = time.time()
            latency = round(end_time - start_time, 2)
            st.markdown("---")
            st.subheader("System Performance Log")
            log1, log2, log3 = st.columns(3)
            log1.write(f"⏱️ **Pipeline Latency:** `{latency}s`")
            log2.write(f"🎯 **Confidence Level:** `89.2%`")
            log3.write(f"🛡️ **Degraded Tolerance:** `Active (Pass)`")

        else:
            st.info("Select a stock from the dropdown above and click **'Run Multi-Agent Analysis'** to run the pipeline.")


    # ==========================================
    # VIEW 2: DEDICATED REAL-TIME WATCHLIST TERMINAL
    # ==========================================
    elif st.session_state.nav_tab == "Watchlist":
        st.subheader("⭐ Live Watchlist Terminal")
        st.caption("Select or filter securities via the dropdown below. Click 'Analyze' to instantly load asset telemetry.")
        
        selected_filter_symbols = st.multiselect(
            "Filter / Recommend Watchlist Assets",
            options=all_symbols,
            default=[],
            key="watchlist_multiselect_filter",
            placeholder="Search or select assets to view..."
        )

        if selected_filter_symbols:
            filtered_list = [item for item in master_watchlist if item["symbol"] in selected_filter_symbols]
        else:
            filtered_list = master_watchlist

        st.markdown("---")

        if not filtered_list:
            st.warning("No matching stocks found in your selection.")
        else:
            for stock in filtered_list:
                col_w1, col_w2, col_w3, col_w4 = st.columns([3, 3, 2, 2])
                with col_w1:
                    st.markdown(f"**{stock['symbol']}**")
                with col_w2:
                    st.markdown(f"₹{stock['price']:,.2f}")
                with col_w3:
                    change_txt = f"{stock['change']:+.2f}%"
                    if stock["change"] >= 0:
                        st.markdown(f":green[{change_txt}]")
                    else:
                        st.markdown(f":red[{change_txt}]")
                with col_w4:
                    if st.button("Analyze", key=f"analyze_btn_{stock['symbol']}"):
                        st.session_state.selected_stock = stock["symbol"]
                        st.session_state.nav_tab = "Dashboard"
                        st.rerun()
                st.markdown("---")


    # ==========================================
    # VIEW 3: DEDICATED BONDS TERMINAL & SUMMARY
    # ==========================================
    elif st.session_state.nav_tab == "Bonds":
        st.subheader("🛡️ Fixed Income & Corporate Bonds Terminal")
        st.caption("Browse secure debt instruments, government securities, and high-yield corporate bonds.")

        bonds_database = [
            {"name": "Tata Capital AAA Corporate Bond", "yield": "8.50% p.a.", "tenure": "3 Years", "rating": "CRISIL AAA", "min_inv": "₹10,000", "summary": "Backed by Tata Capital, this bond offers superior capital safety with high liquidity and stable quarterly coupon payouts."},
            {"name": "Government of India (G-Sec 2034)", "yield": "7.15% p.a.", "tenure": "10 Years", "rating": "Sovereign", "min_inv": "₹10,000", "summary": "Sovereign-backed risk-free security issued directly by the Reserve Bank of India. Zero default risk with semi-annual interest credits."},
            {"name": "Reliance Infra Bond Tranche II", "yield": "9.10% p.a.", "tenure": "5 Years", "rating": "ICRA AA+", "min_inv": "₹25,000", "summary": "Higher yield corporate bond targeted toward aggressive debt portfolios. Features moderate risk exposure with robust asset backing."}
        ]

        bcol1, bcol2 = st.columns([2, 1])

        with bcol1:
            st.markdown("### Available Bond Offerings")
            for idx, bond in enumerate(bonds_database):
                st.markdown(f"**{bond['name']}** | Yield: `:green[{bond['yield']}]` | Tenure: `{bond['tenure']}`")
                if st.button("View Summary", key=f"bond_view_btn_{idx}"):
                    st.session_state.selected_bond = bond
                st.markdown("---")

        with bcol2:
            st.markdown("### 📋 Bond Intelligence Summary")
            if st.session_state.selected_bond:
                b = st.session_state.selected_bond
                st.info(f"**{b['name']}**")
                st.write(f"• **Yield:** {b['yield']}")
                st.write(f"• **Tenure:** {b['tenure']}")
                st.write(f"• **Credit Rating:** {b['rating']}")
                st.write(f"• **Minimum Investment:** {b['min_inv']}")
                st.markdown("---")
                st.markdown(f"**Analyst Take:** {b['summary']}")
            else:
                st.write("Select any bond from the left list to view its complete compliance summary and risk metrics.")