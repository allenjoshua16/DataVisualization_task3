# DataVisualization_task3

**Abstract**

This report analyzes global terrorism incidents using multi-dimensional visualizations. The study highlights target types, attack trends, regional intensities, and dominant terrorist groups. Interactive visualizations created with Bokeh, Plotly, and D3.js allow for deep exploration of the data from region_05_clean.csv, offering insights into temporal, categorical, and geographical patterns of terrorism worldwide.

**Data Preparation**

The dataset region_05_clean.csv was cleaned and processed to ensure consistency:
•	Removed missing or invalid iyear, targtype1_txt, nkill, nwound values.
•	Computed Total Casualties = nkill + nwound.
•	Handled large dataset sampling for performance optimization.
•	Columns used: iyear, targtype1_txt, gname, attacktype1_txt, country_txt, nkill, nwound.

**Visualization1:  Geospatial Heatmap (D3.js)**
File: d3_heatmap.html
Goal: Display global distribution of terrorism incidents per year.
Features:
•	Interactive world map with zoom and year slider.
•	Red color intensity represents higher number of incidents.
•	Tooltip displays country and number of incidents.
•	Dynamic statistics below slider show total incidents and affected countries.
Insight:
Regions in the Middle East and South Asia show high-intensity clusters, particularly after 2000, indicating persistent regional instability.


**Visualization 2: Attack Types Over Time (Plotly)**
File: attack_types.html
Goal: Analyze changing attack strategies over time.
Features:
•	Stacked area chart showing frequency of each attack type per year.
•	Toggle between stacked, grouped, and 100% stacked views.
•	Hover displays year, attack type, and count.
Insight:
Bombings and armed assaults remain dominant over decades, with a sharp rise between 2010–2015, coinciding with global terrorism escalation.


**Visualization 3: Target Types and Casualties (Bokeh)**
File: target_types_&_casualities.html
Goal: Compare casualties across target types.
Features:
•	Interactive scatter plot with dynamic year range slider and target type filter.
•	Circle size proportional to total casualties.
•	Hover tooltip shows detailed incident data.
•	Reset button restores full dataset view.
Insight:
Civilian and government targets experience the most casualties, indicating that non-combatant populations bear the brunt of terrorist attacks.


**Visualization 4: Top 10 Terrorist Groups (D3.js)**
File: d3_top10_groups.html
Goal: Identify the most active groups per year.
Features:
•	Dropdown menu to select year.
•	Animated horizontal bar chart for top 10 groups.
•	Hover tooltip shows incident count per group.
•	Color intensity represents magnitude of incidents.
Insight:
Group dominance changes over time—certain organizations peak sharply in specific years, revealing shifting geopolitical dynamics.


**Key Findings**

•	Temporal trend: Steady rise in incidents from 2000–2015.
•	Geographical pattern: High activity in Middle East, South Asia, and parts of Africa.
•	Target preference: Civilian and government entities are primary targets.
•	Attack strategy: Bombings dominate; newer patterns show diversification.
•	Group dynamics: Few groups account for a large share of incidents in each period.


**Limitations and Assumptions**

•	Missing or inconsistent data in some years may bias results.
•	Casualty numbers may vary due to reporting accuracy.
•	Dataset limited to Region_05; may not represent all global patterns.
•	Visualizations rely on browser rendering; performance depends on local resources.


**Conclusion**

The visualizations collectively reveal how terrorism patterns evolve spatially, temporally, and strategically. Combining Bokeh, Plotly, and D3.js offers comprehensive exploration — bridging static reporting and dynamic analytics for better understanding and prevention strategies.
Overall: The dataset portrays terrorism as a persistent and evolving global threat with dynamic actors, shifting hotspots, and escalating casualty impact through time.

