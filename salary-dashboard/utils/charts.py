import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.config import CHART_COLORS, COLORS, DIMENSION_LABELS
from utils.metrics import salary_summary_by
from utils.modeling import LinearModelResult


def _format_vn(value: float | int, decimals: int = 0) -> str:
    formatted = f"{value:,.{decimals}f}"
    return formatted.replace(",", "X").replace(".", ",").replace("X", ".")


def _style_figure(figure: go.Figure, height: int = 390) -> go.Figure:
    figure.update_layout(
        autosize=True,
        colorway=CHART_COLORS,
        height=height,
        margin=dict(l=20, r=20, t=64, b=22),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        font=dict(
            family="IBM Plex Sans, Segoe UI, sans-serif",
            color=COLORS["navy"],
            size=12,
        ),
        title=dict(
            font=dict(size=17, color=COLORS["navy"], weight=700),
            x=0.01,
            xanchor="left",
            y=0.97,
            yanchor="top",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11),
        ),
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor=COLORS["border"],
            font_color=COLORS["navy"],
            font_family="IBM Plex Sans, Segoe UI, sans-serif",
        ),
        hovermode="closest",
        separators=",.",
    )
    figure.update_xaxes(
        gridcolor=COLORS["grid"],
        linecolor=COLORS["border"],
        zeroline=False,
        title_font=dict(size=12, color=COLORS["muted"]),
        tickfont=dict(color=COLORS["muted"], size=11),
        automargin=True,
    )
    figure.update_yaxes(
        gridcolor=COLORS["grid"],
        linecolor=COLORS["border"],
        zeroline=False,
        title_font=dict(size=12, color=COLORS["muted"]),
        tickfont=dict(color=COLORS["muted"], size=11),
        automargin=True,
    )
    return figure


def salary_histogram(df: pd.DataFrame) -> go.Figure:
    figure = px.histogram(
        df,
        x="Salary",
        nbins=39,
        title="Phân bố mức lương",
        labels={"Salary": "Mức lương", "count": "Số nhân viên"},
        color_discrete_sequence=[COLORS["blue"]],
    )
    figure.update_traces(marker_line_width=0.5, marker_line_color="#FFFFFF")
    mean_salary = float(df["Salary"].mean())
    figure.add_vline(
        x=mean_salary,
        line_dash="dash",
        line_color=COLORS["teal"],
        annotation_text=f"Trung bình {_format_vn(mean_salary)}",
        annotation_position="top right",
    )
    figure.update_yaxes(title="Số nhân viên")
    return _style_figure(figure, height=410)


def department_donut(df: pd.DataFrame) -> go.Figure:
    counts = df["Department"].value_counts().rename_axis("Department").reset_index(name="count")
    figure = px.pie(
        counts,
        names="Department",
        values="count",
        hole=0.58,
        title="Nhân viên theo phòng ban",
        color_discrete_sequence=CHART_COLORS,
    )
    figure.update_traces(
        textinfo="percent",
        domain=dict(x=[0.0, 0.56]),
        hovertemplate="%{label}<br>%{value:,.0f} nhân viên<br>%{percent}<extra></extra>",
    )
    figure.add_annotation(
        text=f"<b>{_format_vn(len(df))}</b><br><span style='font-size:11px'>nhân viên</span>",
        x=0.28,
        y=0.5,
        showarrow=False,
        font=dict(color=COLORS["navy"], size=16),
    )
    _style_figure(figure, height=360)
    figure.update_layout(
        legend=dict(orientation="v", yanchor="middle", y=0.48, xanchor="left", x=0.62),
        margin=dict(l=12, r=12, t=62, b=12),
    )
    return figure


def department_salary_bar(df: pd.DataFrame) -> go.Figure:
    summary = salary_summary_by(df, "Department").sort_values("mean")
    figure = px.bar(
        summary,
        x="Department",
        y="mean",
        title="Lương trung bình theo phòng ban",
        labels={"Department": "Phòng ban", "mean": "Lương trung bình"},
        color="Department",
        color_discrete_sequence=CHART_COLORS,
        text_auto=".3s",
    )
    figure.update_traces(showlegend=False, hovertemplate="%{x}<br>%{y:,.0f}<extra></extra>")
    return _style_figure(figure, height=360)


def comparison_bar(df: pd.DataFrame, dimension: str) -> go.Figure:
    summary = salary_summary_by(df, dimension)
    melted = summary.melt(
        id_vars=[dimension, "count"],
        value_vars=["mean", "median"],
        var_name="metric",
        value_name="salary",
    )
    melted["metric"] = melted["metric"].map({"mean": "Trung bình", "median": "Trung vị"})
    label = DIMENSION_LABELS[dimension]
    figure = px.bar(
        melted,
        x=dimension,
        y="salary",
        color="metric",
        barmode="group",
        title=f"Lương theo {label.lower()}",
        labels={dimension: label, "salary": "Mức lương", "metric": "Thang đo"},
        color_discrete_map={"Trung bình": COLORS["blue"], "Trung vị": COLORS["teal"]},
        custom_data=["count"],
    )
    figure.update_traces(
        hovertemplate="%{x}<br>%{fullData.name}: %{y:,.0f}<br>Cỡ mẫu: %{customdata[0]:,.0f}<extra></extra>"
    )
    return _style_figure(figure, height=390)


def salary_boxplot(df: pd.DataFrame, dimension: str) -> go.Figure:
    label = DIMENSION_LABELS[dimension]
    figure = px.box(
        df,
        x=dimension,
        y="Salary",
        color=dimension,
        points="outliers",
        title=f"Phân bố lương theo {label.lower()}",
        labels={dimension: label, "Salary": "Mức lương"},
        color_discrete_sequence=CHART_COLORS,
    )
    figure.update_traces(showlegend=False)
    return _style_figure(figure, height=390)


def experience_scatter(df: pd.DataFrame, model: LinearModelResult | None = None) -> go.Figure:
    figure = px.scatter(
        df,
        x="Experience_Years",
        y="Salary",
        title="Kinh nghiệm so với mức lương",
        labels={"Experience_Years": "Số năm kinh nghiệm", "Salary": "Mức lương"},
        opacity=0.28,
        color_discrete_sequence=[COLORS["blue"]],
    )
    figure.update_traces(marker=dict(size=6), name="Nhân viên")
    if model is not None:
        figure.add_trace(
            go.Scatter(
                x=model.line_x,
                y=model.line_y,
                mode="lines",
                name="Đường hồi quy",
                line=dict(color=COLORS["teal"], width=3),
                hovertemplate="Kinh nghiệm: %{x:.1f}<br>Dự đoán: %{y:,.0f}<extra></extra>",
            )
        )
    return _style_figure(figure, height=390)


def experience_group_bar(df: pd.DataFrame) -> go.Figure:
    summary = (
        df.groupby("Experience_Group", observed=False)["Salary"]
        .agg(mean="mean", count="size")
        .reset_index()
    )
    figure = px.bar(
        summary,
        x="Experience_Group",
        y="mean",
        title="Lương theo nhóm kinh nghiệm",
        labels={"Experience_Group": "Nhóm kinh nghiệm", "mean": "Lương trung bình"},
        color="Experience_Group",
        color_discrete_sequence=CHART_COLORS,
        text_auto=".3s",
        custom_data=["count"],
    )
    figure.update_traces(
        showlegend=False,
        hovertemplate="%{x} năm<br>Trung bình: %{y:,.0f}<br>Cỡ mẫu: %{customdata[0]:,.0f}<extra></extra>",
    )
    return _style_figure(figure, height=430)


def residual_plot(result: LinearModelResult) -> go.Figure:
    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=result.test_predicted,
            y=result.residuals,
            mode="markers",
            name="Phần dư",
            marker=dict(color=COLORS["blue"], opacity=0.38, size=6),
            hovertemplate="Dự đoán: %{x:,.0f}<br>Phần dư: %{y:,.0f}<extra></extra>",
        )
    )
    figure.add_hline(y=0, line_dash="dash", line_color=COLORS["gray"])
    figure.update_layout(title="Phần dư của mô hình")
    figure.update_xaxes(title="Giá trị dự đoán")
    figure.update_yaxes(title="Phần dư")
    return _style_figure(figure, height=310)


def age_scatter(df: pd.DataFrame) -> go.Figure:
    figure = px.scatter(
        df,
        x="Age",
        y="Salary",
        title="Độ tuổi so với mức lương",
        labels={"Age": "Độ tuổi", "Salary": "Mức lương"},
        opacity=0.25,
        color_discrete_sequence=[COLORS["purple"]],
    )
    figure.update_traces(marker=dict(size=6))
    return _style_figure(figure, height=390)


def age_group_bar(df: pd.DataFrame) -> go.Figure:
    summary = (
        df.groupby("Age_Group", observed=True)["Salary"]
        .agg(mean="mean", median="median", count="size")
        .reset_index()
    )
    figure = px.bar(
        summary,
        x="Age_Group",
        y=["mean", "median"],
        barmode="group",
        title="Lương theo nhóm tuổi",
        labels={"Age_Group": "Nhóm tuổi", "value": "Mức lương", "variable": "Thang đo"},
        color_discrete_sequence=[COLORS["blue"], COLORS["teal"]],
    )
    figure.for_each_trace(
        lambda trace: trace.update(name={"mean": "Trung bình", "median": "Trung vị"}.get(trace.name, trace.name))
    )
    return _style_figure(figure, height=390)
