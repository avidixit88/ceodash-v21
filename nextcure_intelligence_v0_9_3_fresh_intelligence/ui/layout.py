"""Reusable layout fragments for the dashboard."""

from __future__ import annotations

from html import escape

import streamlit as st

from config.settings import APP_SUBTITLE, APP_TITLE, APP_VERSION


def render_hero() -> None:
    st.markdown(
        f"""
        <div class="hero">
            <div class="status-pill">● {APP_VERSION}</div>
            <div class="eyebrow" style="margin-top: 1.1rem;">{APP_SUBTITLE}</div>
            <h1>{APP_TITLE}</h1>
            <p>
                A CEO-ready market intelligence surface for understanding whether the market is working for NextCure,
                how NXTC is behaving relative to biotech and Nasdaq benchmarks, and where peer momentum is concentrating.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _card_html(label: str, value: str, caption: str = "", detail: str | None = None, card_class: str = "card") -> str:
    detail_html = f'<div class="detail-pill">Detail: {escape(detail)}</div>' if detail else ""
    return (
        f'<div class="{card_class}">'
        f'<div class="metric-label">{escape(label)}</div>'
        f'<div class="metric-value">{escape(value)}</div>'
        f'<div class="muted card-caption">{escape(caption)}</div>'
        f'{detail_html}'
        f'</div>'
    )


def render_kpi_cards(kpis: list[dict[str, str]]) -> None:
    cols = st.columns(len(kpis))
    for col, item in zip(cols, kpis):
        with col:
            st.markdown(
                _card_html(str(item["label"]), str(item["value"]), str(item.get("caption", ""))),
                unsafe_allow_html=True,
            )


def render_dashboard_nav(pages: list[str], active_page: str) -> str:
    """Render a readable button-based navigation bar.

    We avoid binding a widget directly to `st.session_state.active_page` so the
    snapshot/detail buttons can safely update the active page without triggering
    Streamlit's post-instantiation session-state exception.
    """
    st.markdown('<div class="nav-title">Dashboard Sections</div>', unsafe_allow_html=True)
    for start in range(0, len(pages), 4):
        row = pages[start:start + 4]
        cols = st.columns(len(row), gap="small")
        for col, page in zip(cols, row):
            with col:
                label = f"● {page}" if page == active_page else page
                if st.button(label, key=f"nav_{page}"):
                    st.session_state.active_page = page
                    st.rerun()
    return st.session_state.active_page


def _summary_title(line: str) -> str:
    if ":" in line:
        return line.split(":", 1)[0]
    return "Readout"


def _summary_body(line: str) -> str:
    if ":" in line:
        return line.split(":", 1)[1].strip()
    return line


def _is_detail_line(line: str) -> bool:
    lower = line.lower()
    detail_markers = [
        "cdh6 / ovarian adc:",
        "b7-h4 adc:",
        "adc capital flow:",
        "ovarian cancer:",
        "data quality note:",
        "capital is strongest",
        "capital is weakest",
        "nxtc event positioning",
    ]
    return any(marker in lower for marker in detail_markers)


def _build_executive_narrative(insights: list[str]) -> str:
    joined = " ".join(insights).lower()
    activation = next((line for line in insights if line.lower().startswith("market activation")), "")
    action = next((line for line in insights if line.lower().startswith("what you can do")), "")

    if "not currently being rewarded" in joined or "stock-specific weakness" in joined:
        p1 = "The current read is defensive: NXTC is not being rewarded versus XBI and the broader biotech tape is not providing much help."
    elif "outperform" in joined or "constructive" in joined:
        p1 = "The current read is constructive: NXTC is showing signs of better positioning, but the quality of that move still needs to be checked against volume, peers, and catalyst timing."
    else:
        p1 = "The current read is selective: some signals are useful, but the market has not fully aligned behind the story yet."

    if activation:
        activation_body = _summary_body(activation)
        p2 = activation_body
    else:
        p2 = "The practical question is not only whether the technicals improve, but whether investors understand the upcoming catalyst well enough to start positioning ahead of it."

    if action:
        p3 = _summary_body(action)
        return f"{p1} {p2} Operator lens: {p3}"
    return p1 + " " + p2


def render_insights(insights: list[str]) -> None:
    st.markdown('<div class="section-title">Executive Readout</div>', unsafe_allow_html=True)
    if not insights:
        st.markdown('<div class="insight">No executive readout is available yet.</div>', unsafe_allow_html=True)
        return

    top_lines = [line for line in insights if not _is_detail_line(line)][:5]
    detail_lines = [line for line in insights if line not in top_lines]

    st.markdown(
        f'<div class="executive-narrative"><div class="summary-title">Plain-English CEO summary</div>'
        f'<div class="summary-body">{escape(_build_executive_narrative(insights))}</div></div>',
        unsafe_allow_html=True,
    )

    for row_start in range(0, len(top_lines), 2):
        row = top_lines[row_start:row_start + 2]
        cols = st.columns(len(row), gap="medium")
        for col, line in zip(cols, row):
            with col:
                st.markdown(
                    f'<div class="summary-card"><div class="summary-title">{escape(_summary_title(line))}</div>'
                    f'<div class="summary-body">{escape(_summary_body(line))}</div></div>',
                    unsafe_allow_html=True,
                )

    if detail_lines:
        with st.expander("Click to see more granular channel, catalyst, and technical detail"):
            for insight in detail_lines:
                st.markdown(f'<div class="insight">{escape(insight)}</div>', unsafe_allow_html=True)


def _detail_target(label: str) -> str:
    text = label.lower()
    if "technical" in text or "alignment" in text:
        return "Technical + Catalyst"
    if "catalyst" in text or "capital" in text:
        return "Catalyst & Capital"
    if "adc" in text or "ovarian" in text or "quarter" in text:
        return "Channel Intelligence"
    if "synthesis" in text or "interpretation" in text or "strategic relevance" in text:
        return "Interpretation Engine"
    if "attention" in text or "activation" in text:
        return "Strategy & Timing"
    if "market" in text or "nxtc" in text or "driver" in text or "window" in text:
        return "Strategy & Timing"
    return "Relevant tab"


def _priority_watch_items(items: list[dict[str, str]]) -> list[dict[str, str]]:
    keep = {"Market", "NXTC Posture", "Driver", "Window Score", "Market Attention", "Catalyst Phase", "Technical Setup", "Alignment", "Synthesis"}
    prioritized = [item for item in items if str(item.get("label", "")) in keep]
    # keep order stable, but avoid showing too many cards at the top
    return prioritized[:8]


def render_watch_items(items: list[dict[str, str]]) -> None:
    if not items:
        return
    st.markdown('<div class="section-title">Intelligence Snapshot</div>', unsafe_allow_html=True)
    visible_items = _priority_watch_items(items)
    if not visible_items:
        visible_items = items[:6]

    for row_start in range(0, len(visible_items), 4):
        row = visible_items[row_start:row_start + 4]
        cols = st.columns(len(row), gap="medium")
        for col, item in zip(cols, row):
            label = str(item.get("label", ""))
            value = str(item.get("value", ""))
            caption = str(item.get("caption", ""))
            target = _detail_target(label)
            with col:
                st.markdown(
                    _card_html(label, value, caption, card_class="snapshot-card"),
                    unsafe_allow_html=True,
                )
                if st.button(f"View {target} →", key=f"detail_{label}_{row_start}"):
                    st.session_state.active_page = target
                    st.rerun()


def render_synthesis_summary(synthesis) -> None:
    """Render v0.9 interpretation/synthesis layer."""
    if synthesis is None:
        return

    st.markdown('<div class="section-title">Interpretation Engine</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="executive-narrative"><div class="summary-title">Synthesized meaning</div>'
        f'<div class="summary-body">{escape(str(synthesis.headline))}<br><br>{escape(str(synthesis.thesis))}</div></div>',
        unsafe_allow_html=True,
    )

    cards = list(getattr(synthesis, "signal_cards", []) or [])
    for row_start in range(0, len(cards), 2):
        row = cards[row_start:row_start + 2]
        cols = st.columns(len(row), gap="medium")
        for col, card in zip(cols, row):
            with col:
                st.markdown(
                    f'<div class="synthesis-card">'
                    f'<div class="metric-label">{escape(str(card.label))}</div>'
                    f'<div class="metric-value" style="font-size:1.12rem;">{escape(str(card.state))}</div>'
                    f'<div class="summary-body" style="margin-top:.55rem;">{escape(str(card.meaning))}</div>'
                    f'<div class="detail-pill">Evidence: {escape(str(card.evidence))}</div>'
                    f'<div class="muted" style="margin-top:.7rem; font-size:.82rem;">Implication: {escape(str(card.implication))}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )


    relevance = getattr(synthesis, "strategic_relevance", None)
    if relevance is not None:
        st.markdown('<div class="section-title" style="font-size:1rem;">Strategic Relevance Engine</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="executive-narrative"><div class="summary-title">Personalized to Michael / NextCure</div>'
            f'<div class="summary-body">{escape(str(relevance.headline))}</div></div>',
            unsafe_allow_html=True,
        )
        brief = getattr(relevance, "executive_brief", []) or []
        if brief:
            cols = st.columns(2, gap="medium")
            for idx, item in enumerate(brief[:4]):
                with cols[idx % 2]:
                    st.markdown(f'<div class="insight">{escape(str(item))}</div>', unsafe_allow_html=True)

        signal_table = getattr(relevance, "signal_table", None)
        if signal_table is not None and not signal_table.empty:
            st.markdown('<div class="section-title" style="font-size:.95rem;">Relevance-Scored Incoming Signal Map</div>', unsafe_allow_html=True)
            st.dataframe(signal_table, use_container_width=True, hide_index=True)

        theme_table = getattr(relevance, "theme_table", None)
        if theme_table is not None and not theme_table.empty:
            st.markdown('<div class="section-title" style="font-size:.95rem;">Repeated Theme Concentration</div>', unsafe_allow_html=True)
            st.dataframe(theme_table, use_container_width=True, hide_index=True)

        query_map = getattr(relevance, "query_map", None)
        with st.expander("How this becomes fresh patent / grant / abstract intelligence"):
            st.markdown(
                "The system now has a contract for incoming information: every patent, grant, abstract, PR, or filing can be scored against NextCure-specific targets, modalities, side channels, and value drivers before it reaches the executive layer."
            )
            if query_map is not None and not query_map.empty:
                st.dataframe(query_map, use_container_width=True, hide_index=True)

    st.markdown('<div class="section-title" style="font-size:1rem;">New Intelligence: Delta / Gap Detection</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="muted" style="margin-bottom:.65rem;">This is the differentiated layer: it looks for lane acceleration, fading, NXTC perception gaps, and peer read-through signals instead of repeating the executive narrative.</div>',
        unsafe_allow_html=True,
    )

    delta_table = getattr(synthesis, "insight_delta_table", None)
    if delta_table is not None and not delta_table.empty:
        st.dataframe(delta_table, use_container_width=True, hide_index=True)
    else:
        st.markdown('<div class="insight">No lane-level delta signal was strong enough to elevate in this run.</div>', unsafe_allow_html=True)

    gap_table = getattr(synthesis, "competitive_gap_table", None)
    if gap_table is not None and not gap_table.empty:
        st.markdown('<div class="section-title" style="font-size:1rem;">Competitive Read-Through Signals</div>', unsafe_allow_html=True)
        st.dataframe(gap_table, use_container_width=True, hide_index=True)

    radar_items = getattr(synthesis, "trend_radar", []) or []
    if radar_items:
        st.markdown('<div class="section-title" style="font-size:1rem;">Trend Radar</div>', unsafe_allow_html=True)
        for item in radar_items:
            st.markdown(f'<div class="insight">{escape(str(item))}</div>', unsafe_allow_html=True)

    left, right = st.columns(2, gap="large")
    with left:
        st.markdown('<div class="section-title" style="font-size:1rem;">What Changed / What Matters</div>', unsafe_allow_html=True)
        for item in getattr(synthesis, "what_changed", []) or []:
            st.markdown(f'<div class="insight">{escape(str(item))}</div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="section-title" style="font-size:1rem;">Emerging Competitive Edges</div>', unsafe_allow_html=True)
        for item in getattr(synthesis, "competitive_edges", []) or []:
            st.markdown(f'<div class="insight">{escape(str(item))}</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title" style="font-size:1rem;">Operating Recommendations</div>', unsafe_allow_html=True)
    for item in getattr(synthesis, "operating_recommendations", []) or []:
        st.markdown(f'<div class="insight">{escape(str(item))}</div>', unsafe_allow_html=True)

    questions = getattr(synthesis, "next_questions", []) or []
    if questions:
        st.markdown('<div class="section-title" style="font-size:1rem;">Questions This Layer Now Answers</div>', unsafe_allow_html=True)
        for item in questions:
            st.markdown(f'<div class="insight">{escape(str(item))}</div>', unsafe_allow_html=True)

    with st.expander("Patent / grant intelligence roadmap"):
        st.markdown(
            "This v0.9 layer prepares the schema and interpretation questions for patents and grants without pretending live ingestion is already complete."
        )
        table = getattr(synthesis, "patent_grant_watch", None)
        if table is not None and not table.empty:
            st.dataframe(table, use_container_width=True, hide_index=True)
