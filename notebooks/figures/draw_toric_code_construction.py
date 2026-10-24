"""Draw one arrow convention for Q, P, R1/R2, and the square-lattice PEPS."""
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch, FancyArrowPatch

OUT = Path(__file__).parent
GRAY, BLUE, GREEN, ORANGE = '0.3', '#2878a5', '#27825e', '#bc5a16'
VERTICES = [(x, y) for x in (0, 2, 4) for y in (-2, 0, 2)]
EDGES = ([(x, y) for y in (-2, 0, 2) for x in (1, 3)]
         + [(x, y) for x in (0, 2, 4) for y in (-1, 1)])
GROUPS = {(1, 0): 'A', (3, 0): 'A', (2, 1): 'B', (2, -1): 'B'}


def line(ax, start, end, color=GRAY, arrow=True, interval=(.28, .60), **kwargs):
    """The arrow runs from a negative leg to a positive leg."""
    ax.plot([start[0], end[0]], [start[1], end[1]], color=color, lw=1.4, zorder=1, **kwargs)
    if arrow:
        points = [tuple((1-t)*a+t*b for a,b in zip(start,end)) for t in interval]
        ax.add_patch(FancyArrowPatch(*points, arrowstyle='-|>', mutation_scale=16,
                                    color=color, lw=1.3, shrinkA=0, shrinkB=0, zorder=2))


def node(ax, xy, label, radius=.14, color='white', square=False, fontsize=11):
    x, y = xy
    patch = (Rectangle((x-radius, y-radius), 2*radius, 2*radius,
                       facecolor=color, edgecolor=GRAY, zorder=3)
             if square else Circle(xy, radius, facecolor=color, edgecolor=GRAY, zorder=3))
    ax.add_patch(patch)
    ax.text(x, y, label, ha='center', va='center', fontsize=fontsize,
            color='black' if color == 'white' else 'white', zorder=4)


def physical_leg(ax, xy, label=True, length=.32):
    end = xy[0]+length, xy[1]+length
    # All ket physical legs have positive signature, so their arrows point inward.
    line(ax, end, xy, color=ORANGE, interval=(.18,.48))
    ax.plot(*end, '.', color=ORANGE, ms=3)
    if label:
        ax.text(end[0]+.08, end[1]+.03, '$s$', color=ORANGE, fontsize=11)


fig, ax = plt.subplots(figsize=(8.5, 5.8), constrained_layout=True)
for x,y in EDGES:
    if x % 2:  # Horizontal virtual bonds point right.
        line(ax,(x-1,y),(x,y))
        line(ax,(x,y),(x+1,y))
    else:      # Vertical virtual bonds point down.
        line(ax,(x,y+1),(x,y))
        line(ax,(x,y),(x,y-1))
for x,y in VERTICES:
    for dx,dy in ((0,1),(1,0),(0,-1),(-1,0)):
        if (x+2*dx,y+2*dy) not in VERTICES:
            end=(x+.8*dx,y+.8*dy)
            start,stop=(end,(x,y)) if dx<0 or dy>0 else ((x,y),end)
            line(ax,start,stop)
    node(ax,(x,y),'$Q$',square=True,radius=.16,fontsize=12)
for xy in EDGES:
    physical_leg(ax,xy,length=.38)
    node(ax,xy,'$P$',color=BLUE,radius=.16,fontsize=12)
ax.set(xlim=(-.9,4.9),ylim=(-2.9,2.9),aspect='equal')
ax.set_title('Physical spins on the original edges',fontsize=13)
ax.axis('off')
fig.savefig(OUT/'toric_code_edge_arrows.png',dpi=200)
plt.close(fig)

fig,axes=plt.subplots(1,3,figsize=(10.5,5.8),
                     gridspec_kw={'width_ratios':[1.65,.23,1]},constrained_layout=True)
ax=axes[0]
# Restore the original-lattice embedding. Arrows are computed from the same
# fixed tensor signatures and axis assignments used in the notebook code.
for y in (-2,0,2):
    line(ax,(-.8,y),(4.8,y),color='0.87',arrow=False,linestyle=':')
for x in (0,2,4):
    line(ax,(x,-2.8),(x,2.8),color='0.87',arrow=False,linestyle=':')
for (x,y),label in GROUPS.items():
    color=BLUE if label=='A' else GREEN
    width,height=(1.44,.54) if label=='A' else (.54,1.44)
    ax.add_patch(FancyBboxPatch((x-width/2,y-height/2),width,height,
                               boxstyle='round,pad=.025',edgecolor=color,
                               facecolor='#edf5fa' if label=='A' else '#edf7f2',
                               linestyle='--',lw=1.5,zorder=0))
    textpos=(x,y-.53) if label=='A' else (x+.54,y)
    ax.text(*textpos,f'${label}$',color=color,fontsize=15,ha='center',va='center',
            bbox={'facecolor':'white','edgecolor':'none','pad':.5},zorder=5)

signatures={'R1': (1,1,-1), 'R2': (-1,-1,1), 'P': (1,1,-1)}
for x,y in VERTICES:
    positions={'N':(x,y+.45), 'E':(x+.45,y),
               'S':(x,y-.45), 'W':(x-.45,y)}
    kinds={'N':'R1','E':'R1','S':'R2','W':'R2'}
    bonds=[(('N',1),('W',1)), (('N',2),('E',0)),
           (('S',1),('E',1)), (('S',2),('W',0))]
    for first,second in bonds:
        a=signatures[kinds[first[0]]][first[1]]
        b=signatures[kinds[second[0]]][second[1]]
        assert a == -b
        start,end=positions[first[0]],positions[second[0]]
        if a==1:
            start,end=end,start
        line(ax,start,end)
    # External (Q) axes are U+, L+, D-, R-.
    for name,axis,dx,dy in (('N',0,0,1), ('W',2,-1,0),
                            ('S',0,0,-1), ('E',2,1,0)):
        inside=(x+2*dx,y+2*dy) in VERTICES
        end=(x+dx*(1 if inside else .8), y+dy*(1 if inside else .8))
        factor=positions[name]
        sign=signatures[kinds[name]][axis]
        if inside:
            p_axis=2 if sign==1 else 1
            assert signatures['P'][p_axis] == -sign
        start,stop=(end,factor) if sign==1 else (factor,end)
        line(ax,start,stop)
    for name,xy in positions.items():
        node(ax,xy,'$R_'+kinds[name][-1]+'$',radius=.15,fontsize=11)
for xy in EDGES:
    physical_leg(ax,xy,label=xy in GROUPS)
    node(ax,xy,'$P$',radius=.16,color=BLUE,fontsize=11)
ax.set(xlim=(-.9,4.9),ylim=(-2.9,2.9),aspect='equal')
ax.set_title('Decompose Q and group the edge spins into A and B',fontsize=12)
ax.axis('off')

axes[1].text(.5,.55,r'$\longrightarrow$',ha='center',va='center',fontsize=25,transform=axes[1].transAxes)
axes[1].text(.5,.43,'contract\nand rotate',ha='center',va='center',fontsize=10,transform=axes[1].transAxes)
axes[1].axis('off')

ax=axes[2]
for y in (0,-2):
    for start,end in (((-.65,y),(0,y)),((0,y),(2,y)),((2,y),(2.65,y))):
        line(ax,start,end)
for x in (0,2):
    for start,end in (((x,.65),(x,0)),((x,0),(x,-2)),((x,-2),(x,-2.65))):
        line(ax,start,end)
for x,y,label in ((0,0,'A'),(2,0,'B'),(0,-2,'B'),(2,-2,'A')):
    physical_leg(ax,(x,y),length=.4)
    node(ax,(x,y),f'${label}$',radius=.23,color=BLUE if label=='A' else GREEN,fontsize=16)
ax.text(1,-2.95,r'$2\times2$ unit cell',ha='center',va='center',fontsize=12)
ax.set(xlim=(-.9,2.9),ylim=(-3.2,1),aspect='equal')
ax.set_title('Square-lattice PEPS',fontsize=12)
ax.axis('off')
fig.savefig(OUT/'toric_code_embedded_R1_R2.png',dpi=220)
plt.close(fig)
