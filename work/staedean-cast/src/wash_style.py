"""Optional ink-and-wash colour study, preserving the existing SVG puppets.

Unlike the marker treatment, this leaves backgrounds nearly white and keeps
colour concentrated in clothing and props. Stable pigment noise avoids flicker.
Select with MS_STYLE=wash; marker remains the default for the existing film.
"""
import re, colorsys
from rig import W,H,defs

# These are art-direction choices, not changes to the underlying character rigs.
PALETTE={
    '#c3e2f4':'#d7edf4', '#a3cbe6':'#9fcddd',
    '#f7d3b4':'#f9dfc4', '#f4c3a3':'#f2c5a9', '#f0cdb0':'#f7d9b7',
    '#1f2342':'#222c64', '#00316c':'#154a96',
    '#8c5630':'#78432c', '#b5523b':'#d83246', '#9a4330':'#ad2037',
    '#fa5a4f':'#df2643', '#17c8be':'#04acb3',
    '#f5e9d2':'#fffefa', '#ead8b6':'#f7f3e6',
    '#c4ece8':'#ffffff', '#fdf1e2':'#ffffff',
    '#b3d9a8':'#edf4e4', '#97c486':'#b3d28c',
    '#aebccb':'#e7eef2', '#8e9fb2':'#c9dbe5', '#c4d0dc':'#edf3f7',
    '#d9cdb5':'#fcfaf3', '#d7ba94':'#ded9c7',
    '#e8dcc2':'#fcfaf3', '#cdb790':'#dce5dc',
}

def lighten(col,amount):
    rgb=[int(col[i:i+2],16) for i in (1,3,5)]
    return '#'+''.join(f'{round(v+(255-v)*amount):02x}' for v in rgb)

def wrap(art,view,seed,brand_map):
    vb=view or (0,0,W,H);z=W/vb[2]
    def recolour(m):
        col=brand_map.get(m.group(2).lower(),m.group(2)).lower()
        return f'{m.group(1)}="{PALETTE.get(col,col)}"'
    art=re.sub(r'(fill|stroke|stop-color)="(#[0-9a-fA-F]{6})"',recolour,art)
    art=art.replace('fill="url(#skyG)"','fill="#ffffff"')
    art=art.replace('filter="url(#wc)"','filter="url(#pigment)"')
    gradients={}
    def paint(m):
        tag=m.group(0)
        colour=re.search(r'fill="(#[0-9a-fA-F]{6})"',tag)
        if not colour or 'url(#pigment)' not in tag:return tag
        col=colour.group(1).lower()
        ident='wash'+col[1:]
        # Broad translucent highlights, with deep colour over most of the shape.
        gradients[ident]=(col,lighten(col,.64),lighten(col,.18))
        return tag.replace(f'fill="{col}"',f'fill="url(#{ident})"')
    art=re.sub(r'<path\b[^>]*>',paint,art)
    def paint_limb(m):
        tag=m.group(0)
        stroke=re.search(r'stroke="(#[0-9a-fA-F]{6})"',tag)
        width=re.search(r'stroke-width="([0-9.]+)"',tag)
        if not stroke or not width or float(width.group(1))<=14:return tag
        col=stroke.group(1).lower()
        if col in ('#1f1a17','#2e2520'):
            return tag.replace(width.group(0),f'stroke-width="{float(width.group(1))-2.5}"')
        # Stroke-only limbs can have zero-width bounds; object-box gradients
        # and filters would clip their rounded ends. Use the body's midtone.
        return tag.replace(stroke.group(0),f'stroke="{lighten(col,.18)}"')
    art=re.sub(r'<path\b[^>]*>',paint_limb,art)
    # Keep the contour fine and continuous. Thick strokes are limb fills or
    # their outlines, so preserve their paired widths rather than thinning limbs.
    art=re.sub(r'stroke-width="([0-9.]+)"',lambda m:f'stroke-width="{float(m.group(1))*(.7 if float(m.group(1))<14 else 1):.2f}"',art)
    grad=''.join(f'<radialGradient id="{ident}" cx="28%" cy="22%" r="85%"><stop offset="0" stop-color="{hi}"/><stop offset=".32" stop-color="{mid}"/><stop offset=".85" stop-color="{col}"/></radialGradient>' for ident,(col,hi,mid) in gradients.items())
    pigment=f'''<filter id="pigment" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency=".012 .018" numOctaves="2" seed="17" result="noise"/>
      <feColorMatrix in="noise" type="matrix" values="0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 .16 .16 .16 0 -.08" result="bloom"/>
      <feComposite in="bloom" in2="SourceAlpha" operator="in" result="clipped"/>
      <feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="clipped"/></feMerge>
    </filter>'''
    base=defs(seed,z).replace(f'scale="{5/z:.3f}"',f'scale="{2.2/z:.3f}"')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="{" ".join(map(str,vb))}">'
        +base+'<defs>'+grad+pigment+'</defs>'
        +'<rect x="-1000" y="-1000" width="5000" height="4000" fill="#ffffff"/>'
        +f'<g filter="url(#wobble)">{art}</g></svg>')
