"""Optimist SVG primitives, measured layout checks, and deterministic Inter export."""
from pathlib import Path
from functools import lru_cache
import html, math, re, json, subprocess, os
from PIL import ImageFont

W,H=1600,900
L,R,CLEAR=50,1550,12
BG,SUR,BOR,INK,BLK='#D8DEF1','#FFFFFF','#C3CBE8','#141A2E','#000000'
PRI,DARK,LIGHT,AMB='#5B5BD6','#37418C','#8FA6E8','#E8A63C'
TINT,AMBT='#F3F5FC','#FFF6E6'
PALETTE=dict(bg=BG,sur=SUR,bor=BOR,ink=INK,blk=BLK,pri=PRI,dark=DARK,light=LIGHT,amb=AMB,tint=TINT,ambt=AMBT,
 series=[PRI,DARK,LIGHT,'#6FBFA6','#4E86C4','#B27BB0'],
 scale=dict(zip(range(50,51),['#EEEEFC'])),
 semantic=dict(success='#4FA98C',warning='#E0A85B',error='#D06A6A',info='#4E86C4'),
 ink700='#3A4056',slate='#838AA0',divider='#E7EAF3',bg_light='#E7EBF7',muted=BLK)
PALETTE['scale']={50:'#EEEEFC',100:'#DEDFF8',200:'#C0C1F1',300:'#9EA0EA',400:'#7B7BE1',500:PRI,600:'#4A48B6',700:'#393893',800:'#2B2B6E',900:'#1D1D49'}
NAVY = {
    'background': '#151D27', 'text': '#F0F3F6', 'secondary': '#B6C1CE',
    'muted': '#91A0B1', 'grid': '#2C3744', 'baseline': '#506071',
    'historical': '#668097', 'exception': '#C6A571', 'focus': '#55CBB6',
    'event_band': '#20242A',
    'surface': '#20242A', 'heading': '#F0F3F6',
}
WHITE = {
    'background': BG, 'text': BLK, 'secondary': BLK, 'muted': BLK,
    'grid': BOR, 'baseline': '#C6CDD1', 'historical': DARK, 'exception': AMB,
    'focus': PRI, 'event_band': AMBT, 'surface': SUR, 'heading': INK,
}
PALETTES = {'white': WHITE, 'navy': NAVY}
# Preserve imports used by earlier figure generators.
DARK_ARTICLE = NAVY

def palette_name(name):
    name = name.strip().lower()
    name = {'dark': 'navy', 'dark-article': 'navy', 'light': 'white',
            'lavender': 'white', 'standard': 'white'}.get(name, name)
    if name not in PALETTES:
        raise ValueError(f'Unknown palette {name!r}; choose "navy" or "white".')
    return name

ASSETS=Path(__file__).resolve().parents[1]/'assets'
FONT_FILES={400:ASSETS/'fonts/Inter-Regular.otf',600:ASSETS/'fonts/Inter-SemiBold.otf',700:ASSETS/'fonts/Inter-Bold.otf'}

def snap(w):return min(FONT_FILES,key=lambda n:abs(n-w))
@lru_cache(maxsize=256)
def font(size,w=400):return ImageFont.truetype(str(FONT_FILES[snap(w)]),round(size*4))
def measure(text,size,weight=400):
    b=font(size,weight).getbbox(str(text))
    return (b[2]-b[0])/4,(b[3]-b[1])/4
@lru_cache(maxsize=2)
def mark(name):
    return re.search(r'\bd="([^"]+)"',(ASSETS/name).read_text()).group(1)

class Fig:
    def __init__(self,palette='white'):
        self.palette_name=palette_name(palette)
        self.colors=PALETTES[self.palette_name].copy()
        self.el=[];self.box=[]
        self.rect(0,0,W,H,self.colors['background'])
    def add(self,s):self.el.append(s)
    def reg(self,x0,y0,x1,y1,name,grp=None):
        self.box.append((x0,y0,x1,y1,name,grp or name))
    def rect(self,x,y,w,h,fill,r=0,stroke=None,sw=1.5,track=None,grp=None):
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke or "none"}" stroke-width="{sw}"/>')
        if track:self.reg(x,y,x+w,y+h,track,grp)
    def line(self,x1,y1,x2,y2,col=None,sw=1.5,dash=None,track=None,grp=None):
        col=self.colors['grid'] if col is None else col
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{sw}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
        if track:self.reg(min(x1,x2)-sw/2,min(y1,y2)-sw/2,max(x1,x2)+sw/2,max(y1,y2)+sw/2,track,grp)
    def arrow(self,x1,y1,x2,y2,col=None,sw=3,head=10,track=None,grp=None):
        col=self.colors['focus'] if col is None else col
        a=math.atan2(y2-y1,x2-x1);u=(math.cos(a),math.sin(a));v=(-u[1],u[0])
        self.line(x1,y1,x2-u[0]*head,y2-u[1]*head,col,sw)
        pts=[(x2,y2),(x2-u[0]*1.8*head+v[0]*.85*head,y2-u[1]*1.8*head+v[1]*.85*head),(x2-u[0]*1.8*head-v[0]*.85*head,y2-u[1]*1.8*head-v[1]*.85*head)]
        self.add('<polygon points="'+' '.join(f'{x},{y}' for x,y in pts)+f'" fill="{col}"/>')
        if track:self.sample_arrow(x1,y1,x2,y2,track,grp,grp)
    def node(self,cx,cy,r=34,fill=None,stroke=None,sw=1.5,track=None,grp=None):
        fill=self.colors['focus'] if fill is None else fill
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke or "none"}" stroke-width="{sw}"/>')
        if track:self.reg(cx-r,cy-r,cx+r,cy+r,track,grp)
    def arc_arrow(self,cx,cy,R,a0,a1,color=None,sw=6,head=True):
        color=self.colors['focus'] if color is None else color
        a,b=map(math.radians,(a0,a1));x0,y0=cx+R*math.sin(a),cy-R*math.cos(a);x1,y1=cx+R*math.sin(b),cy-R*math.cos(b)
        self.add(f'<path d="M{x0},{y0} A{R},{R} 0 {int((a1-a0)%360>180)} 1 {x1},{y1}" fill="none" stroke="{color}" stroke-width="{sw}"/>')
        if head:
            u=(math.cos(b),math.sin(b));v=(-math.sin(b),math.cos(b))
            pts=[(x1,y1),(x1-u[0]*14+v[0]*7.5,y1-u[1]*14+v[1]*7.5),(x1-u[0]*14-v[0]*7.5,y1-u[1]*14-v[1]*7.5)]
            self.add('<polygon points="'+' '.join(f'{x},{y}' for x,y in pts)+f'" fill="{color}"/>')
    def text(self,x,y,t,size=14,w=400,fill=None,anchor='start',extra='',track=True,name=None,grp=None):
        fill=self.colors['text'] if fill is None else fill
        self.add(f'<text x="{x}" y="{y}" font-family="Inter" font-size="{size}" font-weight="{snap(w)}" fill="{fill}" text-anchor="{anchor}" {extra}>{html.escape(str(t))}</text>')
        if track:
            width,height=measure(t,size,w);x0=x-width*({'start':0,'middle':.5,'end':1}[anchor])
            self.reg(x0,y-height,x0+width,y+size*.25,name or str(t),grp)
    def lead(self,x,y,head,rest,size=15,grp=None,anchor='start',name=None):
        gap=size*.28 if rest.startswith(' ') else 0;rest=rest.lstrip(' ')
        hw,hh=measure(head,size,700);rw,rh=measure(rest,size,400);width=hw+gap+rw
        x0=x-width*({'start':0,'middle':.5,'end':1}[anchor])
        self.text(x0,y,head,size,700,self.colors['focus'],track=False);self.text(x0+hw+gap,y,rest,size,400,track=False)
        self.reg(x0,y-max(hh,rh),x0+width,y+size*.25,name or head[:24],grp)
    def container(self,x,y,w,h,name,fill=None,**kw):
        fill=self.colors['surface'] if fill is None else fill
        self.rect(x,y,w,h,fill,track='__box__'+name,grp=name,**kw)
    def sample_arrow(self,x1,y1,x2,y2,name,src=None,dst=None,n=9):
        for i in range(n):
            t=i/(n-1);x=x1+t*(x2-x1);y=y1+t*(y2-y1)
            self.reg(x-2,y-2,x+2,y+2,f'{name}:{i}',src if i<2 else dst if i>=n-2 else name)
    def header(self,title,sub):
        navy=self.palette_name=='navy';c=self.colors
        self.add(f'<path d="{mark("optimist-o-mark.svg")}" transform="translate(19 35) scale(.56)" fill="{c["heading"]}"/>')
        self.reg(19,35,103,119,'O','header')
        self.text(127,65,title,40 if navy else 42,600 if navy else 700,c['heading'],grp='header')
        self.text(127,112,sub,22 if navy else 24,400,c['secondary'],grp='header')
    def footer(self,asof,source,note):
        navy=self.palette_name=='navy';c=self.colors
        if navy:
            self.line(L,810,R,810,c['grid'],1)
            rows=[836,858,880];weight=600;logo=(1380,828,170,54.2)
        else:
            self.add('<line x1="50" y1="808" x2="1550" y2="808" stroke="#C6CDD1" stroke-opacity=".6" stroke-width="1.5"/>')
            rows=[835,857,879];weight=700;logo=(1315,815,240,77)
        for y,label,value in zip(rows,['Data as of:','Source:','Note:'],[asof,source,note]):
            lw,_=measure(label,12,weight)
            self.text(L,y,label,12,weight,c['secondary'],grp='footer')
            self.text(L+lw+5,y,value,12,fill=c['muted'],grp='footer')
            if L+lw+5+measure(value,12)[0]>logo[0]-25:raise ValueError('Footer row reaches the logo; shorten the text.')
        x,y,w,h=logo
        self.add(f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="0 0 240 76.5"><path d="{mark("optimist-logo.svg")}" fill="{c["heading"]}"/></svg>')
        self.reg(x,y,x+w,y+h,'lockup','footer')
    def check(self):
        problems=[]
        for i,a in enumerate(self.box):
            if a[0]<0 or a[1]<0 or a[2]>W or a[3]>H:problems.append((-999,a[4],'canvas'))
            for b in self.box[i+1:]:
                if a[5]==b[5]:continue
                ox=min(a[2],b[2])-max(a[0],b[0]);oy=min(a[3],b[3])-max(a[1],b[1])
                if ox>-CLEAR and oy>-CLEAR:problems.append((min(-ox,-oy),a[4],b[4]))
        print(f'Clearance: {len(self.box)} tracked; '+('clear' if not problems else str(sorted(problems)[:15])))
        return not problems
    def check_containment(self,pad=12):
        containers=[b for b in self.box if b[4].startswith('__box__')];problems=[]
        for b in self.box:
            if b[4].startswith('__box__'):continue
            # Group ownership catches overflow even if the label centre leaves its box.
            matches=[c for c in containers if c[5]==b[5]]
            if not matches:
                matches=[c for c in containers if c[0]<(b[0]+b[2])/2<c[2] and c[1]<(b[1]+b[3])/2<c[3]]
            if not matches:continue
            c=min(matches,key=lambda c:(c[2]-c[0])*(c[3]-c[1]))
            pads=dict(left=b[0]-c[0],top=b[1]-c[1],right=c[2]-b[2],bottom=c[3]-b[3]);side=min(pads,key=pads.get)
            if pads[side]<pad:problems.append((b[4],side,round(pads[side],2)))
        print('Containment: '+('clear' if not problems else str(problems)))
        return not problems
    def save(self,path):
        path=Path(path).with_suffix('.svg');path.parent.mkdir(parents=True,exist_ok=True)
        svg='<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">'+''.join(self.el)+'</svg>'
        path.write_text(svg)
        try:
            import resvg_py
            png=resvg_py.svg_to_bytes(svg_string=svg,width=3200,height=1800,font_files=[str(f) for f in FONT_FILES.values()],skip_system_fonts=True)
            path.with_suffix('.png').write_bytes(png)
        except ImportError:
            # CairoSVG requires installed Inter; resvg-py loads the packaged fonts directly.
            import cairosvg
            cairosvg.svg2png(bytestring=svg.encode(),write_to=str(path.with_suffix('.png')),output_width=3200,output_height=1800)
        path.with_suffix('.layout.json').write_text(json.dumps(self.box,indent=2))

if __name__=='__main__':
    f=Fig();f.header('Toolkit test','header, container, both checks')
    f.container(50,200,700,180,'card',r=10,stroke=BOR,sw=2)
    f.text(400,300,'centred inside its container',21,anchor='middle',grp='card')
    f.container(820,200,300,180,'tight',r=10,stroke=BOR,sw=2)
    f.text(970,300,'a line far too long for this narrow box',21,anchor='middle',grp='tight')
    f.footer('Sep. 6, 2026','self-test','Checks behave independently.')
    assert f.check()
    assert not f.check_containment()
    print('Self-test passed: intentional containment failure detected.')
