"""Streamlit dashboard for DataToInsightWorkflowAgent."""

from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from data_to_insight.ui_helpers import (
    CLASSIFICATION_OPTIONS,
    PRIORITY_OPTIONS,
    ROUTE_OPTIONS,
    build_processed_table,
    build_summary_metrics,
    export_panel_status,
    filter_items,
    flatten_actions,
    get_default_paths,
    get_high_value_items,
    get_noise_review_items,
    group_actions_by_priority,
    load_or_run_dashboard_data,
)


st.set_page_config(
    page_title="DataToInsightWorkflowAgent",
    layout="wide",
)


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        .block-container { padding-top: 1.6rem; padding-bottom: 3rem; }
        .d2i-hero {
            border: 1px solid #e7edf3;
            border-radius: 8px;
            padding: 1.25rem 1.35rem;
            background: #fbfcfe;
            margin-bottom: 1rem;
        }
        .d2i-hero h1 { margin: 0 0 .35rem 0; font-size: 2rem; }
        .d2i-hero p { margin: .2rem 0; color: #485466; }
        .d2i-badges span {
            display: inline-block;
            border: 1px solid #d9e2ec;
            border-radius: 999px;
            padding: .22rem .55rem;
            margin: .35rem .35rem 0 0;
            background: #ffffff;
            color: #223044;
            font-size: .82rem;
        }
        .d2i-card {
            border: 1px solid #e5eaf0;
            border-radius: 8px;
            padding: 1rem;
            background: #ffffff;
            margin: .6rem 0;
        }
        .d2i-card h3 { margin-top: 0; font-size: 1.05rem; }
        .d2i-muted { color: #607086; font-size: .92rem; }
        .d2i-notice {
            border-left: 4px solid #4f7cff;
            padding: .8rem 1rem;
            background: #f6f8fc;
            border-radius: 6px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    st.markdown(
        """
        <div class="d2i-hero">
          <h1>数据洞察工作流智能体</h1>
          <p><strong>DataToInsightWorkflowAgent</strong></p>
          <p>把杂乱资料转化成高价值信号、优先级判断和下一步行动建议。</p>
          <p>A local-first, public-safe data-to-insight workflow agent for ranked insight signals, action recommendations, and AgentHub-ready exports.</p>
          <div class="d2i-badges">
            <span>Local-first</span>
            <span>Public-safe</span>
            <span>Demo-mode</span>
            <span>AgentHub-ready</span>
            <span>No real connector</span>
            <span>Synthetic demo data only</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_workflow_map() -> None:
    steps = [
        ("Data Intake", "读取 synthetic demo data，不上传真实文件。"),
        ("Normalization", "统一字段、文本和标签，方便后续处理。"),
        ("Classification", "规则型分类，识别学习、商业、项目、求职和噪音。"),
        ("Scoring", "多维 0-5 评分，生成优先级。"),
        ("Noise Filtering", "分离低价值、重复和需复核内容。"),
        ("Insight Extraction", "提取可用信号，不做普通全文总结。"),
        ("Action Recommendation", "生成下一步行动和目标 Agent。"),
        ("Export / AgentHub", "导出 Markdown report 和 AgentHub JSON。"),
    ]
    st.subheader("Workflow Map / 工作流地图")
    columns = st.columns(4)
    for index, (title, description) in enumerate(steps):
        with columns[index % 4]:
            st.markdown(
                f"""
                <div class="d2i-card">
                  <h3>{index + 1}. {title}</h3>
                  <p class="d2i-muted">{description}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def first_signal(item: dict) -> dict:
    signals = item.get("key_signals", [])
    return signals[0] if signals else {}


def first_action(item: dict) -> dict:
    actions = item.get("recommended_actions", [])
    return actions[0] if actions else {}


def render_high_value_items(items: list[dict]) -> None:
    st.subheader("High-value Signals / 高价值信号")
    high_items = get_high_value_items(items)
    if not high_items:
        st.info("No high-value item matches the current filters.")
        return

    for item in high_items:
        signal = first_signal(item)
        action = first_action(item)
        st.markdown(
            f"""
            <div class="d2i-card">
              <h3>{item.get("title")}</h3>
              <p><strong>Classification:</strong> {item.get("classification")} &nbsp; <strong>Score:</strong> {item.get("overall_score")} &nbsp; <strong>Route:</strong> {item.get("recommended_route")}</p>
              <p><strong>Key signal:</strong> {signal.get("signal", "")}</p>
              <p><strong>Why it matters:</strong> {signal.get("why_it_matters", "")}</p>
              <p><strong>Possible use:</strong> {signal.get("possible_use", "")}</p>
              <p><strong>Recommended action:</strong> {action.get("action_type", "")} -> {action.get("target", "")}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_action_board(items: list[dict]) -> None:
    st.subheader("Action Board / 行动建议板")
    grouped = group_actions_by_priority(flatten_actions(items))
    for group_name, actions in grouped.items():
        with st.expander(f"{group_name} ({len(actions)})", expanded=group_name == "High Priority Actions"):
            if not actions:
                st.caption("No actions in this group.")
                continue
            for action in actions:
                st.markdown(
                    f"""
                    <div class="d2i-card">
                      <h3>{action.get("action_type")} -> {action.get("target")}</h3>
                      <p><strong>Source:</strong> {action.get("source_title")}</p>
                      <p><strong>Priority:</strong> {action.get("priority")} &nbsp; <strong>Classification:</strong> {action.get("classification")}</p>
                      <p><strong>Reason:</strong> {action.get("reason")}</p>
                      <p><strong>Next step:</strong> {action.get("next_step")}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def render_noise_queue(items: list[dict]) -> None:
    st.subheader("Noise / Review Queue / 噪音与复核队列")
    queue_items = get_noise_review_items(items)
    if not queue_items:
        st.info("No low-value, noise, or review item matches the current filters.")
        return

    for item in queue_items:
        st.markdown(
            f"""
            <div class="d2i-card">
              <h3>{item.get("title")}</h3>
              <p><strong>Classification:</strong> {item.get("classification")} &nbsp; <strong>Score:</strong> {item.get("overall_score")}</p>
              <p><strong>Keep or ignore:</strong> {item.get("keep_or_ignore")}</p>
              <p><strong>Reason:</strong> {item.get("reason")}</p>
              <p><strong>Why not high priority:</strong> lower score, weak evidence, duplicate/noise label, or review-needed status.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_export_panel(summary: dict, root: Path) -> None:
    st.subheader("Export / AgentHub Panel")
    status = export_panel_status(root)

    left, right = st.columns(2)
    with left:
        st.markdown("**Markdown report**")
        st.code(str(status["markdown_report_path"]))
        st.write("Exists:", status["markdown_report_exists"])
        st.markdown("**AgentHub summary JSON**")
        st.code(str(status["agenthub_summary_path"]))
        st.write("Exists:", status["agenthub_summary_exists"])

    with right:
        st.markdown("**Agent manifest**")
        st.code(str(status["agent_manifest_path"]))
        st.write("Exists:", status["agent_manifest_exists"])
        st.markdown("**Agent contract**")
        st.code(str(status["agent_contract_path"]))
        st.write("Exists:", status["agent_contract_exists"])

    st.markdown("**AgentHub-ready summary**")
    agenthub_keys = [
        "agent_id",
        "agent_name",
        "status",
        "demo_mode",
        "public_safe",
        "total_items_processed",
        "high_value_signals",
        "recommended_actions_count",
        "top_routes",
    ]
    st.json({key: summary.get(key) for key in agenthub_keys})


def render_public_safe_notice() -> None:
    st.markdown(
        """
        <div class="d2i-notice">
        <strong>Public-safe Notice</strong><br>
        This dashboard uses synthetic demo data only. No real connector is enabled. No external API call is made.
        No .env, token, credential, or secret is required. No real user file is processed.<br><br>
        本 Dashboard 仅使用 synthetic demo data。未接入真实 connector。不调用外部 API。
        不读取 .env、token、credential 或 secret。不处理真实用户文件。
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    apply_styles()
    root = Path(__file__).resolve().parent
    paths = get_default_paths(root)

    st.sidebar.header("Controls / 控制面板")
    run_demo = st.sidebar.button("Run demo pipeline")
    priority_filter = st.sidebar.selectbox("Priority filter", PRIORITY_OPTIONS)
    classification_filter = st.sidebar.selectbox("Classification filter", CLASSIFICATION_OPTIONS)
    route_filter = st.sidebar.selectbox("Route filter", ROUTE_OPTIONS)
    st.sidebar.divider()
    st.sidebar.caption("Default input: demo_data/demo_items.json")
    st.sidebar.caption("No upload. No connector. Synthetic demo data only.")

    items, summary = load_or_run_dashboard_data(
        paths["input_path"],
        paths["output_dir"],
        force_run=run_demo,
    )
    filtered_items = filter_items(items, priority_filter, classification_filter, route_filter)
    metrics = build_summary_metrics(summary)

    render_hero()

    st.subheader("Overview Metrics / 总览指标")
    metric_cols = st.columns(6)
    metric_cols[0].metric("Total Items Processed", metrics["total_items_processed"])
    metric_cols[1].metric("High-value Signals", metrics["high_value_signals"])
    metric_cols[2].metric("Medium-value Items", metrics["medium_value_items"])
    metric_cols[3].metric("Low / Noise / Review", metrics["low_value_or_noise_items"])
    metric_cols[4].metric("Recommended Actions", metrics["recommended_actions_count"])
    metric_cols[5].metric("Top Route", metrics["top_recommended_route"])

    render_workflow_map()
    render_high_value_items(filtered_items)
    render_action_board(filtered_items)
    render_noise_queue(filtered_items)

    st.subheader("Processed Items Table / 处理结果表")
    st.dataframe(build_processed_table(filtered_items), use_container_width=True, hide_index=True)

    render_export_panel(summary, root)
    render_public_safe_notice()


if __name__ == "__main__":
    main()
