from bokeh.plotting import figure, show, output_file
from bokeh.models import (
    ColumnDataSource, HoverTool, RangeSlider,
    CustomJS, CheckboxGroup, Div, Button
)
from bokeh.layouts import column, row
from bokeh.palettes import Category20_20, Turbo256
import pandas as pd


# ==============================================================
# 1️⃣ LOAD & PREPARE DATA
# ==============================================================

def load_and_prepare_data(filepath='region_05_clean.csv', sample_limit=50000):
    """
    Load and prepare terrorism data for visualization.
    """
    df = pd.read_csv(filepath, low_memory=False)
    print(f"Loaded {len(df):,} records from {filepath}")

    required_cols = ['iyear', 'targtype1_txt', 'nkill', 'nwound']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' not found in dataset")

    # Handle missing & invalid data
    df['nkill'] = pd.to_numeric(df['nkill'], errors='coerce').fillna(0)
    df['nwound'] = pd.to_numeric(df['nwound'], errors='coerce').fillna(0)
    df['iyear'] = pd.to_numeric(df['iyear'], errors='coerce')
    df = df.dropna(subset=['iyear', 'targtype1_txt'])
    df = df[df['iyear'] > 1900]

    # Total casualties
    df['total_casualties'] = df['nkill'] + df['nwound']
    max_casualties = df['total_casualties'].max()
    df['circle_size'] = 8 + (df['total_casualties'] / max_casualties * 22) if max_casualties > 0 else 10

    # ✅ Performance optimization: sample if dataset too large
    if len(df) > sample_limit:
        print(f"Large dataset detected ({len(df):,} rows) — sampling {sample_limit:,} for performance.")
        df = df.sample(sample_limit, random_state=42)

    print(f"Prepared {len(df):,} valid records")
    print(f"Year range: {int(df['iyear'].min())} - {int(df['iyear'].max())}")
    print(f"Unique target types: {df['targtype1_txt'].nunique()}")

    return df


# ==============================================================
# 2️⃣ COLOR MAPPING
# ==============================================================

def create_color_mapping(df):
    unique_targets = sorted(df['targtype1_txt'].unique())
    n_targets = len(unique_targets)
    if n_targets <= 20:
        colors = Category20_20[:n_targets]
    else:
        step = len(Turbo256) // n_targets
        colors = [Turbo256[i * step] for i in range(n_targets)]
    return dict(zip(unique_targets, colors)), unique_targets


# ==============================================================
# 3️⃣ VISUALIZATION CREATION
# ==============================================================

def create_visualization(df, output_path='terrorism_casualties.html'):
    color_map, unique_targets = create_color_mapping(df)
    df['color'] = df['targtype1_txt'].map(color_map)
    original_df = df.copy()
    source = ColumnDataSource(df)

    # Figure setup
    p = figure(
        title="Terrorism Casualties by Target Type (All Years)",
        x_axis_label="Number Killed",
        y_axis_label="Number Wounded",
        width=1000, height=650,
        tools="pan,wheel_zoom,box_zoom,reset,save",
        active_scroll="wheel_zoom",
        toolbar_location="above"
    )

    circles = p.circle(
        x='nkill', y='nwound',
        source=source,
        size='circle_size',
        color='color',
        fill_alpha=0.6,
        line_color='white',
        line_width=0.5,
        legend_field='targtype1_txt'
    )

    hover = HoverTool(
        renderers=[circles],
        tooltips=[
            ("Year", "@iyear{0}"),
            ("Target Type", "@targtype1_txt"),
            ("Killed", "@nkill{0,0}"),
            ("Wounded", "@nwound{0,0}"),
            ("Total Casualties", "@total_casualties{0,0}")
        ]
    )
    p.add_tools(hover)

    # Legend & styling
    p.legend.title = "Target Type (Click to hide/show)"
    p.legend.location = "top_right"
    p.legend.click_policy = "hide"
    p.legend.label_text_font_size = "9pt"
    p.title.text_font_size = "16pt"
    p.xaxis.axis_label_text_font_size = "12pt"
    p.yaxis.axis_label_text_font_size = "12pt"
    p.background_fill_color = "#fafafa"
    p.border_fill_color = "white"
    p.grid.grid_line_alpha = 0.25
    p.grid.grid_line_color = "#ddd"
    p.grid.grid_line_dash = [6, 4]
    p.outline_line_color = None
    p.toolbar.autohide = True

    # Year slider
    year_min, year_max = int(df['iyear'].min()), int(df['iyear'].max())
    year_slider = RangeSlider(
        start=year_min, end=year_max,
        value=(year_min, year_max),
        step=1,
        title="Filter by Year Range", width=950
    )

    # Checkbox for target types
    checkbox = CheckboxGroup(labels=unique_targets, active=list(range(len(unique_targets))))

    # Reset button
    reset_button = Button(label="Reset Filters", button_type="primary", width=150)
    reset_button.js_on_click(CustomJS(args=dict(slider=year_slider, checkbox=checkbox),
                                      code="slider.value=[slider.start,slider.end]; checkbox.active=Array.from(Array(checkbox.labels.length).keys());"))

    # Stats div
    stats_div = Div(text=f"""
        <div style="padding:10px;background-color:#e8f4f8;border-radius:5px;">
            <strong>Showing:</strong> {len(df):,} incidents | 
            <strong>Years:</strong> {year_min} - {year_max} | 
            <strong>Total Killed:</strong> {df['nkill'].sum():,.0f} | 
            <strong>Total Wounded:</strong> {df['nwound'].sum():,.0f}
        </div>
    """, width=950, height=50)

    # ✅ Combined JS callback (Year + Checkbox + Axis autoscale + Stats update)
    callback = CustomJS(args=dict(
        source=source, slider=year_slider, checkbox=checkbox,
        plot=p, stats_div=stats_div, original_data=original_df.to_dict('list')
    ), code="""
        const orig = original_data;
        const [start, end] = slider.value;
        const selected = checkbox.active.map(i => checkbox.labels[i]);

        const new_data = { 'iyear': [], 'targtype1_txt': [], 'nkill': [], 'nwound': [],
                           'total_casualties': [], 'circle_size': [], 'color': [] };

        let total_killed = 0, total_wounded = 0;

        for (let i = 0; i < orig['iyear'].length; i++) {
            const year = orig['iyear'][i];
            const targ = orig['targtype1_txt'][i];
            if (year >= start && year <= end && selected.includes(targ)) {
                new_data['iyear'].push(year);
                new_data['targtype1_txt'].push(targ);
                new_data['nkill'].push(orig['nkill'][i]);
                new_data['nwound'].push(orig['nwound'][i]);
                new_data['total_casualties'].push(orig['total_casualties'][i]);
                new_data['circle_size'].push(orig['circle_size'][i]);
                new_data['color'].push(orig['color'][i]);
                total_killed += orig['nkill'][i];
                total_wounded += orig['nwound'][i];
            }
        }

        source.data = new_data;

        const count = new_data['iyear'].length;
        plot.title.text = `Terrorism Casualties by Target Type (${start} - ${end})`;

        stats_div.text = `
            <div style="padding:10px;background-color:#e8f4f8;border-radius:5px;">
                <strong>Showing:</strong> ${count.toLocaleString()} incidents |
                <strong>Years:</strong> ${start} - ${end} |
                <strong>Total Killed:</strong> ${total_killed.toLocaleString()} |
                <strong>Total Wounded:</strong> ${total_wounded.toLocaleString()}
            </div>`;

        // ✅ Dynamic axis rescale
        const x_vals = new_data['nkill'], y_vals = new_data['nwound'];
        if (x_vals.length > 0) {
            const x_min = Math.min(...x_vals), x_max = Math.max(...x_vals);
            const y_min = Math.min(...y_vals), y_max = Math.max(...y_vals);
            plot.x_range.start = x_min - 1;
            plot.x_range.end = x_max + 1;
            plot.y_range.start = y_min - 1;
            plot.y_range.end = y_max + 1;
        }

        source.change.emit();
    """)

    year_slider.js_on_change('value', callback)
    checkbox.js_on_change('active', callback)

    layout = column(
        stats_div,
        row(year_slider, reset_button),
        checkbox,
        p,
        sizing_mode="scale_width"
    )

    output_file(output_path)
    show(layout)

    print(f"\nVisualization saved to: {output_path}")
    print(f"Total data points: {len(df):,}")
    print(f"Target types displayed: {df['targtype1_txt'].nunique()}")


# ==============================================================
# MAIN EXECUTION
# ==============================================================

if __name__ == "__main__":
    df = load_and_prepare_data('region_05_clean.csv')
    create_visualization(df)
    print("\n✓ Visualization complete! Open 'terrorism_casualties.html' to view it.")
