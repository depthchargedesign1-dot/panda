# eBay shop set-up: Foxy Printing (do these before the first upload)

These steps take about 20 minutes in Seller Hub. They are one-offs. Every upload file after this uses them.

## 1. Business policies (Account > Business policies)

Create these three policies. The **names must match exactly**, because the CSV files point at them by name.

| Policy name (type exactly) | What to set |
|---|---|
| `FOXY Royal Mail 24` | **Postage.** Domestic service 1: Royal Mail Tracked 24 or 1st Class, £2.99 for the first item. Each additional item: **£0.00**, so a buyer who orders 4 masks pays postage once, like on the website. Service 2 (optional): Royal Mail Special Delivery Guaranteed, £12.99. Set the dispatch (handling) time you can keep to. Item location: Kirkbymoorside, YO62 6AR. |
| `FOXY 30 Day Returns` | **Returns.** Accepted, within 30 days, buyer pays return postage. This is the same as the website's refund policy. Personalised items (made from the buyer's photo or name) can only be returned if faulty, and the listing text already says so. |
| `FOXY Payment` | **Payment.** eBay's managed payments default; nothing else is needed. |

**Free postage, or charge for it?** You said to charge postage unless eBay promotes free postage. I couldn't find anything showing that eBay UK ranks free-postage listings higher. eBay says search ("Best Match") ranks on relevance, price, popularity and seller record. Buyers can tick a "Free postage" filter, though, so some of them won't see paid-postage listings.
- **Suggestion:** start with paid postage (£2.99) on the 50-mask test. If it sells slowly, switch the policy to free postage and add about £2.99 to each price. That's a single change to the policy, plus one re-upload with `price_multiplier` or a price bump.

**eBay fees on cheap masks.** eBay takes a percentage of the item price plus postage, and a fixed fee per order. On a £1.50 DIY mask with £2.99 postage, that eats a big part of the money. If you want the eBay prices higher than Shopify, change `price_multiplier` in `config/masks-celebrity.json` (e.g. 1.2 = +20%). Then I rebuild the file.

## 2. Turn on "message to seller" (needed for the Personalise box)

The personalised photo masks use eBay's **Personalise** item specific. Buyers then see a box next to Buy It Now where they type the names, and the text reaches you as a message. eBay's own steps are:
1. Add the "Personalise" item specific. The CSV does this.
2. Give the buyer instructions. The CSV does this too.
3. **Turn on "message to seller"** in your account's communication settings, or the box won't show.

Notes from other sellers:
- The box can take about 15 minutes to appear after a listing goes live.
- It only works in categories that allow personalisation.
- After uploading `M-A-01`, open one listing and check the box is there. If it isn't, tell me. The listing text also tells buyers to send names and photos through eBay messages, so orders still work.

## 3. Shop design (Seller Hub > Store > Edit Store)

| eBay field | Use |
|---|---|
| Store logo (300 x 300) | `shop/store-logo-300.png` |
| Billboard / banner (1280 x 288) | `shop/store-billboard-1280x288.jpg` |
| Store name | Foxy Printing (if it's free on eBay; otherwise your existing eBay store name) |
| Store description (max 1,000 characters) | the text below |

Store description (918 characters):

> Foxy Printing is a family print shop in Kirkbymoorside, North Yorkshire. We print everything to order in our own workshop: celebrity and personalised party face masks, novelty and personalised mugs, posters and word art prints, baby grows, cards and party printing.
>
> Our face masks are printed in full colour on thick 350gsm silk card at full A4 adult size. Choose Ready Cut (face shape and eye holes cut, elastic supplied) or DIY (printed only), on elastic or on a stick. Ideal for stag and hen dos, birthdays, leaving dos, photo booths and fancy dress.
>
> Want your own face on a mask? Order our personalised photo masks. Type the names in the Personalise box, then send us your photo through eBay messages after you buy.
>
> Questions about an order or a custom design? Message us through eBay and we'll get back to you.

**Store categories** (Store > Store categories). Make these, then tell me their numbers (eBay shows a number for each). I'll fill the `StoreCategory` column so each listing lands in the right one.
- Celebrity Face Masks
  - TV & Film Stars
  - Music Stars
  - Sports Stars & Darts
  - Mask Packs
- Personalised Photo Masks
- Mugs
  - Personalised Mugs
  - Novelty & Job Mugs
- Posters & Prints
- Baby Grows

## 4. Listing template

Every description in the CSV files uses `templates/listing.html`, in the same colours and fonts as the website:
- the navy header with the fox logo (the version without the phone number, hosted in Shopify Files);
- the orange-to-teal stripe;
- coloured badges;
- a yellow "How to personalise" box on personalised items;
- the product description;
- Postage, Returns and About Us boxes.

The template has no scripts, no links off eBay and no phone numbers or web addresses, which eBay doesn't allow. It also works on phones. A preview of a finished description is in `shop/preview-*.png`.
