"""Facts and mapping for the 6 Portman & Pooch dog clothing upgrades (8 Oct 2026).
Source: shop.ralawise.com/portman-pooch/<page>/ read 8 Oct 2026 (public page, via a fetch)."""
R = 'https://shop.ralawise.com'
P = {
 'personalised-dog-raglan-t-shirt': dict(id='gid://shopify/Product/16064461111677', code='PP001', garment='raglan T-shirt', page='dogs-raglan-t-shirt',
   number=True, tag='dog raglan t-shirt', sizes_3xl=['Black','Black/White'],
   colours={'Black/White':R+'/491bac/globalassets/ralawise/pp/pp001bkwh/pp001_black_white_ft.jpg','Black':R+'/491bac/globalassets/ralawise/pp/pp001blac/pp001_black_ft.jpg',
            'Navy':R+'/491ba7/globalassets/ralawise/pp/pp001navy/pp001_navy_ft.jpg','Navy/White':R+'/491ba7/globalassets/ralawise/pp/pp001nywh/pp001_navy_white_ft.jpg',
            'Pink/White':R+'/491ba7/globalassets/ralawise/pp/pp001pkwh/pp001_pink_white_ft.jpg'},
   print_area={'XS':(100,100),'S':(100,150),'M':(150,180),'L':(180,230),'XL':(180,230),'2XL':(180,230)}),
 'personalised-dog-fleece-hoodie': dict(id='gid://shopify/Product/16064461439357', code='PP002', garment='hoodie', page='dogs-hoodie',
   number=True, tag='dog hoodie', sizes_3xl=['Black','Grey'],
   colours={'Black':R+'/491b9e/globalassets/ralawise/pp/pp002blac/pp002_black_ft.jpg','Grey':R+'/491b9e/globalassets/ralawise/pp/pp002grey/pp002_grey_ft.jpg',
            'Navy':R+'/491b9e/globalassets/ralawise/pp/pp002navy/pp002_navy_ft.jpg','Pink':R+'/491b99/globalassets/ralawise/pp/pp002pink/pp002_pink_ft.jpg'},
   print_area={'XS':(100,100),'S':(100,150),'M':(150,180),'L':(180,230),'XL':(180,230),'2XL':(180,230)}),
 'personalised-dog-denim-jacket': dict(id='gid://shopify/Product/16064458523005', code='PP003', garment='denim jacket', page='dogs-denim-jacket',
   number=False, tag='dog denim jacket', sizes_3xl=['Indigo'],
   colours={'Indigo':R+'/492a2c/globalassets/ralawise/pp/pp003indi/pp003_indigo_ft2.jpg','Black':R+'/492c39/globalassets/ralawise/pp/pp003blac/pp003_black_ft2.jpg'},
   print_area={'XS':(90,90),'S':(100,140),'M':(115,180),'L':(130,200),'XL':(180,230),'2XL':(180,230)}),
 'personalised-dog-puffer-jacket': dict(id='gid://shopify/Product/16064459407741', code='PP004', garment='puffer jacket', page='dogs-puffer-jacket',
   number=False, tag='dog puffer jacket', sizes_3xl=None,
   colours={'Black':R+'/491b8d/globalassets/ralawise/pp/pp004blac/pp004_black_ft.jpg','Grey':R+'/4a5bdf/globalassets/ralawise/pp/pp004grey/pp004_grey_ft.png'},
   print_area={'XS':(100,25),'S':(100,40),'M':(150,40),'L':(180,60),'XL':(180,60),'2XL':(190,80)}),
 'personalised-dog-parka-jacket': dict(id='gid://shopify/Product/16064459637117', code='PP006', garment='parka jacket', page='dogs-parka-jacket',
   number=False, tag='dog parka', sizes_3xl=None,
   colours={'Khaki':R+'/491b8d/globalassets/ralawise/pp/pp006khak/pp006_khaki_ft.jpg','Black':R+'/4a5bdf/globalassets/ralawise/pp/pp006blac/pp006_black_ft.jpg'},
   print_area={'XS':(100,100),'S':(130,130),'M':(130,200),'L':(140,230),'XL':(180,230),'2XL':(180,230)}),
 'personalised-dog-football-t-shirt': dict(id='gid://shopify/Product/16064460652925', code='PP008', garment='football T-shirt', page='dogs-football-t-shirt',
   number=True, tag='dog football shirt', sizes_3xl=None,
   colours={'White/Red/Navy':R+'/49a5eb/globalassets/ralawise/pp/pp008whrn/pp008_white_red_navy_ft.jpg','Navy':R+'/49a5eb/globalassets/ralawise/pp/pp008nynw/pp008_navy_navy_white_ft.jpg',
            'Red':R+'/49a5eb/globalassets/ralawise/pp/pp008rewg/pp008_red_white_green_ft.jpg','Yellow':R+'/49a5eb/globalassets/ralawise/pp/pp008yewg/pp008_yellow_white_green_ft.jpg'},
   print_area=None),  # ASK: Ralawise gives no print area for PP008
}
# print_area = (width across the back, length along the back) in mm, from Ralawise "PrintArea L x W"
