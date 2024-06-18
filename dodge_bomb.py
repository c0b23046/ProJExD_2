import os
import sys
import pygame as pg
import random

os.chdir(os.path.dirname(os.path.abspath(__file__)))

WIDTH, HEIGHT = 1600, 900
diff = {  #移動量辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, 5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (5, 0),
}
def dict_i() -> dict:
    image_dict = {  #画像辞書
        (0, 0): pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0),
        (5, 0): pg.transform.flip(pg.transform.rotozoom(pg.image.load("fig/3.png"), 180, 2.0), False, True),
        (5, 5): pg.transform.flip(pg.transform.rotozoom(pg.image.load("fig/3.png"), 225, 2.0), False, True),
        (0, 5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 90, 2.0),
        (-5, 5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 2.0),
        (-5, 0): pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0),
        (-5, -5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 315, 2.0),
        (0, -5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 270, 2.0),
        (5, -5): pg.transform.flip(pg.transform.rotozoom(pg.image.load("fig/3.png"), 135, 2.0), False, True),                                
    }
    return image_dict

#画面端の判定
def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect or 爆弾Rect
    戻り値：横方向・縦方向の真理値タプル（True：画面内／False：画面外)
    Rectオブジェクトのleft, right, top, bottomの値から画面内・外を判断する
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def bomb_accs() -> tuple:
    accs = [a for a in range(1, 11)]
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255,0,0),(10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
    return [bb_imgs, accs]


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bb_imgs, bb_accs = accl()
    bb_img = pg.Surface((20,20))  # 1辺の20の空のSurfaceを作る
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 空のSurfaceに赤い円を描く
    bb_img.set_colorkey((0,0,0))
    bb_rct = bb_imgs[0].get_rect()  # 爆弾Rect
    kk_rct.center = random.randint (0, WIDTH), random.randint (0,HEIGHT)
    vx, vy = +5 ,+5  # 爆弾の横方向速度、縦方向速度
    clock = pg.time.Clock()
    tmr = 0
    
    

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        #衝突判定
        if kk_rct.colliderect(bb_rct):
            return  #gameover
        
        

        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        #方向キー移動
        for k, v in diff.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        
        img_dict = dict_i()
        sum_tuple = tuple(sum_mv)
        kk_img = img_dict[sum_tuple]

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        bb_img.set_colorkey((0,0,0))

        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(avx,avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko: #横方向にはみ出たら
            vx *= -1
        if not tate: #縦方向にはみ出たら
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
