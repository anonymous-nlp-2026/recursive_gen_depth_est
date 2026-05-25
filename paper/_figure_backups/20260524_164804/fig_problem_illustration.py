import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif', 'serif'],
    'mathtext.fontset': 'cm',
    'font.size': 9,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.04,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
})

C = {
    'd0_bg': '#DCE4EC', 'd0_bd': '#8BA0B4',
    'd1_bg': '#F2E4D2', 'd1_bd': '#C4A47A',
    'd2_bg': '#EACEA8', 'd2_bd': '#AD8A56',
    'dk_bg': '#D8B07A', 'dk_bd': '#8E6A3A',
    'arrow':  '#9AA4AE',
    'main':   '#2C3E50',
    'sub':    '#6B7B8D',
    'red':    '#B05A3A',
    'cls_bg': '#EDF2F7', 'cls_bd': '#8BA0B4',
    'accent': '#B87840',
    'binary': '#9EAAB4',
    'ours_bg':'#EEF2F6', 'ours_bd':'#BCC8D4',
}

W, H = 7.0, 2.45
fig = plt.figure(figsize=(W, H))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(-0.05, H)
ax.axis('off')

def rbox(ax, x, y, w, h, bg, bd, lw=0.7, zorder=3, shadow=True):
    if shadow:
        for dx, dy, a in [(0.015, -0.015, 0.04), (0.025, -0.025, 0.02)]:
            ax.add_patch(FancyBboxPatch(
                (x+dx, y+dy), w, h,
                boxstyle='round,pad=0.03,rounding_size=0.05',
                fc='#000000', ec='none', alpha=a, zorder=zorder-2))
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h,
        boxstyle='round,pad=0.03,rounding_size=0.05',
        fc=bg, ec=bd, lw=lw, zorder=zorder))

def doc_icon(ax, cx, cy, s=0.09, c='#6B7B8D', zorder=5):
    px = [cx-s, cx-s, cx+s*0.5, cx+s, cx+s, cx-s]
    py = [cy-s*1.15, cy+s*1.15, cy+s*1.15, cy+s*0.65, cy-s*1.15, cy-s*1.15]
    ax.fill(px, py, fc='white', ec=c, lw=0.5, zorder=zorder)
    fx = [cx+s*0.5, cx+s*0.5, cx+s]
    fy = [cy+s*1.15, cy+s*0.65, cy+s*0.65]
    ax.fill(fx, fy, fc='#E8ECF0', ec=c, lw=0.4, zorder=zorder+1)
    for frac in [0.45, 0.12, -0.21, -0.54]:
        lw_l = s * (1.15 if frac > 0.3 else (0.95 if frac > -0.3 else 0.55))
        ax.plot([cx-s*0.55, cx-s*0.55+lw_l], [cy+s*frac]*2,
                c=c, lw=0.4, alpha=0.45, zorder=zorder+1)

def thin_arrow(ax, xy1, xy2, **kw):
    defaults = dict(arrowstyle='->', color=C['arrow'], lw=0.8,
                    mutation_scale=8, zorder=4)
    defaults.update(kw)
    ax.add_patch(FancyArrowPatch(xy1, xy2, **defaults))

# ═══════════════════════════════════════
# Section 1 — Recursive Generation Chain
# ═══════════════════════════════════════
ax.add_patch(FancyBboxPatch(
    (0.18, 1.22), 6.64, 0.82,
    boxstyle='round,pad=0.02,rounding_size=0.05',
    fc='#F7F8FA', ec='#E4E8EC', lw=0.4, zorder=1))

ax.text(3.50, 2.10, 'Recursive Generation Chain',
        fontsize=10, fontweight='bold', color=C['main'], ha='center')

bw, bh = 0.72, 0.58
by = 1.30
nodes = [
    (0.52,  r'$\mathcal{D}_0$', 'Human',  C['d0_bg'], C['d0_bd']),
    (1.74,  r'$\mathcal{D}_1$', 'Gen-1',  C['d1_bg'], C['d1_bd']),
    (2.96,  r'$\mathcal{D}_2$', 'Gen-2',  C['d2_bg'], C['d2_bd']),
    (5.58,  r'$\mathcal{D}_K$', r'Gen-$K$', C['dk_bg'], C['dk_bd']),
]

for nx, lab, sub, bg, bd in nodes:
    rbox(ax, nx, by, bw, bh, bg, bd, lw=0.8)
    doc_icon(ax, nx+bw/2, by+bh*0.66, s=0.10, c=bd)
    ax.text(nx+bw/2, by+bh*0.24, lab, fontsize=10, fontweight='bold',
            color=C['main'], ha='center', va='center', zorder=6)
    ax.text(nx+bw/2, by+bh*0.04, sub, fontsize=6, color=C['sub'],
            ha='center', va='center', zorder=6)

ay = by + bh/2
for i in range(2):
    x1 = nodes[i][0] + bw + 0.04
    x2 = nodes[i+1][0] - 0.04
    thin_arrow(ax, (x1, ay), (x2, ay))
    ax.text((x1+x2)/2, ay+0.10, 'LoRA ft + sample',
            fontsize=5.5, color=C['sub'], fontstyle='italic',
            ha='center', va='bottom', zorder=6)

thin_arrow(ax, (4.80, ay), (nodes[3][0]-0.04, ay))
ax.text((4.80+nodes[3][0]-0.04)/2, ay+0.10, 'LoRA ft + sample',
        fontsize=5.5, color=C['sub'], fontstyle='italic',
        ha='center', va='bottom', zorder=6)

ax.text(4.45, ay, '· · ·', fontsize=10, color=C['sub'],
        ha='center', va='center', zorder=6)

# ═══════════════════════════════════════
# Section 2 — Depth Estimation Query
# ═══════════════════════════════════════
qy = 0.55

ax.annotate('', xy=(0.88, qy+0.20), xytext=(0.88, by-0.02),
            arrowprops=dict(arrowstyle='->', color=C['arrow'],
                            ls='dashed', lw=0.6, mutation_scale=7), zorder=4)

doc_icon(ax, 0.70, qy+0.03, s=0.11, c=C['d1_bd'], zorder=5)
ax.text(0.70, qy-0.20, r'Text passage $\mathbf{x}$',
        fontsize=7.5, color=C['main'], ha='center', zorder=6)
ax.text(0.70, qy-0.32, r'depth $\mathbf{d}$ = ?',
        fontsize=7, color=C['red'], fontstyle='italic', ha='center', zorder=6)

thin_arrow(ax, (1.15, qy), (1.95, qy))

cw, ch = 1.10, 0.38
cx = 1.98
rbox(ax, cx, qy-ch/2, cw, ch, C['cls_bg'], C['cls_bd'], lw=0.7)
ax.text(cx+cw/2, qy+0.05, 'Depth Classifier',
        fontsize=8, fontweight='bold', color=C['main'], ha='center', zorder=6)
ax.text(cx+cw/2, qy-0.08, '(Statistical Features + RF)',
        fontsize=6, color=C['sub'], ha='center', zorder=6)

thin_arrow(ax, (cx+cw+0.03, qy), (3.80, qy), arrowstyle='-|>')

# ── Bar chart ──
bx0 = 3.88
bw_total = 2.55
bh_max = 0.52
b_base = qy - 0.22

ax.text(bx0+bw_total/2, qy+0.36, 'Estimated Depth Output',
        fontsize=7.5, fontweight='bold', color=C['main'], ha='center', zorder=6)

ax.add_patch(FancyBboxPatch(
    (bx0-0.05, b_base-0.04), bw_total+0.10, bh_max+0.18,
    boxstyle='round,pad=0.02,rounding_size=0.03',
    fc='#FAFBFC', ec='#E4E8EC', lw=0.3, zorder=2))

bars = [
    (r'$d{=}0$', 0.08, '#B4C8DA'),
    (r'$d{=}1$', 0.70, '#DEBB8E'),
    (r'$d{=}2$', 0.15, '#C8A06A'),
    (r'$d{=}K$', 0.04, '#A88050'),
]

sp = bw_total / len(bars)
bwi = sp * 0.50

for i, (lbl, val, col) in enumerate(bars):
    bxi = bx0 + i*sp + (sp-bwi)/2
    h = val * bh_max
    ax.add_patch(FancyBboxPatch(
        (bxi, b_base), bwi, h,
        boxstyle='round,pad=0,rounding_size=0.015',
        fc=col, ec='none', alpha=0.88, zorder=5))
    ax.text(bxi+bwi/2, b_base-0.05, lbl,
            fontsize=6.5, color=C['main'], ha='center', va='top', zorder=6)
    if val >= 0.10:
        ax.text(bxi+bwi/2, b_base+h+0.02, f'{int(val*100)}%',
                fontsize=6.5, fontweight='bold', color=C['main'],
                ha='center', va='bottom', zorder=6)

ax.plot([bx0-0.02, bx0+bw_total+0.02], [b_base, b_base],
        color=C['sub'], lw=0.4, zorder=5)

ax.text(bx0+bw_total/2, b_base-0.22, r'$\hat{d} = 1$',
        fontsize=8.5, fontweight='bold', color=C['accent'], ha='center', zorder=6)

# ═══════════════════════════════════════
# Section 3 — Task Comparison
# ═══════════════════════════════════════
ty = 0.02

ax.text(1.8, ty, 'Binary:  real vs. synthetic',
        fontsize=6.5, color=C['binary'], fontstyle='italic', ha='center', zorder=6)

ax.plot([2.85, 2.85], [ty-0.07, ty+0.07], color='#D0D8E0', lw=0.6, zorder=5)

ax.add_patch(FancyBboxPatch(
    (3.05, ty-0.08), 3.60, 0.16,
    boxstyle='round,pad=0.02,rounding_size=0.03',
    fc=C['ours_bg'], ec=C['ours_bd'], lw=0.4, zorder=3))

ax.text(3.15, ty, r'Ours:  $\hat{d} \in \{0, 1, \ldots, K\}$',
        fontsize=7.5, fontweight='bold', color=C['main'], ha='left', zorder=6)
ax.text(5.05, ty, '(ordinal depth estimation)',
        fontsize=6.5, color=C['sub'], ha='left', zorder=6)

# ── Save ──
out = '/home/ubuntu/.agent-ml-research-idea_gen_0513_2/projects/recursive_gen_depth_est/docs/paper/figures'
fig.savefig(f'{out}/fig_problem_illustration.png', dpi=300, facecolor='white')
fig.savefig(f'{out}/fig_problem_illustration.pdf', facecolor='white')
plt.close()
print('DONE: fig_problem_illustration.png + .pdf')
