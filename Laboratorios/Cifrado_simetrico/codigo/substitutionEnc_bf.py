#!/usr/bin/env python3
"""Descifrador interactivo de sustitución simple en castellano, con análisis de bigramas.

1. Al arrancar propone una clave por frecuencia de letras y la afina con bigramas.
   Si el cifrado conserva los espacios los aprovecha: los inicios y finales de palabra
   (por ejemplo la "y" suelta) aportan mucha información para distinguir letras raras.
2. Muévete con las flechas; si tecleas una letra, la letra cifrada bajo el cursor
   pasa a ser esa letra en todo el texto (queda fijada, en verde).
3. Enter vuelve a optimizar con bigramas las letras que NO has fijado.
4. La barra inferior muestra cuánto sube o baja la puntuación con cada cambio.

Uso: python descifrador_bigramas.py cifrado.txt     (Windows: pip install windows-curses)
"""
import curses
import math
import os
import random
import sys
from bisect import bisect_left, bisect_right
from collections import Counter

# Frecuencia (%) de cada letra en castellano
LETRAS = {
    "e": 16.78, "a": 11.96, "o": 8.69, "l": 8.37, "s": 7.88, "n": 7.01, "d": 6.87,
    "r": 4.94, "u": 4.80, "i": 4.15, "t": 3.31, "c": 2.92, "p": 2.776, "m": 2.12,
    "y": 1.54, "q": 1.53, "b": 0.92, "h": 0.89, "g": 0.73, "f": 0.52, "v": 0.39,
    "j": 0.30, "ñ": 0.29, "z": 0.15, "x": 0.06, "k": 0.0, "w": 0.0,
}

# Bigramas del castellano en el Quijote (Parte I), con fronteras de palabra: "_" es el espacio,
# así "_y" = palabra que empieza por y y "y_" = palabra que termina en y. Formato: par + nº de
# apariciones (1 011 169 pares en total). Los pares que no figuran no existen en castellano.
_CUENTAS = """
    e_40006 o_35826 a_35506 s_24482 _d20801 _e19681 ue19489 en17213 de17013 n_16747 es16384
    qu16342 _l15982 _a15252 _s14295 _q13889 er13699 _c13509 _p13027 os12344 la11346 ra11242
    as11007 an10962 do10597 _m10316 _y10207 l_9721 y_9516 on9513 el9449 r_9352 ar8849 se8567
    ta8276 co8001 al7828 or7752 nt7688 _t7601 re7486 te7482 st6934 to6878 ca6813 no6809 _h6792
    ie6740 lo6694 ro6688 le6573 ad6169 po5819 da5768 nd5712 di5692 ia5660 _n5650 ab5581 _v5477
    ma5299 ll4932 me4919 ci4918 sa4764 ha4679 si4669 mo4440 i_4222 un4199 tr4192 in4187 io4059
    pa4013 ba3956 mi3955 ri3859 na3611 su3513 ed3511 ce3364 cu3318 so3244 _r3194 ti3184 ui3072
    om3070 ve3066 ac3023 am3022 ec2970 _o2938 nc2798 _f2729 pe2717 is2693 ch2677 _b2632 jo2616
    id2613 vi2517 ho2455 bi2431 ne2420 ot2336 uc2287 rt2258 ni2227 gu2188 u_2175 ir2108 od2107
    ij2094 br2092 li2067 ga2013 pu1986 ic1975 ol1973 _u1938 du1931 ua1929 go1888 sp1791 pr1765
    us1756 _g1695 ur1685 at1681 vo1669 mu1626 em1612 d_1607 tu1599 eg1559 ig1547 oc1531 za1454
    im1434 be1399 sc1333 yo1306 _i1296 il1270 rd1260 fu1197 ns1164 rm1153 va1147 he1115 _j1092
    zo1091 it1077 ño1072 aq1062 mp1058 ja1051 gr1051 rr1050 ej1040 et1028 eñ1006 ud998 ng956
    pi927 ea918 lu908 cy904 yl904 ww904 au890 ag884 rc842 cr831 bu822 rs820 mb818 iv813 ib800
    rq799 ev796 dr795 ob794 hi787 az783 ya735 fi733 lg727 fa721 vu716 bl716 añ713 rl675 ez674
    je668 ap659 fe658 bo652 ña624 ul623 nu606 nz603 ay592 lt582 ei578 uy573 eb531 av522 rn521
    ub479 sm478 ai466 tt454 ju454 _w453 ht452 tp452 p_452 w_452 jc452 aj448 pl441 ge424 lm422
    gi417 eo405 hu404 z_399 oy382 lv378 ep378 um370 ru364 rb355 ye349 iz344 uv326 fr310 ah309
    oj307 nq297 nf281 ov277 ld276 oz265 oi262 fo258 lc256 og246 rg238 of238 ut230 ey228 ug225
    cl214 op211 nv203 rz199 uj198 ex195 rv189 ae181 sd180 if168 up160 nr158 ef156 ee149 dm143
    ip142 _z137 af132 gn127 sf125 lp122 zc118 xt116 rp104 sn93 oh90 h_88 gl84 lb84 sl83 ct82
    nm82 sg80 ñe79 fl78 uz78 yu78 iq78 iu77 lz75 sv75 eq70 sh69 dv60 nj56 ñi52 nl50 ls48 uf44
    uo44 lq44 rf44 uñ44 ji42 cc41 iñ40 oe40 rj39 lf38 oq38 sq37 zg37 oñ33 xc32 xp31 zu23 uq23
    ao21 eu21 eh20 t_13 pt13 oo13 zq13 zm13 qe11 ix11 ñu10 bs10 xa10 lh9 oa9 dl8 xm7 x_7 sb7
    aa6 m_6 nn6 nh6 dh5 c_5 bj5 xe4 lr4 dq4 ss3 dn3 lj3 ps3 zn3 uh3 zb3 xi2 tc2 ze2 dj2 sr2
    mn2 iy2 ds1 gm1 _k1 ki1 ts1 uu1 zp1 zt1 q_1 ox1 bb1 md1 g_1 ux1 _ñ1 wa1 j_1 _x1 bd1 v_1
    ax1 ln1 cm1 xo1
"""
CUENTAS = {(t[0].replace("_", " "), t[1].replace("_", " ")): int(t[2:]) for t in _CUENTAS.split()}

# Los mismos bigramas SIN fronteras de palabra, para cifrados escritos sin espacios (820 582 pares).
_CONTINUO = """
    es19985 ue19640 en18800 de17104 qu16342 os15248 el14341 er14315 as13571 ra12349 la11896
    an11870 do10613 al10525 on10477 ad10368 se10196 ar9425 nt8655 re8585 ta8276 or8178 co8001
    le7920 st7759 te7485 ie7250 nd7136 no7087 ed7084 to6879 ro6870 lo6840 ca6815 od6686 sa6647
    ab6134 ia6057 da5857 po5819 di5696 ac5676 am5673 ll5304 ma5300 ec5279 me4919 ci4918 si4835
    ne4737 na4706 ha4691 om4493 in4442 mo4440 ol4352 oe4284 ea4260 un4238 tr4192 io4123 ee4082
    pa4013 ba3956 mi3955 ri3905 oq3804 so3728 nc3714 oc3675 sp3673 em3672 su3634 sd3565 ot3528
    aq3520 ce3364 cu3318 sc3292 ti3185 ui3121 ap3088 ve3066 ep3059 is3050 oy3041 oa3013 ae2978
    et2966 ay2936 id2915 at2900 op2776 pe2717 ch2677 jo2616 rt2598 uc2522 vi2517 ho2455 bi2431
    rd2360 ni2339 ns2327 ic2302 sq2283 ua2211 gu2188 ir2176 aa2167 li2158 ij2112 ev2100 br2092
    eh2073 ya2034 ga2013 sy2002 pu1986 nl1943 du1941 nq1926 av1921 us1909 go1888 ey1838 eg1828
    eq1828 ur1773 pr1765 sm1738 lc1714 rl1695 im1686 vo1669 mu1626 il1615 tu1599 rm1592 sl1585
    yl1580 ig1573 za1482 ss1462 rq1455 rc1439 rs1439 yo1434 ye1429 be1399 ah1333 au1331 ag1271
    oh1241 it1241 fu1197 ng1190 rr1170 va1147 ej1140 ud1128 he1117 lm1107 zo1096 ño1072 ob1067
    mp1059 ja1051 gr1051 yd1028 aj1019 eñ1007 np989 eo979 lu974 lt973 iv961 nm940 ld935 pi927
    eb924 cy904 ww904 lg902 ei890 ov886 sh882 ib864 nu858 cr831 dr823 bu822 az819 mb818 sn812
    yc804 hi789 ai782 rn772 sv742 fi733 lv727 ef727 lp726 fa721 vu716 bl716 añ713 ul708 ys708
    ez705 af675 je668 lh667 fe658 bo652 yp645 rp633 ña624 ls624 nz612 of610 nf609 nv606 ao600
    uy580 yq570 ub556 ru520 eu519 um518 sr514 oo480 ny470 ym469 ip468 ry465 ht458 tt454 ju454
    rb454 tp452 pw452 we452 jc452 pl441 yt439 nr435 uv434 ge424 sf420 gi417 oi413 og410 up405
    hu404 lq390 rv382 lb381 oj380 nh378 nn370 sb345 dd344 iz344 yn336 nb330 lr320 fr310 rg302
    ou298 sg297 ut291 oz284 ug281 if281 iq260 fo258 yv254 uj221 lf216 dq214 cl214 yh212 rz203
    ex195 dm195 ly189 yb188 yf186 ln184 dy181 rh163 yr160 ds153 uh150 yu144 zc142 ih134 rf131
    gn128 iy124 nj122 xt116 dp103 yg99 yy99 iu99 sj96 dv92 dl90 uf87 gl84 lj83 ct82 uz81 lz80
    ñe79 fl78 dc73 zd68 uo58 zy56 rj55 ñi52 uq50 dh47 zq47 uñ44 dt43 yj43 ji42 cc41 iñ40 zg37
    dn37 oñ33 xp33 xc32 zl30 zm28 zu27 zs26 ii26 zp25 ze25 sz21 yi19 zh17 zt17 pt13 hs12 zb12
    qe11 ix11 ñu10 bs10 xa10 zn9 df9 hc8 yz7 db7 xm7 hd7 hl7 zr6 xe6 hv6 uu5 bj5 dj5 hh5 hb4
    zv4 tc3 ps3 md3 hf3 hm3 hq3 xi2 tl2 mn2 tq2 dg2 hg2 hj2 ax2 hp1 cp1 hn1 zj1 gm1 nk1 ki1
    ts1 td1 hr1 qm1 ox1 zi1 bb1 cn1 zf1 my1 ux1 xy1 yw1 wa1 ty1 tv1 jq1 xn1 zz1 bd1 mh1 vc1
    xq1 hz1 cm1 xo1 cs1
"""
CONTINUO = {(t[0], t[1]): int(t[2:]) for t in _CONTINUO.split()}
AYUDA = "←↑↓→ mover | letra: fijar | Enter: optimizar | Backspace: deshacer | Esc: salir"


# ---------------------------------------------------------------- análisis
class Modelo:
    """Probabilidad de cada bigrama; puntúa un texto por su log-verosimilitud."""

    def __init__(self, cuentas):
        total = sum(cuentas.values())
        den = total + 0.5 * 28 * 28  # suavizado: un par no visto cuenta como 0,5 apariciones
        self.pct = {g: 100 * n / total for g, n in cuentas.items()}
        self.log = {g: math.log10((n + 0.5) / den) for g, n in cuentas.items()}
        self.suelo = math.log10(0.5 / den)

    def puntuar(self, pares, clave):
        """Más alto = más parecido al castellano. `pares` cuenta los bigramas del cifrado."""
        get, suelo, total = self.log.get, self.suelo, 0.0
        for (a, b), n in pares.items():
            total += n * get((clave[a], clave[b]), suelo)
        return total


def clave_inicial(cuentas):
    """Permutación completa cifrada->llana, emparejando por frecuencia de letras."""
    cifradas = [c for c, _ in cuentas.most_common()] + [c for c in LETRAS if c not in cuentas]
    llanas = sorted(LETRAS, key=LETRAS.get, reverse=True)
    clave = dict(zip(cifradas, llanas))
    clave[" "] = " "  # la frontera de palabra nunca cambia
    return clave


def optimizar(pares, clave, fijas, modelo, reinicios=6):
    """Hill climbing por intercambios entre las letras NO fijadas, con reinicios perturbados."""
    rng, libres = random.Random(0), [c for c in LETRAS if c not in fijas]
    mejor, mejor_p = dict(clave), modelo.puntuar(pares, clave)
    for r in range(reinicios if len(libres) > 1 else 0):
        k = dict(mejor)
        for _ in range(0 if r == 0 else 4):
            a, b = rng.sample(libres, 2)
            k[a], k[b] = k[b], k[a]
        p, mejora = modelo.puntuar(pares, k), True
        while mejora:
            mejora = False
            for i, a in enumerate(libres):
                for b in libres[i + 1:]:
                    k[a], k[b] = k[b], k[a]
                    q = modelo.puntuar(pares, k)
                    if q > p + 1e-9:
                        p, mejora = q, True
                    else:
                        k[a], k[b] = k[b], k[a]
        if p > mejor_p:
            mejor, mejor_p = dict(k), p
    return mejor


def asignar(clave, c, p):
    """La cifrada c pasa a ser p; quien era p recibe lo que tenía c."""
    nueva, otra = dict(clave), next(k for k, v in clave.items() if v == p)
    nueva[otra], nueva[c] = clave[c], p
    return nueva, otra


# ---------------------------------------------------------------- interfaz
def traducir(ch, clave):
    p = clave.get(ch.lower())
    return ch if p is None else (p.upper() if ch.isupper() else p)


def trocear(texto, ancho):
    """Divide el texto en líneas (inicio, fin) respetando saltos de línea y palabras."""
    lineas, ini, n = [], 0, len(texto)
    while True:
        seg = texto[ini:ini + ancho]
        if "\n" in seg:
            fin = ini + seg.index("\n")
            sig = fin + 1
        elif ini + ancho >= n:
            fin = sig = n
        else:
            k = seg.rfind(" ")
            fin = sig = ini + (k + 1 if k > 0 else ancho)
        lineas.append((ini, fin))
        if fin >= n:
            return lineas
        ini = sig


def app(stdscr, texto, pares, cuentas, clave, modelo, con_palabras):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_YELLOW, -1)

    nav = [i for i, ch in enumerate(texto) if ch.lower() in LETRAS]  # posiciones con letra
    fijas, historial = set(), []
    pos, top, lineas, ancho = nav[0], 0, [], 0
    ultima = modelo.puntuar(pares, clave)  # puntuación antes del último cambio
    delta = 0.0

    def linea_de(p):
        return bisect_right([a for a, _ in lineas], p) - 1

    def vertical(d):
        nonlocal pos
        j, col = linea_de(pos) + d, pos - lineas[linea_de(pos)][0]
        while 0 <= j < len(lineas):
            a, b = lineas[j]
            lo, hi = bisect_left(nav, a), bisect_left(nav, b)
            if lo < hi:
                pos = min(nav[lo:hi], key=lambda q: abs(q - (a + col)))
                return
            j += d

    while True:
        h, w = stdscr.getmaxyx()
        if w - 1 != ancho:
            ancho = max(10, w - 1)
            lineas = trocear(texto, ancho)
        alto, li = max(1, h - 3), linea_de(pos)
        top = min(max(top, li - alto + 1), li)  # mantener el cursor visible
        c_cur = texto[pos].lower()
        i = bisect_left(nav, pos)
        punt = modelo.puntuar(pares, clave)
        if abs(punt - ultima) > 1e-9:
            delta = punt - ultima
        ultima = punt

        stdscr.erase()
        try:
            stdscr.addnstr(0, 0, AYUDA, w - 1, curses.A_BOLD)
            for y, (a, b) in enumerate(lineas[top:top + alto]):
                for x, j in enumerate(range(a, b)):
                    c = texto[j].lower()
                    attr = (curses.A_REVERSE if j == pos else
                            curses.color_pair(2) | curses.A_BOLD | curses.A_UNDERLINE if c == c_cur else
                            curses.color_pair(1) if c in fijas else curses.A_NORMAL)
                    stdscr.addstr(y + 1, x, traducir(texto[j], clave), attr)
            n = cuentas[c_cur]
            stdscr.addnstr(h - 2, 0, f"cifrada '{c_cur}' -> '{clave[c_cur]}'  ({n} veces, "
                           f"{100 * n / sum(cuentas.values()):.1f}%)  fijadas: {len(fijas)}", w - 1)
            if con_palabras:  # el siguiente carácter real (o frontera de palabra)
                sig = texto[pos + 1].lower() if pos + 1 < len(texto) else " "
                sig = sig if sig in LETRAS else " "
            else:
                sig = texto[nav[i + 1]].lower() if i + 1 < len(nav) else " "
            par = clave[c_cur] + clave[sig]
            stdscr.addnstr(h - 1, 0, f"bigrama '{par.replace(' ', '_')}': {modelo.pct.get((par[0], par[1]), 0):.2f}%"
                           f" | puntuación {punt:.1f} (último cambio {delta:+.1f})", w - 1)
        except curses.error:
            pass
        stdscr.refresh()

        try:
            k = stdscr.get_wch()
        except KeyboardInterrupt:
            break
        if k == curses.KEY_RIGHT:
            pos = nav[min(i + 1, len(nav) - 1)]
        elif k == curses.KEY_LEFT:
            pos = nav[max(i - 1, 0)]
        elif k == curses.KEY_DOWN:
            vertical(1)
        elif k == curses.KEY_UP:
            vertical(-1)
        elif k in ("\n", "\r", curses.KEY_ENTER):
            historial.append((clave, set(fijas)))
            clave = optimizar(pares, clave, fijas, modelo)
        elif k in (curses.KEY_BACKSPACE, "\x7f", "\b"):
            if historial:
                clave, fijas = historial.pop()
        elif k == "\x1b":
            break
        elif isinstance(k, str) and k.lower() in LETRAS and clave[c_cur] != k.lower():
            historial.append((clave, set(fijas)))
            clave, otra = asignar(clave, c_cur, k.lower())
            fijas.discard(otra)  # cambió como consecuencia: ya no es decisión tuya
            fijas.add(c_cur)
    return clave


def main():
    texto = open(sys.argv[1], encoding="utf-8").read().rstrip("\n") if len(sys.argv) > 1 \
        else input("Pega el texto cifrado: ")
    simbolos = [ch.lower() if ch.lower() in LETRAS else " " for ch in texto]  # " " = frontera de palabra
    palabras = "".join(simbolos).split()
    cuentas = Counter(s for s in simbolos if s != " ")
    if sum(cuentas.values()) < 2:
        sys.exit("El texto no contiene letras suficientes.")

    # ¿Hay palabras de verdad? Si todos los bloques miden lo mismo (p. ej. grupos de 5) se ignoran.
    con_palabras = len({len(p) for p in palabras[:-1]}) > 1
    if con_palabras:
        s = " " + " ".join(palabras) + " "
        modelo = Modelo(CUENTAS)
    else:
        s = "".join(palabras)
        modelo = Modelo(CONTINUO)
    pares = Counter(zip(s, s[1:]))
    print("Con separación de palabras: se usan sus fronteras." if con_palabras
          else "Sin palabras separadas: se analiza como texto continuo.")

    print("Analizando bigramas...")
    clave = optimizar(pares, clave_inicial(cuentas), set(), modelo)

    os.environ.setdefault("ESCDELAY", "25")  # que Esc responda al instante
    clave = curses.wrapper(app, texto, pares, cuentas, clave, modelo, con_palabras)

    print("".join(traducir(ch, clave) for ch in texto))
    print("\nClave (cifrada -> llana):")
    print("  " + " ".join(sorted(LETRAS)))
    print("  " + " ".join(clave[c] for c in sorted(LETRAS)))


if __name__ == "__main__":
    main()