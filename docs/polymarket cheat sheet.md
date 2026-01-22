# Polymarket API Cheat Sheet - Complete Reference

> Comprehensive reference of ALL Polymarket API endpoints and parameters
> Sources: Existing cheat sheet + Full documentation + Test files

---

## CLOB API

**Base URL:** `https://clob.polymarket.com`

### GET Endpoints

| Endpoint | Parameters | Description |
|----------|------------|-------------|
| `/book` | token_id |  |
| `/midpoint` | token_id |  |
| `/price` | side, token_id |  |
| `/prices` | *None* |  |
| `/prices-history` | endTs, fidelity, interval, market, startTs |  |

### POST Endpoints

| Endpoint | Parameters | Description |
|----------|------------|-------------|
| `/books` | body: token_id, side |  |
| `/prices` | body: token_id, side |  |
| `/spreads` | body: token_id, side |  |

---

## Data API

**Base URL:** `https://data-api.polymarket.com`

### GET Endpoints

| Endpoint | Parameters | Description |
|----------|------------|-------------|
| `/` | *None* |  |
| `/activity` | end, eventId, limit, market, offset, side, sortBy, sortDirection, start, type <small>(+1 more)</small> |  |
| `/holders` | limit, market, minBalance |  |
| `/live-volume` | id |  |
| `/oi` | market |  |
| `/positions` | eventId, limit, market, mergeable, offset, redeemable, sizeThreshold, sortBy, sortDirection, title <small>(+1 more)</small> |  |
| `/supported-assets` | *None* |  |
| `/traded` | user |  |
| `/trades` | eventId, filterAmount, filterType, limit, market, offset, side, takerOnly, user |  |
| `/v1/builders/leaderboard` | limit, offset, timePeriod |  |
| `/v1/builders/volume` | timePeriod |  |
| `/v1/closed-positions` | eventId, limit, market, offset, sortBy, sortDirection, title, user |  |
| `/v1/leaderboard` | category, limit, offset, orderBy, timePeriod, user, userName |  |
| `/value` | market, user |  |

### POST Endpoints

| Endpoint | Parameters | Description |
|----------|------------|-------------|
| `/deposit` | body: address |  |

---

## Gamma API

**Base URL:** `https://gamma-api.polymarket.com`

### GET Endpoints

| Endpoint | Parameters | Description |
|----------|------------|-------------|
| `/comments` | ascending, get_positions, holders_only, limit, offset, order, parent_entity_id, parent_entity_type |  |
| `/comments/user_address/{user_address}` | ascending, limit, offset, order, user_address |  |
| `/comments/{id}` | get_positions, id |  |
| `/events` | active, archived, ascending, closed, cyom, end_date_max, end_date_min, exclude_tag_id, featured, id <small>(+16 more)</small> |  |
| `/events/slug/{slug}` | include_chat, include_template, slug |  |
| `/events/{id}` | id, include_chat, include_template |  |
| `/events/{id}/tags` | id |  |
| `/markets` | ascending, clob_token_ids, closed, condition_ids, cyom, end_date_max, end_date_min, game_id, id, imit <small>(+17 more)</small> |  |
| `/markets/slug/{slug}` | *None* |  |
| `/markets/{id}` | include_tag, slug |  |
| `/markets/{id}/tags` | id |  |
| `/public-profile` | address |  |
| `/public-search` | ascending, cache, events_status, events_tag, exclude_tag_id, keep_closed_markets, limit_per_type, optimized, page, q <small>(+4 more)</small> |  |
| `/series` | ascending, categories_ids, categories_labels, closed, include_chat, limit, offset, order, recurrence, slug |  |
| `/series/{id}` | id, include_chat |  |
| `/sports` | image, ordering, resolution, series, sport, tags |  |
| `/sports/market-types` | *None* |  |
| `/status` | *None* |  |
| `/tags` | ascending, include_template, is_carousel, limit, offset, order |  |
| `/tags/slug/{slug}` | include_template, slug |  |
| `/tags/slug/{slug}/related-tags` | omit_empty, slug, status |  |
| `/tags/slug/{slug}/related-tags/tags` | omit_empty, slug, status |  |
| `/tags/{id}` | id, include_template |  |
| `/tags/{id}/related-tags` | id, omit_empty, status |  |
| `/tags/{id}/related-tags/tags` | id, omit_empty, status |  |
| `/teams` | abbreviation, ascending, league, limit, name, offset, order |  |

---

## Summary Statistics

**Total Unique Endpoints:** 49

- CLOB API: 8 endpoints
- Data API: 15 endpoints
- Gamma API: 26 endpoints

---

*This cheat sheet combines information from multiple sources to ensure completeness.*