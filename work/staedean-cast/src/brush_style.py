"""Still-frame brush study: opaque paper reserves beneath overlapping washes.

Brush shapes live in normalized shape coordinates, so the pattern follows each
puppet part. This avoids cutting holes through the character into the background.
"""
import re,colorsys
from rig import W,H,defs
from wash_style import PALETTE,lighten

def brush_pattern(ident,col,bounds=None):
    rgb=[int(col[i:i+2],16)/255 for i in (1,3,5)]
    hue,sat,val=colorsys.rgb_to_hsv(*rgb)
    # Skin and near-white objects need much quieter reserves than clothing.
    skin=.045<hue<.13 and val>.8 and sat<.42
    pale=skin or sat<.12 or min(rgb)>.8
    if bounds:
        x,y,w,h=bounds
        attributes=f'patternUnits="userSpaceOnUse" x="{x}" y="{y}" width="{w}" height="{h}" viewBox="0 0 1 1" preserveAspectRatio="none"'
    else:
        attributes='patternUnits="objectBoundingBox" width="1" height="1" viewBox="0 0 1 1" preserveAspectRatio="none"'
    base=lighten(col,.5 if skin else .8) if pale else '#ffffff'
    # Broad, asymmetric brush footprints, with deliberate paper left at the
    # edges and between strokes. Overlaps deepen colour without bevel shading.
    strokes=(
        f'<path d="M .04,-.06 Q .34,.01 .55,-.04 L .89,.06 .95,.27 .83,.43 .96,.63 .91,1.08 .48,1.06 .07,.96 .12,.74 .02,.55 .09,.32 .01,.17 Z" fill="{lighten(col,.3)}"/>',
        f'<path d="M .43,-.08 L 1.06,-.02 1.03,.26 .93,.35 1.06,.53 1.01,1.06 .66,1.04 .72,.83 .59,.69 .66,.49 .53,.28 Z" fill="{col}" opacity=".76"/>',
        f'<path d="M -.04,.49 L .07,.43 .15,.58 .21,.69 .18,.88 .31,1.07 -.05,1.05 Z" fill="{lighten(col,.12)}" opacity=".84"/>',
        f'<path d="M .36,.57 Q .48,.47 .61,.55 L .72,.76 .65,.94 .78,1.04 .35,1.07 .42,.86 .32,.73 Z" fill="{col}" opacity=".3"/>',
    )
    # A narrow, broken dry-brush skip is distinct from an evenly lit highlight.
    skips='' if pale else '<path d="M .13,.06 L .18,.12 .15,.25 .19,.34 .17,.46 .13,.41 .14,.3 .1,.23 Z M .31,.81 L .34,.86 .3,.95 .33,1.04 .27,1.03 .28,.92 Z" fill="#ffffff" opacity=".9"/>'
    return f'<pattern id="{ident}" {attributes}><rect width="1" height="1" fill="{base}"/><g filter="url(#brush-edge)" opacity="{.38 if pale else 1}">{"".join(strokes)}{skips}</g></pattern>'

def wrap(art,view,seed,brand_map):
    vb=view or (0,0,W,H);z=W/vb[2]
    def recolour(m):
        col=brand_map.get(m.group(2).lower(),m.group(2)).lower()
        return f'{m.group(1)}="{PALETTE.get(col,col)}"'
    art=re.sub(r'(fill|stroke|stop-color)="(#[0-9a-fA-F]{6})"',recolour,art)
    art=art.replace('fill="url(#skyG)"','fill="#ffffff"')
    patterns=[]
    def paint(m):
        tag=m.group(0)
        fill=re.search(r'fill="(#[0-9a-fA-F]{6})"',tag)
        if fill and 'filter="url(#wc)"' in tag:
            col=fill.group(1);ident=f'brush{len(patterns)}'
            patterns.append(brush_pattern(ident,col))
            return tag.replace(fill.group(0),f'fill="url(#{ident})"').replace('filter="url(#wc)"','')
        stroke=re.search(r'stroke="(#[0-9a-fA-F]{6})"',tag)
        width=re.search(r'stroke-width="([0-9.]+)"',tag)
        if not stroke or not width or float(width.group(1))<=14:return tag
        col=stroke.group(1).lower();w=float(width.group(1))
        if col in ('#1f1a17','#2e2520'):
            return tag.replace(width.group(0),f'stroke-width="{w-3}"')
        # Tube limbs are polylines. Explicit user-space bounds include their
        # rounded caps, including vertical legs whose path bounds have no width.
        path=re.search(r'd="([^"]+)"',tag)
        if not path:return tag
        nums=[float(x) for x in re.findall(r'-?\d+(?:\.\d+)?',path.group(1))]
        xs,ys=nums[::2],nums[1::2]
        if not xs or len(xs)!=len(ys):return tag
        bounds=(min(xs)-w/2,min(ys)-w/2,max(xs)-min(xs)+w,max(ys)-min(ys)+w)
        ident=f'brush{len(patterns)}';patterns.append(brush_pattern(ident,col,bounds))
        return tag.replace(stroke.group(0),f'stroke="url(#{ident})"')
    art=re.sub(r'<path\b[^>]*>',paint,art)
    art=re.sub(r'stroke-width="([0-9.]+)"',lambda m:f'stroke-width="{float(m.group(1))*(.65 if float(m.group(1))<14 else 1):.2f}"',art)
    # Pattern coordinates are normalized to 0..1. Soft pigment edges and
    # seeded displacement break the vector geometry without blurring the ink.
    edge_filter='''<filter id="brush-edge" filterUnits="userSpaceOnUse" x="-.2" y="-.2" width="1.4" height="1.4" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="12 20" numOctaves="3" seed="23" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale=".045" xChannelSelector="R" yChannelSelector="G"/>
      <feGaussianBlur stdDeviation=".009"/>
    </filter>'''
    base=defs(seed,z).replace(f'scale="{5/z:.3f}"',f'scale="{3/z:.3f}"')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="{" ".join(map(str,vb))}">'
        +base+'<defs>'+edge_filter+''.join(patterns)+'</defs><rect x="-1000" y="-1000" width="5000" height="4000" fill="white"/>'
        +f'<g filter="url(#wobble)">{art}</g></svg>')
