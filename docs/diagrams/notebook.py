# Shared "engineering notebook" look for the Bakfiets diagrams.
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
PAPER='#fbf8f1'; GRID='#e7e1d3'; MARGIN='#e8b4b0'
INK='#1d2a44'; PENCIL='#45413a'; RED='#c0392b'; GREEN='#2f7d4f'; BLUE='#2f5fa7'; GOLD='#c98a0b'
HAND='Ink Free'; MONO='Consolas'
def page(w,h,figsize):
    plt.rcParams['path.sketch']=(0.7,45,1.6)
    fig,ax=plt.subplots(figsize=figsize,dpi=150)
    ax.set_xlim(0,w); ax.set_ylim(0,h); ax.axis('off')
    fig.patch.set_facecolor(PAPER); ax.set_facecolor(PAPER)
    with plt.rc_context({'path.sketch':None}):
        for x in range(0,w+1,2): ax.plot([x,x],[0,h],color=GRID,lw=0.5,zorder=0)
        for y in range(0,h+1,2): ax.plot([0,w],[y,y],color=GRID,lw=0.5,zorder=0)
        ax.plot([5,5],[0,h],color=MARGIN,lw=1.2,zorder=0)
    return fig,ax
def note(ax,x,y,s,size=11,color=INK,**kw):
    if size < 11: size = round(size * 1.15, 1)
    kw.setdefault('va','center'); return ax.text(x,y,s,fontsize=size,color=color,family=HAND,**kw)
def mono(ax,x,y,s,size=9,color=INK,**kw):
    if size < 9: size = round(size * 1.12, 1)
    kw.setdefault('va','center'); return ax.text(x,y,s,fontsize=size,color=color,family=MONO,**kw)
def point(ax,text_xy,target,s,size=10.5,color=PENCIL,rad=0.3,**kw):
    if size < 11: size = round(size * 1.15, 1)
    ax.annotate(s,xy=target,xytext=text_xy,fontsize=size,color=color,family=HAND,
        arrowprops=dict(arrowstyle='->',color=color,lw=1.3,connectionstyle=f'arc3,rad={rad}',shrinkA=4,shrinkB=3,relpos=kw.pop('relpos',(0.5,0.5))),**kw)
def save(fig,name):
    fig.savefig(name,bbox_inches='tight',facecolor=PAPER); print('saved',name)
