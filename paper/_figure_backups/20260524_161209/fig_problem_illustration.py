import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'mathtext.fontset': 'cm',
    'font.size': 10,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
})

fig, ax = plt.subplots(figsize=(7.0, 2.8))
ax.set_xlim(-0.1, 10.6)
ax.set_ylim(-0.25, 3.55)
ax.axis('off')
fig.patch.set_facecolor('white')

# --- Color palette: blue (human) → orange (deep recursive) ---
box_fills = ['#D6EAF8', '#FDEBD0', '#F5CBA7', '#E59866', '#D35400']
box_edges = ['#2980B9', '#E67E22', '#D35400', '#C0392B', '#922B21']
dark_text = '#2C3E50'
gray_text = '#7F8C8D'
accent_red = '#C0392B'

# === TOP ROW: Recursive generation chain ===
chain_y = 2.85
box_w, box_h = 1.10, 0.68
depth_labels = [
    r'$\mathcal{D}_0$', r'$\mathcal{D}_1$', r'$\mathcal{D}_2$',
    r'$\mathcal{D}_3$', r'$\mathcal{D}_K$'
]
depth_subtitles = ['Human', 'Gen-1', 'Gen-2', 'Gen-3', r'Gen-$K$']
x_positions = [0.7, 2.55, 4.4, 6.25, 9.2]

for i, (xp, label, sub) in enumerate(zip(x_positions, depth_labels, depth_subtitles)):
    rect = patches.FancyBboxPatch(
        (xp - box_w/2, chain_y - box_h/2), box_w, box_h,
        boxstyle="round,pad=0.08", facecolor=box_fills[i],
        edgecolor=box_edges[i], linewidth=1.4
    )
    ax.add_patch(rect)
    label_color = 'white' if i == 4 else dark_text
    sub_color = '#E8E8E8' if i == 4 else gray_text
    ax.text(xp, chain_y + 0.08, label, ha='center', va='center',
            fontsize=12.5, fontweight='bold', color=label_color)
    ax.text(xp, chain_y - 0.20, sub, ha='center', va='center',
            fontsize=6.5, color=sub_color, style='italic')

# Arrows between consecutive boxes (plot + marker to avoid aspect-ratio distortion)
arrow_color = '#5D6D7E'
for i in range(3):
    x_start = x_positions[i] + box_w/2 + 0.06
    x_end = x_positions[i+1] - box_w/2 - 0.06
    ax.plot([x_start, x_end - 0.08], [chain_y, chain_y], '-',
            color=arrow_color, lw=1.5, solid_capstyle='butt')
    ax.plot(x_end - 0.08, chain_y, marker='>',
            color=arrow_color, markersize=6, zorder=3)
    mid_x = (x_start + x_end) / 2
    ax.text(mid_x, chain_y - box_h/2 - 0.18, 'LoRA ft + sample',
            ha='center', va='center', fontsize=5.5, color=gray_text,
            fontstyle='italic')

# Ellipsis between D3 and DK
for dot_x in [7.55, 7.95, 8.35]:
    ax.plot(dot_x, chain_y, '.', color='#5D6D7E', markersize=5)

# === MIDDLE-LEFT: Sample passage box ===
sample_y = 1.25
sample_x = 2.2

# Dashed arrow from D1 down to sample box
_ax1 = x_positions[1]
_ay1 = chain_y - box_h/2 - 0.03
_ax2 = sample_x + 0.3
_ay2 = sample_y + 0.35
ax.plot([_ax1, _ax2], [_ay1, _ay2], '--', color=accent_red, lw=1.2, dashes=(4, 3))
ax.plot(_ax2, _ay2, marker='v', color=accent_red, markersize=5, zorder=3)

sample_w, sample_h = 2.3, 0.55
sample_rect = patches.FancyBboxPatch(
    (sample_x - sample_w/2, sample_y - sample_h/2), sample_w, sample_h,
    boxstyle="round,pad=0.07", facecolor='#FDF2E9',
    edgecolor=accent_red, linewidth=1.1, linestyle='--'
)
ax.add_patch(sample_rect)
ax.text(sample_x, sample_y + 0.08, r'Text passage $\mathbf{x}$',
        ha='center', va='center', fontsize=10, color=dark_text)
ax.text(sample_x, sample_y - 0.15, r'depth $d$ = ?', ha='center', va='center',
        fontsize=9, color=accent_red, fontweight='bold')

# === MIDDLE-RIGHT: Classifier → output distribution ===
# Arrow from sample to classifier box
cls_x = 5.6
cls_y = sample_y
_sx = sample_x + sample_w/2 + 0.06
_ex = cls_x - 0.55
ax.plot([_sx, _ex - 0.08], [cls_y, cls_y], '-', color='#2980B9', lw=1.4, solid_capstyle='butt')
ax.plot(_ex - 0.08, cls_y, marker='>', color='#2980B9', markersize=6, zorder=3)

# Classifier box
cls_w, cls_h = 1.1, 0.42
cls_rect = patches.FancyBboxPatch(
    (cls_x - cls_w/2, cls_y - cls_h/2), cls_w, cls_h,
    boxstyle="round,pad=0.06", facecolor='#EBF5FB',
    edgecolor='#2980B9', linewidth=1.0
)
ax.add_patch(cls_rect)
ax.text(cls_x, cls_y, r'Classifier', ha='center', va='center',
        fontsize=8.5, color='#2980B9', style='italic')

# Arrow from classifier to bars
bar_region_x = 8.8
_cx = cls_x + cls_w/2 + 0.04
_bx = bar_region_x - 1.65
ax.plot([_cx, _bx - 0.08], [cls_y, cls_y], '-', color='#2980B9', lw=1.4, solid_capstyle='butt')
ax.plot(_bx - 0.08, cls_y, marker='>', color='#2980B9', markersize=6, zorder=3)

# Probability bar chart: d=0, d=1, d=2, ellipsis, d=K
bar_labels = ['0', '1', '2', r'$K$']
bar_probs = [0.05, 0.70, 0.15, 0.03]
bar_colors_est = ['#D6EAF8', '#FDEBD0', '#F5CBA7', '#D35400']
bar_edge_est = ['#2980B9', '#E67E22', '#D35400', '#922B21']
bar_w_total = 2.4
bar_h_each = 0.11
bar_gap = 0.04
ellipsis_gap = 0.12
bar_x_start = bar_region_x - bar_w_total / 2 + 0.3

n_visible = len(bar_labels)
total_bar_height = n_visible * bar_h_each + (n_visible - 1) * bar_gap + ellipsis_gap
bar_y_top = cls_y + total_bar_height / 2

for j, (lbl, prob, bc, be) in enumerate(zip(bar_labels, bar_probs, bar_colors_est, bar_edge_est)):
    if j < 3:
        by = bar_y_top - j * (bar_h_each + bar_gap) - bar_h_each
    else:
        by = bar_y_top - 3 * (bar_h_each + bar_gap) - ellipsis_gap - bar_h_each
    # Background bar
    ax.add_patch(patches.Rectangle((bar_x_start, by), bar_w_total, bar_h_each,
                                    facecolor='#F4F6F7', edgecolor='#E5E8E8',
                                    linewidth=0.4))
    # Filled bar
    filled_w = bar_w_total * prob
    ax.add_patch(patches.Rectangle((bar_x_start, by), filled_w, bar_h_each,
                                    facecolor=bc, edgecolor=be, linewidth=0.5))
    # Label left
    ax.text(bar_x_start - 0.50, by + bar_h_each/2, f'$d$={lbl}',
            ha='left', va='center', fontsize=5.8, color=dark_text)
    # Probability value right of filled bar
    if prob >= 0.10:
        ax.text(bar_x_start + filled_w + 0.06, by + bar_h_each/2,
                f'{prob:.0%}', ha='left', va='center', fontsize=5.5,
                color=dark_text, fontweight='bold')

# Ellipsis between d=2 and d=K
ellipsis_y = bar_y_top - 3 * (bar_h_each + bar_gap) - ellipsis_gap / 2
ax.text(bar_x_start + 0.3, ellipsis_y, r'$\vdots$',
        ha='center', va='center', fontsize=7, color=gray_text)

# Predicted label below bars
pred_y = bar_y_top - 3 * (bar_h_each + bar_gap) - ellipsis_gap - bar_h_each - 0.28
ax.text(bar_x_start + bar_w_total / 2, pred_y,
        r'$\hat{d} = 1$', ha='center', va='center', fontsize=9.5,
        color='#E67E22', fontweight='bold')

# === BOTTOM: comparison tagline ===
comp_y = 0.0
ax.text(2.2, comp_y, 'Binary:  real vs. synthetic',
        ha='center', va='center', fontsize=7.5, color='#BDC3C7', style='italic')
ax.plot([4.3, 4.3], [comp_y - 0.12, comp_y + 0.12],
        color='#D5D8DC', lw=0.7)
ax.text(7.8, comp_y, r'Ours:  $\hat{d} \in \{0, 1, \ldots, K\}$  (ordinal depth estimation)',
        ha='center', va='center', fontsize=7.5, color='#2980B9', fontweight='bold')

out_dir = '/home/ubuntu/.agent-ml-research-idea_gen_0513_2/projects/recursive_gen_depth_est/docs/paper/figures'
fig.savefig(f'{out_dir}/fig_problem_illustration.pdf')
fig.savefig(f'{out_dir}/fig_problem_illustration.png')
plt.close(fig)
print('Done: fig_problem_illustration.pdf + .png')
