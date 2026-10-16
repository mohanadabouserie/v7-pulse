# V7 Pulse: design system

The look of the dashboard (`V7_Pulse_Dashboard.html`, Version 15 onwards). Follow it for every new tab or panel.
The tokens live at the top of the `<style>` block; `tests/test_v15.py` checks the main rules.

## 1. Where it comes from
- **V7's own website**, https://v7-benefits.com, checked 7 Oct 2026:
  - green header `#0A7F40`, white and light grey (`#EFEFEF`) grounds, black text;
  - the Avenir typeface, with a light weight paired with a black weight for headlines ("FROM EGYPT / TO THE WORLD");
  - uppercase headings and rounded pill buttons.
- **The cans:**
  - The retail flavor cans are white with V7's green V.
  - The newer cans give each flavor its own color.
  - V Cola (Super Soda) is navy, silver and gold. The malts are black and gold.
- **Best-practice sources:**
  - [NN/g on dashboards](https://www.nngroup.com/articles/dashboards-preattentive/): use length and position for quantities; avoid pies, gauges and area; use color for categories, never for size.
  - Dashboard UX guides: 5–9 key numbers per screen, most important top-left, a comparison and a trend on every number, flat and high-contrast styling.
  - Social listening tools (Sprout Social, Brandwatch, Talkwalker): performance summary first, then conversation, themes and messages.

## 2. Color roles (light / dark)
| Role | Token | Light | Dark | Use |
|---|---|---|---|---|
| V7 brand | `--accent` | `#0A7F40` | `#4CC383` | Primary button, selected states, links, V7 in comparisons |
| Sidebar | `--side-bg` | `#08703A` | `#0D2A1C` | Navigation. A shade deeper than the brand green, so white text reaches 6.2:1 and labels 4.6:1 |
| Quantity | `--bar` | `#22396B` (V Cola navy) | `#8EA9E0` | Plain amounts: bars, sparklines, line charts |
| Positive / neutral / negative | `--pos` `--neu` `--neg` | `#1A9150` `#C5CEC8` `#E2483D` | `#4CC383` `#4A5D53` `#F0705F` | Sentiment only |
| Mixed (Version 23) | `--mix`, text `--mix-text` | `#D9822B`, text `#8A4510` | `#F0A35E`, text `#F3B27A` | Mixed sentiment only: praise and a complaint in one. Orange, apart from the events gold |
| Events, things to review | `--lemon` | `#E8A317` (Super Soda gold) | `#F2B53A` | Event markers, pending counts, "Real data" badge |
| Competitors | `--co-pepsi` `--co-coke` `--co-other` | `#1F5BC6` `#D22B36` `#9AA5A0` | lighter versions | PepsiCo blue, Coca-Cola red, others grey. V7 is always green |
| Text | `--ink` `--ink-2` `--muted` | `#12201A` `#3F4F47` `#5F6F67` | `#E8F1EC` `#B3C5BB` `#8DA297` | Body, secondary, labels |
| Grounds | `--ground` `--paper` `--sunk` | `#EEF2EF` `#FFFFFF` `#E6ECE8` | `#0A1510` `#0F1E17` `#0C1913` | Page, cards, tracks |

**Rules**
- Green means V7 and good news. Red means negative or critical. Navy means "how much", with no judgement.
- Don't use green for neutral data, and don't introduce new hues for single panels.
- Never rely on color alone. Deltas carry ▲/▼, sentiment carries a label and a percentage, and every chart has a legend.
- All text pairs meet WCAG AA (4.5:1). Check new pairs with the contrast function in `tests/test_v15.py`.

## 3. Product colors (from the cans)
| Product | Color | Product | Color |
|---|---|---|---|
| Pomegranate | `#B23A45` | Pineapple Malt | `#C9A35A` |
| Piña Colada | `#F2C744` | Apple Malt | `#7B5A2C` |
| Lemon Mint | `#9CBF4A` | Cream Soda | `#1A93AB` |
| Blueberry | `#5A5CA8` | V Cola | `#1B3366` |
| Pineapple | `#E8902F`* | V Cola Diet | `#A7B0BE` |
| Pink Lemonade | `#D63462` | Lemon-Lime (V Lemon) | `#2F8C46` |
| V Orange (new, 11 Oct 2026) | `#EE6A1F`† | | |

\* Plain Pineapple isn't on V7's site, so it gets a pineapple orange, distinct from Piña Colada's yellow.

† Set before seeing the can: a redder orange than Pineapple's. Swap in the can's colour once V Orange is in shops.

**Where product colors appear**
- They're stored as `PRODUCTS[].c`.
- `pdot(id)` draws the dot next to a product's name: in chips, the product filter, product lists and the product details title.
- Product cards carry a 5 px strip in the can color.
- They identify a product. They are never used as chart series (13 colors is too many to tell apart).

## 4. Type
- **Nunito Sans:** the closest free match to V7's Avenir, used for all Latin text. It's loaded from Google Fonts in weights 400–900.
- **IBM Plex Sans Arabic:** used for Arabic text.
- **Digits:** they're already equal-width, so numbers line up in tables. Don't use a monospace font.

| Element | Style |
|---|---|
| Page title | 900 weight, uppercase, 26 px (22 px on phones) |
| Panel title | 800 weight, 15.5 px |
| Small labels (KPI names, table headers, group names) | 800 weight, 11 px, uppercase, 0.08em letter spacing |
| Big numbers | 900 weight, 30 px |
| Body | 14 px |

## 5. Shapes and components
- **Pills (fully rounded):**
  - buttons, filter chips, segmented controls, badges, status tags;
  - deltas (▲ 14%), shown as tinted pills for up and down; neutral notes stay plain text.
- **Cards:** 16 px radius, 1 px border, white on a light grey page. No heavy shadows or gradients.
- **Segmented controls:** a grey track, with the selected option as a white raised pill in green text.
  - Only one solid-green button per screen: "Ask V7 Pulse", or the main action of a panel.
- **Sidebar:** green, with a white pill for the current tab.
  - Count badges are white with a red number, or gold for things waiting for approval.
  - On phones it becomes a scrolling green bar at the top.

## 6. Layout and order
- **Navigation:**
  - Overview;
  - **Conversation**: All posts, Products, Customer voice, People, Facebook groups, Hashtags & words, Our content;
  - **To act on**: Alerts, Rumors & attacks, Events;
  - **Market**: Online stores, Restaurants, Search trends;
  - **International**: Outside Egypt.
- **Every tab:** status and actions first (KPIs, "What changed", "Needs attention"), then details, with competitor rows and long lists on demand.
- **Overview:** KPI row, then "What changed this period" (left) next to the daily chart, then breakdowns, then lists.
- **Phones:** the filters fold behind a **Filters** button, which shows a green dot when filters differ from the defaults. KPIs must be visible in the first screen.

## 7. Charts
- Use bars and lines, never pies, donuts or gauges.
- Sentiment is stacked as positive, then neutral, then negative.
- Events are gold numbered markers.
- Axis text is 11 px, muted, with horizontal gridlines in `--hair`.
- In comparisons, V7 is green, PepsiCo blue and Coca-Cola red, in every tab.

## 8. Patterns added in Version 16
- **Status banner** (`.sbanner ok|warn|bad`): one sentence that answers "is anything wrong?", with the check date underneath. Use it at the top of status tabs.
- **Status pills** (`.av in|low|out|na`): ✓ In stock (green tint), Low · 8 left (solid gold), ✕ Out (red tint), Not sold here (plain muted text). On phones in tight grids, show ✓ and — with a one-line key.
- **Problem rows** (`.prob`): name and store, what happened in words (with a demo tag when it's demo data), a day strip (`.strip`), and the status now. List only what went wrong, and sum up the rest in one line.
- **Clickable rows** open the side panel (`openDrawer`) with a full chart (`bigLine`, with `invert:true` for ranks). Show a › chevron in the last column, and outline the small trend line on hover.
- **Like-for-like prices:** always show per-100 ml next to the shelf price, shade the cheapest option, and state the difference from V7 in words.
- **Class names:** never reuse `demo`, `real`, `st` or `pill` for new elements (DECISIONS #69).
- **Price and stock apart** (Versions 17 and 19):
  - A price cell holds only the price and price notes.
  - When a table covers several stores, each store gets its own Price and Stock columns under a store header, separated by a thin line (`.smx-g`). Stock cells (`td.sk`) show ✓, a gold pill with the count left, or ✕ Out.
  - Never use one Stock column for several stores.
  - On phones the stock columns aren't drawn; problems sit under the product name with the store named (`.stk-m`).

## 9. Real-data views (Version 18)
- **The header badge** says "Real data" on every view built from real collections (Online stores, Restaurants, Search trends, Rumors & attacks). Views whose data spans more than the demo period hide the date filters.
- **Real posts** (`rCard`) show:
  - the platform badge;
  - the name, or "X user" and so on for private people (DECISIONS #75);
  - the account kind and followers;
  - a "Real post" badge and the full date with the year;
  - the text, then an English "In short" note;
  - what the post does as a flag (red: repeats it, grey: asks, green: corrects), the metrics, and the link.
- **Claim status pills:** Active, Watching (grey), Slowing, Contained or Ended (green), Handled and Dismissed (muted).
- **Charts that span years** count posts per month, with "Mon YYYY" labels. Short episodes count per day.

## 10. Honest numbers (Version 20)
- **Small numbers:**
  - Show a change under 10 as the difference ("+3", "−2"), never a percentage.
  - Show net sentiment only from 5 items up; otherwise use "—" with "Too few to score".
  - "Biggest gain" style sentences use a percentage only on a base of 10 or more.
- **Volumes:** demo volumes follow what real collection returns. Posts and comments show together by default, and a "Where it happens" split says how much is comments under V7's posts.
- **Don't add:**
  - emotion labels or word clouds;
  - dialect splits beyond Egyptian Arabic, other Arabic, English and Franco-Arabic;
  - badges that say nothing (only Seasonal is shown).
- **Data that needs V7's accounts** is labelled with its source ("Instagram insights · demo numbers").

## 11. The marketing team's feedback (Version 23)
- **"Needs your attention" first:**
  - Overview and Customer voice open with up to 4 cards (3 on Customer voice). Each card has:
    - a severity label and a matching left border: red for act now, gold for watch, green for opportunity;
    - a title and one line of evidence;
    - **Next step**, and an owner chip (Social team, Customer care, Sales, E-commerce, PR);
    - "View →".
  - Order: urgent items, then social issues, replies waiting, posts worth amplifying, and at most one store item.
  - On phones the cards are a row to swipe, so the KPI numbers still start in the first screen.
- **Posts show their image:**
  - A 112 px square on the card (84 px on phones), with a play mark for videos and an album mark for carousels.
  - Card text stops at 6 lines; the full text is in the post view.
  - Demo posts never get an invented image.
  - Images are embedded as small JPEGs (360 px, quality 55), so the dashboard stays one file: 183 posts, about 2.4 MB.
- **Post view:**
  - A drawer that opens from "View post", the image or the caption in Our posts.
  - Order: the image (shown whole on black), "the video plays on …", the full text, chips, the numbers, buttons to open and copy the link.
  - Then the comments, with V7's replies under them on a green left rule.
  - It ends with a line saying what's real.
- **Alert preview:**
  - An email card: From, To and Subject in a grey header, then small uppercase section labels (What people are posting, Next step, Suggested reply).
  - A phone notification mock: a dark phone with a light card, drawn the same in both themes.
- **Daily brief:**
  - Brand-health tiles with the four-part sentiment bar.
  - Red flags as left-ruled items by severity; positive signals in green.
  - "Worth amplifying" cards with a suggested step under each.
  - Numbered actions, each with an owner chip.
- **"Partly real" badge:** also on Daily brief, Alerts and Events, with a tooltip saying which parts are real.
- **Telegram (Version 24):**
  - The alert preview's phone shows a Telegram notification: a round blue Telegram mark, "V7 Pulse" as the title, then the alert.
  - The Daily brief has an "Open in Telegram ↗" button next to "See the email".
  - Ask V7 Pulse has a quiet line under the question box.

